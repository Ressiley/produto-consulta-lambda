from dataclasses import dataclass


@dataclass(frozen=True)
class Produto:
    codigo_produto: str
    tipo_produto: str
    cod_prod_rds: str | None = None

    def __post_init__(self) -> None:
        if not self.codigo_produto.strip():
            raise ValueError("O código do produto é obrigatório.")

        if not self.tipo_produto.strip():
            raise ValueError("O tipo do produto é obrigatório")

        if self.cod_prod_rds is not None and not self.cod_prod_rds.strip():
            raise ValueError("O código RDS não pode ser vazio.")
