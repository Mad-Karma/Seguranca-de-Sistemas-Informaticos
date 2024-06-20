
import sys

def ler_ficheiro(nome_ficheiro):
    try:
        with open(nome_ficheiro, 'r') as ficheiro:
            conteudo = ficheiro.read()
            print(conteudo)
    except FileNotFoundError:
        print("Erro: Ficheiro não encontrado.")
    except PermissionError:
        print("Erro: Permissão negada para aceder ao ficheiro.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python3 programa.py <nome_do_ficheiro>")
        sys.exit(1)

    nome_ficheiro = sys.argv[1]
    ler_ficheiro(nome_ficheiro)




