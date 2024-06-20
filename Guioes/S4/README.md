# Respostas das Questões

### Perguntas e Respostas

- **Q1:Qual o impacto de se considerar um NONCE fixo (e.g. tudo 0)? Que implicações terá essa prática na segurança da cifra?**

    **R:** A utilização de um NONCE fixo, como por exemplo, com todos os bits a zero, na cifra ChaCha20, tem implicações significativas na segurança. O NONCE desempenha um papel importante no algoritmo e a sua repetição ou previsibilidade compromete a cifra. O principal impacto é a perda da propriedade de não repetição, pois como o Nonce é usado juntamente com a Key, se o NONCE for sempre fixo, com a mesma chave vai produzir sempre o mesmo keystream. Isto faz com que surja vulnerabilidade, incluindo padrões previsíveis no texto cifrado, tornando-o suscetível a análises estatísticas. Além disso, a falta de diversidade no NONCE facilita ataques de força bruta, comprometendo a confidencialidade dos dados e violando a propriedade fundamental de não repetição.


- **Q2:Qual o impacto de utilizar o programa chacha20_int_attck.py nos criptogramas produzidos pelos programas cfich_aes_cbc.py e cfich_aes_ctr.py? Comente/justifique a resposta.**
  
    **R:** No modo CBC, um ataque a um bloco específico afetará não apenas esse bloco, mas também todos os blocos subsequentes devido à dependência entre os blocos de texto cifrado. Se o bloco atacado for o primeiro, todos os blocos subsequentes serão afetados diretamente. Se o bloco atacado estiver mais adiante na sequência, a alteração se propagará de forma consecutiva para os blocos seguintes. Em resumo, o impacto de um ataque no modo CBC se estende aos blocos subsequentes na sequência da mensagem.

  Por outro lado, no modo de operação CTR (Counter), cada bloco de texto cifrado é gerado de forma independente, sem depender de blocos anteriores ou posteriores. Portanto, se um bloco específico for atacado no modo CTR, a alteração afetará apenas esse bloco em particular, sem afetar diretamente os blocos subsequentes. Cada bloco é cifrado independentemente usando um contador único, o que significa que uma modificação em um bloco não terá impacto nos blocos adjacentes na sequência. Em resumo, no modo CTR, o impacto de um ataque é limitado ao bloco modificado e não se propagará para os blocos subsequentes na sequência da mensagem.


# Relatório do Guião da Semana 4

## Cifra de Ficheiro

### Descrição Geral

Nesta semana, explorámos a cifra de ficheiro para garantir a confidencialidade dos dados armazenados. 
Utilizamos diferentes cifras para entender as suas propriedades.

### PROG: cfich_chacha20.py

O programa `cfich_chacha20.py` foi projetado para cifrar e decifrar um ficheiro utilizando a cifra sequencial ChaCha20. Ele aceita diferentes operações, como setup, enc (cifragem), e dec (decifragem), e requer argumentos específicos para cada operação.

### Operações

1. **setup <fkey>:**
   - Cria um ficheiro contendo uma chave apropriada para a cifra ChaCha20 com o nome <fkey>.

2. **enc <fich> <fkey>:**
   - Cifra o ficheiro especificado (<fich>) usando a chave lida do ficheiro <fkey>.
   - O criptograma resultante é gravado como <fich>.enc.

3. **dec <fich> <fkey>:**
   - Decifra o criptograma contido no ficheiro especificado (<fich>), utilizando a chave lida do ficheiro <fkey>.
   - Armazena o texto-limpo recuperado num ficheiro com nome <fich>.dec.


## PROG: chacha20_int_attck.py
A cifra ChaCha20, por si só, não garante integridade dos dados. O programa `chacha20_int_attck.py` ilustra como a informação cifrada pode ser manipulada. Recebe argumentos como <fctxt> <pos> <ptxtAtPos> <newPtxtAtPos>, onde <fctxt> é o nome do ficheiro com o criptograma, <pos> é a posição onde sabemos ter sido cifrado <ptxtAtPos>, e <newPtxtAtPos> é o resultado desejado ao decifrar o ficheiro. O criptograma manipulado é gravado em <fctxt>.attck.


## PROG: cfich_aes_cbc.py e cfich_aes_ctr.py
Com o objetivo de expandir as capacidades de cifragem de ficheiros, foram desenvolvidos os programas `cfich_aes_cbc.py` e `cfich_aes_ctr.py`. Ambas as implementações utilizam o algoritmo de cifra por blocos AES, sendo adaptadas para os modos Cipher Block Chaining (CBC) e Counter (CTR), respetivamente.

### cfich_aes_cbc.py

Para testar o `cfich_aes_cbc.py` recorremos aos seguintes comandos:

Para gerar a key:

```bash
 python3 cfich_aes_cbc.py setup chave_cbc.txt
```
Para fazer o encoding do file `testarcbc.txt`:

```bash
python3 cfich_aes_cbc.py enc testarcbc.txt chave_cbc.txt
```
Para fazer o decoding do file gerado pelo enc `testarcbc.txt.enc`:

```bash
python3 cfich_aes_cbc.py dec testarcbc.txt.enc  chave_cbc.txt
```

### cfich_aes_ctr.py

Para testar o `cfich_aes_ctr.py` recorremos aos seguintes comandos:
Para gerar a key:

```bash
 python3 cfich_aes_ctr.py setup chave_ctr.txtt
```
Para fazer o encoding do file `testarctr.txt`:

```bash
python3 cfich_aes_ctr.py enc testarctr.txt chave_ctr.txt
```
Para fazer o decoding do file gerado pelo enc `testarctr.txt.enc`:

```bash
python3 cfich_aes_ctr.py dec testarctr.txt.enc chave_ctr.txt
```

## PROG: pbenc_chacha20.py

O `pbenc_chacha20.py` utiliza Encriptação Baseada em Passwords (PBE), adotando uma abordagem mais segura. Ao derivar chaves a partir de uma passphrase usando Funções de Derivação de Chave (KDFs), como o PBKDF2, e armazenar os segredos em keystore encriptados, torna-o numa opção mais segura segura e confiável em comparação com o `cfich_chacha20.py`.

Para testar o programa `pbenc_chacha20.py`, utilizamos os seguintes comandos:

Como já não é necessário gerar uma key, passamos diretamente para o encoding do file da seguinte forma:

```bash
python3 pbenc_chacha20.py enc mensagem.txt
```

Para fazer o decoding do file mensagem.txt.enc (gerado pelo encoding do file), utilizamos o seguinte comando:

```bash
python3 pbenc_chacha20.py dec mensagem.txt.enc
```

