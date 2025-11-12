from setuptools import setup, find_packages

setup(
    name="beautify-print",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
    ],
    python_requires=">=3.7",
    author="Your Name",
    description="A module for beautifying console output using Rich",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)