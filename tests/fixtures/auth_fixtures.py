from pytest import fixture
from tests.builders.auth_builder import AuthBuilder


@fixture
def auth_builder(client):
    return AuthBuilder(client)


@fixture
def registered_user(auth_builder):
    """Fixture to register a user for testing purposes."""
    return auth_builder.register(
        email="john@test.com",
        username="John123",
        password="John@123"
    )


@fixture()
def second_registered_user(auth_builder):
    """Fixture to register a second user for testing purposes."""
    return auth_builder.register(
        email="alice@test.com",
        username="Alice123",
        password="Alice@123"
    )


@fixture
def logged_in_user(auth_builder, registered_user):
    """Fixture to log in a registered user and provide their authentication details."""

    login = auth_builder.login(
        email=registered_user["email"],
        password=registered_user["password"],
    )

    return {
        **registered_user,
        **login
    }


@fixture()
def second_logged_in_user(auth_builder, second_registered_user):
    """Fixture to log in a second registered user and provide their authentication details."""
    
    login = auth_builder.login(
        email=second_registered_user["email"],
        password=second_registered_user["password"],
    )

    return {
        **second_registered_user,
        **login
    }