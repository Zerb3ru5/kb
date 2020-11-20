from setuptools import setup, find_packages

setup(
    name='kb',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts':{
            'kb = kb.__main__:main'
        }
    }, install_requires=['click']
)