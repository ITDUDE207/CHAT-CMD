from setuptools import setup

setup(
    name="chatapp",
    version="1.0.0",
    py_modules=["legacy.main"],
    entry_points={"console_scripts": ["chatapp=legacy.main:main"]},
)
