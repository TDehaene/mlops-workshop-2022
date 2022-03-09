"""
This file is the entrypoint of the component. 
The main function parses all the components and passes them to the actual component logic.
"""
import fire

from evaluation import evaluate_model


if __name__ == '__main__':
    fire.Fire(evaluate_model)