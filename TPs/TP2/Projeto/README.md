IMPORTANTE:
 - A pasta Projeto (pasta principal do trabalho que com a src e restantes pastas) tem de ser colocada na pasta "home" do sistema

 - Pasta "home" do sistema não é a pasta home do user, a pasta deve estar no mesmo local que as pastas dos users


Iniciar o programa:
 
 - O programa opera partindo do principio que todos os utilizadores envolvidos têm permissões suficientes para o correto funcionamento do programa. Para que isso aconteça é necessário garantir que todos os users têm totais permissões para todos, ou seja 777

 - Fazer make dentro da pasta do projeto para gerar os executáveis. Estes são gerados dentro da pasta "obj".

 - Criar o daemon que irá executar o servidor.

 - Conteudo do ficheiro .daemon:

[Unit]
Description=Executa meu programa

[Service]
Type=simple
ExecStart=/home/Projeto/src/servidor
User=root
WorkingDirectory=/home/Projeto/daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target


Executar comandos:

 - Para executar um comando o utilizador deve aceder à pasta obj do projeto e executar os programas que existem na pasta.
 
 - Cada comando corresponde a um programa (ex: para enviar uma mensagem fazer ./enviar user mensagem)



Comandos suportados:

 - Comandos de gestão de acesso ao programa:

    - ./ativar : este comando adiciona o utilizar ao sistema de mensagens, colocando-o no grupo concordia, necessário para utilizar o programa

    - ./desativar : este comando remove o utilizar ao sistema de mensagens, removendo-o do grupo concordia

 - Comandos para grupos:

    - ./criar-grupo nome_grupo : cria um grupo para troca de mensagens (e adiciona o utilizador que executou o comando ao grupo automáticamente)

    - ./remover-grupo nome_grupo : remove um grupo para troca de mensagens

    - ./grupo-adicionar nome_user nome_grupo : adiciona um user a um grupo

    - ./grupo-remover nome_user nome_grupo : remove um user de um grupo

    - ./grupo-listar nome_grupo : lista os membros de um grupo

 - Comandos relativos a mensagens:

    - ./enviar destinatario mensagem : envia uma mensagem para o destinatário

    - ./ler id_mensagem : apresenta o conteudo da mensagem com o id fornecido

    - ./listar "-a" : apresenta as mensagens não lidas. Caso tenha a opção "-a" lista todas as mensagens existentes 

    - ./responder id_mensagem mensagem : envia uma mensagem para o user que enviou a mensagem com o id indicado