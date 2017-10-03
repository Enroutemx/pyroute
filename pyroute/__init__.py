
def I(module):
    class Helper(*module):
        pass
    return Helper

# class Decorators(object):
#     pass
