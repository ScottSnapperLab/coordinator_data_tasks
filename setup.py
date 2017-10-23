#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from pathlib import Path


def filter_req_paths(paths, func):
    """Return list of filtered libs."""
    if not isinstance(paths, list):
        raise ValueError("Paths must be a list of paths.")

    libs = set()
    junk = set(['\n'])
    for p in paths:
        with Path(p).open(mode='r') as reqs:
            lines = set([line for line in reqs if func(line)])
            libs.update(lines)

    return list(libs - junk)


def is_pipable(s):
    """Filter for pipable reqs."""
    if "# not_pipable" in s:
        return False
    elif s.startswith('#'):
        return False
    else:
        return True


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = filter_req_paths(paths=["requirements.txt",
                                       "requirements.pip.txt"], func=is_pipable)

setup_requirements = filter_req_paths(paths=["requirements.setup.txt"], func=is_pipable)

test_requirements = filter_req_paths(paths=["requirements.test.txt"], func=is_pipable)

setup(
    name='coordinator_data_tasks',
    version='0.0.2',
    description="A python-based command line utility to automate some of the most common data tasks faced by the Clinical Coordinators.",
    long_description=readme + '\n\n' + history,
    author="Gus Dunn",
    author_email='w.gus.dunn@gmail.com',
    url='https://github.com/xguse/coordinator_data_tasks',
    packages=find_packages(include=['coordinator_data_tasks']),
    entry_points={
        'console_scripts': [
            'data_tasks=coordinator_data_tasks.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='coordinator_data_tasks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
