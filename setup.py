"""Setup module."""
import setuptools

with open("README.md", "r", encoding="utf-8") as f_file:
    long_description = f_file.read()

extras = {
    "test": [
        "pytest >=2.7.3",
    ]
}


setuptools.setup(
    name="juungle",
    version="0.6.0",
    author="Eduardo Elias",
    author_email="camponez@gmail.com",
    description="Juungle python package for juungle.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="juungle.net api nfts",
    url="https://github.com/Juungle/juungle-python",
    project_urls={
        "Bug Tracker": "https://github.com/Juungle/juungle-python/issues",
        "Source Code": "https://github.com/Juungle/juungle-python",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    install_requires=[
        'requests'
    ],
    extras_require=extras,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
