from dataclasses import FrozenInstanceError

import pytest

from product_query.domain.produto import Produto

def test_deve_criar_produto_valido():
    produto = Produto(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
    )

    assert produto.codigo_produto == "1001"
    assert produto.tipo_produto == "FUNDIDO"
    assert produto.cod_prod_rds is None


def test_deve_criar_produto_com_codigo_rds():
    produto = Produto(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
        cod_prod_rds="RDS9001",
    )

    assert produto.cod_prod_rds == "RDS9001"


def test_deve_rejeitar_codigo_produto_vazio():
    with pytest.raises(
        ValueError,
        match="O tipo do produto é obrigatório"
    ):
        Produto(
            codigo_produto="1001",
            tipo_produto="",
        )


def test_deve_rejeitar_cod_rds_vazio():
    with pytest.raises(
        ValueError,
        match="O código RDS não pode ser vazio",
    ):
        Produto(
            codigo_produto="1001",
            tipo_produto="FUNDIDO",
            cod_prod_rds="",
        )


def test_produto_deve_ser_imutavel():
    produto = Produto(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
    )

    with pytest.raises(FrozenInstanceError):
        setattr(produto, "codigo_produto" ,"2002")


def test_deve_rejeitar_tipo_produto_vazio():
    with pytest.raises(
        ValueError,
        match="O tipo do produto é obrigatório",
    ):
        Produto(
            codigo_produto="1001",
            tipo_produto="",
        )