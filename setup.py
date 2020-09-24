from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

package_name = 'infrastructure'

setup(
    name=package_name,
    version='0.0.1',
    author='Aaron Mamparo',
    author_email='aaronmamparo@gmail.com',
    description='Shared infrastructure helpers for the Yahoo Fantasy Football project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yahoo-fantasy-football/infrastructure',
    packages=find_packages('src/%s' % package_name),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>= 3.7'
)
