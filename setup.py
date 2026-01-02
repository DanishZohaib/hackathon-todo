from setuptools import setup, find_packages

setup(
    name="todo-cli-app",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'todo-cli=src.cli.main:main',
        ],
    },
    install_requires=[],
    author="Todo App Team",
    description="A CLI-based Todo application for Phase I",
    python_requires='>=3.11',
)