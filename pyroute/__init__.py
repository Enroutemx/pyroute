
def I(module):
    print("mesjae  desde I")

    class Helper(*module):
        pass

    return Helper

# class Decorators(object):
#     pass
