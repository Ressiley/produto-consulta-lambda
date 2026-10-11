from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProdutoConsultaInput:
    codigo_produto: str

    def __post_init__(self) -> None:
        if not isinstance(self.codigo_produto, str):
            raise TypeError("codigo_produto deve ser uma string.")

        if not self.codigo_produto.strip():
            raise ValueError("codigo_produto não pode ser vazio.")


@dataclass(frozen=True, slots=True)
class ConsultaProdutosInput:
    tipo_produto: str
    produtos: tuple[ProdutoConsultaInput, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.tipo_produto, str):
            raise TypeError("tipo_produto deve ser uma string.")

        if not self.tipo_produto.strip():
            raise ValueError("tipo_produto não pode ser vazio.")

        if not isinstance(self.produtos, tuple):
            raise TypeError("produtos deve ser uma tupla.")

        if not self.produtos:
            raise ValueError("A consulta deve conter pelo menos um produto.")

        if not all(isinstance(produto, ProdutoConsultaInput) for produto in self.produtos):
            raise TypeError("Todos os itens devem ser do tipo ProdutoConsultaInput.")
