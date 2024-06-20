#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1024

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <nome_do_grupo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *groupName = argv[1];
    FILE *groupFile;
    char line[MAX_LINE_LENGTH];
    int found = 0;

    groupFile = fopen("/etc/group", "r");
    if (groupFile == NULL) {
        perror("Falha ao abrir o arquivo /etc/group");
        return EXIT_FAILURE;
    }

    while (fgets(line, sizeof(line), groupFile) != NULL) {
        char *currentGroupName = strtok(line, ":");
        if (strcmp(currentGroupName, groupName) == 0) {
            strtok(NULL, ":");
            strtok(NULL, ":");
            char *members = strtok(NULL, "\n");
            if (members == NULL || strlen(members) == 0) {
                printf("Grupo '%s' não tem membros.\n", groupName);
            } else {
                printf("Membros do grupo '%s': %s\n", groupName, members);
            }
            found = 1;
            break;
        }
    }

    fclose(groupFile);

    if (!found) {
        printf("Grupo '%s' não encontrado.\n", groupName);
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
