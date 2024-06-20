CC = gcc
CFLAGS = -Wall -g -Iinclude
LDFLAGS =

# Destinos finais para os executáveis
BIN_DIR = bin
OBJ_DIR = obj
TMP_DIR = tmp

# Cria as pastas necessárias caso não existam
folders:
	@mkdir -p $(BIN_DIR) $(OBJ_DIR) $(TMP_DIR)

# Regra padrão
all: folders $(BIN_DIR)/orchestrator $(BIN_DIR)/client

# Regras para compilar os executáveis
$(BIN_DIR)/orchestrator: $(OBJ_DIR)/orchestrator.o
	$(CC) $(LDFLAGS) $^ -o $@

$(BIN_DIR)/client: $(OBJ_DIR)/client.o
	$(CC) $(LDFLAGS) $^ -o $@

# Regra padrão para compilar objetos de fontes
$(OBJ_DIR)/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Limpeza de arquivos de compilação e temporários
clean:
	rm -rf $(OBJ_DIR)/* $(TMP_DIR)/* $(BIN_DIR)/*
