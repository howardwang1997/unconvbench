from setuptools import setup, find_packages
import os

from unconvbench.constant import VERSION

with open('requirements.txt') as f:
    requirements = f.read().split('\n')
if requirements[-1] == '':
    requirements.pop(-1)

setup(
    name="unconvbench",
    version=VERSION,
    description="Benchmark for unconventional crystal materials",
    long_description="Benchmark for unconventional crystal materials. Including 2D materials, MOFs and defected crystals. "
    "https://github.com/howardwang1997/unconvbench",
    url="https://github.com/howardwang1997/unconvbench",
    author="Howard WANG Hongyi",
    author_email="howardwang1997@gmail.com",
    license="MIT license",
    packages=find_packages(include=["unconvbench*"], exclude=["*tests"]),
    package_data={"matbench": ["*.json"]},
    install_requires=requirements,
)
