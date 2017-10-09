from setuptools import setup

setup(
    name='pyroute',
    version='0.1',
    py_modules=['pyroute'],
    install_requires=['Click', 'requests', "pytest","WebDriver"],
    entry_points='''
    [console_scripts]
    pyroute=pyroute.cli:runnable
    '''
)
