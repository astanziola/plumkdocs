from setuptools import find_packages, setup
import io
import os

def read(*paths, **kwargs):
  content = ""
  with io.open(
    os.path.join(os.path.dirname(__file__), *paths),
    encoding=kwargs.get("encoding", "utf8"),
  ) as open_file:
    content = open_file.read().strip()
  return content

def read_requirements(path):
  return [
    line.strip()
    for line in read(path).split("\n")
    if not line.startswith(('"', "#", "-", "git+"))
  ]

setup(
    packages=find_packages(include=["plumkdocs*"]),
    python_requires=">=3.7",
    install_requires=read_requirements("requirements.txt"),
    include_package_data=True,
)
