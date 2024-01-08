"""
Taken from Jenna's Cellpainting repo (exceptions.py) https://github.com/WayScience/nf1_cellpainting_data/blob/main/utils/errors/exceptions.py
This class defines a custom exception class for exceeding the max workers on a machine.
"""

class MaxWorkerError(Exception):
    """
    Raised when the number of workers assigned to `max_workers` exceeds the number of CPU/workers on the machine. 
    """
    pass
    
