"""Setup module."""
import setuptools

with open("README.md", "r", encoding="utf-8") as f_file:
    long_description = f_file.read()


setuptools.setup(
    name="juungle",
    version="0.5",
    author="Eduardo Elias",
    author_email="camponez@gmail.com",
    description="Juungle python package for juungle.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Juungle/juungle-python",
    project_urls={
        "Bug Tracker": "https://github.com/Juungle/juungle-python/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
