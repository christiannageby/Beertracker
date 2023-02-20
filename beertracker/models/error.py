"""This defines and creates the exceptions"""

class FermentingDoneBeforeBrewError(Exception):
    """ Exception raised when the brew is done fermenting before the brew is brewed"""

    def __init__(self, message="The brew cant be done fermenting when it is not brewed."):
        self.message: str = message
