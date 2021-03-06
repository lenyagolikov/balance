import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = 'app'

module = SourceFileLoader(
    module_name, os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(filename: str) -> list[str]:
    requirements = []
    with open(filename, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(
                f'{req.name}{extras}{req.specifier}'
            )
    return requirements


setup(
    name=module_name,
    version=module.__version__,
    author=module.__author__,
    email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    url='https://github.com/lenyagolikov/balance',
    long_description=open('README.md').read(),
    platforms='all',
    python_requires='>=3.10',
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            f'{module_name} = {module_name}.main:main',
            f'{module_name}-db = {module_name}.init_db:main',
        ]
    },
    include_package_data=True
)
