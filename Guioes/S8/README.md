# Respostas das Questões

### Perguntas e Respostas

*Q1: Criar ficheiros, exercitar permissões e controlo de acesso
Criar diretorias (contendo ficheiros), exercitar permissões e controlo de acesso
Tenha em conta a semântica particular das permissões em diretorias
Tenha em conta o controlo de acesso em cada componente do caminho para um ficheiro ou diretoria*

   *R:* Para criar ficheiros, exercitar permissões e controlo de acesso, foram utilizados os seguintes comandos:
  
  1. **Criar ficheiros:**
     - O comando `touch` foi empregado para criar ficheiros.
  
  2. **Ver permissões:**
     - Para visualizar as permissões de ficheiros e diretorias, utilizou-se o comando `ls -l`.
  
  3. **Alterar permissões:**
     - O comando `chmod` foi utilizado para alterar as permissões de ficheiros e diretorias.
  
  Além disso, ao criar diretorias (contendo ficheiros) e exercitar permissões e controlo de acesso, foi utilizado o seguinte comando:
  
  - **Criar diretorias:**
    - O comando `mkdir` foi empregado para criar diretorias.
   


*Q2:Criar utilizador para cada membro da equipa
Criar grupos contendo dois elementos da equipa e um contendo todos os elementos da equipa
Iniciar sessão com os diferentes utilizadores e revistar os exercício anteriores*


*R:* 
1. **Criação de utilizadores:**
   - Utilizando o comando `adduser <nome_user>`, foram criados os users para cada membro do grupo (joao, sandra e diogo).

    ```bash
    adduser sandra
    adduser diogo
    adduser joao
    ```
     

2. **Criação de Grupos:**
   - Utilizando o comando `sudo groupadd <nome_grupo>`, foram criados os grupos necessários. Foram criados os grupos "grupo2", que contém dois dos users criados, e o "grupo3" que contém os três users criados.
  
    ```bash
    sudo addgroup grupo2
    sudo addgroup grupo3
    ```
    

3. **Associação de Utilizadores aos Grupos:**
   - Com o comando `sudo usermod -aG`, os users foram adicionados aos diferentes grupos criados.
   
   - Os users "diogo" e "sandra" foram adicionados ao grupo "grupo2" da seguinte forma:
   ```bash
    sudo usermod -aG grupo2 diogo
    sudo usermod -aG grupo2 sandra
    ```
   - Os users  "sandra", "diogo" e "joao" foram adicionados ao grupo "grupo3" de forma semelhante:
    ```bash
    sudo usermod -aG grupo3 diogo
    sudo usermod -aG grupo3 sandra
    sudo usermod -aG grupo3 joao
    ```

Estas operações garantem que os utilizadores tenham acesso aos recursos partilhados pelos grupos aos quais pertencem.


*Q3:Criar um programa binário executável que imprima o conteúdo de um ficheiro de texto cujo nome é passado como único argumento da sua linha de comando (ou erro caso não o consiga fazer)
Definir permissão de setuid para o ficheiro executável*

*R:* Foi criado o programa `q3.py` que cria então o nosso executável que imprime o conteúdo de um ficheiro de texto cujo nome é passado como único argumento.
Posto isto foi usado o comando `sudo chomd +s q3.py` para definir a permissão setuid para o executável criado.

*Q4: Definir permissões específicas para os utilizadores e grupos criados (via ACL estendida)
Experimentar os mecanismos de controlo de acesso à luz das novas permissões definidas*

*R:* 
- Para definir permissões para um utilizador específico. Foi utilizado o seguinte comando:

`setfacl -m u:nome_utilizador:permissoes caminho_para_ficheiro`

Da seguinte forma:

`setfacl -m u:joao:rw ola.txt`

Este comando faz com que o user joao tenha permissões de leitura e escrita no ficheiro `ola.txt`.
Assim, o user joao terá permissão para ler e escrever no ficheiro ola.txt, enquanto que os outros users podem ter permissões diferente.
- Para definir permissões para um grupo específico foi usado o comando:
  
`setfacl -m g:nome_grupo:permissoes caminho_para_ficheiro`

Da seguite forma:

`setfacl -m g:grupo2:rw ola.txt`

`setfacl -m g:grupo3:rw ola.txt `

Estes comandos permitem dar permissões de leitura e escrita (rw) para os membros dos grupos grupo2 e grupo3 no ficheiro ola.txt.

Dessa forma, os utilizadores que pertencem a esses grupos poderão ler e escrever no ficheiro, enquanto outros utilizadores podem ter permissões diferentes.




  

