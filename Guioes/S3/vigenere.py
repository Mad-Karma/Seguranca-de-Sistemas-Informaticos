import sys

def preproc(str):
      l = []
      for c in str:
          if c.isalpha():
              l.append(c.upper())
      return "".join(l)

def cesar(tipo, chave, letra):
      chave_ascii = ord(chave) - 65

      if tipo == "enc":
           if (ord(letra) + chave_ascii) <= 90:
                return chr(ord(letra) + chave_ascii)
           else:
                return chr(65 + ((ord(letra) + chave_ascii) % 26))
      elif tipo == "dec":
           if (ord(letra) - chave_ascii) >= 65:
                return chr(ord(letra) - chave_ascii)
           else:
                return chr(91 - (65 - (ord(letra) - chave_ascii)))

def vigenere(tipo, chave, mensagem):
     mensagem_filtrada = preproc(mensagem)
     mensagem_encriptada = ""
     tamanho = len(chave)
     index = 0

     for caractere in mensagem_filtrada:
          mensagem_encriptada += cesar(tipo, chave[index], caractere)
          index = index + 1
          if index > tamanho-1:
               index = 0
     
     print(mensagem_encriptada)
     

if __name__ == "__main__":
     tipo = sys.argv[1]
     chave = sys.argv[2]
     mensagem_original = sys.argv[3]

     vigenere(tipo, chave, mensagem_original)

     