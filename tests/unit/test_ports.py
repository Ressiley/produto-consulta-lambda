from product_query.application.ports.produto_repository import (ProdutoRepository,)
from product_query.application.ports.produto_externo_repository import (ProdutoExternoClient,)


class FakeProdutoRepository:
    def buscar_codigo_rds(
            self,
            codigo_produto: str,
            tipo_produto: str,
    ) -> str | None:
        return "RDS9001"

class FakeProdutoExternoClient:
    def consultar_produto(
            self,
            codigo_produto_rds: str,
    ) -> dict:
        return {"descricao": "Produto exemplo"}


def test_repositorio_impmente_contrato():
    repositorio = FakeProdutoRepository()

    assert isinstance(repositorio, ProdutoRepository)


def test_cliente_externo_implementa_contrato():
    cliente = FakeProdutoExternoClient()

    assert isinstance(cliente, ProdutoExternoClient)