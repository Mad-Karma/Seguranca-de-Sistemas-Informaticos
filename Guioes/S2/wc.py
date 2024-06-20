import sys

def contar_estatisticas(arquivo):
    linhas = 0
    palavras = 0
    caracteres = 0

    with open(arquivo, 'r') as f:
        for linha in f:
            linhas += 1
            palavras += len(linha.split())
            caracteres += len(linha)

    return linhas, palavras, caracteres

def main():
    if len(sys.argv) != 2:
        print("Uso: python wc.py <arquivo>")
        sys.exit(1)

    arquivo = sys.argv[1]
    linhas, palavras, caracteres = contar_estatisticas(arquivo)

    print(f"{linhas:8} {palavras:8} {caracteres:8} ")

if __name__ == "__main__":
    main()
