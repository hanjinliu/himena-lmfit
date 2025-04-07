from himena.testing import install_plugin
import pytest

@pytest.fixture(scope="session", autouse=True)
def init_pytest(request):
    install_plugin("himena-lmfit")
