from pytest import fixture

from tests.builders.blueprint_builder import BlueprintBuilder


@fixture
def blueprint_builder(client):
    return BlueprintBuilder(client)


@fixture
def created_blueprint(
    blueprint_builder,
    logged_in_user,
):
    blueprint = blueprint_builder.create(
        access_token=logged_in_user["access_token"],
        payload=BlueprintBuilder.build_payload(),
    )

    return {
        **logged_in_user,
        **blueprint,
    }


@fixture
def second_created_blueprint(
    blueprint_builder,
    second_logged_in_user,
):
    blueprint = blueprint_builder.create(
        access_token=second_logged_in_user["access_token"],
        payload=BlueprintBuilder.build_payload(),
    )

    return {
        **second_logged_in_user,
        **blueprint,
    }