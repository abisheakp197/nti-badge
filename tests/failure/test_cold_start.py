"""Cold start: modules import without DB configured."""


def test_all_modules_import(clean_env):
    import lib.mode
    import lib.db
    import lib.store
    import lib.crypto
    import lib.certificate
    import lib.drift
    import lib.tiers
    import lib.spec
    import lib.oidc
    import lib.hub_store
    import lib.aggregator
    import lib.federation_client
    assert True


def test_mode_info_shape(clean_env):
    from lib.mode import get_node_info
    info = get_node_info()
    assert "mode" in info
