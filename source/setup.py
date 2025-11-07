"""
@file setup.py
@author WaterRun
@version 10
@date 2025-11-07
@description Setup configuration for SimpSave
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simpsave',
    version='10.0.0',
    packages=find_packages(),
    author='WaterRun',
    author_email='2263633954@qq.com',
    description='A lightweight Python library for persisting basic variables with multiple storage engines. Simple, fast, and ideal for small-scale data storage.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Water-Run/SimpSave',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.10',
    install_requires=[
    ],
    extras_require={
        'yml': ['PyYAML>=6.0'],
        'toml': [
            'tomli>=2.0.0; python_version<"3.11"',
            'tomli-w>=1.0.0',
        ],
        'redis': ['redis>=4.0.0'],
        
        'clean': [],  
        'basic': ['PyYAML>=6.0', 'tomli>=2.0.0; python_version<"3.11"', 'tomli-w>=1.0.0'],
        'sqlite': [], 
        'full': [
            'PyYAML>=6.0',
            'tomli>=2.0.0; python_version<"3.11"',
            'tomli-w>=1.0.0',
            'redis>=4.0.0',
        ],
    },
)