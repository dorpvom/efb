from setuptools import find_packages, setup
from pathlib import Path

VERSION = '0.0'

setup(
    name='efficient_back_up',
    version=VERSION,
    description='Ideas to allow backing up data more nicely.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Johannes vom Dorp',
    author_email='dorp@cs.uni-bonn.de',
    python_requires='>=3.6.0',
    packages=find_packages(),
    install_requires=[
        'prompt_toolkit',
        'git+https://github.com/fkie-cad/common_helper_process.git'
    ],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
