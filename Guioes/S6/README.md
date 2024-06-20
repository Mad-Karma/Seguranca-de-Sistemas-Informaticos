# Respostas das Questões



# Relatório do Guião da Semana 6

## Comunicação segura entre Cliente/Servidor

### Descrição Geral

Nesta semana, foi nos proposto modidifcar dois programas, sendo eles o `Client.py` e o `Server.py` (fornecidos pelos docentes), de modo, a garantir uma comunicação segura entre os clientes e o servidor. E para tal, elaboramos os seguintes programas visando esse objetivo:

### PROG: `Client_sec.py` & `Server_sec.py`

Os programas `Client_sec.py` e `Server_sec.py` utilizam a cifra autenticada AES-GCM, a mesma do ultimo guião, para encriptar (`aes_gcm_enc`) e desencriptar (`aes_gcm_dec`) as mensagens trocadas entre o cliente e o servidor. Para tal, a cifra AES-GCM utiliza umam chave estática (key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"), sendo a mesma para o cliente e para o servidor.

Para executar o programa, temos de abrir dois terminais diferentes, um para o servidor e outro para o cliente.

No primeiro terminal vamos executar o `Server_sec.py`, da seguinte forma:
```bash
python3 Server_sec.py
```

Tendo o servidor aberto, podemos passar para o `Client_sec.py`, e podemos corre-lo da seguinte forma:
```bash
python3 Client_sec.py
```

Desta forma, o cliente e o servidor já estão prontos para comunicar.

### PROG: `Client_dh.py` & `Server_dh.py`

Nos programas `Client_dh.py` e `Server_dh.py`, tal como, nos programas `Client_sec.py` e `Server_sec.py`, utilizamos a cifra AES-GCM para encriptar e desencriptar mensagens, mas agora a chave utilizada resulta da execução do protocolo de acordo de chaves Diffie-Hellman, para tal, o cliente e o servidor trocam as suas chaves públicas e cada um calcula a mesma chave compartilhada utilizando a sua chave privada e a chave pública recebida da outra parte. Desta forma conseguimos uma comunicação mais segura entre o cliente e o servidor.

Para executar o programa, temos de abrir dois terminais diferentes, um para o servidor e outro para o cliente.

No primeiro terminal vamos executar o `Server_dh.py`, da seguinte forma:
```bash
python3 Server_dh.py
```

Tendo o servidor aberto, podemos passar para o `Client_dh.py`, e podemos corre-lo da seguinte forma:
```bash
python3 Client_dh.py
```

Desta forma, o cliente e o servidor já estão prontos para comunicar.

