
from distutils.core import setup
from setuptools import setup, find_packages
from codecs import open
from os import path


setup(
    name='cofffee',         
    version='1.1.0.0',
    description='A complete python visualizer, using an intuitive, consistent, and approachable, OOP framework.',
    url='https://github.com/Brian-Masse/Coffee',

    author='Brian J. Masse',
    author_email='brianm25it@gmail.com',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',

    packages=["cofffee"],
    include_package_data=True,
    install_requires=[         
        'numpy',
        'pandas',
        'pygame',
        'matplotlib',
        'openpyxl'
    ],
    
    # download_url='https://github.com/Brian-Masse/Coffee/archive/refs/tags/v1.0.07.tar.gz',
    keywords=['Visualization', 'python', 'pandas', 'rendering', 'data', 'customizable',
              'powerful', 'intuitive'],   # Keywords that define your package best
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
    
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
