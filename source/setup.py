from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simpsave',
    version='4.0',
    install_requires=['PyYAML'],
    packages=find_packages(),
    author='WaterRun',
    author_email='2263633954@qq.com',
    description='A lightweight Python library for persisting basic variables using .yml files. Simple, fast, and ideal for small-scale data storage.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Water-Run/SimpSave',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.10',
)