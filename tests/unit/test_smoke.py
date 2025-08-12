def test_import_package():
    import importlib

    pkg = importlib.import_module("mlops_e2e")
    assert pkg is not None
