# Respostas das Questões

### Perguntas e Respostas

- **Q1:Qual o impacto de executar o programa `chacha20_int_attck.py` sobre um criptograma produzido por `pbenc_chacha20_poly1305.py`? Justifique.**

    **R:** Ao manipular um criptograma gerado pelo pbenc_chacha20_poly1305.py com o programa chacha20_int_attck.py, o impacto é limitado devido ao uso do Poly1305, que é responsável por proteger a integridade dos dados cifrados. Embora seja possível manipular os dados cifrados numa posição específica, qualquer alteração resultaria numa falha na verificação de autenticação, tornando difícil realizar uma manipulação bem-sucedida sem a chave de autenticação correspondente.

- **Q2:Qual o motivo da sugestão de usar `m2` com mais de 16 byte? Será possível contornar essa limitação?**
  
    **R:** A sugestão de utilizar uma mensagem m2 com mais de 16 bytes é feita devido ao facto de o CBC-MAC se tornar mais seguro quando mensagens mais longas são utilizadas, uma vez que a tag é baseada no último bloco do criptograma. Isso aumenta a complexidade da tag, dificultando a sua falsificação. No entanto, mesmo com essa prática, não é possível eliminar completamente a vulnerabilidade do CBC-MAC a ataques de extensão de comprimento, pois ainda é possível construir uma nova mensagem que se encaixe perfeitamente no último bloco de criptograma da mensagem original.



# Relatório do Guião da Semana 5

## Cifra Autenticada de Ficheiro

### Descrição Geral

Nesta semana, foi nos proposto melhorar a funcionalidade no programa de cifra do ficheiro para garantir simultaneamente a confidencialidade dos dados e a integridade da informação. E para tal, elaboramos os seguintes programas visando esse objetivo:

### PROG: `pbenc_aes_ctr_hmac.py`


O program `pbenc_aes_ctr_hmac.py` utiliza o algoritmo ChaCha20 para cifrar e decifrar ficheiros. A partir de uma chave fornecida pelo utilizador é gerada uma chave para a cifragem. Durante o processo de cifragem, é gerado um nonce aleatório sendo utilizado o algoritmo ChaCha20 para cifrar o ficheiro, acrescentando um código de autenticação HMAC-SHA256 para assegurar a integridade dos dados. Na decifragem, o programa verifica a integridade dos dados através da utilização de um código de autenticação HMAC-SHA256.

Para testar o programa podemos correr os seguintes comandos: 

Para encriptar a mensagem, utilizamos o seguinte comando:

```bash
python3 pbenc_aes_ctr_hmac.py enc mensagem.txt
```

De seguida, para desencriptar a mensagem corremos o seguinte comando:

```bash
 python3 pbenc_aes_ctr_hmac.py dec mensagem.txt.enc
```


### PROG: `pbenc_chacha20_poly1305.py`

O programa utiliza a cifra ChaCha20Poly1305 para criptografar e autenticar dados. A cifra ChaCha20 gera uma sequência pseudoaleatória de bytes (keystream) a partir de uma chave secreta e um nonce, utizada para criptograr os dados. Enquanto isso o Poly1305 garante que os dados permaneçam íntegros e não tenham sido modificados, proporcionando uma camada adicional de segurança além da criptografia.

Para testar o programa podemos correr os seguintes comandos: 

Para encriptar a mensagem, utilizamos o seguinte comando:

```bash
python3 pbenc_chacha20_poly1305.py enc mensagem.txt
```

De seguida, para desencriptar a mensagem corremos o seguinte comando:

```bash
 python3 pbenc_chacha20_poly1305.py dec mensagem.txt.enc
```

### PROG: `pbenc_aes_gcm.py`

O programa utiliza a cifra AES-GCM, através de uma senha, fornecida pelo utilizador, é derivada uma chave utilizando o algoritmo PBKDF2 com SHA256. Durante a criptografia um salt e um nonce são gerados de forma aleatória e escritos no ficheiro de saída junto com a mensagem criptografada. Durante a descriptografia, o salt e o nonce são lidos do ficheiro de entrada e juntamente com a chave são utilizados para descriptografar a mensagem, garantindo a integridade dos dados.

Para testar o programa podemos correr os seguintes comandos: 

Para encriptar a mensagem, utilizamos o seguinte comando:

```bash
python3 pbenc_aes_gcm.py enc mensagem.txt
```

De seguida, para desencriptar a mensagem corremos o seguinte comando:

```bash
 python3 pbenc_aes_gcm.py dec mensagem.txt.enc
```

