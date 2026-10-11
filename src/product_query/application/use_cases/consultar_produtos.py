from typing import Any

from product_query.application.dto.consulta_produtos_input import (
    ConsultaProdutosInput,
)
from product_query.application.dto.consulta_produtos_output import (
    ConsultaProdutosOutput,
    ProdutoConsultaOutput,
)
from product_query.application.dto.status_consulta_produto import (
    StatusConsultaProduto,
)
from product_query.application.exceptions import ProdutoExternoError
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

    def _buscar_codigo_rds(
        self,
        codigo_produto: str,
        tipo_produto: str,
    ) -> str | None:
        return self._produto_repository.buscar_codigo_rds(
            codigo_produto=codigo_produto,
            tipo_produto=tipo_produto,
        )

    def _consultar_produto_externo(
        self,
        cod_prod_rds: str,
    ) -> dict[str, Any]:
        return self._produto_externo_client.consultar_produto(cod_prod_rds)

    def executar(
        self,
        codigo_produto: str,
        tipo_produto: str,
    ) -> dict[str, Any] | None:
        cod_prod_rds = self._buscar_codigo_rds(
            codigo_produto=codigo_produto,
            tipo_produto=tipo_produto,
        )

        if cod_prod_rds is None:
            return None

        dados_externos = self._consultar_produto_externo(cod_prod_rds)

        return {
            "codigo_produto": codigo_produto,
            "tipo_produto": tipo_produto,
            "cod_prod_rds": cod_prod_rds,
            "dados_externos": dados_externos,
        }

    def executar_multiplos(
        self,
        entrada: ConsultaProdutosInput,
    ) -> ConsultaProdutosOutput:
        resultados = []

        for produto in entrada.produtos:
            cod_prod_rds = self._buscar_codigo_rds(
                codigo_produto=produto.codigo_produto,
                tipo_produto=entrada.tipo_produto,
            )

            if cod_prod_rds is None:
                resultado = ProdutoConsultaOutput(
                    codigo_produto=produto.codigo_produto,
                    tipo_produto=entrada.tipo_produto,
                    cod_prod_rds=None,
                    dados_externos=None,
                    status=StatusConsultaProduto.NAO_ENCONTRADO,
                )
            else:
                try:
                    dados_externos = self._consultar_produto_externo(cod_prod_rds)

                    resultado = ProdutoConsultaOutput(
                        codigo_produto=produto.codigo_produto,
                        tipo_produto=entrada.tipo_produto,
                        cod_prod_rds=cod_prod_rds,
                        dados_externos=dados_externos,
                        status=StatusConsultaProduto.SUCESSO,
                    )

                except ProdutoExternoError:
                    resultado = ProdutoConsultaOutput(
                        codigo_produto=produto.codigo_produto,
                        tipo_produto=entrada.tipo_produto,
                        cod_prod_rds=cod_prod_rds,
                        dados_externos=None,
                        status=StatusConsultaProduto.ERRO,
                    )

            resultados.append(resultado)

        return ConsultaProdutosOutput(resultados=tuple(resultados))
