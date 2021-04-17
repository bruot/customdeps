# How to build a new PyPi package for CustomDeps

## Quick steps

Install the following packages:

```
pip install build twine
```

In the project root directory, execute:

```
python -m build
```

This creates .whl and .tar.gz files in the dist directory.

Upload the files to PyPi with twine:

```
python -m twine upload --repository testpypi dist/*
```


## Reference

https://packaging.python.org/tutorials/packaging-projects/
