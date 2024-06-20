#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <pwd.h>
#include <sys/stat.h>
#include <sys/types.h>

#define MAX_BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: ./ler <id_mensagem>\n");
        return EXIT_FAILURE;
    }

    int id = atoi(argv[1]);
    char *username = getenv("USER");

    int i = 0;

    char path[MAX_BUFFER_SIZE];
    char path1[MAX_BUFFER_SIZE];
    char path2[MAX_BUFFER_SIZE];
    snprintf(path1, sizeof(path1), "../../%s/Caixa de Entrada/Novas Mensagens/mensagem_%d", username, id);
    snprintf(path2, sizeof(path2), "../../%s/Caixa de Entrada/Historico de Mensagens/mensagem_%d", username, id);

    FILE *file = fopen(path1, "r");
    if (file == NULL) {
        file = fopen(path2, "r");
        if (file == NULL) {
            perror("Falha ao abrir o arquivo");
            return EXIT_FAILURE;
        }
        strcpy(path, path2);
        i = 2;
    }
    else {
        strcpy(path, path1);
        i = 1;
    }

    char content[MAX_BUFFER_SIZE];

    // Lê o arquivo linha por linha até o fim
    while (fgets(content, MAX_BUFFER_SIZE, file) != NULL) {
        printf("%s", content);
    }

    // Checar se a leitura terminou devido a um erro
    if (ferror(file)) {
        perror("Erro ao ler o arquivo");
        fclose(file);
        return EXIT_FAILURE;
    }

    fclose(file);

    char new_path[MAX_BUFFER_SIZE];
    snprintf(new_path, sizeof(new_path), "../../%s/Caixa de Entrada/Historico de Mensagens/mensagem_%d", username, id);

    if(i == 1) {
        if (rename(path, new_path) != 0) {
            perror("Falha ao mover o arquivo");
            return EXIT_FAILURE;
        }
    }

    return 0;
}
