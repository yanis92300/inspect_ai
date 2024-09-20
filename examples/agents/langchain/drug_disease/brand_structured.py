# from typing import Any, cast
# from inspect_langchain import langchain_solver
# from langchain.agents import AgentExecutor
# from langchain_core.language_models import BaseChatModel
# from inspect_ai import Task, task
# from inspect_ai.dataset import json_dataset
# from inspect_ai.scorer import model_graded_fact,answer
# from inspect_ai.solver import Solver, solver
# from langchain_openai import ChatOpenAI
# from langchain_experimental.agents import create_csv_agent


# #TODO : generic brand swap => add in prompt/prefix the fact that if the name is not found maybe he can try to reason or maybe I have to do RAG instead of Iformation retrieval
# #TODO : comparer ablation prompt vs pas d ablation (run sur X experiments)
# #TODO : RAG vs string matching (agent)
# #TODO : MIMIC ? 
# import pandas as pd


# @solver
# def csv_query(csv_file_path: str, max_iterations: int | None = 15, max_execution_time: float | None = None) -> Solver:
#     async def agent(llm: BaseChatModel, input: dict[str, Any]):
#         # Create CSV agent
#         csv_agent = create_csv_agent( 
#             llm,
#             csv_file_path,
#             prefix="""You are a pandas dataframe agene working with a pandas DataFrame named 'df'. 
#                        When using python_repl_ast, you must only use the 'df' variable to refer to the dataframe.
#                        The DataFrame contains information about drug interactions and is already loaded in the environment. Dont Sample DataFrame resembling the structure from the prompt. :""",
#             verbose=True,
#             agent_type="openai-tools",
#             allow_dangerous_code=True,
              
#         )
#         original_query = input
#         modified_query = f"""
#         To answer the question: {original_query}
#         Please follow these steps:
#         1. Check for entries where display_relation is 'synergistic interaction'.
#         2. For the drug in question, check both x_name and y_name columns.
#         3. If the drug is found in x_name, look for interaction drugs in y_name.
#         4. If the drug is found in y_name, look for interaction drugs in x_name.
#         5. Combine the results from steps 3 and 4.
#         6. Based on the combined results, answer the original question.
#         Provide a step-by-step explanation of your process and findings.
#         """
#         # Execute the agent and return output
#         result = await csv_agent.ainvoke(original_query)
#         print(result)
#         return result

#     # Return agent function as inspect solver
#     return langchain_solver(agent)

# @task
# def csv_task() -> Task:
#     return Task(
#         dataset=json_dataset("interaction_100.jsonl"),
#         plan=csv_query("top50_sample_100.csv"),
#         scorer=model_graded_fact(),
#     )
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Any, cast
from inspect_langchain import langchain_solver
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent, create_csv_agent
from langchain_core.language_models import BaseChatModel
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import model_graded_fact, answer
from inspect_ai.solver import Solver, solver
from langchain_openai import ChatOpenAI
import pandas as pd

@solver
def pandas_df_query(csv_file_path: str, max_iterations: int | None = 15, max_execution_time: float | None = None) -> Solver:
    async def agent(llm: BaseChatModel, input: dict[str, Any]):
        # Load CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Create Pandas DataFrame agent
        pandas_agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            agent_type="openai-tools",
            prefix = """
            You are a pandas dataframe agent working with a pandas DataFrame named 'df'.
            When using python_repl_ast, you must only use the 'df' variable to refer to the dataframe.
            The DataFrame contains information about drug and disease contraindications and is already loaded in the environment.
            Dont Sample DataFrame resembling the structure from the prompt.
            If a brand name for a drug is provided in the query, first convert it to its generic name using your knowledge of pharmaceuticals.
            Always use the generic name when querying the DataFrame.
            Explain your reasoning 
            """,
            allow_dangerous_code=True,
        )
        
        original_query = input
        modified_query = f"""
    To answer the question: {original_query}
    Please follow these steps:
    1. If a brand name is given, convert it to its generic name using your knowledge of pharmaceuticals. Explain your reasoning for this conversion.
    2. Check for entries where display_relation is 'contraindication'.
    3. For the identified drug (using its generic name), check both x_name and y_name columns.
    4. If the drug is found in x_name, look for contraindicated diseases in y_name.
    5. If the drug is found in y_name, look for contraindicated diseases in x_name.
    6. Combine the results from steps 4 and 5.
    7. Based on the combined results, answer the original question.
    8. In the final answer, include both the brand name and generic name of the drug in question.
    Provide a step-by-step explanation of your process and findings.
    """
        
        # Execute the agent and return output
        result = await pandas_agent.ainvoke(modified_query)
        print(result)
        return result

    # Return agent function as inspect solver
    return langchain_solver(agent)

@task
def pandas_df_task() -> Task:
    return Task(
        dataset=json_dataset("brand_drug_disease.jsonl"),
        plan=pandas_df_query("filtered_drug_disease_generic_top50.csv"),
        scorer=model_graded_fact(),
    )
    
#  To answer the question: {original_query}
#         Please follow these steps:
#         1. Look entries that are ralated to interactions.
#         2. check if you find the drug in the data
#         3. If the drug is found in the data find the interaction drugs.
#         4. then answer the original question.
#         Provide a step-by-step explanation of your process and findings.