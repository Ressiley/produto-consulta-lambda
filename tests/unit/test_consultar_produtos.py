from unittest.mock import create_autospec

from product_query.application.ports.produto_externo_client import ProdutoExternoClient
from product_query.application.ports.produto_repository import ProdutoRepository
from product_query.application.use_cases.consultar_produtos import (
    ConsultarProdutosUseCase,
)


def test_deve_consultar_produto_com_sucesso():
    repository = create_autospec(ProdutoRepository, instance=True)
    external_client = create_autospec(ProdutoExternoClient, instance=True)

    repository.buscar_codigo_rds.return_value = "RDS9001"
    external_client.consultar_produto.return_value = {
        "descricao": "Produto exemplo",
        "situacao": "ATIVO",
    }

    use_case = ConsultarProdutosUseCase(
        produto_repository=repository, produto_externo_client=external_client
    )

    resultado = use_case.executar(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
    )

    assert resultado == {
        "codigo_produto": "1001",
        "tipo_produto": "FUNDIDO",
        "cod_prod_rds": "RDS9001",
        "dados_externos": {
            "descricao": "Produto exemplo",
            "situacao": "ATIVO",
        },
    }

    repository.buscar_codigo_rds.assert_called_once_with(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
    )

    external_client.consultar_produto.assert_called_once_with(
        cod_prod_rds="RDS9001",
    )


def test_nao_deve_consultar_api_quando_produto_nao_existe():
    repository = create_autospec(ProdutoRepository, instance=True)
    external_client = create_autospec(ProdutoExternoClient, instance=True)

    repository.buscar_codigo_rds.return_value = None

    use_case = ConsultarProdutosUseCase(
        produto_repository=repository,
        produto_externo_client=external_client,
    )

    resultado = use_case.executar(codigo_produto="9999", tipo_produto="FUNDIDO")

    assert resultado is None

    repository.buscar_codigo_rds.assert_called_once_with(
        codigo_produto="9999", tipo_produto="FUNDIDO"
    )

    external_client.consultar_produto.assert_not_called()
