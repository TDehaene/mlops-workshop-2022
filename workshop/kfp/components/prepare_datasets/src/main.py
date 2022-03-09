"""
This file is the entrypoint of the component. 
The main function parses all the parameters and passes them to the actual component logic.
"""
import fire

from prepare_datasets import prepare_datasets


if __name__ == '__main__':
    fire.Fire(prepare_datasets)
