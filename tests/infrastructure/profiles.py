from pytest import fixture

@fixture(scope="session")
def async_tasks(request):
    return request.config.getoption("--async-tasks")