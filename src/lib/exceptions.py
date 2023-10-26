class ParseException(Exception):
    def __init__(self, cmd: str, lineno: str) -> None:
        self.message = f"Internal Error: {cmd}: could not parse tokens in {lineno}"         


class LUIParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("LUI", str(lineno))

class AUIPCParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("AUIPC", str(lineno))

class JALRParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("JALR", str(lineno))
    
class JALParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("JAL", str(lineno))

class BranchParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("BRANCH", str(lineno))

class LoadParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("LOAD", str(lineno))


class StoreParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("STORE", str(lineno))

class ImmediateArithParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("ARITHI", str(lineno))

class ArithParseException(ParseException):
    def __init__(self, lineno: str | int) -> None:
        super().__init__("ARITH", str(lineno))