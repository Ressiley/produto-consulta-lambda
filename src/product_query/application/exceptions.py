class ApplicationError(Exception):
    """Exceção base para erros conhecidos da aplicação."""


class ProdutoExternoError(ApplicationError):
    """Falha individual ao consultar um produto na API externa."""


class ProdutoExternoTimeoutError(ProdutoExternoError):
    """Tempo limite excedido na consulta externa de um produto."""


class AuthenticationError(ApplicationError):
    """Falha na autenticação com a API externa."""


class CredentialsError(ApplicationError):
    """Falha ao obter as credenciais necessárias."""
