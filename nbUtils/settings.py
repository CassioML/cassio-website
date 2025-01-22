"""
Settings for the (mostly automated) colabification of notebooks
"""

import os
import json

from filesystem import (
    joinFilePath,
)

from nbmanipulate import (
    # findNbHeadings,
    # replaceNbCodeLines,
    cleanNb,
)

# (old_part_of_line, full_new_line_or_None)
# None means simply make the line disappear.
# Depending on the framework, different replacement rules apply
codeLineReplacements0 = [
]

# this maps dot-joined pathLists to replacements with partial pathlist matching
# i.e. keys = dot-joined pathlists, values = lists of 2-tuples for replacement.
# (You can also have notebook-specific prescriptions)
# NOTE: if you specify rules that walk on each other, your're on your own.
codeLineReplacementsMap = {
    "": codeLineReplacements0,
}

# path -> (filetitles, replacement_pairs) -> 
dependencyReplacementsMap = {}

_dependencyReplacementsUnfoldedMap = {
    f"{path}/{ftitle}": dict(reppairs)
    for path, (ftitles, reppairs) in dependencyReplacementsMap.items()
    for ftitle in ftitles
}

# SEQUENCES OF COLAB-SPECIFIC CLOSING CELLS (just a cta)
defaultColabCellClosingSequences = [
    'seq_colab_closing_cta',
]

# Per-notebook overrides:
perNotebookColabCellSequences = {}
perNotebookColabCellClosingSequences = {}
# Cell sequence generators, and their mapping, are defined here:
#
baseDir = os.path.abspath(os.path.dirname(__file__))

def loadAndStripColabSnippetCells(jsonTitle):
    filePath = os.path.join(baseDir, 'colab_snippets', jsonTitle)
    cells = cleanNb(
        json.load(open(filePath)),
        options={
            'stripCellIds': True,
            'stripStdoutOutput': True,
        }
    )['cells']
    return cells

def colabClosingCTA(pathList, fileTitle, nbTree, **kwargs):
    # e.g. "https://cassio.org/frameworks/examples/quickstart/"
    nbUrl = kwargs['nbUrl']
    cells = loadAndStripColabSnippetCells('colab_closing_cta.json')
    return [
        {
            k: (
                v
                if k != 'source'
                else [
                    lin
                        .replace('__NOTEBOOK_URL__', nbUrl)
                    for lin in v
                ]
            )
            for k, v in c.items()
        }
        for c in cells
    ]

def prepareTitleCells(pathList, fileTitle, nbTree, **kwargs):
    headings = kwargs.get('headings', {})
    title = headings.get('title')
    subtitle = headings.get('subtitle')
    if title is None:
        return []
    else:
        _mdlines = [
            r
            for r in [
                f"# {title}",
                "" if subtitle is not None else None,
                subtitle,
            ]
            if r is not None
        ]
        mdlines = [
            r if i+1 == len(_mdlines) else f'{r}\n'
            for i, r in enumerate(_mdlines)
        ]
        return [{
            "cell_type": "markdown",
            # "id": "84094469",
            "metadata": {},
            "source": mdlines,
        }]

cellSequenceCreatorMap = {
    'seq_colab_closing_cta':                colabClosingCTA,
}
