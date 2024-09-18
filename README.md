# Drug Interaction Experiments

This repository contains a series of experiments to evaluate the ability of GPT-4o mini to understand drug-drug interactions using various approaches. The experiments cover both generic and brand names, as well as different querying strategies.


# Drug Interaction Experiments

This repository contains a series of experiments to evaluate the ability of GPT-4o mini to understand drug-drug interactions using various approaches. The experiments cover both generic and brand names, as well as different querying strategies.

## Prerequisite

Before running the experiments, ensure the following setup steps are completed:
- create .env file with your `OPENAI_API_KEY`

- Install the necessary package by running:  
  ```bash
  pip install inspect-ai
  pip intstall openai
  export OPENAI_API_KEY
  ```
- go in the langchain experimental folder usually  `libs/experimental/langchain_experimental/agents/agent_toolkits/pandas/base.py` and change all the ```python number_of_head_rows: int = 5```  by ```python number_of_head_rows: int = 1000``` (adapt to number of CSV line for rags, here is 1000)


## Experiments

### 1. GPT-4o mini Out-of-the-Box (Generic Names)
- **File**: `\inspect_fork\benchmarks\drug_drug_generic.py`
- **Description**: Evaluates GPT-4o mini's ability to understand drug-drug interactions using generic names in the questions.

### 2. GPT-4o mini Out-of-the-Box (Brand Names)
- **File**: `\inspect_fork\benchmarks\drug_drug_brand.py`
- **Description**: Same as Experiment 1, but uses brand names in the questions.

### 3. GPT-4o mini + RAG (Generic Names, Standard Query)
- **File**: `\inspect_fork\examples\agents\langchain\no_swap_standard.py`
- **Dataset**: `\inspect_fork\examples\agents\langchain\no_swap_experiments.jsonl`
- **RAG Database**: `\inspect_fork\examples\agents\langchain\filtered_drug_drug_generic_top50.csv`
- **Description**: Uses GPT-4o mini with RAG on generic names, querying the LLM with straightforward questions.

### 4. GPT-4o mini + RAG (Generic Names, Detailed Query)
- **File**: `\inspect_fork\examples\agents\langchain\no_swap_structured.py`
- **Dataset**: Same as Experiment 3
- **RAG Database**: Same as Experiment 3
- **Description**: Similar to Experiment 3, but uses detailed queries instead of straightforward ones.

### 5. GPT-4o mini + RAG (Brand to Generic Swap, Standard Query)
- **File**: `\inspect_fork\examples\agents\langchain\swap_standard_query.py`
- **Dataset**: `\inspect_fork\examples\agents\langchain\swap_experiment.jsonl`
- **Description**: Uses GPT-4o mini with RAG, swapping generic names to brand names, and using standard straightforward queries.

### 6. GPT-4o mini + RAG (Brand to Generic Swap, Detailed Query)
- **File**: `\inspect_fork\examples\agents\langchain\swap_structured_query.py`
- **Dataset**: Same as Experiment 5
- **Description**: Similar to Experiment 5, but uses detailed queries instead of straightforward ones.

## Running the Experiments

- To run each experiment, use the following command: `inspect eval .<name_of_the_file> --model <name_of_the_model>`
- For example, to run the experiment in Experiment 5 (Brand to Generic Swap, Standard Query): `inspect eval .\swap_standard_query.py --model openai/gpt-4o-mini`


## Data Files

- `filtered_drug_drug_generic_top50.csv`: RAG database for generic drug names
- `no_swap_experiments.jsonl`: Dataset for experiments without name swapping
- `swap_experiment.jsonl`: Dataset for experiments with generic to brand name swapping


