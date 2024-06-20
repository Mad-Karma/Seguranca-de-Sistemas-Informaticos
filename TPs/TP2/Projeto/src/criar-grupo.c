#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <nome_do_grupo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char command[256];
    char *user = getenv("USER");  // Obtem o nome do usuário atual

    if (user == NULL) {
        fprintf(stderr, "Não foi possível obter o nome do usuário atual.\n");
        return EXIT_FAILURE;
    }

    // Cria o comando para adicionar o grupo
    snprintf(command, sizeof(command), "sudo groupadd %s", argv[1]);
    printf("Criando o grupo: %s\n", argv[1]);

    int result = system(command);

    if (result == -1) {
        perror("Falha ao executar o comando para criar o grupo");
        return EXIT_FAILURE;
    } else if (result == 127) {
        fprintf(stderr, "Erro ao executar shell ou comando para criar o grupo não encontrado\n");
        return EXIT_FAILURE;
    }

    // Cria o comando para adicionar o usuário ao grupo criado
    snprintf(command, sizeof(command), "sudo usermod -aG %s %s", argv[1], user);
    printf("Adicionando o usuário '%s' ao grupo '%s'.\n", user, argv[1]);

    result = system(command);

    if (result == -1) {
        perror("Falha ao executar o comando para adicionar o usuário ao grupo");
        return EXIT_FAILURE;
    } else if (result == 127) {
        fprintf(stderr, "Erro ao executar shell ou comando para adicionar o usuário ao grupo não encontrado\n");
        return EXIT_FAILURE;
    } else {
        printf("Usuário '%s' adicionado ao grupo '%s' com sucesso.\n", user, argv[1]);
        printf("ola");
    }

    return EXIT_SUCCESS;
}
