#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <nome_do_grupo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char command[256];
    snprintf(command, sizeof(command), "sudo groupdel %s", argv[1]);

    printf("Removendo o grupo: %s\n", argv[1]);

    int result = system(command);

    if (result == -1) {
        perror("Falha ao executar o comando system");
        return EXIT_FAILURE;
    } else if (result == 127) {
        fprintf(stderr, "Erro ao executar shell ou comando não encontrado\n");
        return EXIT_FAILURE;
    } else if (result != 0) {
        printf("Falha ao remover o grupo '%s'. Verifique se o grupo existe e se você tem permissões adequadas.\n", argv[1]);
        return EXIT_FAILURE;
    } else {
        printf("Grupo '%s' removido com sucesso\n", argv[1]);
    }

    return EXIT_SUCCESS;
}
