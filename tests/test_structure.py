from product_query import adapters, application, domain, entrypoints


def test_project_package_can_be_imported():
    assert domain is not None
    assert application is not None
    assert adapters is not None
    assert entrypoints is not None
