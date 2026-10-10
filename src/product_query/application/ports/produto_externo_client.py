from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ProdutoExternoClient(Protocol):
    def consultar_produto(
        self,
        cod_prod_rds: str,
    ) -> dict[str, Any]:
        """Consulta os dados de um produto na API  externa"""
        ...
