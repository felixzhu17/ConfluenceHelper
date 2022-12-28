from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="confluence-generator",
    version="0.0.10",
    license="MIT",
    author="Felix Zhu",
    author_email="zhu.felix@outlook.com",
    description="Confluence Generator",
    long_description=long_description,
    packages=find_packages(),
    setup_requires=["setuptools_scm"],
    url="https://github.com/felixzhu17/ConfluenceGenerator",
    install_requires=[
        "atlassian-python-api",
        "requests",
        "jinja2",
        "pandas",
        "plotly",
        "kaleido",
    ],
)
