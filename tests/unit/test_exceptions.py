import pytest

from product_query.application.exceptions import (
    ApplicationError,
    AuthenticationError,
    CredentialsError,
    ProdutoExternoError,
    ProdutoExternoTimeoutError,
)


def test_produto_externo_error_herda_de_application_error():
    erro = ProdutoExternoError("Falha na consul externa")

    assert isinstance(erro, ApplicationError)
    assert isinstance(erro, ProdutoExternoError)


def test_timeout_herda_de_produto_externo_error():
    erro = ProdutoExternoTimeoutError("Timeout na API externa")

    assert isinstance(erro, ProdutoExternoError)
    assert isinstance(erro, ApplicationError)


@pytest.mark.parametrize(
    "classe_erro",
    [
        AuthenticationError,
        CredentialsError,
    ],
)
def test_falhas_gerais_nao_sao_erros_individuais(classe_erro):
    erro = classe_erro("Falha geral")

    assert isinstance(erro, ApplicationError)
    assert not isinstance(erro, ProdutoExternoError)
