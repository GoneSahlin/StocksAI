from setuptools import setup, find_packages

setup(
    name='stocksai',
    version='0.0.0',
    packages=find_packages(include=['collector.price_historical']),
    install_requires=[
        'selenium',
        'requests',
        'polars',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
