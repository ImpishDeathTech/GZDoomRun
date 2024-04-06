class GZDoomRunError(Exception):

    def __init__(self, code: int, reason: str):
        self.__what__ : str = f"[GZDoom Run Error] ({code}): {reason}"
        self.__code__ : int = code
    
    def what(self, exit_app: bool=True):
        print(self.__what__)
        
        if exit_app:
            sys.exit(self.__code__)