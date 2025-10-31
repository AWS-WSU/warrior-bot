"""Setup configuration for Warrior Bot."""

from setuptools import find_packages, setup

setup(
    name="warrior-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "warrior-bot=warrior_bot.cli:cli",
        ],
    },
    python_requires=">=3.10",
)
