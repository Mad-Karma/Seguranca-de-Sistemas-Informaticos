#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: %s <nome_do_usuario> <nome_do_grupo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char *user = argv[1];
    char *group = argv[2];
    char command[256];

    // Monta o comando para adicionar o usuário ao grupo
    snprintf(command, sizeof(command), "sudo usermod -aG %s %s", group, user);

    printf("Adicionando o usuário '%s' ao grupo '%s'.\n", user, group);

    // Executa o comando
    int result = system(command);

    if (result == -1) {
        perror("Falha ao executar o comando system");
        return EXIT_FAILURE;
    } else if (result == 127) {
        fprintf(stderr, "Erro ao executar shell ou comando não encontrado\n");
        return EXIT_FAILURE;
    } else if (result != 0) {
        printf("Falha ao adicionar o usuário ao grupo. Verifique se os nomes estão corretos e se você tem permissões adequadas.\n");
        return EXIT_FAILURE;
    } else {
        printf("Usuário '%s' adicionado ao grupo '%s' com sucesso.\n", user, group);
    }

    return EXIT_SUCCESS;
}
