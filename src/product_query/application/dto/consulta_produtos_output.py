from dataclasses import dataclass
from typing import Any

from product_query.application.dto.status_consulta_produto import (
    StatusConsultaProduto,
)


@dataclass(frozen=True, slots=True)
class ProdutoConsultaOutput:
    codigo_produto: str
    tipo_produto: str
    cod_prod_rds: str | None
    dados_externos: dict[str, Any] | None
    status: StatusConsultaProduto


@dataclass(frozen=True, slots=True)
class ConsultaProdutosOutput:
    resultados: tuple[ProdutoConsultaOutput, ...]
