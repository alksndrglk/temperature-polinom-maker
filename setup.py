
from setuptools import setup, find_packages


setup(
    name="coefs",
    version="1.0.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["coefs=temp_coefs:main"]},
)

