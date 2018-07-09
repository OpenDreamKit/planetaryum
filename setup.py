from setuptools import setup, find_packages

setup(
    name='planetaryum',
    version='0.1.0',
    description='A Jupyter notebook gallery framework',
    url='https://github.com/opendreamkit/planetaryum',
    author='Luca De Feo',
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],
    keywords='jupyter web',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['jupyter', 'docopt'],
    entry_points={
        'console_scripts': [
            'planetaryum = planetaryum.cli:main',
            ],
        },
)
