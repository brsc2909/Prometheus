from setuptools import setup

setup(
    entry_points={
        "console_scripts": [
            "prometheus=prometheus.__main__:main"
        ]
    },
)
