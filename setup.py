from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='robotframework-chromefortesting',
    version='0.9.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests",
        "robotframework"
    ],
    url='https://github.com/extraorange/robotframework-chromefortesting',
    author='extraorange',
    author_email='extraorangeio@pm.me',
    description='The only extension for seamless setup of Chrome for Testing (CfT) in and within Robot Framework.',
    license='GNU General Public License v3.0',
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Framework :: Robot Framework :: Library',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Testing :: Acceptance',
    'Topic :: Software Development :: Testing :: BDD'
    ]
)