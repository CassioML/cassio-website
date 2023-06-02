#!/bin/env python

import os
import sys
import json


from filesystem import (
    getColabifiedFileCoordinates,
    joinFilePath,
    joinDirs,
    mkDirP,
)

from nbmanipulate import (
    findNbTitle,
    replaceNbCodeLines,
    cleanNb,
)

from settings import codeLineReplacements, suppressColabify

# cell enrichments

dependencyInstallerLineClosing = ' \\\n'

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


colabSetupPreambleCells = loadAndStripCells('colab_setup_preamble.json')
colabSetupCells = loadAndStripCells('colab_setup.json')


def prepareTitleCells(title):
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


def prepareDependencyCells(pathList):
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


# enrichment-specific tools

def enrichNbTree(pathList, fileTitle, nbTree, **kwargs):
    # what cell sequences should be added?
    # TODO: here customization of enrichment
    cellSequences = [
        ('seq_title',                   prepareTitleCells(kwargs['title'])),
        ('seq_colab_setup_preamble',    colabSetupPreambleCells),
        ('seq_colab_setup',             prepareDependencyCells(pathList)),
        ('seq_colab_setup',             colabSetupCells),
    ]
    #
    return {
        k: (
            v
            if k != 'cells'
            else [
                cell
                for seq_id, seq_cells in cellSequences
                for cell in seq_cells
                # if seq_id ... (customization)
            ] + v
        )
        for k, v in nbTree.items()
    }


def colabifyNotebook(pathList, fileTitle):
    inputFile = joinFilePath(pathList, fileTitle)
    colabPathList, colabFileTitle = getColabifiedFileCoordinates(pathList, fileTitle)
    outputDir = joinDirs(colabPathList)
    mkDirP(outputDir)
    outputFile = joinFilePath(colabPathList, colabFileTitle)
    # phase 1: inspect to find out the title
    inNbTree = json.load(open(inputFile))
    nbTitle = findNbTitle(inNbTree)
    # phase 2: clean specific lines in specific cells
    cleanedNbTree = replaceNbCodeLines(
        inNbTree,
        codeLineReplacements,
    )
    # phase 3: add cells to the beginning, both dynamic and static groups
    enrichedNbTree = enrichNbTree(
        pathList,
        fileTitle,
        #
        cleanedNbTree,
        #
        title=nbTitle,
    )
    #
    # save the new notebook
    with open(outputFile, 'w') as of:
        cleaned_json = json.dumps(
            enrichedNbTree,
            indent=1,
            ensure_ascii=False,
            sort_keys=True,
        )
        of.write(f'{cleaned_json}\n')


if __name__ == '__main__':
    # TODO: BETTER here: scan and prepare file tree, etc etc
    import subprocess
    notebookNames = [
        nbn
        for nbn in subprocess.check_output('find -iname "*ipynb" | grep -v ".colab" | grep -v ".ipynb_checkpoints"',shell=True).decode().split('\n')
        if nbn
    ]
    def _parseNBN(pth):
        parts = [p for p in pth.split('/') if p != '.']
        return parts[:-1], parts[-1]
    #
    parsed = [
        _parseNBN(nbn)
        for nbn in notebookNames
    ]

    # TODO: use config files for exclusion, etc
    skippedFileTitles = [
        f'{fr}.ipynb'
        for fr in suppressColabify
    ]

    for pathList, fileTitle in parsed:
        pathString = joinFilePath(pathList, fileTitle)
        if fileTitle not in skippedFileTitles:
            print(f'* Doing "{pathString}" ... ', end='')
            colabifyNotebook(pathList, fileTitle)
            print('done.')

