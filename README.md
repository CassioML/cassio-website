# CassIO, website

## Local run (with auto-reload)

Create a virtualenv e.g. `cassio-website-3.10`

`pip install -r requirements.txt`


## Run MkDocs 
Serve with:

```
mkdocs serve
```

Build with
```
mkdocs build
````

## Notebook cleaning

For cleanliness, please run this after closing the notebooks and before committing:

```
find -name "*.ipynb" | grep -v ".ipynb_checkpoints" | grep -v ".colab" | xargs ./nbUtils/notebook_cleaner.py
```

This simply strips `stderr` noise (and possibly other stuff that gets in the way) from notebooks.
