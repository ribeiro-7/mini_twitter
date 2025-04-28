CASO 1: Registro de Usuário
    -> Os usuários devem poder se inscrever por meio da API fornecendo um e-mail, nome de usuário e senha.
    -> Use o JWT para lidar com a autenticação para login e gerenciamento de sessão.

CASO 2: Criação de Postagens
    -> Usuários autenticados podem criar uma postagem com texto e uma imagem como conteúdo
    -> As postagens podem ser curtidas por outros usuários.

CASO 3: Seguir/Deixar de seguir usuário
    -> Os usuários devem poder seguir ou deixar de seguir outros.
    -> O feed deve mostrar apenas postagens de usuários que o usuário autenticado segue.

CASO 4: Visualização de Feed
    -> O usuário pode visualizar uma lista paginada de postagens dos usuários que ele segue.
    -> As postagens devem ser ordenadas por data de criação, da mais recente para a mais antiga.

------------------------------------------------------------------------------------------------------------------

Tweets: 
    -> Creating
        -> Text
        -> Image
    -> Update (Edit)
    -> Delete
    -> Like

Users:
    -> Register
    -> Login
    -> Logout
    -> Profile
        -> Follow button
    -> Feed
        -> User + who they follow"


Followers 
