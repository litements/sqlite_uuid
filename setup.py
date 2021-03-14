from setuptools import setup, Extension  # type: ignore

# read the contents of README
from os import path
import os


library_dirs = []
include_dirs = []


if os.getenv("CUSTOM_INCLUDE", None) is not None:
    include_dirs += [os.getenv("CUSTOM_INCLUDE")]

if os.getenv("CUSTOM_LIBRARIES", None) is not None:
    library_dirs += [os.getenv("CUSTOM_LIBRARIES")]


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

sqlite_uuid_ext = Extension(
    "sqlite_uuid_ext",
    sources=["uuid.c"],
    library_dirs=library_dirs,
    include_dirs=include_dirs,
)

setup(
    name="sqlite-uuid",
    version="0.9.1",
    author="Ricardo Ander-Egg Aguilar",
    author_email="rsubacc@gmail.com",
    description="Loadable uuid extension for sqlite",
    py_modules=["sqlite_uuid"],
    ext_modules=[sqlite_uuid_ext],
    url="https://github.com/litements/sqlite_uuid",
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=["wheel"],
    python_requires=">=3.6",
)
