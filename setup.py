import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", encoding="utf-8") as f:
    requires = f.read().split()

setuptools.setup(
    name="pyrothrottle",
    version="0.1.1",
    author="asteroid_den",
    author_email="denbartolomee@gmail.com",
    description="Throttle and debounce add-ons for Pyrogram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/asteroidden/pyrothrottle/",
    packages = ['pyrothrottle'],
    license = 'MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = requires,
    python_requires = '>=3.6',
)
