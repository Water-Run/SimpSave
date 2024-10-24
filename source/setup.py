from setuptools import setup, find_packages

setup(
    name='simpsave',
    version='0.13',
    author='WaterRun',
    author_email='linzhangrun49@gmail.com',
    url='https://github.com/Water-Run/SimpSave',
    description='A lightweight Python library for simple persistent storage using .ini files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
