# Pyroute Exceptions

class PyrouteException(Exception):
    pass

class EngineError(PyrouteException):
    pass

class ModuleError(PyrouteException):
    pass

class AmbiguousMethodCallError(PyrouteException):
    pass

class MethodNotFoundError(PyrouteException):
    pass

class AssignmentError(PyrouteException):
    pass

class PyrouteAssertionError(PyrouteException):
    pass

class TestError(PyrouteException):
    pass

class CaseError(PyrouteException):
    pass
