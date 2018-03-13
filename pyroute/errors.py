# Pyroute Exceptions

"""
	This file will manage every exception Pyroute might throw.
"""

"""**PyrouteException** is the most general exception, every other exception will depend on this one."""
class PyrouteException(Exception):
    pass

"""**EngineError** will handle every exception the engine.py file might encounter."""
class EngineError(PyrouteException):
    pass

"""**ModuleError** will be used when the module you want to load doesn't exist."""
class ModuleError(PyrouteException):
    pass

"""**AmbiguousMethodCallError** will pop up only when you're running test with two or more modules loaded.
If this exception is showed it means one of the methods used in the test has the same name in two or
more modules."""
class AmbiguousMethodCallError(PyrouteException):
    pass

"""**MethodNotFoundError** means the method used in the test is either misspelled or doesn't exist."""
class MethodNotFoundError(PyrouteException):
    pass

"""**AssignmentError** will raise when you try to assign something to an existing method inside the loaded module."""
class AssignmentError(PyrouteException):
    pass

"""**PyrouteAssertionError** will be used when a custom assertion raises an error."""
class PyrouteAssertionError(PyrouteException):
    pass

"""**TestError** will indicate if the test doesn't exist or if the name is different from the one specified in
the configuration file."""
class TestError(PyrouteException):
    pass

"""**CaseError** is used to keep count of how many test cases failed, but it will depend on the testing scenario if
whether or not it raises an error."""
class CaseError(PyrouteException):
    pass
