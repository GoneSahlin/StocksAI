from setuptools import setup, find_packages

setup(
    name='collector',
    version='0.0.0',
    packages=find_packages(include=['price_historical']),
    install_requires=[
        'selenium',
        'requests',
        'polars',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)