#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define MAX_BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: ./responder <id_mensagem> <mensagem>\n");
        return EXIT_FAILURE;
    }

    char *comando = "enviar";
    char *origem = getenv("USER");;
    int idMensagem = atoi(argv[1]);
    char *mensagem = argv[2];

    int i = 0;

    char path[MAX_BUFFER_SIZE];
    char path1[MAX_BUFFER_SIZE];
    char path2[MAX_BUFFER_SIZE];
    snprintf(path1, sizeof(path1), "../../%s/Caixa de Entrada/Novas Mensagens/mensagem_%d", origem, idMensagem);
    snprintf(path2, sizeof(path2), "../../%s/Caixa de Entrada/Historico de Mensagens/mensagem_%d", origem, idMensagem);

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

    char sender[MAX_BUFFER_SIZE];

    fgets(sender, sizeof(sender), file);
    fclose(file);

    char *destino = strchr(sender, ':');
    if (destino != NULL) {
        destino += 2;
    } else {
        fprintf(stderr, "Formato do remetente inválido.\n");
        return EXIT_FAILURE;
    }

    printf("%s", destino);

    char *fifoPath = "../tmp/Server_fifo.fifo";

    int serverFifo = open(fifoPath, O_WRONLY);

    int tamanho_necessario = strlen(comando) + strlen(origem) + strlen(destino) + strlen(mensagem) + 4;
    char *string_total = malloc(tamanho_necessario);
    snprintf(string_total, tamanho_necessario, "%s %s %s %s", comando, origem, destino, mensagem);

    write(serverFifo, string_total, strlen(string_total));

    printf("Mensagem envida.\n");

    close(serverFifo);
    free(string_total);

    return 0;
}
