from setuptools import setup, find_packages

setup(
    name="recontrack",
    version="0.1.0",
    description="CLI tool and library to extract tracking codes from websites",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "recontrack=scripts.cli:cli",
        ],
    },
    python_requires=">=3.6",
)
