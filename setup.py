import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


# This call to setup() does all the work
setup(
    name="permissions-system",
    version="0.2.3",
    description="Alternative to admin utilities for more autonomy, targeted towards FastAPI.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zero-shubham/permissions_system",
    author="Shubham Biswas",
    author_email="shubhambiswas.zero@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests", "develop")),
    include_package_data=True,
    install_requires=[
        "sqlalchemy==1.3.20",
        "pydantic==1.6.1"
    ],
    setup_requires=['wheel']
)
