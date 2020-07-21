from setuptools import setup
from setuptools import find_packages

setup(
    name='enerbal-py',
    version='1.0',
    description='Energy balances monitor tool',
    author='gadmin',
    author_email='aea.gadmin@protonmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
