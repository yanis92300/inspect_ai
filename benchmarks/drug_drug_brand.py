from inspect_ai import Task, task
from inspect_ai.dataset import Sample, hf_dataset
from inspect_ai.scorer import choice,model_graded_fact
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


TEMPLATE = r"""
Answer the following multiple choice question. The last line of your response should be of the following format: 'ANSWER: $LETTER' (without quotes) where LETTER is one of {letters}. Think step by step before answering .

{question}

{choices}
""".strip()


@task
def drugs_drugs():
    dataset = hf_dataset(
        path="yanischamson/PKG_final_drug_brand",
        split="train",  # or "validation" or "test", depending on which split you want
        sample_fields=record_to_sample,
        trust=True,
        shuffle=True,
    )

    return Task(
        dataset=dataset,
        plan=[multiple_choice(template=TEMPLATE)],
        scorer=choice(),
    )
