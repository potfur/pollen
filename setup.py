from distutils.core import setup

from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='pollen',
    packages=find_packages(exclude=[]),
    version='0.1.0',
    description='Dependency injection container.',
    long_description=readme,
    author='Michal Wachowski',
    author_email='wachowski.michal@gmail.com',
    url='https://github.com/potfur/pollen',
    download_url='https://github.com/potfur/pollen/archive/0.1.0.tar.gz',
    keywords=[
        'dependency injection',
        'container',
        'inversion of control',
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
        'flake8'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)
