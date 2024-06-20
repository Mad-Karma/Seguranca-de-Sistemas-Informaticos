# Relatório do Projeto de Criptografia Aplicada

<p align="center">
  <img src='https://upload.wikimedia.org/wikipedia/commons/9/93/EEUMLOGO.png' width="30%" />
</p>

<h3 align="center">Licenciatura em Engenharia Informática <br> Projecto de Criptografia Aplicada <br> <br> TP1 <br> 2023/2024 </h3>

<h3 align="center"> Autores 🤝 </h3>

<div align="center">

| Nome                           |  Número | Username github |
|--------------------------------|---------|-----------------|
| Diogo Gabriel Lopes Miranda    | A100839 |DMirandex        |
| João Ricardo Ribeiro Rodrigues | A100598 |Mad-Karma        |
| Sandra Fabiana Pires Cerqueira | A100681 |SandraCerqueira1 |

</div>

*******

## Introdução
* Neste relatório, apresentamos o projeto de Criptografia Aplicada desenvolvido como parte do trabalho prático (TP1), da unidade curricular Segurança de Sistemas Informáticos. O projeto consistiu na implementação de um serviço de Message Relay que proporciona uma comunicação segura entre os membros de uma organização. O serviço é suportado por um servidor responsável por manter o estado da aplicação e interagir com os clientes. O objetivo principal é garantir a autenticidade das mensagens trocadas, bem como a integridade e confidencialidade das comunicações.
*******
## Descrição do Projeto
* O projeto envolveu o desenvolvimento de dois programas em Python: `msg_server.py` e `msg_client.py`. O servidor é responsável por responder às solicitações dos clientes e manter o estado da aplicação, enquanto o cliente é executado por cada utilizador para que este consiga ter acesso às funcionalidades oferecidas pelo serviço.
*******
### Comandos da Aplicação Cliente

Os clientes interagem com o sistema através do programa `msg_client.py`, que aceita os seguintes comandos:

- `-user <FNAME>`: Especifica o ficheiro *.p12* que possui os dados do utilizador.
- `send <UID> <SUBJECT>`: Envia uma mensagem com assunto especificado para um determinado o destinatário com o `<UID>` indicado.
- `askqueue`: Solicita ao servidor a lista de mensagens não lidas na queue do utilizador atual.
- `getmsg <NUM>`: Solicita ao servidor o envio de uma mensagem específica que está na queue do utilizador.
- `help`: Imprime as instruções de uso do programa.
*******
## **Processo de Implementação**

Para iniciar a implementação do nosso serviço de Message Replay, utilizamos o código fornecido pela equipa docente nos ficheiros Client.py e Server.py  e incorporámo-lo nos nossos programas msg_server.py e msg_client.py, respetivamente. Estes ficheiros já estabeleciam a base para a comunicação cliente-servidor. No servidor, a cada cliente era atribuído um número de ordem e as mensagens enviadas por ele eram impressas no terminal, convertidas para maiúsculas e enviadas de volta para o cliente. Adicionalmente, o servidor registava quando um cliente fechava a conexão.


### **Algoritmos do Guiao7 como base da conexão segura**
Tendo esta base, o grupo optou por reutilizar parte do trabalho que desenvolveu no Guião da Semana 7. 

#### **Porquê os algortimos do guião 7?**

Optamos por recorrer a este guião, pois os algoritmos utilizados nele são comprovadamente seguros e amplamente reconhecidos na comunidade de segurança de sistemas informática. Aqui estão alguns pontos-chave que destacam a segurança desses algoritmos:

* 1. **Diffie-Hellman (DH):** O protocolo Diffie-Hellman é amplamente utilizado para estabelecer chaves partilhadas de forma segura numa rede não segura. A sua segurança baseia-se na dificuldade computacional do problema do logaritmo discreto, tornando-o resistente a ataques de força bruta.

* 2. **RSA (Rivest-Shamir-Adleman):** O algoritmo RSA é amplamente utilizado para assinaturas digitais e criptografia de chave pública. A sua segurança baseia-se na dificuldade de factorização de números inteiros grandes, o que é considerado um problema computacionalmente difícil. Até ao momento, nenhum método eficiente de factorização de números inteiros grandes foi descoberto, tornando o RSA seguro na prática.
     
* 3. **Padding PSS (Probabilistic Signature Scheme):** O esquema de preenchimento PSS é utilizado para assinaturas RSA e oferece uma margem de segurança adicional contra ataques de quebra de assinatura. Utiliza técnicas probabilísticas para criar uma assinatura única para cada mensagem, dificultando a previsibilidade das assinaturas.

* 4. **Certificados X.509:** Os certificados X.509 são amplamente utilizados para autenticar entidades numa rede, como servidores e clientes. Fornecem uma estrutura robusta para verificar a autenticidade das chaves públicas através de uma cadeia de confiança, garantindo que as comunicações sejam seguras e fiáveis.
  

Ao longo do semestre tivemos a oportunidade de trabalhar com diversos algoritmos, no decorrer da realização dos diversos guiões práticos. Agora, ao nos depararmos com este projeto, surge a oportunidade de aplicar o conhecimento adquirido nos guiões anteriores, especialmente no Guião da semana 7. Pois, neste último, como referido em cima, para além de lidarmos com a troca segura de mensagens entre cliente e servidor, também abordamos a questão dos certificados X509.

