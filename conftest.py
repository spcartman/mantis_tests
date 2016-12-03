import pytest
import json
import os.path
import importlib
from fixture.application import Application


fixture = None
target = None


@pytest.fixture(scope="session")
def config(request):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--target"))
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request, config):
    global fixture
    if (fixture is None) or (not fixture.is_valid()):
        fixture = Application(browser=request.config.getoption("--browser"), base_url=config["web"]["baseUrl"],
                              user=config["webadmin"]["user"], password=config["webadmin"]["pass"])
        fixture.navigation.home_page()
    fixture.session.ensure_login(username=fixture.user, password=fixture.password)
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


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            test_data = importlib.import_module("data.%s" % fixture[5:]).test_data
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])
