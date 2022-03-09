"""
This file is the entrypoint of the component. 
The main function parses all the components and passes them to the actual component logic.
"""
import fire

from training import train_model


if __name__ == '__main__':
    fire.Fire(train_model)