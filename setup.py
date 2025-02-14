from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_name:str) -> List[str]:
    with open(file_name) as f:
        requirements = f.read().splitlines()
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        return requirements

setup(
    name='mlproject',
    version='0.0.1',
    packages=find_packages(),
    author='Kevin Kam',
    description='Ml Ops Project',
    install_requires=get_requirements('requirements.txt')
)

# if __name__ == '__main__':
#     print(get_requirements('requirements.txt'))