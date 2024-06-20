#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

int main() {
    int status;
    char command[256];

    // Usando getenv para obter o nome de usuário do usuário que executou o sudo
    char *user = getenv("SUDO_USER");

    // Se o comando está sendo executado sem sudo, SUDO_USER será nulo
    if (user == NULL) {
        printf("Este programa deve ser executado com sudo.\n");
        return EXIT_FAILURE;
    }

    // Preparar o comando para remover o usuário do grupo "concordia"
    snprintf(command, sizeof(command), "sudo gpasswd -d %s concordia", user);

    // Executar o comando
    printf("Executando comando: %s\n", command);
    status = system(command);

    if (status == -1) {
        perror("Falha ao executar o comando");
        return EXIT_FAILURE;
    } else {
        printf("Usuário %s removido do grupo 'concordia' com sucesso.\n", user);
    }

    return EXIT_SUCCESS;
}
