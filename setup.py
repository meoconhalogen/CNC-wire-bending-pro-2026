"""
Setup configuration for CNC Wire Bending Pro 2026
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="cnc-wire-bending-pro-2026",
    version="2026.1.0",
    author="meoconhalogen",
    description="Professional DXF to G-code converter for CNC wire bending machines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meoconhalogen/CNC-wire-bending-pro-2026",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Topic :: Multimedia :: Graphics :: CAD",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cnc-wire-bending=src.main:main",
        ],
    },
)