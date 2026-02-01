from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in project_management/__init__.py
from project_management import __version__ as version

setup(
    name="project_management",
    description="Project Management System with Tasks, Resources, and Budget Tracking",
    author="Your Name",
    version=version,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)