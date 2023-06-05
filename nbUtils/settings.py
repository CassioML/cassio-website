"""
Settings for the (mostly automated) colabification of notebooks
"""

import os
import json

from filesystem import (
    joinFilePath,
)

from nbmanipulate import (
    # findNbTitle,
    # replaceNbCodeLines,
    cleanNb,
)

# (old_part_of_line, full_new_line_or_None)
# None means simply make the line disappear.
codeLineReplacements = [
    (
        'from cqlsession import',
        '# creation of the DB connection',
    ),
    (
        'import suggestLLMProvider',
        '# creation of the LLM resources'
    ),
    (
        '= suggestLLMProvider',
        None,
    ),
    (
        'Alternatively set llmProvider',
        None,
    ),
    (
        "cqlMode = 'astra_db' # 'astra_db'/'local'",
        "cqlMode = 'astra_db'",
    )
]

# NOTE: currently you HAVE to mirror these changes
# to a list in overrides/main.html (*) to suppress
# the 'open in colab' button!
#       (*) note: slightly different way to express the path, check it there.
suppressColabify = [
    'docs/frameworks/langchain/prompt-templates-feast.ipynb',
    'docs/frameworks/dir1/dir2/another-notebook-not-colabified.ipynb', 
]

# SEQUENCES OF COLAB-SPECIFIC CELLS
# Default:
defaultColabCellSequences = [
    'seq_title',
    'seq_colab_setup_preamble',
    'seq_colab_dependency_setup',
    'seq_colab_setup',
]
# Per-notebook overrides:
perNotebookColabCellSequences = {
    'docs/frameworks/langchain/chat-prompt-templates.ipynb': (
        defaultColabCellSequences + [
            'colab_setup_provision_db',
        ]
    ),
    'docs/frameworks/langchain/prompt-templates-basic.ipynb': (
        defaultColabCellSequences + [
            'colab_setup_provision_db',
        ]
    ),
    'docs/frameworks/langchain/prompt-templates-partialing.ipynb': (
        defaultColabCellSequences + [
            'colab_setup_provision_db',
        ]
    ),
}
# Cell sequence generators, and their mapping, are defined here:
#
baseDir = os.path.abspath(os.path.dirname(__file__))

def loadAndStripCells(jsonTitle):
    filePath = os.path.join(baseDir, 'colab_snippets', jsonTitle)
    cells = cleanNb(
        json.load(open(filePath)),
        options={
            'stripCellIds': True,
            'stripStdoutOutput': True,
        }
    )['cells']
    return cells


def colabSetupPreambleCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripCells('colab_setup_preamble.json')


def colabSetupCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripCells('colab_setup.json')


def colabSetupProvisionDBCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripCells('colab_setup_provision_db.json')


def prepareTitleCells(pathList, fileTitle, nbTree, **kwargs):
    title = kwargs.get('title')
    if title is None:
        return []
    else:
        return [{
            "cell_type": "markdown",
            # "id": "84094469",
            "metadata": {},
            "source": [
                f"# {title}"
            ]
        }]


dependencyInstallerLineClosing = ' \\\n'
def prepareDependencyCells(pathList, fileTitle, nbTree, **kwargs):
    reqFiles = [
        f
        for f in os.listdir(os.path.join(*pathList))
        if len(f) > 3
        if f.startswith('requirements')
        if f[-4:] == '.txt'
    ]
    if reqFiles:
        reqFileTitle = reqFiles[0]
        reqFilePath = joinFilePath(pathList, reqFileTitle)
        dependencies = [
            line
            for line in (
                _line.strip()
                for _line in open(reqFilePath).readlines()
            )
            if len(line) > 0 and line[0] != '#'
        ]
        if dependencies:
            numDeps = len(dependencies)
            return [{
                "cell_type": "code",
                "execution_count": None,
                "id": "2953d95b",
                "metadata": {},
                "outputs": [],
                "source": [
                    "# install required dependencies\n",
                    "! pip install \\\n",
                ] + [
                    f"    \"{depline}\"{'' if deplinei+1 == numDeps else dependencyInstallerLineClosing}"
                    for deplinei, depline in enumerate(dependencies)
                ]
            }]
        else:
            return []
    else:
        return []


cellSequenceCreatorMap = {
    'seq_title':                   prepareTitleCells,
    'seq_colab_setup_preamble':    colabSetupPreambleCells,
    'seq_colab_dependency_setup':  prepareDependencyCells,
    'seq_colab_setup':             colabSetupCells,
    'colab_setup_provision_db':    colabSetupProvisionDBCells,
}