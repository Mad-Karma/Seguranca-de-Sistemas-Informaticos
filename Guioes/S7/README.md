# Respostas das Questões

### Perguntas e Respostas

- **Q1: Como pode verificar que as chaves fornecidas nos ficheiros mencionados (por exemplo, em `MSG_SERVER.key` e `MSG_SERVER.crt`) constituem de facto um par de chaves RSA válido? **

    **R: ** Para confirmar se as chaves nos ficheiros `MSG_SERVER.key` e `MSG_SERVER.crt` formam um par de chaves RSA válido, podemos seguir os seguintes passos. Primeiro, analisamos o formato dos ficheiros para garantir que estejam no formato esperado para chaves RSA, como PEM ou DER. Em seguida, carregamos e examinamos os ficheiros para garantir que correspondem ao formato correto e que a chave privada e o certificado sejam válidos.

  Após essa validação inicial, verificamos se a chave pública contida no certificado (`MSG_SERVER.crt`) corresponde à chave privada no ficheiro da mesma (`MSG_SERVER.key`).

  Finalmente, realizamos um teste que consiste em encriptar e desencriptar uma mensagem utilizando a chave, de modo a garantir que funcione conforme o esperado, confirmando assim a validade do par de chaves RSA. Esta abordagem permite-nos garantir a integridade e a funcionalidade das chaves fornecidas.

- **Q2: Visualize o conteúdo dos certificados fornecidos, e refira quais dos campos lhe parecem que devam ser objecto de atenção no procedimento de verificação. **
  
    **R:** Após uma análise dos certificados fornecidos, podemos concluir que é necessário ter em atenção as datas de validade, o campo "Nome Comum" e a assinatura digital. Além disso, é importante verificar a cadeia de certificados e verificar a correspondência entre a chave pública e privada. Estes são os campos que requerem maior atenção no procedimento de verificação dos certificados utilizados.



# Relatório do Guião da Semana 7

## Utilização de Certificados

### Descrição Geral
Nesta semana foi nos proposto implementar duas funcionalidades, sendo elas, a validação de certificados e o protocolo Station-to-Station simplificado. Para atingir o resultado esperado, desenvolvemos os seguintes programas:

### PROG: `Client_sts.py` & `Server_sts.py`


Os programas Client_sts.py e Server_sts.py implementam um sistema de troca de mensagens entre um cliente e um servidor utilizando o protocolo Station-to-Station simplificado. Para garantir a segurança da comunicação, utilizamos a cifra autenticada AES-GCM, assim como a validação de certificados. Estes certificados desempenham um papel crucial na autenticação das chaves públicas trocadas no início da conexão entre cliente e servidor.

Tanto o cliente quanto o servidor validam os certificados para assegurar a autenticidade das chaves públicas. Essa validação inclui a verificação da origem, do período de validade, do nome comum e das extensões dos certificados. Além disso, é realizada a verificação das assinaturas para confirmar a autenticidade dos certificados.

Outra característica importante do nosso programa é a implementação do protocolo Station-to-Station simplificado. Esse protocolo envolve a troca de chaves Diffie-Hellman, seguida por uma troca de assinaturas para autenticação adicional. Durante a troca de chaves Diffie-Hellman, o cliente e o servidor geram chaves públicas e privadas e calculam uma chave compartilhada. Após isso, eles assinam as chaves públicas trocadas e verificam as assinaturas para garantir a autenticidade. Uma vez autenticadas, eles derivam uma chave de sessão compartilhada para encriptar as mensagens subsequentes. Esse protocolo assegura uma troca segura de chaves e a autenticação mútua entre as partes.

Para executar o programa, temos de abrir dois terminais diferentes, um para o servidor e outro para o cliente.

No primeiro terminal vamos executar o `Server_sts.py`, da seguinte forma:
```bash
python3 Server_sts.py
```

Tendo o servidor aberto, podemos passar para o `Client_sts.py`, e podemos corre-lo da seguinte forma:
```bash
python3 Client_sts.py
```

Desta forma, o cliente e o servidor já estão prontos para comunicar.





