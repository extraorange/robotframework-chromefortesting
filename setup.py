from setuptools import setup, find_packages

setup(
    name='robotframework-chromefortesting',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        requests,
        robotframework
    ],
    entry_points={
        'console_scripts': [

        ],
    },
)