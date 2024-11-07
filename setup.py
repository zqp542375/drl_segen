from setuptools import setup, find_packages

import os

here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
def get_requirements():
    """
    Return requirements as list.
    Handles cases where git links are used.

    """
    with open(os.path.join(here, "requirements.txt")) as f:
        packages = []
        for line in f:
            line = line.strip()
            # let's also ignore empty lines and comments
            if not line or line.startswith("#"):
                continue
            if "https://" not in line:
                packages.append(line)
                continue

            rest, package_name = line.split("#egg=")[0], line.split("#egg=")[1]
            if "-e" in rest:
                rest = rest.split("-e")[1]
            package_name = package_name + "@" + rest
            packages.append(package_name)
    return packages


REQUIRED = get_requirements()
setup(
    name='segen',
    version='0.1.0',
    description='For training models with reinforcement learning',
    author='qpw',
    author_email='your.email@example.com',
    url='',  # Update with your repository URL
    packages=find_packages(exclude=["train_results", "tests"]),
    install_requires=REQUIRED,
    entry_points={
        'console_scripts': [
            'gen=segen.cli:main'  # Assuming you have a main() function in app.py
        ],
    },
)

