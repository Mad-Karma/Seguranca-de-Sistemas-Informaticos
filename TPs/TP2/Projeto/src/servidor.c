#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#include <time.h>
#include <pwd.h>
#include <sys/stat.h>
#include <grp.h>

#define MAX_BUFFER_SIZE 1024

int count_files_in_directory(char *path) {
    int file_count = 0;
    struct dirent *entry;
    DIR *dir = opendir(path);
    struct stat file_stat;
    char full_path[1024];

    if (dir == NULL) {
        perror("Failed to open directory");
        return -1;
    }

    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);
        if (stat(full_path, &file_stat) == 0) {
            if (S_ISREG(file_stat.st_mode)) {
                file_count++;
            }
        } else {
            perror("Failed to get file statistics");
        }
    }
    closedir(dir);
    return file_count;
}

void ensure_directory_exists(const char* path, const char* username) {
    struct stat st = {0};
    umask(0);
    if (stat(path, &st) == -1) {
        if (mkdir(path, 0770) != -1) {
            struct passwd *pw = getpwnam(username);
            struct group *gr = getgrnam("concordia");
            if (pw != NULL && gr != NULL) {
                if (chown(path, pw->pw_uid, gr->gr_gid) == -1) {
                    perror("Falha ao mudar a propriedade do diretório");
                }
            } else {
                if (pw == NULL) fprintf(stderr, "Usuário não encontrado\n");
                if (gr == NULL) fprintf(stderr, "Grupo não encontrado\n");
            }
            if (chmod(path, 0750) == -1) {
                perror("Falha ao definir permissões do diretório");
            }
        } else {
            perror("Falha ao criar diretório");
        }
    } else {
        printf("Diretório '%s' já existe.\n", path);
    }
}

int check_identity_type(const char *name) {
    if (getpwnam(name) != NULL) {
        return 1;
    }
    if (getgrnam(name) != NULL) {
        return 2;
    }
    return 0;
}

char** get_group_members(const char* group_name, int* count) {
    struct group *grp;
    grp = getgrnam(group_name);
    if (grp == NULL) {
        *count = 0;
        return NULL;
    }

    int num_members = 0;
    while (grp->gr_mem[num_members] != NULL) {
        num_members++;
    }

    *count = num_members;
    char** members = malloc(num_members * sizeof(char*));
    if (members == NULL) {
        *count = 0;
        return NULL;
    }

    for (int i = 0; i < num_members; i++) {
        members[i] = strdup(grp->gr_mem[i]);
        if (members[i] == NULL) {
            for (int j = 0; j < i; j++) {
                free(members[j]);
            }
            free(members);
            *count = 0;
            return NULL;
        }
    }

    return members;
}

void send_message_to_user(const char* origem, const char* destino, const char* mensagem) {
    char path[MAX_BUFFER_SIZE];
    char new_messages_path[2*MAX_BUFFER_SIZE];
    char history_messages_path[2*MAX_BUFFER_SIZE];

    snprintf(path, sizeof(path), "../../%s/Caixa de Entrada", destino);
    snprintf(new_messages_path, sizeof(new_messages_path), "%s/Novas Mensagens", path);
    snprintf(history_messages_path, sizeof(history_messages_path), "%s/Historico de Mensagens", path);

    ensure_directory_exists(path, destino);
    ensure_directory_exists(new_messages_path, destino);
    ensure_directory_exists(history_messages_path, destino);

    int number_files = count_files_in_directory(new_messages_path) + count_files_in_directory(history_messages_path);
    printf("%d", number_files);

    char file_path[3*MAX_BUFFER_SIZE];
    snprintf(file_path, sizeof(file_path), "%s/mensagem_%d", new_messages_path, number_files+1);

    time_t rawtime;
    struct tm *timeinfo;
    char buffer[80];

    time(&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer, sizeof(buffer), "%d-%m-%Y %H:%M:%S", timeinfo);

    FILE *fp = fopen(file_path, "w");
    
    fprintf(fp, "Remetente: %s\n", origem);
    fprintf(fp, "%s\n\n", buffer);
    fprintf(fp, "%s\n", mensagem);
    
    fclose(fp);

    struct passwd *pw = getpwnam(destino);
    if (pw != NULL) {
        if (chown(file_path, pw->pw_uid, -1) == -1) {
            perror("Falha ao mudar a propriedade do arquivo");
        }
    } else {
        fprintf(stderr, "Usuário destinatário não encontrado\n");
    }
}

int main() {
    const char *fifoPath = "../tmp/Server_fifo.fifo";
    
    if (mkfifo(fifoPath, 0666) < 0) {
        printf("Server fifo already exists.\n");
    }

    int serverFifo = open(fifoPath, O_RDONLY);
    if (serverFifo < 0) {
        perror("Failed to open FIFO");
        return EXIT_FAILURE;
    }

    char buf[MAX_BUFFER_SIZE];
    int read_bytes;

    while(1) {
        while ((read_bytes = read(serverFifo, buf, MAX_BUFFER_SIZE)) > 0) {
            buf[read_bytes] = '\0';

            char comando[50];
            char info[MAX_BUFFER_SIZE];

            sscanf(buf, "%s %[^\n]", comando, info);

            printf("%s", comando);

            if(strcmp(comando, "enviar") == 0) {
                char origem[50];
                char destino[50];
                char mensagem[MAX_BUFFER_SIZE];

                sscanf(info, "%s %s %[^\n]", origem, destino, mensagem);

                int identity = check_identity_type(destino);

                if (identity == 1) { // Caso destino seja um usuário
                    send_message_to_user(origem, destino, mensagem);
                } else if (identity == 2) { // Caso destino seja um grupo
                    int count;
                    char** members = get_group_members(destino, &count);
                    if (members != NULL) {
                        for (int i = 0; i < count; i++) {
                            send_message_to_user(origem, members[i], mensagem);
                            free(members[i]); // Libera memória alocada para cada membro
                        }
                        free(members); // Libera a memória do array de membros
                    } else {
                        fprintf(stderr, "Erro ao buscar membros do grupo %s\n", destino);
                    }
                } else {
                    fprintf(stderr, "Destinatário %s não é um usuário nem um grupo\n", destino);
                }
            }
        }
    }

    close(serverFifo);
    return 0;
}
