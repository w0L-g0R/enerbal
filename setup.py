from setuptools import setup
from setuptools import find_packages

setup(
    name='enspect-py',
    version='1.0',
    description='Energy balances monitor tool',
    author='wgo',
    author_email='wolfgang.goritschnig@protonmail.com',
    #packages=find_packages('src/enspect'),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    package_dir={'': 'src/enspect'},
)
