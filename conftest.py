import pytest
import json
import os.path
from fixture.application import Application


fixture = None
target = None


def load_conf_file(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):
    global fixture
    web_config = load_conf_file(request.config.getoption("--target"))["web"]
    if (fixture is None) or (not fixture.is_valid()):
        fixture = Application(browser=request.config.getoption("--browser"), base_url=web_config["baseUrl"])
        fixture.navigation.open_home_page()
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
