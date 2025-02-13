# CassIO, website

> [!WARNING]
> **Discontinued as a public library**
> Starting March 2024, efforts to improve CassIO are put on hold. The library, while still used as is within other projects and receiving occasional updates, is now essentially **discontinued** for use by the general public.


## Local run (with auto-reload)

Create a virtualenv e.g. `cassio-website-3.10`

`pip install -r requirements.txt`


## Run MkDocs 
Serve with:

```bash
mkdocs serve
```

Build with

```bash
mkdocs build
````

## Notebook cleaning

For cleanliness, please run this after closing the notebooks and before committing:

```bash
find -name "*.ipynb" | grep -v ".ipynb_checkpoints" | grep -v ".colab" | xargs ./nbUtils/notebook_cleaner.py
```

This simply strips `stderr` noise (and possibly other stuff that gets in the way)
and cleans the cell numbering in the notebooks.


## Colab generation

Run this after the above cleaning:

```bash
./nbUtils/notebook_colabifier.py
```

## Branch model

Do not push to `main`. The `main` branch should only receive merges from `eng`.

Push to `eng` directly only in quick-fix circumstances. Preferrably work on a feature branch and then submit a PR to `eng`.
