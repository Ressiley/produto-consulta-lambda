import pytest

from product_query.application.dto.consulta_produtos_input import (
    ConsultaProdutosInput,
    ProdutoConsultaInput,
)


def test_deve_criar_produto_consulta_input_valido():
    produto = ProdutoConsultaInput(codigo_produto="1001")

    assert produto.codigo_produto == "1001"


@pytest.mark.parametrize(
    "codigo_produto",
    ["", " ", "   "],
)
def test_deve_rejeitar_codigo_produto_vazio(codigo_produto):
    with pytest.raises(ValueError, match="codigo_produto não pode ser vazio"):
        ProdutoConsultaInput(codigo_produto=codigo_produto)


@pytest.mark.parametrize(
    "codigo_produto",
    [None, 123, True],
)
def test_deve_rejeitar_codigo_produto_com_tipo_invalido(codigo_produto):
    with pytest.raises(TypeError, match="codigo_produto deve ser uma string"):
        ProdutoConsultaInput(codigo_produto=codigo_produto)


def test_deve_criar_consulta_com_multiplos_produtos():
    produtos = (
        ProdutoConsultaInput(codigo_produto="1001"),
        ProdutoConsultaInput(codigo_produto="1002"),
    )

    consulta = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=produtos,
    )

    assert consulta.tipo_produto == "FUNDIDO"
    assert len(consulta.produtos) == 2
    assert consulta.produtos[0].codigo_produto == "1001"
    assert consulta.produtos[1].codigo_produto == "1002"


@pytest.mark.parametrize(
    "tipo_produto",
    ["", " ", "   "],
)
def test_deve_rejeitar_tipo_produto_vazio(tipo_produto):
    with pytest.raises(ValueError, match="tipo_produto não pode ser vazio"):
        ConsultaProdutosInput(
            tipo_produto=tipo_produto,
            produtos=(ProdutoConsultaInput(codigo_produto="1001"),),
        )


@pytest.mark.parametrize(
    "tipo_produto",
    [None, 123, True],
)
def test_deve_rejeitar_tipo_produto_com_tipo_invalido(tipo_produto):
    with pytest.raises(TypeError, match="tipo_produto deve ser uma string"):
        ConsultaProdutosInput(
            tipo_produto=tipo_produto,
            produtos=(ProdutoConsultaInput(codigo_produto="1001"),),
        )


def test_deve_rejeitar_consulta_sem_produtos():
    with pytest.raises(ValueError, match="pelo menos um produto"):
        ConsultaProdutosInput(
            tipo_produto="FUNDIDO",
            produtos=(),
        )


def test_deve_rejeitar_produtos_que_nao_sejam_tupla():
    with pytest.raises(TypeError, match="produtos deve ser uma tupla"):
        ConsultaProdutosInput(
            tipo_produto="FUNDIDO",
            produtos=[],
        )


def test_deve_rejeitar_item_com_tipo_invalido():
    with pytest.raises(TypeError, match="ProdutoConsultaInput"):
        ConsultaProdutosInput(
            tipo_produto="FUNDIDO",
            produtos=("1001",),
        )
