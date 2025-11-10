"""
@file setup.py
@author WaterRun
@version 10.1
@date 2025-11-10
@description Setup configuration for SimpSave
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simpsave',
    version='10.1.0',
    packages=find_packages(where='.'),  
    package_dir={'': '.'},              
    author='WaterRun',
    author_email='2263633954@qq.com',
    description=(
        'A lightweight Python library for persisting basic variables '
        'with multiple storage engines. Ideal for small-scale data storage '
        'with "read-and-use" capability.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Water-Run/SimpSave',
    project_urls={
        'Bug Tracker': 'https://github.com/Water-Run/SimpSave/issues',
        'Documentation': 'https://github.com/Water-Run/SimpSave',
        'Source Code': 'https://github.com/Water-Run/SimpSave',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
        'Development Status :: 4 - Beta',
    ],
    keywords='persistence, storage, key-value, database, lightweight, simple',
    python_requires='>=3.10',
    install_requires=[],
    extras_require={
        'xml': [],
        'ini': [],
        'json': [],
        'yml': ['PyYAML>=6.0'],
        'toml': [
            'tomli>=2.0.0; python_version<"3.11"',
            'tomli-w>=1.0.0',
        ],
        'sqlite': [],
        'clean': [],
        'basic': [
            'PyYAML>=6.0',
            'tomli>=2.0.0; python_version<"3.11"',
            'tomli-w>=1.0.0',
        ],
        'full': [
            'PyYAML>=6.0',
            'tomli>=2.0.0; python_version<"3.11"',
            'tomli-w>=1.0.0',
        ],
    },
    license='MIT',
    zip_safe=False,
)