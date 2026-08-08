from pytest import fixture

@fixture(scope="session")
def async_tasks(request):
    """
    Fixture to determine if async tasks should be enabled for testing. 
    It checks the command-line option --async-tasks and returns its value, 
    allowing tests to conditionally run based on whether async tasks are enabled or disabled.
    """
    return request.config.getoption("--async-tasks")