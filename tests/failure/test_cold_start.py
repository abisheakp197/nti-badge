"""Cold start: modules import without DB configured."""

import lib.db
import lib.mode
import lib.routes
import nti_badge


def test_all_modules_import(clean_env: None) -> None:
    assert nti_badge.__version__ == "0.1.0"
    assert lib.mode.get_mode() == "standalone"
    assert lib.db.get_backend() == "file"


def test_mode_info_shape(clean_env: None) -> None:
    from lib.mode import get_node_info
    info = get_node_info()
    assert "mode" in info
