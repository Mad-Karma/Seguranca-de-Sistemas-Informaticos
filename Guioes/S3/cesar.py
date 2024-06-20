import sys

def preproc(str):
      l = []
      for c in str:
          if c.isalpha():
              l.append(c.upper())
      return "".join(l)

def cesar(tipo, chave, mensagem):
      chave_ascii = ord(chave) - 65
      mensagem_filtrada = preproc(mensagem)
      mensagem_encriptada = ""

      if tipo == "enc":
          for caractere in mensagem_filtrada:
               if (ord(caractere) + chave_ascii) <= 90:
                   caractere_mod = chr(ord(caractere) + chave_ascii)
               else:
                    caractere_mod = chr(65 + ((ord(caractere) + chave_ascii) % 26))

               mensagem_encriptada += caractere_mod
      elif tipo == "dec":
           for caractere in mensagem_filtrada:
                if (ord(caractere) - chave_ascii) >= 65:
                   caractere_mod = chr(ord(caractere) - chave_ascii)
                else:
                    caractere_mod = chr(90 - (65 - (ord(caractere) - chave_ascii)))

                mensagem_encriptada += caractere_mod

      print(mensagem_encriptada)     


if __name__ == "__main__":
     tipo = sys.argv[1]
     chave = sys.argv[2]
     mensagem_original = sys.argv[3]

     cesar(tipo, chave, mensagem_original)