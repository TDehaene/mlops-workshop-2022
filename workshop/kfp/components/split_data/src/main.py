"""
This file is the entrypoint of the component. 
The main function parses all the parameters and passes them to the actual component logic.
"""
import fire

from split_data import train_test_split


if __name__ == '__main__':
    fire.Fire(train_test_split)
