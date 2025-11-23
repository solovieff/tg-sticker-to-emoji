"""Setup configuration for sticker-to-emoji package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8").splitlines()
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="tg-sticker-to-emoji",
    version="1.1.0",
    author="Telegram Sticker Converter Contributors",
    description="Convert Telegram sticker packs to custom emoji packs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tg-sticker-to-emoji",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/tg-sticker-to-emoji/issues",
        "Documentation": "https://github.com/yourusername/tg-sticker-to-emoji#readme",
        "Source Code": "https://github.com/yourusername/tg-sticker-to-emoji",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sticker-to-emoji=sticker_to_emoji.converter:main",
        ],
    },
    keywords="telegram sticker emoji converter tgs lottie",
    include_package_data=True,
)
