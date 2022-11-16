import sys

sys.stderr.write(
    """
===============================
Unsupported installation method
===============================
app-model does not support installation with `python setup.py install`.
Please use `python -m pip install .` instead.
"""
)
sys.exit(1)


# The below code will never execute, however GitHub is particularly
# picky about where it finds Python packaging metadata.
# See: https://github.com/github/feedback/discussions/6456
#
# To be removed once GitHub catches up.

setup(  # noqa: F821
    name="app-model",
    install_requires=[
        "psygnal>=0.3.4",
        "pydantic>=1.8",
        "in-n-out>=0.1.5",
        "typing_extensions",
    ],
)
