from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def resource_dir():
    """Fixture to provide the path to the resources directory for testing."""
    return Path(__file__).parents[1] / "resources" / "extractors"