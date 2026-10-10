from typing import Any

from product_query.application.ports.produto_externo_client import (
    ProdutoExternoClient,
)
from product_query.application.ports.produto_repository import (
    ProdutoRepository,
)


class ConsultarProdutosUseCase:
    def __init__(
        self,
        produto_repository: ProdutoRepository,
        produto_externo_client: ProdutoExternoClient,
    ) -> None:
        self._produto_repository = produto_repository
        self._produto_externo_client = produto_externo_client

    def executar(
        self,
        codigo_produto: str,
        tipo_produto: str,
    ) -> dict[str, Any] | None:
        cod_prod_rds = self._produto_repository.buscar_codigo_rds(
            codigo_produto=codigo_produto,
            tipo_produto=tipo_produto,
        )

        if cod_prod_rds is None:
            return None

        dados_externos = self._produto_externo_client.consultar_produto(
            cod_prod_rds=cod_prod_rds,
        )

        return {
            "codigo_produto": codigo_produto,
            "tipo_produto": tipo_produto,
            "cod_prod_rds": cod_prod_rds,
            "dados_externos": dados_externos,
        }
