from typing import Protocol, runtime_checkable

@runtime_checkable
class ProdutoRepository(Protocol):
    def buscar_codigo_rds(
            self,
            codigo_rds: str,
            tipo_produto: str
    ) -> str | None:
       """Busca o código RDS correspondente ao produto."""
       ...