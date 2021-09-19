from setuptools import find_packages, setup

setup(
    name="pyconjp_domains",
    version="0.0.1",
    packages=find_packages(exclude=["tests.*", "tests"]),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Japanese",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    extras_require={
        "dev": ["black", "flake8", "isort", "pytest", "pytest-randomly"]
    },
    description="Domain objects for talks of PyCon JP 2021.",
    url="https://github.com/pyconjp/talks.domain.2021",
    author="nikkie",
    author_email="takuyafjp+develop@gmail.com",
    license="MIT license",
    test_suite="tests",
    zip_safe=False,
)
