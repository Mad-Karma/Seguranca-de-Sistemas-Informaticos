#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define MAX_BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: ./enviar <destinatario> <mensagem>\n");
        return EXIT_FAILURE;
    }

    char *comando = "enviar";
    char *origem = getenv("USER");
    char *destino = argv[1];
    char *mensagem = argv[2];

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
