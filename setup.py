#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version('cyclosible')


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()


setup(
    name='cyclosible',
    version=version,
    url='http://www.cycloid.io/cyclosible',
    license='Apache',
    description='Cyclosible is a web-api to manage ansible',
    author='Cycloid',
    author_email='julien.syx@cycloid.io',  # SEE NOTE BELOW (*)
    packages=get_packages('cyclosible'),
    package_data=get_package_data('cyclosible'),
    install_requires=[
        'djangorestframework',
        'django>=1.8',
        'mysqlclient',
        'django-rest-swagger',
        'colorlog',
        'ansible',
        'PyYAML',
        'django-celery',
        'markdown',
        'django-guardian',
        'django-filter',
        'boto',
        'redis',
        'django-websocket-redis',
        'stevedore'
    ],
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    entry_points={
        'console_scripts': [
            'cyclosible = cyclosible.manage:main',
        ],
        'cyclosible.plugins.storage': [
            's3 = cyclosible.playbook.plugins.storage.s3:S3Plugin',
        ],
        'cyclosible.plugins.vault': [
            'password = cyclosible.playbook.plugins.vault.password:PasswordPlugin',
            'file = cyclosible.playbook.plugins.vault.file:FilePlugin',
            'hashicorp = cyclosible.playbook.plugins.vault.hashicorp:HashicorpPlugin',
        ],
    },
)

# (*) Please direct queries to the discussion group, rather than to us directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
