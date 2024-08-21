from inspect_ai import Task, task
from inspect_ai.dataset import Sample, hf_dataset
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice


def record_to_sample(record):
    target_mapping = {0: "A", 1: "B", 2: "C", 3: "D"}
    return Sample(
        input=str(record["sent1"]),
        target=target_mapping[
            int(record["label"])
        ],  # Convert label to corresponding letter
        choices=[
            str(record["ending0"]),
            str(record["ending1"]),
            str(record["ending2"]),
            str(record["ending3"]),
        ],
    )


# TEMPLATE = r"""
# The entire content of your response should be of the following format: 'ANSWER:
# $NUMBER' (without quotes) where LETTER is one of {number}.

# Given either a question or a statement followed by 4 possible solutions
# labelled 0,1,2 or 3, choose the most appropriate solution. If a question is given,
# the solutions answer the question. If a statement is given, the solutions
# explain how to achieve the statement.

# {question}

# {choices}
# """.strip()


@task
def drugs_drugs():
    dataset = hf_dataset(
        path="yanischamson/pkg_dataset_drugs_disease_easy",
        split="train",  # or "validation" or "test", depending on which split you want
        sample_fields=record_to_sample,
        trust=True,
        shuffle=True,
    )

    return Task(
        dataset=dataset,
        plan=[multiple_choice()],
        scorer=choice(),
    )
