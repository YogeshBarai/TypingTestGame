""" Setup script for TypingTestGame """

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="TypingTestGame",
    version="1.0.7",
    author="Yogesh Barai",
    author_email="yogesh.barai@gmail.com",
    description="A command line tool to improve typing speed",
    url="https://github.com/YogeshBarai",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={"TypingTestGame": ["TypingTest_DB.db"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        'console_scripts': ['TypingTestGame=TypingTestGame.TypingTestApp:TypingTestApp']
    }
)