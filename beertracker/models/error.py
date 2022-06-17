class FermentingDoneBeforeBrewError(Exception):
    """ Exception raised when the brew is done fermenting before the brew is brewn"""

    def __init__(self, message="The brew cant be done femneting when it is not brewn."):
        self.message: str = message
