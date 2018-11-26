from setuptools import setup, find_packages

__doc__ = open('README.md').read()

VERSION = '0.0.1'
REQUIREMENTS = open("requirements.txt").read().splitlines()
AUTHOR = "Brendan Scullion"
EMAIL = "brsc2909@gmail.com"
SUMMARY = ""
URL = ""
DESCRIPTION = __doc__

setup(
    name="prometheus",
    packages=find_packages(),
    include_package_data=True,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    description=SUMMARY,
    setup_requires=[],
    tests_require=[],
    zip_safe=False,
    scripts=[],
    entry_points={
        "console_scripts": [
            "prometheus=prometheus.__main__:main"
        ]
    },
    cmdclass={}
)
