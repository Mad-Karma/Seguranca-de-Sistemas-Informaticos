# Respostas das Questões
## Q1
* Qual a versão da biblioteca `cryptography` instalada?

Ao utilizar no terminal do ubunto, usando wsl, o seguinte comando :
  ```bash
$ python3  -c "import cryptography; print(cryptography.__version__)" 
```
 Obtivemos a versão "42.0.2".
 
# Relatório do Guião da Semana 2
Após a instalação de todos os programas necessários para a realização dos guiões e dos trabalhos futuros que irão ser realizados, foi efetuado um pequeno script em python chamado wc.py para testar se a instalação da 'cryptography'. O script contém um pequeno programa que conta o número de linhas, palavras e caracteres de um ficheiro passado como argumento.

* Para testar o mesmo foi criado ainda um ficheiro exemplo.txt, que consta em anexo, e de seguida usado o comando:
  ```bash
   $ python3 wc.py exemplo.txt
  ```
  O que nos permitui obter  como resultado o seguinte:
   ```bash
       1       98      606
     ```
