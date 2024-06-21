from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name="your_project",
    ext_modules=cythonize(["your_module.pyx"]),
    setup_requires=["Cython>=0.29"],
)
