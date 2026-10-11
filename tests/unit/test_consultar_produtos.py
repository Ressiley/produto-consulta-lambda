from unittest.mock import create_autospec

import pytest

from product_query.application.dto.consulta_produtos_input import (
    ConsultaProdutosInput,
    ProdutoConsultaInput,
)
from product_query.application.dto.status_consulta_produto import (
    StatusConsultaProduto,
)
from product_query.application.exceptions import (
    AuthenticationError,
    CredentialsError,
    ProdutoExternoError,
)
from product_query.application.ports.produto_externo_client import ProdutoExternoClient
from product_query.application.ports.produto_repository import ProdutoRepository
from product_query.application.use_cases.consultar_produtos import (
    ConsultarProdutosUseCase,
)


def test_deve_consultar_produto_com_sucesso():
    repository = create_autospec(ProdutoRepository, instance=True)
    external_client = create_autospec(ProdutoExternoClient, instance=True)

    repository.buscar_codigo_rds.return_value = "RDS9001"
    external_client.consultar_produto.return_value = {
        "descricao": "Produto exemplo",
        "situacao": "ATIVO",
    }

    use_case = ConsultarProdutosUseCase(
        produto_repository=repository, produto_externo_client=external_client
    )

    resultado = use_case.executar(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
    )

    assert resultado == {
        "codigo_produto": "1001",
        "tipo_produto": "FUNDIDO",
        "cod_prod_rds": "RDS9001",
        "dados_externos": {
            "descricao": "Produto exemplo",
            "situacao": "ATIVO",
        },
    }

    repository.buscar_codigo_rds.assert_called_once_with(
        codigo_produto="1001",
        tipo_produto="FUNDIDO",
    )

    external_client.consultar_produto.assert_called_once_with(
        cod_prod_rds="RDS9001",
    )


def test_nao_deve_consultar_api_quando_produto_nao_existe():
    repository = create_autospec(ProdutoRepository, instance=True)
    external_client = create_autospec(ProdutoExternoClient, instance=True)

    repository.buscar_codigo_rds.return_value = None

    use_case = ConsultarProdutosUseCase(
        produto_repository=repository,
        produto_externo_client=external_client,
    )

    resultado = use_case.executar(codigo_produto="9999", tipo_produto="FUNDIDO")

    assert resultado is None

    repository.buscar_codigo_rds.assert_called_once_with(
        codigo_produto="9999", tipo_produto="FUNDIDO"
    )

    external_client.consultar_produto.assert_not_called()


def test_deve_consultar_multiplos_produtos_com_sucesso():
    repositorio = create_autospec(
        ProdutoRepository,
        instance=True,
    )
    cliente_externo = create_autospec(
        ProdutoExternoClient,
        instance=True,
    )

    repositorio.buscar_codigo_rds.side_effect = [
        "RDS1001",
        "RDS1002",
    ]

    cliente_externo.consultar_produto.side_effect = [
        {"descricao": "Produto 1001"},
        {"descricao": "Produto 1002"},
    ]

    caso_de_uso = ConsultarProdutosUseCase(
        repositorio,
        cliente_externo,
    )

    entrada = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=(
            ProdutoConsultaInput(codigo_produto="1001"),
            ProdutoConsultaInput(codigo_produto="1002"),
        ),
    )

    saida = caso_de_uso.executar_multiplos(entrada)

    assert len(saida.resultados) == 2

    assert saida.resultados[0].codigo_produto == "1001"
    assert saida.resultados[0].cod_prod_rds == "RDS1001"
    assert saida.resultados[0].dados_externos == {"descricao": "Produto 1001"}
    assert saida.resultados[0].status == StatusConsultaProduto.SUCESSO

    assert saida.resultados[1].codigo_produto == "1002"
    assert saida.resultados[1].cod_prod_rds == "RDS1002"
    assert saida.resultados[1].dados_externos == {"descricao": "Produto 1002"}
    assert saida.resultados[1].status == StatusConsultaProduto.SUCESSO

    assert repositorio.buscar_codigo_rds.call_count == 2
    assert cliente_externo.consultar_produto.call_count == 2


def test_deve_consultar_multiplos_produtos_com_item_nao_encontrado():
    repositorio = create_autospec(
        ProdutoRepository,
        instance=True,
    )
    cliente_externo = create_autospec(
        ProdutoExternoClient,
        instance=True,
    )

    repositorio.buscar_codigo_rds.side_effect = [
        "RDS1001",
        None,
    ]

    cliente_externo.consultar_produto.return_value = {
        "descricao": "Produto 1001",
    }

    caso_de_uso = ConsultarProdutosUseCase(
        repositorio,
        cliente_externo,
    )

    entrada = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=(
            ProdutoConsultaInput(codigo_produto="1001"),
            ProdutoConsultaInput(codigo_produto="1002"),
        ),
    )

    saida = caso_de_uso.executar_multiplos(entrada)

    assert len(saida.resultados) == 2

    primeiro = saida.resultados[0]
    assert primeiro.codigo_produto == "1001"
    assert primeiro.cod_prod_rds == "RDS1001"
    assert primeiro.dados_externos == {
        "descricao": "Produto 1001",
    }
    assert primeiro.status == StatusConsultaProduto.SUCESSO

    segundo = saida.resultados[1]
    assert segundo.codigo_produto == "1002"
    assert segundo.cod_prod_rds is None
    assert segundo.dados_externos is None
    assert segundo.status == StatusConsultaProduto.NAO_ENCONTRADO

    assert repositorio.buscar_codigo_rds.call_count == 2
    cliente_externo.consultar_produto.assert_called_once_with("RDS1001")