Neste projeto também temos de lidar com certificados, e a sua inclusão e tratamento devido é crucial, pois isto vai além de uma simples comunicação segura. Agora, não estamos apenas preocupados em garantir que as mensagens são transmitidas de forma confidencial e íntegra, mas também em verificar a autenticidade das partes envolvidas na comunicação.

Portanto, ao escolhermos utilizar como base os algoritmos do trabalho desenvolvido no Guião 7, estamos a garantir não apenas a segurança da comunicação, mas também a validade e autenticidade das chaves públicas utilizadas, proporcionando uma camada adicional de proteção para o nosso projeto.

*******
### Trabalho do S7
Nesse guiao tivemos então que complementar o programa com o acordo de chaves Diffie-Hellman para incluir a funcionalidade análoga à do protocolo Station-to-Station. Isso envolveu a troca de assinaturas entre um cliente e um servidor para garantir a autenticidade e integridade da comunicação, utilizando o algoritmo de assinatura RSA. Também enfrentámos o desafio de gerir a troca de mensagens envolvendo várias componentes com tamanhos imprevisíveis, para o qual utilizámos as funções `mkpair` e `unpair` para serializar e desserializar pares bytestrings.

Além disso, introduzimos o uso de certificados x509 para estabelecer a autenticidade das chaves públicas utilizadas, certificados estes que contem chaves RSA e são os mesmos que nos foram fornecidos neste projeto nos ficheiros: [`MSG_CA.crt`](projCA/MSG_CA.crt) , [`MSG_CLI1.crt`](projCA/MSG_CLI1.crt), [`MSG_CLI1.key`](projCA/MSG_CLI1.key), [`MSG_SERVER.crt`](projCA/MSG_SERVER.crt), [`MSG_SERVER.key`](projCA/MSG_SERVER.key). 

Para validar estes certificados, implementamos métodos para verificar o período de validade, o titular do certificado e a aplicabilidade do mesmo. Como a biblioteca cryptography oferece suporte limitado para a validação de certificados, adotamos os métodos fornecidos pela equipa docente para tratar dessas validações.
*******
#### Considerações iniciais

* O servidor e o cliente estão preparados para receber arrays de bytes. Como os dados com que nós trabalhamos são por norma strings, certificados ou assinaturas, precisamos de os serializar antes de os enviar ( e desserializar quando receber). Para tal, utilizamos o `encode()/decode()`  e as funções de serialização/desserialização das bibliotecas utilizadas.

* Deixámos de usar diretamente os ficheiros *".key"* e *".cert"* , uma vez que agora estas informações estavam todas nos ficheiros *".p12"* fornecidos, sendo eles:

    * [`MSG_CLI1.p12`](projCA/MSG_CLI1.p12), [`MSG_CLI2.p12`](projCA/MSG_CLI2.p12) e [`MSG_CLI3.p12`](projCA/MSG_CLI3.p12) -- *keystores* contendo os certificados e chave privadas do servidor e de três utilizadores. As *keystores* não dispõe de qualquer protecção[^1]. Por conveniencia, as *keystores* contém ainda o certificado da EC do sistema.


