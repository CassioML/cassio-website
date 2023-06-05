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

from settings import (
    codeLineReplacements,
    suppressColabify,
    defaultColabCellSequences,
    perNotebookColabCellSequences,
    cellSequenceCreatorMap,
)

# enrichment-specific tools

def enrichNbTree(pathList, fileTitle, nbTree, **kwargs):
    inputFile = joinFilePath(pathList, fileTitle)
    cellSequenceIDs = perNotebookColabCellSequences.get(
        inputFile,
        defaultColabCellSequences,
    )
    # what cell sequences should be added to this notebook?
    return {
        k: (
            v
            if k != 'cells'
            else [
                cell
                for cellSeqID in cellSequenceIDs
                for cell in cellSequenceCreatorMap[cellSeqID](pathList, fileTitle, nbTree, **kwargs)
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

    for pathList, fileTitle in parsed:
        pathString = joinFilePath(pathList, fileTitle)
        if pathString not in suppressColabify:
            print(f'* Doing "{pathString}" ... ', end='')
            colabifyNotebook(pathList, fileTitle)
            print('done.')

