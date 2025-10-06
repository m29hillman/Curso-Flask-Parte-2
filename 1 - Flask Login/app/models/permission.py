# Define uma classe para gerenciar as permissões dos usuários.
# Esta abordagem utiliza valores que são potências de 2 (1, 2, 4, 8, 16...).
# Isso permite que as permissões de um usuário sejam combinadas em um único número inteiro
# usando operações bitwise (OU para adicionar, E para verificar).
class Permission:
    # Permissão para seguir outros usuários.
    FOLLOW = 1
    # Permissão para escrever comentários.
    COMMENT = 2
    # Permissão para escrever artigos ou posts.
    WRITE = 4
    # Permissão para moderar comentários de outros usuários.
    MODERATE = 8
    # Permissão total de administrador.
    ADMIN = 16