def test_nao_deve_consultar_api_quando_nenhum_produto_existe():
    repositorio = create_autospec(
        ProdutoRepository,
        instance=True,
    )
    cliente_externo = create_autospec(
        ProdutoExternoClient,
        instance=True,
    )

    repositorio.buscar_codigo_rds.return_value = None

    caso_de_uso = ConsultarProdutosUseCase(
        repositorio,
        cliente_externo,
    )

    entrada = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=(
            ProdutoConsultaInput(codigo_produto="1001"),
            ProdutoConsultaInput(codigo_produto="1002"),
        ),
    )

    saida = caso_de_uso.executar_multiplos(entrada)

    assert len(saida.resultados) == 2

    assert [produto.codigo_produto for produto in saida.resultados] == ["1001", "1002"]

    for produto in saida.resultados:
        assert produto.cod_prod_rds is None
        assert produto.dados_externos is None
        assert produto.status == StatusConsultaProduto.NAO_ENCONTRADO

    assert repositorio.buscar_codigo_rds.call_count == 2

    cliente_externo.consultar_produto.assert_not_called()


def test_deve_continuar_consulta_quando_um_produto_apresenta_erro():
    repositorio = create_autospec(
        ProdutoRepository,
        instance=True,
    )
    cliente_externo = create_autospec(
        ProdutoExternoClient,
        instance=True,
    )

    repositorio.buscar_codigo_rds.side_effect = [
        "RDS1001",
        "RDS1002",
        "RDS1003",
    ]

    cliente_externo.consultar_produto.side_effect = [
        {"descricao": "Produto 1001"},
        ProdutoExternoError("Falha na API externa"),
        {"descricao": "Produto 1003"},
    ]

    caso_de_uso = ConsultarProdutosUseCase(
        repositorio,
        cliente_externo,
    )

    entrada = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=(
            ProdutoConsultaInput(codigo_produto="1001"),
            ProdutoConsultaInput(codigo_produto="1002"),
            ProdutoConsultaInput(codigo_produto="1003"),
        ),
    )

    saida = caso_de_uso.executar_multiplos(entrada)

    assert len(saida.resultados) == 3

    assert saida.resultados[0].status == StatusConsultaProduto.SUCESSO
    assert saida.resultados[1].status == StatusConsultaProduto.ERRO
    assert saida.resultados[2].status == StatusConsultaProduto.SUCESSO

    assert saida.resultados[0].codigo_produto == "1001"
    assert saida.resultados[1].codigo_produto == "1002"
    assert saida.resultados[2].codigo_produto == "1003"

    assert saida.resultados[1].dados_externos is None

    assert repositorio.buscar_codigo_rds.call_count == 3
    assert cliente_externo.consultar_produto.call_count == 3


@pytest.mark.parametrize(
    "classe_erro",
    [
        AuthenticationError,
        CredentialsError,
    ],
)
def test_deve_interromper_consulta_quando_ocorre_falha_geral(
    classe_erro,
):
    repositorio = create_autospec(
        ProdutoRepository,
        instance=True,
    )
    cliente_externo = create_autospec(
        ProdutoExternoClient,
        instance=True,
    )

    repositorio.buscar_codigo_rds.return_value = "RDS1001"

    cliente_externo.consultar_produto.side_effect = classe_erro("Falha geral na integração")

    caso_de_uso = ConsultarProdutosUseCase(
        repositorio,
        cliente_externo,
    )

    entrada = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=(
            ProdutoConsultaInput(codigo_produto="1001"),
            ProdutoConsultaInput(codigo_produto="1002"),
        ),
    )

    with pytest.raises(classe_erro):
        caso_de_uso.executar_multiplos(entrada)

    repositorio.buscar_codigo_rds.assert_called_once_with(
        "1001",
        "FUNDIDO",
    )

    cliente_externo.consultar_produto.assert_called_once_with("RDS1001")


def test_deve_preservar_codigo_rds_quando_api_externa_falha():
    repositorio = create_autospec(
        ProdutoRepository,
        instance=True,
    )
    cliente_externo = create_autospec(
        ProdutoExternoClient,
        instance=True,
    )

    repositorio.buscar_codigo_rds.return_value = "RDS1001"

    cliente_externo.consultar_produto.side_effect = ProdutoExternoError("Falha na API externa")

    caso_de_uso = ConsultarProdutosUseCase(
        repositorio,
        cliente_externo,
    )

    entrada = ConsultaProdutosInput(
        tipo_produto="FUNDIDO",
        produtos=(ProdutoConsultaInput(codigo_produto="1001"),),
    )

    saida = caso_de_uso.executar_multiplos(entrada)

    assert len(saida.resultados) == 1

    resultado = saida.resultados[0]

    assert resultado.codigo_produto == "1001"
    assert resultado.status == StatusConsultaProduto.ERRO
    assert resultado.cod_prod_rds == "RDS1001"
    assert resultado.dados_externos is None

    repositorio.buscar_codigo_rds.assert_called_once_with(
        "1001",
        "FUNDIDO",
    )

    cliente_externo.consultar_produto.assert_called_once_with("RDS1001")
