from models.enums import EvaluationTypes

class QuestionNormalizer:
    @classmethod
    def build(cls, content: dict, evaluation_type: EvaluationTypes):
        NORMALIZER = {
            EvaluationTypes.QUIZ: cls._quiz_normalizer,
            EvaluationTypes.EXAM: cls._exam_normalizer
        }

        return NORMALIZER[evaluation_type](content)
    
    @staticmethod
    def _quiz_normalizer(content: dict):
        question_map = {}

        for question in content["questions"]:
            question_id = question["question_id"]

            question_map[question_id] = {
                **question,
                "answer_type": "MCQ",
                "question_type": "single_choice",
            }

        return question_map
    
    @staticmethod
    def _exam_normalizer(content: dict):
        question_map = {}

        for section in content["sections"]:
            for group in section["question_groups"]:
                question_type = group["defaults"]["question_type"]
                answer_type = group["defaults"]["answer_type"]

                if group["questions"]:
                    for question in group["questions"]:
                        question_id = question["question_id"]

                        question_map[question_id] = {
                            **question,
                            "answer_type": answer_type,
                            "question_type": question_type,
                        }

                else:
                    for alt in group["alternatives"]:
                        for question in alt["questions"]:
                            question_id = question["question_id"]

                            question_map[question_id] = {
                                **question,
                                "answer_type": answer_type,
                                "question_type": question_type,
                            }

            return question_map