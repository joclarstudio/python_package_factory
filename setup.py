from setuptools import setup, find_packages

try:
    setup(
        packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    )
except Exception:
    print(
        "\n\nAn error occurred while building the project, "
        "please ensure you have the most updated version of setuptools, "
        "setuptools_scm and wheel with:\n"
        "\tpip install -U setuptools setuptools_scm wheel\n\n"
    )
    raise
