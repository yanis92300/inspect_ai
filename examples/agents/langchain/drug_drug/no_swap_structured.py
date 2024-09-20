import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Any, cast
from inspect_langchain import langchain_solver
from langchain.agents import AgentExecutor
from langchain_core.language_models import BaseChatModel
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import model_graded_fact,answer
from inspect_ai.solver import Solver, solver
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_csv_agent


#TODO : chat memory so that we dont need to load the csv file everytime
#TODO : rework the prompt so that the agent do always the same steps ? chain ? 

import pandas as pd


@solver
def csv_query(csv_file_path: str, max_iterations: int | None = 15, max_execution_time: float | None = None) -> Solver:
    async def agent(llm: BaseChatModel, input: dict[str, Any]):
        # Create CSV agent
        csv_agent = create_csv_agent( 
            llm,
            csv_file_path,
            prefix = """Assume 'df' is the dataframe provided and already loaded in the environment. You are a pandas dataframe agent working with a pandas DataFrame named 'df'.
            When using python_repl_ast, you must only use the 'df' variable to refer to the dataframe.
            The DataFrame contains information about drug interactions and is already loaded in the environment.
            Dont Sample DataFrame resembling the structure from the prompt.
            """,
            verbose=True,
            agent_type="openai-tools",
            allow_dangerous_code=True,
              
        )
        original_query = input
        modified_query = f"""
        To answer the question: {original_query}
        Please follow these steps:
        1. Check for entries where display_relation is 'synergistic interaction'.
        2. For the drug in question, check both x_name and y_name columns.
        3. If the drug is found in x_name, look for interaction drugs in y_name.
        4. If the drug is found in y_name, look for interaction drugs in x_name.
        5. Combine the results from steps 3 and 4.
        6. Based on the combined results, answer the original question.
        Provide a step-by-step explanation of your process and findings.
        """
        # Execute the agent and return output
        result = await csv_agent.ainvoke(modified_query)
        print(result)
        return result

    # Return agent function as inspect solver
    return langchain_solver(agent)

@task
def csv_task() -> Task:
    return Task(
        dataset=json_dataset("no_swap_experiments.jsonl"),
        plan=csv_query("filtered_drug_drug_generic_top50.csv"),
        scorer=model_graded_fact(),
    )