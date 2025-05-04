# Mini Twitter - Django Rest Framework

## 📚 Sobre o Projeto
Este projeto foi desenvolvido para a seleção de desenvolvedores backend Python da empresa b2bit. O projeto "Mini-twitter", é uma API RESTful desenvolvida com Django e Django Rest Framework que simula funcionalidades básicas de uma rede social estilo Twitter. O sistema permite que usuários se cadastrem, publiquem tweets com ou sem imagem, vejam um feed global com todos os tweets e um feed 'for you' com tweets apenas de pessoas que ele segue. Além disso, o usuário é capaz de interagir com perfis de outros usuários, além de outras funcionalidades muito interessantes. Toda a aplicação é conteinerizada com Docker, utilizando PostgreSQL como banco de dados.

## 🚀 Funcionalidades

**Users**:
  - Cadastro e login de usuários com JWT.
  - Logout com revogação do token refresh.
  - O usuário consegue ver seu perfil contendo seus dados: id, email, username e sua contagem de seguidores.
  - O usuário também consegue deletar sua própria conta.
  
**Tweets**:
  - O usuário tem acesso a um feed 'for you' contendo os tweets apenas daqueles usuários que ele segue. Os tweets são ordenados pela data de criação mais recente.
  - O usuário tem acesso a um feed 'global' contendo todos os tweets de todos os usuários por ordem de criação mais recente.
  - É possível criar tweet com conteúdo em texto e uma imagem, sendo obrigatório no mínimo um dos dois campos.
  - É possível editar o tweet alterando tanto texto, como imagem.
  - Também é posível deletar um tweet.
  - O usuário pode também curtir a publicação de outro e, se já tiver curtido, pode descurtir.
  - Há uma contagem de curtidas no tweet.
  - Por último há uma funcionalidade de pesquisa de tweets por palavra-chave ou hashtag, retornando os tweets que possuem a palavra pesquisada.

**Profile**:
  - Cada usuário quando cria sua conta tem automaticamente seu perfil criado e é capaz de seguir o perfil de outros usuários e, se já estiver seguindo, pode deixar de seguir.

## 📂 Models

**User (modelo padrão do Django Contrib)**
  - Campos padrões: id, email, username, password
  - Utilizado para autenticação com JWT
  - Se relaciona com tweets e profile

**Profile**
  - user: Chave estrangeira relacionada a user
  - created_when: Data de criação do Perfil
  - followers: Relação de muitos pra muitos com user
  - Relacionado automaticamente ao criar um novo usuário

**Tweets**
  - user: Usuário autor do tweet (Chave Estrangeira de user)
  - content: Texto do tweet (pode ser vazio se houver imagem)
  - image: Upload de imagem (opcional)
  - created_at: Timestamp de criação
  - Likes: Relação de muitos pra muitos com user
  - Tweets são exibidos em ordem decrescente por data no feed for you e global

## 📄 Documentação
  - A documentação foi feita pelo **Postman** com todos os endpoints e como as requisições são feitas. Pode ser vista no link:
  https://documenter.getpostman.com/view/40491697/2sB2j4fArv

## ⚙️ Instalação
  - `git clone https://github.com/ribeiro-7/mini-twitter.git`
  - `cd mini-twitter`
  - Dentro do projeto há um arquivo chamada '.env.example' lá tem instruções para criar e configurar o arquivo .env para colocar suas informações de configuração.
  - Lembrando que é necessário ter o PostgreSQL instalado em sua máquina e adicionar suas informações corretamente, leia atentamente as instruções no arquivo .env.example e siga passo a passo.

## 🐳 Docker

  **Build e up do conteiner**:
  - `docker-compose up --build`
    
  **Criando as tabelas no banco de dados**:
  - `docker-compose exec web python manage.py migrate`
    
  **Se quiser criar um superuser**:
  - `docker-compose exec web python manage.py createsuperuser`

## ✅ Testes

  **Testes de views**:
  - `docker-compose exec web python manage.py test tweets.tests.tests_tweets_views`
  - `docker-compose exec web python manage.py test tweets.tests.tests_user_views`
  - `docker-compose exec web python manage.py test profiles.tests.tests_profile_view`
    
  **Testes de models**:
  - `docker-compose exec web python manage.py test tweets.tests.tests_tweet_model`
  - `docker-compose exec web python manage.py test tweets.tests.tests_user_model`
  - `docker-compose exec web python manage.py test profiles.tests.tests_profile_model`

## 🛡️ Segurança
  - Senhas são criptografadas com o sistema padrão do Django.
  - Autenticação feita com JWT.
  - Tokens refresh podem ser revogados com logout.
  - Todas os endpoints protegidos, é necessário passar o token de acesso Bearer Token para fazer as requisições.

## 🔟 Requisições
  - Na documentação fornecida acima mostra o formato json utilizado no postman para que as requisições possam ser feitas corretamente.
  - Lembre de passar o token de acesso no campo de authorization com o tipo Bearer Token para ter autorização nas requisições.

