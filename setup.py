from setuptools import setup, find_namespace_packages

setup(
    name="gestion-quittances",
    version="0.1",
    packages=find_namespace_packages(include=['src*']),
    package_dir={'': '.'},
    install_requires=[
        'click>=8.1.7',
        'reportlab>=4.1.0',
    ],
    entry_points={
        'console_scripts': [
            'gestion-quittances=src.interface.cli:cli',
        ],
    },
) 