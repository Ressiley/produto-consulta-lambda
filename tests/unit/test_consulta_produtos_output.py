import pytest

from product_query.application.dto.consulta_produtos_output import (
    ConsultaProdutosOutput,
    ProdutoConsultaOutput,
)
from product_query.application.dto.status_consulta_produto import (
    StatusConsultaProduto,
)


def test_criar_produto_consulta_output_com_sucesso():
    produto = ProdutoConsultaOutput(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
        cod_prod_rds="ABC123",
        dados_externos={
            "descricao": "Produto exemplo",
        },
        status=StatusConsultaProduto.SUCESSO,
    )

    assert produto.codigo_produto == "1001"
    assert produto.tipo_produto == "FUNDIDO"
    assert produto.cod_prod_rds == "ABC123"
    assert produto.dados_externos == {
        "descricao": "Produto exemplo",
    }
    assert produto.status == StatusConsultaProduto.SUCESSO


def test_criar_produto_output_nao_encontrado():
    produto = ProdutoConsultaOutput(
        codigo_produto="1002",
        tipo_produto="FUNDIDO",
        cod_prod_rds=None,
        dados_externos=None,
        status=StatusConsultaProduto.NAO_ENCONTRADO,
    )

    assert produto.cod_prod_rds is None
    assert produto.dados_externos is None
    assert produto.status == StatusConsultaProduto.NAO_ENCONTRADO


def test_criar_consulta_produtos_output_com_multiplos_produtos():
    produto_1 = ProdutoConsultaOutput(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
        cod_prod_rds="ABC123",
        dados_externos={"descricao": "Produto exemplo"},
        status=StatusConsultaProduto.SUCESSO,
    )

    produto_2 = ProdutoConsultaOutput(
        codigo_produto="1002",
        tipo_produto="FUNDIDO",
        cod_prod_rds=None,
        dados_externos=None,
        status=StatusConsultaProduto.NAO_ENCONTRADO,
    )

    resultado = ConsultaProdutosOutput(resultados=(produto_1, produto_2))

    assert len(resultado.resultados) == 2
    assert resultado.resultados[0] == produto_1
    assert resultado.resultados[1] == produto_2
    assert resultado.resultados[0].status == StatusConsultaProduto.SUCESSO
    assert resultado.resultados[1].status == StatusConsultaProduto.NAO_ENCONTRADO


def test_consulta_produtos_output_e_imutavel():
    resultado = ConsultaProdutosOutput(resultados=())

    with pytest.raises(AttributeError):
        # noinspection PyDataclass
        resultado.resultados = ()
