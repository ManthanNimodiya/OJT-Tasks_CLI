from setuptools import setup

setup(
    name="ojt-task-cli",
    version="0.0.7",
    packages=["ojt_task_cli"],
    package_dir={"ojt_task_cli": "src"},
    entry_points={
        "console_scripts": [
            "task-cli=ojt_task_cli.cli:main",
        ],
    },
    install_requires=[],
    author="Manthan Nimodiya",
    description="A command-line interface for managing tasks with projects and priorities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ManthanNimodiya/OJT-Tasks_CLI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
