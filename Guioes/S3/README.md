# Respostas das Questões

### Perguntas e Respostas

- **Q1: Consegue observar diferenças no comportamento dos programas `otp.py` e `bad_otp.py`? Se sim, quais?**

    **R:** Observamos que `otp.py` usa um gerador de números aleatórios seguro, enquanto `bad_otp.py` usa um gerador inseguro (`bad_prng`), introduzindo uma vulnerabilidade.

- **Q2: O ataque realizado no ponto anterior não entra em contradição com o resultado que estabelece a "segurança absoluta" da cifra *one-time pad*? Justifique.**
  
    **R:** O ataque em `bad_otp_attack.py` não entra em contradição com a segurança absoluta da cifra One-Time Pad, pois a vulnerabilidade está na implementação do gerador de números aleatórios, não na cifra em si. A segurança da OTP permanece intacta quando implementada corretamente com uma chave verdadeiramente aleatória.



# Relatório do Guião da Semana 3

## Cifras Clássicas: César e Vigenère

### Descrição Geral

Nesta semana, exploramos diversas cifras sendo elas:
Cifra de César
Cifra de Vigenère
Cifra **One-Time-Pad** (OTP)
Para cada uma das 3 primeiras realizamos a sua implementação e explorámos as suas fraquesas implementando ataques a cada uma delas. Na última, após a sua implementação com um gerador de números aleatório seguro, elabourou-se a criação do `bad_otp.py`
que utiliza um gerador inseguro, e de seguida elabourou-se o `bad_otp_attack.py`.

### Cifra de César

Implementamos a cifra de César em Python, com um programa chamado `cesar.py`. Este programa recebe uma operação (`enc` para cifrar ou `dec` para decifrar), uma chave secreta e a mensagem a ser cifrada ou decifrada. Após isto testámos se a implementação da cifra estava correta através dos seguintes comandos, através do terminal:

```bash
$ python3 cesar.py enc G "CartagoEstaNoPapo"
```
```bash
$ python3 cesar.py dec G "IGXZGMUKYZGTUVGVU"
```
Tendo obtido como respostas respetivamente:
```bash
IGXZGMUKYZGTUVGVU
```
```bash
CARTAGOESTANOPAPO
```

Depois de implementarmos e testarmos a cifra de César, passámos para implementar o script `cesar_attack.py` para realizar um ataque à cifra de César. 

O ataque envolve fornecer um criptograma e uma lista de palavras que podem estar presentes no texto original. O programa tenta todas as possíveis chaves para encontrar uma correspondência com as palavras fornecidas.

Para testar o programa foram executados os seguintes comandos no terminal:

```bash
$ python3 cesar_attack.py "IGXZGMUKYZGTUVGVU" BACO TACO
```
```bash
$ python3 cesar_attack.py "IGXZGMUKYZGTUVGVU" BACO PAPO
``` 
Tendo obdito como respostas, respetivamente:
```bash
G
```
```bash
CARTAGOESTANOPAPO
```

### Cifra de Vigenère

De seguida, criamos o programa `vigenere.py`, ela funciona de forma semelhante ao `cesar.py`, mas é capaz de lidar com uma chave representada por uma palavra.

Para testar o nosso código usamos os seguintes comandos, no terminal:

```bash
$ python3 vigenere.py enc BACO "CifraIndecifravel"
```

```bash
$ python3 vigenere.py dec BACO "DIHFBIPRFCKTSAXSM"
```

E obtivemos os seguintes outputs, respetivamente:

```bash
DIHFBIPRFCKTSAXSM
```
```bash
CIFRAINDECIFRAVEL
```

Depois tentamos implementar o programa chamado `vigenere_attack.py` para atacar a cifra de Vigenère. 

Este programa exige o tamanho da chave, o criptograma e uma lista de palavras presentes no texto original. Similar ao ataque à cifra de César, tenta encontrar a chave que corresponde às palavras fornecidas.
No entanto, a implementação não ficou a 100%, pois não conseguimos implementar o cálculo da chave através do uso das letras mais frequentes do alfabeto.
Para testar este programa corremos no terminal o seguinte comando:

```bash
$ python3 vigenere_attack.py 3 "PGRGARHSFHPRGCVHOJHWEPZRSCJFIVSOFRWUTBKPZGGOZPZLHWKPBR" PAPO PRAIA
```
Do qual deveríamos ter obtido o seguinte output:
```bash
POR
ASARMASEOSBAROESASSINALADOSQUEDAOCIDENTALPRAIALUSITANA
```
Mas obtivemos:

```bash
HOR
ISAZMAAEOABAZOEAASAINILALOSYUELAOKIDMNTILPZAIILUAITINA
```

### Cifra One-Time Pad (OTP)

Implementámos também o script `opt.py` onde implementámos a cifra OTP que é considerada teoricamente segura quando a chave é completamente aleatória, do mesmo tamanho que a mensagem e usada apenas uma vez. 
O nosso programa permite configurar uma chave, cifrar e decifrar mensagens usando operações de XOR.

Estrutura dos comandos:
* caso o primeiro argumento do program seja `setup`, o segundo argumento será o número de bytes aleatórios a gerar e o terceiro o nome do ficheiro para se escrever os bytes gerados.
 * caso o primeiro argumento seja `enc`, o segundo será o nome do ficheiro com a mensagem a cifrar e o terceiro o nome do ficheiro que contém a chave one-time-pad. O resultado da cifra será guardado num ficheiro com nome do ficheiro da mensagem cifrada com sufixo `.enc`.
 * caso o primeiro argumento seja `dec`, o segundo será o nome do ficheiro a decifrar e o terceiro argumento o nome do ficheiro com a chave. O resultado será guardado num ficheiro cujo nome adiciona o sufixo `.dec` ao nome do ficheiro com o criptograma.

Para testar o código implementado recorremos aos seguintes comandos no terminal:
```bash
$ python3 otp.py setup 30 otp.key
$ echo "Mensagem a cifrar" > ptxt.txt
$ python3 otp.py enc ptxt.txt otp.key
$ python3 otp.py dec ptxt.txt.enc otp.key
$ cat ptxt.txt.enc.dec
Mensagem a cifrar
```

De seguida, com o objetivo de simular uma situação de vulnerabilidade, desenvolvemos o programa `bad_otp.py`, que substitui o gerador de números aleatórios seguro por um gerador inseguro chamado `bad_prng`, este usa a biblioteca `random`, resultando em números pseudo-aleatórios que podem comprometer a segurança.

```bash
$ python3 bad_otp.py setup 30 bad_otp.key
$ echo "Mensagem a cifrar" > ptxt.txt
$ python3 bad_otp.py enc ptxt.txt bad_otp.key
$ python3 bad_otp.py dec ptxt.txt.enc bad_otp.key
$ cat ptxt.txt.enc.dec
Mensagem a cifrar
```


À semelhança do resto dos programas, após termos o bad_otp funcional, criamos o programa `bad_otp_attack.py`, no qual tentámos explorar a vulnerabilidade introduzida pelo gerador inseguro ao realizar um ataque de força bruta na cifra OTP usando uma lista de palavras que pertencem à mensagem para recuperar a mensagem original. No entanto apesar de várias tentativas não conseguimos fazer com que ele decifrasse a mensagem.

**NOTA:** Apesar de não termos conseguido implementar corretamente o `vigenere_attack.py` e o `bad_otp_attack.py` percebemos a ideia por trás dos mesmos e as falhas que eles pretendiam explorar.





