#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

int main() {
    int status;
    char command[256];

    char *user = getenv("SUDO_USER");

    // Preparar o comando para adicionar o usuário ao grupo "concordia"
    snprintf(command, sizeof(command), "sudo usermod -aG concordia %s", user);

    // Executar o comando
    printf("Executando comando: %s\n", command);
    status = system(command);

    if (status == -1) {
        perror("Falha ao executar o comando");
        return EXIT_FAILURE;
    } else {
        printf("Usuário %s adicionado ao grupo 'concordia' com sucesso.\n", user);
    }

    return EXIT_SUCCESS;
}
