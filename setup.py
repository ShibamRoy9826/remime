from setuptools import find_packages, setup
from shutil import copy
from pathlib import Path
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        source_dir = Path(__file__).parent / "assets"  # Adjust based on your structure
        target_dir = Path.home() / ".config" / "remime"
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in source_dir.iterdir():
            if file.is_file():
                copy(file, target_dir)
                print(f"Copied {file} to {target_dir}")

def readRequirements():
    a = []
    with open("requirements.txt") as f:
        for line in f.readlines():
            if not line.startswith("#"):
                a.append(line.strip())
    return a


setup(
    name="remime",
    version="0.1.0",
    description="An easy and efficient way to manage your time using the terminal!",
    author="Shibam Roy",
    author_email="royshibam9826@gmail.com",
    url="https://github.com/ShibamRoy9826/remime",
    packages=find_packages(),  
    install_requires=readRequirements(),
    entry_points={
        "console_scripts": [
            "remime = remime.remime:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)
