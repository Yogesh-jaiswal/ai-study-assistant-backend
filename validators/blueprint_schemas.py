from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field, model_validator
from . import UpdatedBaseModel

QUESTION_ANSWER_COMPATIBILITY = {
    "MCQ": {"single_choice"},
    "MultiSelect": {"multiple_choice"},
    "TrueFalse": {"boolean"},
    "FillBlank": {"text"},
    "Numerical": {"numeric"},
    "SubjectiveShort": {"text"},
    "Subjective": {"essay"},
    "DiagramQuestion": {"drawing"},
    "Custom": {
        "single_choice",
        "multiple_choice",
        "numeric",
        "boolean",
        "text",
        "essay",
        "drawing"
    },
}

class NavigationRules(BaseModel):
    """Model representing the navigation rules for an exam."""
    allow_cross_section_navigation: bool = Field(default=False)
    has_sectional_timers: bool = Field(default=False)
    is_computer_adaptive: bool = Field(default=False)

class QuestionDefaults(BaseModel):
    """Model representing default settings for questions in a question group."""
    question_type: Literal[
        "MCQ",                # Multiple choice supports single_choice
        "Numerical",          # Numerical questions supports numeric
        "Subjective",         # Subjective (Long) questions supports essay
        "SubjectiveShort",   # Subjective short (Short) question supports text
        "TrueFalse",          # True/False supports boolean
        "FillBlank",          # Fill in the blanks supports text
        "MultiSelect",        # Multiple select supports multiple_choice
        "DiagramQuestion",    # Diagram required question supports drawing
        "Custom"              # Custom question type supports all answer types
    ]
    answer_type: Literal[
        "single_choice",      # string/int
        "multiple_choice",    # list
        "numeric",            # number
        "boolean",            # bool
        "text",               # string
        "essay",              # long string
        "drawing",            # image/vector
    ]
    negative_marking: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_question_answer_compatibility(self):
        compatible_answers = QUESTION_ANSWER_COMPATIBILITY[self.question_type]

        if self.answer_type not in compatible_answers:
            raise ValueError(f"Invalid answer type for the given question type: {self.question_type}")
        
        return self

class Part(BaseModel):
    """Model representing a part of a question in a question group."""
    label: str
    count: int = Field(gt=0)
    marks: int = Field(gt=0)

class Alternative(BaseModel):
    """Model representing an alternative set of parts for a question group."""
    title: str
    parts: list[Part]

class SharedMaterial(BaseModel):
    """Model representing shared material for a question group."""
    type: Literal[
        "passage",
        "ascii_table",
        "ascii_diagram",
    ]

class AttemptRule(BaseModel):
    """Model representing the attempt rule for a question group."""
    type: Literal["or", "choose_n", "all"]
    count: int | None = None

    @model_validator(mode="after")
    def validate_count(self):
        if self.type == "choose_n":
            if self.count is None:
                raise ValueError("'count' is required when selection_rule.type is 'choose_n'.")
        elif self.count is not None:
            raise ValueError("'count' is only allowed when selection_rule.type is 'choose_n'.")

        return self
    
class QuestionGroup(BaseModel):
    """Model representing a group of questions in a section."""
    group_title: str
    selection_rule: AttemptRule
    shared_material: SharedMaterial | None = None
    defaults: QuestionDefaults
    parts: list[Part] | None = None
    alternatives: list[Alternative] | None = None

    @model_validator(mode="after")
    def validate_structure(self):
        if self.selection_rule.type == "or":
            if self.parts is not None:
                raise ValueError("'parts' must not be provided when selection_rule.type is 'or'.")

            if not self.alternatives:
                raise ValueError(
                    "'alternative' must contain at least one option when selection_rule.type is 'or'."
                )
            
            if len(self.alternatives) < 2:
                raise ValueError(
                    "'alternative' must contain at least two alternatives for an 'or' selection rule."
                )

        else:
            if self.parts is None:
                raise ValueError(
                    "'parts' is required when selection_rule.type is not 'or'."
                )

            if self.alternatives is not None:
                raise ValueError(
                    "'alternative' is only allowed when selection_rule.type is 'or'."
                )

        return self
        
class Section(BaseModel):
    """Model representing a section in an exam blueprint."""
    section_name: str
    total_marks: int
    section_duration: str | None = None
    question_groups: list[QuestionGroup]

    @model_validator(mode="after")
    def validate_marks(self):
        total_question_marks = 0

        for question_group in self.question_groups:
            selection_type = question_group.selection_rule.type

            if selection_type == "all":
                for part in question_group.parts:
                    total_question_marks += part.count * part.marks

            elif selection_type == "choose_n":
                count = question_group.selection_rule.count

                # For choose_n, the selected number of questions
                # determines the marks contributed by the group.
                remaining = count

                for part in question_group.parts:
                    selected = min(remaining, part.count)
                    total_question_marks += selected * part.marks
                    remaining -= selected

                    if remaining == 0:
                        break

            else:
                # Only ONE alternative is attempted.
                # All alternatives should therefore have the same marks.
                alternative_marks = []

                for alternative in question_group.alternatives:
                    marks = sum(
                        part.count * part.marks
                        for part in alternative.parts
                    )
                    alternative_marks.append(marks)

                if len(set(alternative_marks)) != 1:
                    raise ValueError(
                        f"All alternatives in question group "
                        f"'{question_group.group_title}' must have the same total marks."
                    )

                total_question_marks += alternative_marks[0]

        if total_question_marks != self.total_marks:
            raise ValueError(
                f"Section '{self.section_name}' total_marks ({self.total_marks}) "
                f"does not match the sum of marks from its question groups "
                f"({total_question_marks})."
            )

        return self

class BlueprintSchema(BaseModel):
    """Model representing the structure of an exam blueprint."""
    exam_name: str
    description: str
    total_marks: int
    duration: str
    navigation_rules: NavigationRules
    sections: list[Section]

    @model_validator(mode="after")
    def validate_blueprint(self):
        if self.navigation_rules.has_sectional_timers:
            for section in self.sections:
                if section.section_duration is None:
                    raise ValueError(
                        f"Section '{section.section_name}' must define 'section_duration' "
                        "when sectional timers are enabled."
                    )
                
        section_total = sum(section.total_marks for section in self.sections)

        if self.total_marks != section_total:
            raise ValueError(
                f"Exam total_marks ({self.total_marks}) does not match the sum of section marks ({section_total})."
            )

        return self
    
class BlueprintCreationRequest(UpdatedBaseModel):
    """Request model for creating a new exam blueprint."""
    is_public: bool = Field(default=False)
    structure: BlueprintSchema

class BlueprintCreationResponse(BaseModel):
    """Response model for a successful blueprint creation."""
    blueprint_slug: str
    message: str

class BlueprintMetadata(BaseModel):
    """Model representing metadata for an exam blueprint."""
    id: str
    slug: str
    name: str
    description: str
    is_public: bool
    owner: str | None
    created_at: datetime

class ListBlueprintResponse(BaseModel):
    """Response model for listing all exam blueprints."""
    blueprints: list[BlueprintMetadata]

class GetBlueprintResponse(BlueprintMetadata):
    """Response model for retrieving a specific exam blueprint."""
    structure: BlueprintSchema