"""
This file is the entrypoint of the component. 
The main function parses all the components and passes them to the actual component logic.
"""
import fire

from preprocessing import preprocess


if __name__ == '__main__':
    fire.Fire(preprocess)