from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="beautify_print",  # This will be the package name on PyPI
    version="0.2.0",
    author="ChenDaiwei-99",
    author_email="daiwei.chen2020@outlook.com",
    description="A package for beautiful printing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChenDaiwei-99/beautify_print",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # List your dependencies here
        # e.g., "colorama>=0.4.4",
    ],
)