from setuptools import find_packages, setup

setup(
    packages=find_packages(include=["sample_package*"]),
    include_package_data=True,
)
