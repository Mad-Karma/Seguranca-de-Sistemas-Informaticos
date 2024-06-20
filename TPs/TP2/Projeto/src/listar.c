#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>

#define MAX_BUFFER_SIZE 2048

// Função para listar mensagens de uma pasta específica
void listMessages(const char *folderPath) {
    DIR *dir;
    struct dirent *entry;
    FILE *file;
    char filePath[3*MAX_BUFFER_SIZE];
    char line[MAX_BUFFER_SIZE];
    char sender[MAX_BUFFER_SIZE];
    char date[MAX_BUFFER_SIZE];
    char messageContent[MAX_BUFFER_SIZE] = {0};
    int id, bytesRead = 0;

    dir = opendir(folderPath);
    if (dir == NULL) {
        perror("Falha ao abrir diretório");
        return;
    }

    while ((entry = readdir(dir)) != NULL) {
        snprintf(filePath, sizeof(filePath), "%s/%s", folderPath, entry->d_name);
        struct stat fileStat;
        if (stat(filePath, &fileStat) == 0 && S_ISREG(fileStat.st_mode)) {
            file = fopen(filePath, "r");
            if (file == NULL) {
                perror("Falha ao abrir o arquivo");
                continue;
            }

            fgets(sender, sizeof(sender), file);
            sender[strcspn(sender, "\n")] = 0;

            fgets(date, sizeof(date), file);
            date[strcspn(date, "\n")] = 0;

            bytesRead = 0;
            while (fgets(line, sizeof(line), file) != NULL) {
                line[strcspn(line, "\n")] = 0; // Remove quebra de linha
                strcat(messageContent, line);
                bytesRead += strlen(line);
            }

            sscanf(entry->d_name, "mensagem_%d", &id);

            printf("id: %d\n%s\n%s\ntamanho_mensagem: %d\n\n", id, date, sender, bytesRead);

            fclose(file);
            memset(messageContent, 0, sizeof(messageContent));
        }
    }

    closedir(dir);
}

int main(int argc, char *argv[]) {
    if (argc == 2 && strcmp(argv[1], "-a") != 0) {
        fprintf(stderr, "Uso: ./listar [-a]\n");
        return EXIT_FAILURE;
    }
    
    char *username = getenv("USER");
    char path[MAX_BUFFER_SIZE];
    char newPath[3*MAX_BUFFER_SIZE];
    char historyPath[3*MAX_BUFFER_SIZE];

    snprintf(path, sizeof(path), "../../%s/Caixa de Entrada", username);
    snprintf(newPath, sizeof(newPath), "%s/Novas Mensagens", path);
    snprintf(historyPath, sizeof(historyPath), "%s/Historico de Mensagens", path);

    if (argc == 2 && strcmp(argv[1], "-a") == 0) {
        printf("Todas as mensagens da Caixa de Entrada:\n\n");
        printf("Novas Mensagens:\n\n");
        listMessages(newPath);
        printf("Histórico de Mensagens:\n\n");
        listMessages(historyPath);
    } else {
        printf("Novas Mensagens:\n\n");
        listMessages(newPath);
    }

    return 0;
}
