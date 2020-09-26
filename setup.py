from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='infrastructure',
    version='0.0.23',
    author='Aaron Mamparo',
    author_email='aaronmamparo@gmail.com',
    description='Shared infrastructure helpers for the Yahoo Fantasy Football project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yahoo-fantasy-football/infrastructure',
    package_dir={
        '': 'src'
    },
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'build = infrastructure.build_lambda_deployment_package:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>= 3.7'
)
