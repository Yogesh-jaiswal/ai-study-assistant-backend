def build_answers(exam):
    answers = []

    for section in exam["sections"]:
        for group in section["question_groups"]:

            question_lists = []

            if group["questions"]:
                question_lists.append(group["questions"])
            else:
                for alt in group["alternatives"]:
                    question_lists.append(alt["questions"])

            for questions in question_lists:
                for question in questions:

                    answer = None

                    if question.get("options"):
                        answer = question["options"][0]["label"]

                    answers.append(
                        {
                            "question_id": question["question_id"],
                            "answer": answer,
                        }
                    )

    return answers