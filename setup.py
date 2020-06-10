import re

from setuptools import setup

with open("src/tfspec/__init__.py", encoding="utf8") as f:
    matched = re.search(r'__version__ = "(.*?)"', f.read())
    if matched is None:
        raise ValueError('Must provide version in __init__.py') 
    version = matched.group(1)

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="TerraformSpec",
    version=version,
    install_requires=[
    ],
    extras_require={"dotenv": ["python-dotenv"]},
)