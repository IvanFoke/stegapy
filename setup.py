import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stegapy",
    version="0.0.1",
    author="Ivan Foke",
    author_email="ivan.foke@gmail.com",
    description="A simple steganography project with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IvanFoke/stegapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# python setup.py sdist bdist_wheel
