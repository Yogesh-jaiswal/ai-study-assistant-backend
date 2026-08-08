import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import click
from flask.cli import with_appcontext
from slugify import slugify

from app.extensions import db
from models import ExamBlueprint


BLUEPRINT_DIR = Path("resources/exam_blueprints")


@dataclass(frozen=True)
class BlueprintSeed:
    name: str
    is_public: bool
    is_system: bool
    data: dict


@cache
def load_exam_blueprints() -> tuple[BlueprintSeed]:
    """
    Load and cache all built-in exam blueprints.

    The blueprint files are read and parsed only once for the lifetime
    of the Python process.
    """

    blueprints: list[BlueprintSeed] = []

    for exam in BLUEPRINT_DIR.iterdir():
        if not exam.is_file():
            continue

        is_system = exam.name.startswith("standard_")
        is_public = not is_system

        blueprints.append(
            BlueprintSeed(
                name=exam.name,
                is_public=is_public,
                is_system=is_system,
                data=json.loads(exam.read_text()),
            )
        )

    return tuple(blueprints)


def seed_exam_blueprints():
    """
    Seed all built-in exam blueprints.

    This function is idempotent and can safely be executed multiple times.
    """

    for blueprint in load_exam_blueprints():
        data = blueprint.data

        exists = ExamBlueprint.query.filter_by(
            name=data["exam_name"]
        ).first()

        if exists:
            continue

        db.session.add(
            ExamBlueprint(
                slug=slugify(data["exam_name"]),
                name=data["exam_name"],
                description=data["description"],
                is_public=blueprint.is_public,
                is_system=blueprint.is_system,
                structure=data,
            )
        )

    db.session.commit()


@click.command("seed-exam-blueprints")
@with_appcontext
def seed_exam_blueprints_command():
    """CLI command to seed the default exam blueprints."""

    seed_exam_blueprints()

    click.echo("Default exam blueprints seeded.")