Como agora o conteúdo do certificado e as keys estão nos *".p12"* utilizámos a seguinte função para facilmente extrair o conteúdo das *keystores* recorrendo à classe [PKCS12](https://cryptography.io/en/stable/hazmat/primitives/asymmetric/serialization/#pkcs12) da biblioteca `cryptography`:

```python
def get_userdata(p12_fname):
    with open(p12_fname, "rb") as f:
        p12 = f.read()
    password = None # p12 não está protegido...
    (private_key, user_cert, [ca_cert]) = pkcs12.load_key_and_certificates(p12, password)
    return (private_key, user_cert, ca_cert)
```

Utilizando esta função, conseguimos então extrair a Private Key RSA, o certificado, e o certificado da autoridade certificadora (CA).
*******
## <u> msg_client.py </u>
O ficheiro `msg_client.py` contém as funcionalidades do cliente para nosso sistema de *Message Relay*.

#### <u>  Principais etapas do cliente </u>
Assim que iniciamos o programa, a primeira coisa a ser efetuada é a determinação de qual será o ficheiro *.p12* que será utilizado na função ` get_userdata `. Este pode ser indicado utilizando o comando ` -user <FNAME> `, sendo FNAME o nome do *.p12*, ou, no caso de o comando não ser utilizado, o sistema utiliza um ficheiro predefinido chamado `userdata.p12`.

```python
# comando: -user <FNAME>
        if sys.argv[1] == "-user":
            self.ficheiro = sys.argv[2]
            self.private_key_RSA, self.certificado_cliente, self.certificado_CA = get_userdata(self.ficheiro)
            self.check_user = 1
        else:
            self.ficheiro = "userdata.p12"
            self.private_key_RSA, self.certificado_cliente, self.certificado_CA = get_userdata(self.ficheiro)
```

Tendo obtido a Private Key RSA, o certificado do cliente e o certificado CA, procedemos à aplicação do protocolo *Station-to-Station*, implementado no guião da semana 7. Este é uma versão simplificada do protocolo original. 

### <u> Funcionamento do protocolo </u>


* Inicialmente no cliente, é calculada a sua chave pública através da sua chave privada (obtida usando as constantes p e g fornecidas pela equipa docente no guião da semana 6).

```python
# Fazer o protocolo station to station
        if self.msg_cnt == 1:
            parameters_numbers = dh.DHParameterNumbers(p, g)
            parameters = parameters_numbers.parameters(default_backend())
            self.peer_private_key = parameters.generate_private_key()
            self.peer_public_key = self.peer_private_key.public_key()
            self.peer_public_key_serialized = self.peer_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

            return self.peer_public_key_serialized
```


* Posto isto, a chave pública do cliente é enviada para o servidor. 
* Depois o servidor envia ao cliente  a sua public key, a sua assinatura e o seu certificado.


### <u> Obtenção das assinaturas </u> 

As assinaturas são geradas da seguinte forma:

**No cliente:**
* Assinando a concatenação da chave publica do cliente com a chave publica do servidor;

**No servidor:**

* Assinando a concatenação da chave publica do servidor com a chave publica do cliente;


```python
# codigo da criação da assinatura do servidor
            signature_peer = self.private_key_RSA.sign(
                self.peer_public_key_serialized + server_public_key_serialized,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
```


### <u> Validação do certificado </u>

É então efetuada uma validação do certificado recebido, sendo validado se: 

* O certificado ainda tem validade temporal, utilizando a função `cert_validtime`, fornecida no guião da semana 7;
```python
def cert_validtime(cert, now=None):
    """valida que 'now' se encontra no período
    de validade do certificado."""
    if now is None:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
    if now < cert.not_valid_before_utc or now > cert.not_valid_after_utc:
        raise x509.verification.VerificationError(
            "Certificate is not valid at this time"
        )
```

* Se foi efetivamente emitido pela CA, utilizando a função `verify_directly_issued_by` (função da biblioteca x509)
  
* Se o subject corresponde ao esperado (diferente caso seja um certificado do servidor ou de um cliente), utilizando a função `cert_validsubject`
```python
def cert_validsubject(cert, ent):
    """verifica atributos do campo 'subject'. 'attrs'
    é uma lista de pares '(attr,value)' que condiciona
    os valores de 'attr' a 'value'."""

    if ent == "MSG_SERVER":
        cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        result = bool(re.search(r"SSI Message Relay Server", cn))
    else:
        cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        result = bool(re.search(r"SSI MSG Relay Client", cn))

    if result == False:
        raise x509.verification.VerificationError(
            "Certificate subject does not match expected value"
        )
```

* As extensões do certificado são o esperado, utilizando a função `cert_validexts`
```python
def cert_validexts(cert, policy=[]):
    """valida extensões do certificado.
    'policy' é uma lista de pares '(ext,pred)' onde 'ext' é o OID de uma extensão e 'pred'
    o predicado responsável por verificar o conteúdo dessa extensão."""
    for check in policy:
        ext = cert.extensions.get_extension_for_oid(check[0]).value
        if not check[1](ext):
            raise x509.verification.VerificationError(
                "Certificate extensions does not match expected value"
            )
```

A função que realiza todas estas verificações é a `valida_cert`, que nos indica se o certificado é válido.

```python
def valida_cert(ca_cert, cert):
    if cert.subject:
        for attr in cert.subject:
            if attr.oid == x509.NameOID.PSEUDONYM:
                sender_uid = attr.value.strip()

    if sender_uid == "MSG_SERVER":
        try:
            cert.verify_directly_issued_by(ca_cert)
            cert_validtime(cert)
            cert_validsubject(cert, sender_uid)
            cert_validexts(
                cert,[(
                        x509.ExtensionOID.EXTENDED_KEY_USAGE,
                        lambda e: x509.oid.ExtendedKeyUsageOID.SERVER_AUTH in e,
                    )],
            )
            return True
        except:
            print("Server certificate is invalid!")
            return False
    
    else:
        try:
            cert.verify_directly_issued_by(ca_cert)
            cert_validtime(cert)
            cert_validsubject(cert, sender_uid)
            cert_validexts(
                cert,[(
                        x509.ExtensionOID.EXTENDED_KEY_USAGE,
                        lambda e: x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH in e,
                    )],
            )
            return True
        except:
            print("Client certificate is invalid!")
            return False
```


### <u> Validação da assinatura </u>

É também validada a assinatura recebida, utilizando a public key rsa do servidor e a concatenação por ele assinada, da seguinte forma:
```python
public_key_server_RSA.verify(
                    signature,
                    server_public_key_serialized + self.peer_public_key_serialized,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
```

Se os parâmetros que o servidor enviou (a sua assinatura e o seu certificado) forem inválidos, a conexão é encerrada e é apresentada uma mensagem de erro indicando o que é que falhou. Caso sejam válidos, são geradas a shared key e a deriverd_key do cliente, da seguinte forma:
```python
self.server_public_key = load_pem_public_key(server_public_key_serialized, backend=default_backend())

                self.shared_key = self.peer_private_key.exchange(self.server_public_key)

                self.derived_key = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b'handshake data',
                ).derive(self.shared_key)

```
Posto tudo isto, é agora a vez do cliente assinar a concatenação, da forma referida na secção *`Obtenção de assinaturas`* deste relatório. Com a assinatura gerada, o cliente trata de a enviar, juntamente com o seu certificado, não havendo a necessidade de enviar a public key dele, uma vez que esta já foi enviada.
Como já referido anteriormente, o servidor está preparado para receber um array de bytes, portanto, utilizamos a função `mkpair` para juntar os dois parametros num só array de bytes.

*******

### <u> Comandos </u>


Após este processo de geração da derived key e de verificação de autenticidade das partes envolvidas na comunicação, o programa vai agora processar os comandos inseridos pelo utilizador.

Verificamos se já foi ou não lido um comando `-user <FNAME>`, em caso afirmativo o indice i em que começamos o nosso ciclo será 3 (saltamos os campos que continham o comando), em caso negativo começamos normalmente no indice 1.

```python
# escolha do indice inicial
 start_index = 3 if self.check_user == 1 else 1
```

## <u> send <UID> <SUBJECT></u>

Este é o comando que permite a um cliente enviar uma mensagem com assunto <SUBJECT> destinada ao utilizador com identificador <UID>, o conteúdo da mensagem é lido do stdin, e o tamanho é limitado a 1000 bytes.

**Envio do comando para o servidor**
Antes de se proceder à assinatura e envio da mensagem, é verificado se o tamanho da mensagem excede o limite de 1000 bytes. Essa verificação é realizada com a seguinte condição:

```python
mensagem = input()
                    if len(mensagem) > 1000:
                        sys.stderr.write("\nMSG RELAY SERVICE: message too long! Maximum allowed size is 1000 bytes.\n")
                        return None
```
Se o tamanho da mensagem ultrapassar o limite,  é exibida uma mensagem de erro, como se pode ver acima, e a execução do comando send é interrompida. Isto garante que apenas mensagens dentro do limite estabelecido sejam enviadas, evitando problemas relacionados a mensagens demasiado longas.

De seguida,é necessário incluir na mensagem o pseudónimo do cliente que quer realizar o envio, que é obtido a partir do seu certificado. Isso é feito verificando se o certificado do cliente contém informações sobre o sujeito (subject). Se sim, o código itera sobre os atributos do sujeito e procura pelo atributo com o identificador de objeto (OID) correspondente ao pseudónimo (x509.NameOID.PSEUDONYM).

Se esse atributo for encontrado, o valor associado a ele é extraído e armazenado na variável `uid_sender`, após serem removidos espaços em branco no início e no final do valor utilizando o método strip().

Isto garante que o pseudónimo do cliente seja incluído na mensagem, permitindo que o destinatário identifique o remetente.


```python
if self.certificado_cliente.subject:
                        for attr in self.certificado_cliente.subject:
                            if attr.oid == x509.NameOID.PSEUDONYM:
                                uid_sender = attr.value.strip()

```

Posto isto, o comando send realiza o processo de assinatura da mensagem antes de a enviar para o servidor. Este processo envolve a criação de uma string formatada contendo o remetente, o assunto e o conteúdo da mensagem, seguida pela sua codificação em bytes. Em seguida, é gerada uma assinatura  utilizando a chave privada RSA do cliente sobre essa mensagem formatada. A assinatura é então anexada à mensagem antes de ser enviada para o servidor. 

Esta assinatura gerada garante a autenticidade e integridade da mensagem, uma vez que apenas o cliente possui a chave privada correspondente à chave pública contida no seu certificado. Assim, o servidor pode verificar a autenticidade da mensagem utilizando a chave pública do cliente, que está incluída no seu certificado.

```python
formated_message = f"{uid_sender}:{subject}:{mensagem}"
                    formated_message = formated_message.encode()

                    
                    signature = self.private_key_RSA.sign(
                        formated_message,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )

```

Após o processo de assinatura, a mensagem é preparada para ser enviada para o servidor, sendo criptografada utilizando a cifra AES-GCM para garantir a confidencialidade e integridade dos dados durante a sua transmissão. Finalmente, a mensagem encriptada e é retornada para ser enviada ao servidor.

```python
pair_subject_mensagem = mkpair(subject.encode(), mensagem.encode())
                    pair_ass = mkpair(signature, pair_subject_mensagem)
                    pair_uid = mkpair(uid.encode(), pair_ass)
                    pair_geral = mkpair(arg.encode(), pair_uid)

                    mensagem_enc = self.aes_gcm_enc(pair_geral)

                    return mensagem_enc
```

O processo de envio da mensagem é encapsulado na função `aes_gcm_enc`, que utiliza a cifra AES-GCM para criptografar a mensagem antes de ser enviada para o servidor. Isto adiciona uma camada de segurança, garantindo que terceiros não consigam ler o conteúdo da mensagem.

```python

    def aes_gcm_enc(self, mensagem):        
        nonce = os.urandom(16)
        aesgcm = AESGCM(self.derived_key)

        mensagem_enc = nonce + aesgcm.encrypt(nonce, mensagem, None)

        return mensagem_enc

```

## <u> askqueue </u>

É através deste comando que um cliente solicita ao servidor que lhe envie a lista de mensagens não lidas da sua queue. Para cada mensagem na queue, é devolvida uma linha contendo: <NUM>:<SENDER>:<TIME>:<SUBJECT>, onde <NUM> é o número de ordem da mensagem na queue e <TIME> um timestamp adicionado pelo servidor que regista a altura em que a mensagem foi recebida.

A execução deste comando é dividida em duas étapas, o **envio do comando para o servidor**, e o **processamento da resposta obtida do servidor**. Para o programa identificar em qual das étapas está é utilizada uma verificação da variável `sent`, caso seja igual a 0 encontramo-nos na 1ª étapa, caso seja igual a 1 estámos na 2ª étapa.

**Envio do comando para o servidor**
É realizado o encode do comando inserido para o transformar num array de bytes, e é encriptado e enviado.
```python
          # envio do comando
                    if self.sent == 0:
                        self.sent = 1
                        i = i - 1

                        argumento = arg.encode()
                        argumento_enc = self.aes_gcm_enc(argumento)

                        return argumento_enc
````

**Processamento da resposta obtida do servidor**

A mensagem recebida é desencriptada e desserializada, e impressa no terminal. O formato que a string tem possui um "\n" entre cada mensagem na queue e, por isso, imprime cada uma delas numa linha diferente.

```python
           # processamento da resposta
                    else:
                        msg_decripted = self.aes_gcm_dec(msg)

                         messages_string = msg_decripted.decode()

                        print("\n")
                        print(messages_string)
                        print("\n")
                        
                        return None
```

## <u>  getmsg <NUM> </u>

Este comando permite ao cliente solicitar ao servidor o envio de uma mensagem específica da sua queue, identificada pelo número <NUM>. Em caso de sucesso, a mensagem será impressa no stdout. Uma vez enviada, essa mensagem será marcada como lida, portanto não será listada no próximo comando askqueue, embora ainda seja possível solicitá-la novamente ao servidor.

À semelhança do comando `askqueue`, a execução deste comando é dividida em duas étapas, o **envio do comando para o servidor**, e o **processamento da resposta obtida do servidor**. Para o programa identificar em qual das étapas está é utilizada uma verificação da variável `sent`, caso seja igual a 0 encontramo-nos na 1ª étapa, caso seja igual a 1 estámos na 2ª étapa.

**Envio do comando para o servidor**

Caso ainda não tenha sido enviado, o número da mensagem é recebido como argumento da linha de comando, e é então criado um par contendo o comando (getmsg) e o número da mensagem, o qual é depois encriptado e enviado ao servidor.

```python
# comando: getmsg <NUM>
if arg == "getmsg":
    if self.sent == 0:
        self.sent = 1
        num = sys.argv[i + 1]

        i = i + 1

        pair = mkpair(arg.encode(), num.encode())
        mensagem_enc = self.aes_gcm_enc(pair)

        return mensagem_enc
```

**Processamento da resposta obtida do servidor**
Na segunda etapa, após receber a resposta do servidor, a mensagem é desencriptada e desserializada. O número da mensagem, o timestamp, o conteúdo e a assinatura são então extraídos do par desserializado.

```python
msg_decripted = self.aes_gcm_dec(msg)

    pair_num_timestamp_message, pair_ass_cert = unpair(msg_decripted)
    pair_num_timestamp, formated_message_encoded = unpair(pair_num_timestamp_message)
    num, timestamp = unpair(pair_num_timestamp)
    num = num.decode()
    timestamp = timestamp.decode()
    
    formated_message = formated_message_encoded.decode()

    assinatura, certificado_serialized = unpair(pair_ass_cert)
    certificado = x509.load_pem_x509_certificate(certificado_serialized)

```

Posteriormente, a assinatura da mensagem é verificada utilizando a chave pública do certificado do cliente, garantindo assim que a mensagem não foi alterada. Após garantir isso, pega o UID que se encontra no certificado e compara com o UID do sender. Se estas verificações passarem, os dados da mensagem são impressos no stdout, incluindo o remetente, o timestamp, o assunto e o corpo da mensagem.

```python
if valida_cert(self.certificado_CA, certificado):
        public_key_RSA = certificado.public_key()

        public_key_RSA.verify(
            assinatura,
            formated_message_encoded,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        sender, assunto, corpo = formated_message.split(':')

        print("\nReceived from:", sender)
        print(timestamp)
        print("\nSubject:", assunto)
        print("\n" + corpo + "\n")

```

## <u>  help </u>

O comando help exibe as instruções de uso do programa, listando os comandos disponíveis e as suas respectivas descrições. Ao executar este comando, o utilizador receberá orientações sobre como interagir com o programa, incluindo detalhes sobre como especificar o ficheiro de dados do utilizador, enviar mensagens, solicitar a sua queue de mensagens não lidas e obter mensagens específicas da mesma.

```python
# comando:help
                if arg == "help":
                    

                    print("Usage: python3 msg_client.py [-user <FNAME>] <command>")
                    print("Commands:")
                    print("  -user <FNAME>                 Specify the user data file")
                    print("  send <UID> <SUBJECT>          Send a message to the user with the specified UID")
                    print("  askqueue                      Request the server to send the list of unread messages")
                    print("  getmsg <NUM>                  Request the server to send the message with the specified number from the queue")
                    print("  help                          Display usage instructions")
                    return None

```

## <u> Casos de erro gerais </u>

* O comando -user só pode aparecer em primeiro lugar nos comandos. Caso isso não se verifique é apresentada uma mensagem de erro;
  
* Caso nenhum comando seja fornecido, ou o comando fornecido não corresponder com nenhum dos esperados é apresentada uma mensagem de erro e fornecida a lista e formatação correta dos comandos.
  

## <u> msg_server.py </u>
O ficheiro `msg_server.py` contém as funcionalidades do servidor para nosso sistema de *Message Relay*.

#### <u>  Principais etapas do servidor </u>

##### <u> Funcionamento do protocolo </u>

Aquando da primeira execução do process do servidor, este já está a receber uma mensagem do cliente, que contém a public key do cliente.
Assim a primeira coisa que é efetuada é guardar a public key do cliente na variàvel `peer_public_key`. 
Após isto, ele gera a sua private key e através dela obtém a sua public key.

```python
            self.peer_public_key_serialized = msg
            self.peer_public_key = load_pem_public_key(msg, backend=default_backend())

            parameters_numbers = dh.DHParameterNumbers(p, g)
            parameters = parameters_numbers.parameters(default_backend())
            self.server_private_key = parameters.generate_private_key()
            self.server_public_key = self.server_private_key.public_key()
            self.server_public_key_serialized = self.server_public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

```

De seguida, obtemos a `private_key_RSA`, o `certificado_servidor` e o `certificado_CA` através da função `get_userdata` aplicada ao ficheiro `MSG_SERVER.p12` (note-se que neste caso o ficheiro é especificado em vez de ser obtido através do terminal, uma vez que o server é sempre o mesmo e não varia como os clientes). 

```python
self.private_key_RSA, self.certificado_servidor, self.certificado_CA = get_userdata("MSG_SERVER.p12")
```

Após a obtenção da chave privada RSA, do certificado do servidor e do certificado da autoridade certificadora (CA), o servidor inicia o processo de assinatura, como abordado na secção ***Obtenção das assinaturas*** anteriormente neste relatório. Esta etapa é crucial para garantir a autenticidade das chaves e dos certificados trocados entre o servidor e o cliente.

```python
            #assinatura servidor
            signature = self.private_key_RSA.sign(
                self.server_public_key_serialized + msg,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
```

Como se pode verificar acima, o servidor utiliza sua chave privada RSA para assinar a concatenação da chave pública do servidor e da chave pública do cliente. Esta assinatura é realizada utilizando o algoritmo de padding PSS com hash SHA256. O objetivo é garantir a integridade e autenticidade das chaves públicas trocadas durante o processo de negociação de chaves.

**Envio da chave pública e assinatura para o cliente**

Após a assinatura, o certificado do servidor é serializado,  e a chave pública do servidor juntamente com a assinatura são agrupadas e serializadas. Esse par é então enviado de volta ao cliente para verificação da autenticidade do servidor, que é efetuada como descrito nas secções ***Validação do certificado*** e ***Validação da assinatura*** anteriormente neste relatório.

***Processamento da segunda mensagem***

Após a assinatura e o envio do par contendo a chave pública do servidor e sua assinatura de volta para o cliente, o servidor aguarda a segunda mensagem do cliente.

Quando recebe a segunda mensagem, o servidor verifica a assinatura recebida junto com o certificado do cliente, da forma descrita nas secções  ***Validação da assinatura***  e ***Validação do certificado***. Esta verificação é feita para garantir que o certificado do cliente seja válido e confiável.

```python
if self.msg_cnt == 2:
    signature_peer, certificado_peer_serialized = unpair(msg)

    self.certificado_peer = x509.load_pem_x509_certificate(certificado_peer_serialized)

    if valida_cert(self.certificado_CA, self.certificado_peer):
        public_key_peer_RSA = self.certificado_peer.public_key()

        public_key_peer_RSA.verify(
            signature_peer,
            self.peer_public_key_serialized + self.server_public_key_serialized,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

```
Se estes parâmetros forem inválidos, a ligação é interrompida,casso contrário, são geradas a `shared_key` e a `derived_key` do servidor`.
```python
                self.shared_key = self.server_private_key.exchange(self.peer_public_key)

                self.derived_key = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b'handshake data',
                ).derive(self.shared_key)

            return b'123'
```
Após a conclusão destas etapas, o servidor está pronto para processar mensagens adicionais enviadas pelo cliente e responder de acordo.

## <u> Queues dos clientes </u>


***Decisão sobre o armazenamento das mensagens***

Durante o desenvolvimento do nosso `msg_server.py` , o grupo deparou-se com o problema sobre **como armazenar as mensagens** entre as sessões de execução. Consideramos duas abordagens: usar uma **variável global** ou escrever as mensagens num **ficheiro encriptado**.

 **Opção 1: Variável Global**
 Esta escolha oferece várias vantagens:

* Acesso Eficiente: O acesso direto às mensagens é mais eficiente, pois não há necessidade de operações de leitura e escrita no disco;

* Simplicidade: A lógica do código é simplificada, pois não temos de lidar com a complexidade de encriptação e desencriptação de ficheiros;

* Desempenho: Operações em memória são mais rápidas.

 **Opção 2: Arquivo Encriptado**
Embora a escrita num ficheiro encriptado possa oferecer mais segurança, apresenta desvantagens:

* Implementação mais complexa devido à necessidade de lidar com encriptação e gestão de chaves.

* Operações de leitura e escrita no disco são mais lentas que operações em memória.

Dado o tempo que o grupo tinha e o equilíbrio entre funcionalidade, desempenho e simplicidade, optamos por utilizar uma variável  global `client_queues` para armazenar as mensagens entre asc sessões de execução do servidor. Esta escolha permitui-nos obter uma solução eficaz e de baixa complexidade.
*****

No servidor, as mensagens destinadas a cada cliente são então armazenadas numa queue individual. Essa queue é representada pela variável  `client_queues`, um dicionário onde as keys são os IDs únicos dos clientes (UIDs) e os valores são listas de objetos Mensagem.
```python
    def get_client_queue(self, client_uid):
        global client_queues
        return client_queues.get(client_uid, [])
```

A classe Mensagem é responsável por representar uma mensagem individual, contendo informações como remetente, assunto, corpo, *timestamp*, assinatura e certificado do remetente.
O certificado e a assinatura serão utilizados para o client que recebe uma mensagem poder verificar se o sender que está na mensagem é verdadeiramente o sender que a enviou. A assinatura verifica se o conteudo da mensagem foi alterado e o certificado é usado para aceder ao UID e comparar com o do sender.

```python
class Mensagem:
    def __init__(self, sender, assunto, corpo, timestamp, assinatura, certificado):
        self.sender = sender
        self.assunto = assunto
        self.corpo = corpo
        self.timestamp = timestamp
        self.assinatura = assinatura
        self.certificado = certificado
    
    def imprimir(self):
        print("Enviada por:", self.sender)
        print("Assunto:", self.assunto)
        print("Corpo:", self.corpo)
        print("Timestamp:", self.timestamp)


```
Tendo então explicado este pormenor de guardar as mensagens, vamos de seguida explicar como se procede o processamento de cada comando recebido no servidor.


### <u> Processamento do comando askqueue </u>

## <u> askqueue </u>

O comando `askqueue` é utilizado pelo cliente para para pedir ao cliente a sua lista de mensagens não lidas.
Quando o servidor recebe a mensagem, começa por verificar se o tamanho da mesma é igual a 8, se for sabe que o comando que acabou de receber corresponde ao `askqueue`. Tratando-se desse casp ele vai verificar se certificado do cliente possui um atributo pseudónimo. 

```python
if len(mensagem_dec) == 8:
                if self.certificado_peer.subject:
                    for attr in self.certificado_peer.subject:
                        if attr.oid == x509.NameOID.PSEUDONYM:
                            uid = attr.value.strip()
```
Se o certificado do cliente contiver esse atributo, o servidor guarda-o na variavel `uid`e utiliza-o para obter a queue cuja key corresponde a esse `uid`, queue essa que é então a do cliente que executou o comando.
```python
                client_queue = self.get_client_queue(uid)
```
Em seguida, as mensagens presentes na queue são convertidas numa string com um formato específico. Essa string é então codificada em bytes e encripada usando o algoritmo AES-GCM. Finalmente, a queue encriptada é enviada de volta ao cliente como resposta ao seu pedido.

```python
    formatted_messages = [
    f"{index + 1}:{message.sender}:{message.timestamp}:{message.assunto}"
    for index, message in enumerate(client_queue)
]

queues_string = "\n".join(formatted_messages)

queues_serialized = queues_string.encode()

queue_encrypted = self.aes_gcm_enc(queues_serialized)

return queue_encrypted          

```

### <u> Processamento dos restantes comandos </u>

Quando o servidor recebe  comando por parte do cliente, cujo tamanho não é igual a 8,  ele começa por decodificar a mensagem recebida utilizando a função `unpair`. O primeiro elemento do par retornado pela função `unpair` contém o comando enviado pelo cliente, enquanto que o segundo elemento contém os dados adicionais relevantes para o comando.

Posto isto, o servidor converte o comando de uma representação de bytes para uma string utilizando o método `decode()` e esta string é armazenada na variável `comando`.
```python
                comando, bocado2 = unpair(mensagem_dec)
                comando = comando.decode()
```
Depois o servidor vai verificar qual o comando que recebeu para saber o qeu fazer.
## <u> send <UID> <SUBJECT></u>
Se o comando recebido for `send`, o servidor prossegue para processar os dados adicionais da mensagem, que incluem o UID do destinatário, a assinatura da mensagem, o assunto e o conteúdo da mensagem.

Os dados são decodificados e extraídos, e depois, o servidor regista o tempo atual em segundos  e converte-o em um formato de timestamp legível. O timestamp resultante representa a hora exata em que o processamento da mensagem ocorreu.

```python
                if comando == "send":
                    uid, pair_ass = unpair(bocado2)
                    uid = uid.decode()
                    assinatura, pair_subject_mensagem = unpair(pair_ass)
                    subject, mensagem = unpair(pair_subject_mensagem)
                    subject = subject.decode()
                    mensagem = mensagem.decode()

                    tempo_segundos = int(time.time())
                    timestamp = datetime.datetime.fromtimestamp(tempo_segundos).strftime('%H:%M')
```

Após decodificar e processar os dados adicionais da mensagem, o servidor verifica se o `UID` do destinatário já possui uma entrada na sua queue de mensagens. Se não houver uma entrada para o `UID`, o servidor cria uma nova fila vazia para esse destinatário.
```python
                    if uid not in client_queues:
                        client_queues[uid] = []
```

Depois, o servidor verifica se o certificado do cliente contém um atributo de pseudônimo. Se tiver, extrai o valor desse atributo e coloca-o na variável `sender_uid`, que representa o remetente da mensagem.

```python
                  if self.certificado_peer.subject:
                        for attr in self.certificado_peer.subject:
                            if attr.oid == x509.NameOID.PSEUDONYM:
                                sender_uid = attr.value.strip()
```

Tendo obtido todas as informações necessárias, o servidor cria então um novo objeto `Mensagem` contendo o remetente (sender_uid), o assunto (subject), o conteúdo da mensagem (mensagem), o timestamp (timestamp) e a assinatura (assinatura). Este objeto representa a mensagem que será adicionada à queue do destinatário.

```python
nova_mensagem = Mensagem(sender_uid, subject, mensagem, timestamp, assinatura, self.certificado_peer)
```
Por fim, a nova mensagem é adicionada à fila de mensagens do destinatário, representada pela chave uid em client_queues. 
 ```python
client_queues[uid].append(nova_mensagem)
```

## <u>  getmsg <NUM> </u>
No caso do comando recebido pelo servidor ser `getmsg`, ele começa por decodifiar o número da mensagem que o cliente quer receber (este número está contido na segunda parte da mensagem recebida).

```python
if comando == "getmsg":
   num = bocado2.decode()
```

De seguida, o servidor verifica se o certificado do cliente possui o atributo pseudónimo, se possuir, é extraido o seu valor e o mesmo é atribuido à variavel  `uid`, representando o uid do cliente em questão.

```python
if self.certificado_peer.subject:
    for attr in self.certificado_peer.subject:
        if attr.oid == x509.NameOID.PSEUDONYM:
            uid = attr.value.strip()
```
Depois de obter o uid do cliente, o server pega na queue cuja key corresponde ao uid, utilizando o método `get_client_queue(uid)`.
```python
 client_queue = self.get_client_queue(uid)
```
E posteriormente o servidor pega na mensagem da queue cujo número corresponde ao fornecido pelo cliente, da seguinte forma:
```pyhton
mensagem = client_queue[int(num)]
```
A mensagem é então formatada para ter a seguinte forma: `sender:assunto:corpo`, onde sender é o remetente da mensagem, assunto é o assunto da mensagem e corpo é o conteúdo da mensagem.

Posto isto, o servidor serializa o certificado associado à mensagem em formato PEM. Em seguida, procede à formação de pares de dados relevantes. Estes pares, que incluem o número e o timestamp da mensagem, juntamente com a mensagem formatada, são combinados utilizando a função mkpair, como se pode ver no código abaixo. Posteriormente, esses pares de dados são agrupados num único par, contendo todas as informações necessárias para o processamento pelo algoritmo AES-GCM. 

Após a formação do par contendo todas as informações relevantes da mensagem, servidor utiliza o algoritmo AES-GCM para encriptar esse par de dados, garantindo a confidencialidade e integridade das informações durante a transmissão da resposta para o cliente. Uma vez encriptada, a mensagem é finalmente enviada de volta ao cliente.

```python

                    formated_message = f"{mensagem.sender}:{mensagem.assunto}:{mensagem.corpo}"

                    cert_serialized = mensagem.certificado.public_bytes(encoding=serialization.Encoding.PEM)

                    pair_ass_cert = mkpair(mensagem.assinatura, cert_serialized)
                    pair_num_timestamp = mkpair(num.encode(), mensagem.timestamp.encode())
                    pair_num_timestamp_message = mkpair(pair_num_timestamp, formated_message.encode())
                    pair_geral = mkpair(pair_num_timestamp_message, pair_ass_cert)

                    mensagem_enc = self.aes_gcm_enc(pair_geral)

                    return mensagem_enc
```



## <u> Possiveis valorizações implementadas </u>
### Recibos que atesteam que uma mensagem foi submetida ao sistema

De forma a garantir que o cliente tem feedback acerca das suas ações, mensagens a informar do sucesso ou insucesso dos seus comandos. Nos comandos em que é esperado algo ser impresso no terminal do cliente isto não é necessário, no entanto, no comando send, nada é impresso no terminal e então tornasse útil ter este feedback.

Após enviar para o servidor o comando send e o seu conteudo, caso tudo tenha funcionado corretamente, ele recebe uma resposta do servidor, e é apenas caso receba essa resposta que ele irá realizar o print. 

```python
                  else:
                        uid = sys.argv[i+1]
                        print("\nMessage sent successfully to " + uid + "!\n")  

                        return None
```

### Sistema de Log 

No lado do servidor nenhuma informação era dada (no guiões anteriores). Como tal, implementamos um sistema de log para que possamos analisar a sua atividade, sendo util para ter um histórico dos comandos efetuados e para identificar possiveis erros.

Nas secções de código onde são tratados cada um dos comandos colocamos um print que tem o seguinte formato: `print(timestamp + "  " + uid + " -> comando")`. O `timestamp` é do momento em que o comando é recebido, o `uid` é o UID de quem enviou o comando e o `comando` é o comando recebido e os seus argumentos.

Exemplo:

```python
tempo_segundos = int(time.time())
                timestamp = datetime.datetime.fromtimestamp(tempo_segundos).strftime('%H:%M:%S')
                print(timestamp + "  " + uid + " -> askqueue")
```


## Conclusão

Neste relatório, apresentamos o projeto de Criptografia Aplicada, destacando as funcionalidades implementadas, a abordagem de implementação, e as possíveis valorizações adicionais implementadas. O projeto proporcionou uma experiência significativa no desenvolvimento de sistemas de comunicação segura, ampliando o nosso entendimento sobre criptografia e segurança.

Embora tenhamos enfrentado desafios e não tenhamos conseguido implementar todas as sugestões de possiveis valorizações dadas pelos professores, conseguimos desenvolver com sucesso todas as funcionalidades base do projeto. Das valorizações dadas pelos professores, realizamos a emissão de recibos para confirmar a submissão de mensagens no sistema e um sistema de log para registar os comandos recebidos pelo servidor.

Reconhecemos que as valorizações sugeridas teriam tornado o projeto mais robusto e seguro. No entanto, dedicamos um tempo considerável para garantir a implementação adequada das funcionalidades principais, priorizando a qualidade e a eficiência do sistema.



