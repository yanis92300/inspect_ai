# Inspect_SAFETY: A Framework for Evaluating LLM Safety on Drug Interactions


This repository is a fork of the Inspect framework, originally developed for large language model evaluations. We have adapted it to focus specifically on assessing the safety of large language models (LLMs) in the context of drug interactions.

Inspect provides a variety of built-in components, including facilities for prompt engineering, tool usage, multi-turn dialog, and model-graded evaluations. Extensions to Inspect (e.g., to support new elicitation and scoring techniques) can be integrated via additional Python packages.

## Getting Started

To begin working with this fork of Inspect, clone the repository and install it with the `-e` flag and `[dev]` optional dependencies:

```bash
$ git clone https://github.com/YourUsername/inspect_ai.git
$ cd inspect_ai
$ pip install -e ".[dev]"

