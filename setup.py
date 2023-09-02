from setuptools import setup, find_packages

setup(
    name="invest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["bs4", "requests", "selenium", "pandas", "pygsheets"],
)
