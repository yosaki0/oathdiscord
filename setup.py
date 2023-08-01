from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fp:
    long_description = "\n" + fp.read()

VERSION = "0.0.1"
DESCRIPTION = ""
LONG_DESCRIPTION = ""

setup(
    name="discordOath2",
    version=VERSION,
    author="yosaki0 (0x4eb)",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["discord.py", "aiofiles", "aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ]
) 