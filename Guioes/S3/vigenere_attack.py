import sys

def vigenere_attack(tamanho_chave, criptograma, palavras):
    criptograma = criptograma.upper()
    palavras = [palavra.upper() for palavra in palavras]

    # Realizar o ataque à cifra de Vigenère
    chave = ""
    texto_limpo = ""
    
    for i in range(tamanho_chave):
        # Extrair a i-ésima "fatia" do criptograma
        fatia = criptograma[i::tamanho_chave]

        # Realizar ataque à cifra de César para determinar a letra da chave
        letra_chave = ataque_cesar(fatia)

        if letra_chave is None:
            # Se não foi possível determinar a letra da chave, retorna resposta vazia
            return "", ""

        chave += letra_chave

    # Usar a chave encontrada para decifrar o texto completo
    texto_limpo = dec(chave, criptograma)
    
    return chave, texto_limpo

def ataque_cesar(fatia):
    # Contar a frequência das letras no texto
    frequencias = {chr(i): fatia.count(chr(i)) for i in range(ord('A'), ord('Z') + 1)}

    # Ordenar as letras por frequência decrescente
    letras_ordenadas = sorted(frequencias.keys(), key=lambda x: frequencias[x], reverse=True)

    # Letra mais frequente em português
    letra_mais_frequente = 'A'

    # Calcular a diferença levando em consideração a rotação no alfabeto
    diferenca = ord(letras_ordenadas[0]) - ord(letra_mais_frequente)
    print(letras_ordenadas[0])
    print(fatia)

    # Encontrar a letra da chave
    letra_chave = chr(ord('A') + diferenca)

    return letra_chave

def dec(chave, mensagem):
    resultado = ""
    tamanho_chave = len(chave)

    for i, char in enumerate(mensagem):
        if char.isalpha():
            char_chave = chave[i % tamanho_chave]
            deslocamento = ord(char_chave) - ord('A')
            char_dec = chr((ord(char) - deslocamento - ord('A')) % 26 + ord('A'))
            resultado += char_dec
        else:
            resultado += char

    return resultado

if __name__ == "__main__":
    # Obter argumentos da linha de comando
    tamanho_chave = int(sys.argv[1])
    criptograma = sys.argv[2]
    palavras = sys.argv[3:]

    # Realizar o ataque à cifra de Vigenère
    chave, texto_limpo = vigenere_attack(tamanho_chave, criptograma, palavras)

    # Imprimir os resultados
    if chave:
        print(chave)
        print(texto_limpo)
