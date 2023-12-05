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
        "database_mode = \"cassandra\"  # \"cassandra\" / \"astra_db\"",
        "database_mode = \"astra_db\"  # only \"astra_db\" supported on Colab",
    ),
    (
        "# Ensure loading of database credentials into environment variables:",
        "# Getting ready to initialize the DB connection globally ...",
    ),
    (
        "from dotenv import load_dotenv",
        None,
    ),
    (
        "load_dotenv(\"../../../.env\")",
        None,
    ),
    (
        "from cqlsession import getCassandraCQLSession, getCassandraCQLKeyspace",
        "    # Cassandra not supported on Colab - please define your own getCassandraCQLSession/getCassandraCQLKeyspace",
    ),
]
codeLineReplacementsLangChain = []

# this maps dot-joined pathLists to replacements with partial pathlist matching
# i.e. keys = dot-joined pathlists, values = lists of 2-tuples for replacement.
# (You can also have notebook-specific prescriptions)
# NOTE: if you specify rules that walk on each other, your're on your own.
codeLineReplacementsMap = {
    "": codeLineReplacements0,
    # "docs/frameworks/langchain": codeLineReplacementsLangChain,
}

# NOTE: currently you HAVE to mirror these changes
# to a list in overrides/main.html (*) to suppress
# the 'open in colab' button!
#       (*) note: slightly different way to express the path, check it there.
suppressColabify = [
    'docs/frameworks/langchain/prompt-templates-feast.ipynb',
    'docs/frameworks/dir1/dir2/another-notebook-not-colabified.ipynb', 
]

# SEQUENCES OF COLAB-SPECIFIC CLOSING CELLS (just a cta)
defaultColabCellClosingSequences = [
    'seq_colab_closing_cta',
]

# SEQUENCES OF COLAB-SPECIFIC CELLS (no writeDB, no amontillado)
defaultColabCellSequences = [
    'seq_title',
    'seq_colab_setup_preamble',
    'seq_colab_dependency_setup',
    'seq_colab_setup_db',
    'seq_colab_setup_llm',
    'seq_colab_setup_closing',
]
# variants
writeDB_noLLM_cellSequences = [
    'seq_title',
    'seq_colab_setup_preamble_no_llm',
    'seq_colab_dependency_setup',
    'seq_colab_setup_db',
    'seq_colab_setup_provision_db',
    'seq_colab_setup_closing',
]
noDB_noLLM_cellSequences = [
    'seq_title',
    'seq_colab_setup_preamble_no_llm',
    'seq_colab_dependency_setup',
    'seq_colab_setup_closing',
]
noLLM_cellSequences = [
    'seq_title',
    'seq_colab_setup_preamble_no_llm',
    'seq_colab_dependency_setup',
    'seq_colab_setup_db',
    'seq_colab_setup_closing',
]

noLLM_GPU_cellSequences = [
    'seq_title',
    'seq_colab_setup_preamble_no_llm',
    'seq_colab_setup_switch_to_gpu',
    'seq_colab_dependency_setup',
    'seq_colab_setup_db',
    'seq_colab_setup_closing',
]

# Per-notebook overrides:
perNotebookColabCellSequences = {
    'docs/frameworks/langchain/chat-prompt-templates.ipynb': writeDB_noLLM_cellSequences,
    'docs/frameworks/langchain/prompt-templates-basic.ipynb': writeDB_noLLM_cellSequences,
    'docs/frameworks/langchain/prompt-templates-partialing.ipynb': writeDB_noLLM_cellSequences,
    'docs/frameworks/langchain/qa-basic.ipynb': [
        'seq_title',
        'seq_colab_setup_preamble',
        'seq_colab_dependency_setup',
        'seq_colab_setup_db',
        'seq_colab_setup_llm',
        'seq_colab_setup_download_txt_stories',
            'seq_colab_setup_closing',
    ],
    'docs/frameworks/langchain/qa-vector-metadata.ipynb': [
        'seq_title',
        'seq_colab_setup_preamble',
        'seq_colab_dependency_setup',
        'seq_colab_setup_db',
        'seq_colab_setup_llm',
        'seq_colab_setup_download_txt_stories',
            'seq_colab_setup_closing',
    ],
    'docs/frameworks/langchain/memory-basic.ipynb': noLLM_cellSequences,
    'docs/frameworks/langchain/prompt-templates-engine.ipynb': noDB_noLLM_cellSequences,
    #
    'docs/frameworks/direct_cassio/sound_similarity_vectors.ipynb': noLLM_GPU_cellSequences,
    'docs/frameworks/direct_cassio/image_similarity_vectors.ipynb': noLLM_GPU_cellSequences,
    #
    'docs/frameworks/llamaindex/vector-quickstart.ipynb': [
        'seq_title',
        'seq_colab_setup_preamble',
        'seq_colab_dependency_setup',
        'seq_colab_setup_db',
        'seq_colab_setup_llm',
        'seq_colab_setup_download_llama_pdfs',
        'seq_colab_setup_closing',
    ],
}
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


def colabSetupSuggestGPUSwitchCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_suggest_gpu.json')


def colabSetupPreambleNoLLMCells(pathList, fileTitle, nbTree, **kwargs):
    nbUrl = kwargs['nbUrl']
    cells = loadAndStripColabSnippetCells('colab_setup_preamble_no_llm.json')
    return [
        {
            k: (
                v
                if k != 'source'
                else [
                    lin.replace('__NOTEBOOK_URL__', nbUrl)
                    for lin in v
                ]
            )
            for k, v in c.items()
        }
        for c in cells
    ]


def colabSetupDBCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_db.json')


def colabSetupLLMCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_llm.json')


def colabSetupProvisionDBCells(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_provision_db.json')


def colabSetupClosing(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_closing.json')


def colabSetupDownloadTxtStories(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_download_langchaintxtstories.json')


def colabSetupDownloadLlamaPDFs(pathList, fileTitle, nbTree, **kwargs):
    return loadAndStripColabSnippetCells('colab_setup_fetch_llama_pdfs.json')


def colabSetupPreambleCells(pathList, fileTitle, nbTree, **kwargs):
    nbUrl = kwargs['nbUrl']
    cells = loadAndStripColabSnippetCells('colab_setup_preamble.json')
    return [
        {
            k: (
                v
                if k != 'source'
                else [
                    lin.replace('__NOTEBOOK_URL__', nbUrl)
                    for lin in v
                ]
            )
            for k, v in c.items()
        }
        for c in cells
    ]


def colabClosingCTA(pathList, fileTitle, nbTree, **kwargs):
    # e.g. "https://cassio.org/frameworks/langchain/memory-vectorstore/"
    nbUrl = kwargs['nbUrl']
    # e.g. "https://cassio.org/frameworks/langchain/about/"
    fwUrl = '/'.join(nbUrl.split('/')[:-2] + ['about', ''])
    cells = loadAndStripColabSnippetCells('colab_closing_cta.json')
    return [
        {
            k: (
                v
                if k != 'source'
                else [
                    lin
                        .replace('__NOTEBOOK_URL__', nbUrl)
                        .replace('__FRAMEWORK_URL__', fwUrl)
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


dependencyInstallerLineClosing = ' \\\n'
lastDependencyInstallerLineClosing = ' \n'
postReqInstallCell = {
    "cell_type": "markdown",
    "id": "222f44ff",
    "metadata": {},
    "source": [
        (
            "⚠️ **Do not mind a \"Your session crashed...\" "
            "message you may see.**\n"
        ),
        "\n",
        (
            "It was us, making sure your kernel restarts with all the correct "
            "dependency versions. _You can now proceed with the notebook._"
        )
    ]
}
def colabSetupPrepareDependencyCells(pathList, fileTitle, nbTree, **kwargs):
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
            return [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "id": "2953d95b",
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# install required dependencies\n",
                        # "! pip install -q --progress-bar off --upgrade pip\n",
                        "! pip install -q --progress-bar off \\\n",
                    ] + [
                        f"    \"{depline}\"{lastDependencyInstallerLineClosing if deplinei+1 == numDeps else dependencyInstallerLineClosing}"
                        for deplinei, depline in enumerate(dependencies)
                    ] + [
                        "exit()",
                    ]
                },
                postReqInstallCell
            ]
        else:
            return []
    else:
        return []


cellSequenceCreatorMap = {
    'seq_title':                            prepareTitleCells,
    'seq_colab_setup_switch_to_gpu':        colabSetupSuggestGPUSwitchCells,
    'seq_colab_dependency_setup':           colabSetupPrepareDependencyCells,
    'seq_colab_setup_llm':                  colabSetupLLMCells,
    'seq_colab_setup_provision_db':         colabSetupProvisionDBCells,
    'seq_colab_setup_download_txt_stories': colabSetupDownloadTxtStories,
    'seq_colab_setup_download_llama_pdfs':  colabSetupDownloadLlamaPDFs,
    'seq_colab_setup_closing':              colabSetupClosing,
    'seq_colab_setup_preamble_no_llm':      colabSetupPreambleNoLLMCells,
    'seq_colab_setup_preamble':             colabSetupPreambleCells,
    'seq_colab_setup_db':                   colabSetupDBCells,
    'seq_colab_closing_cta':                colabClosingCTA,
}
