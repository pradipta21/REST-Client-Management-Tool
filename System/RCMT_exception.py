"""
@author: Pradipta
"""

class yamlScannerError(Exception):
    
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        
        if self.message:
            return 'YamlScannerError : {0} '.format(self.message)
        else:
            return 'YamlScannerError has been raised'
        
class argumentDataTypeError(Exception):
    
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        
        if self.message:
            return 'argumentDataTypeError : {0} '.format(self.message)
        else:
            return 'argumentDataTypeError has been raised'
        
class apiAddArgumentError(Exception):
    
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        
        if self.message:
            return 'argumentDataTypeError : {0} '.format(self.message)
        else:
            return 'argumentDataTypeError has been raised'