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
    findNbHeadings,
    findNbUrl,
    replaceNbCodeLines,
    cleanNb,
)

from settings import (
    codeLineReplacementsMap,
    suppressColabify,
    defaultColabCellSequences,
    defaultColabCellClosingSequences,
    perNotebookColabCellSequences,
    perNotebookColabCellClosingSequences,
    cellSequenceCreatorMap,
)

# enrichment-specific tools

def enrichNbTree(pathList, fileTitle, nbTree, **kwargs):
    inputFile = joinFilePath(pathList, fileTitle)
    cellSequenceIDs = perNotebookColabCellSequences.get(
        inputFile,
        defaultColabCellSequences,
    )
    cellClosingSequenceIDs = perNotebookColabCellClosingSequences.get(
        inputFile,
        defaultColabCellClosingSequences,
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
            ] + v + [
                cell
                for cellSeqID in cellClosingSequenceIDs
                for cell in cellSequenceCreatorMap[cellSeqID](pathList, fileTitle, nbTree, **kwargs)
            ]
        )
        for k, v in nbTree.items()
    }


def colabifyNotebook(pathList, fileTitle):
    inputFile = joinFilePath(pathList, fileTitle)
    colabPathList, colabFileTitle = getColabifiedFileCoordinates(pathList, fileTitle)
    outputDir = joinDirs(colabPathList)
    mkDirP(outputDir)
    outputFile = joinFilePath(colabPathList, colabFileTitle)
    # phase 1: inspect to find out a couple of properties
    inNbTree = json.load(open(inputFile))
    nbHeadings = findNbHeadings(inNbTree)
    nbUrl = findNbUrl(pathList, fileTitle)
    # prepare full list of replacements
    codeLineReplacements = [
        repRule
        for pathSlice in (
            (pathList + [fileTitle])[:i]
            for i in range(len(pathList) + 2)
        )
        for repRule in codeLineReplacementsMap.get(
            "/".join(pathSlice),
            [],
        )
    ]
    # phase 2: clean specific lines in specific cells
    cleanedNbTree = replaceNbCodeLines(
        inNbTree,
        codeLineReplacements,
    )
    # phase 3: add cells to the notebook, both dynamic and static groups
    enrichedNbTree = enrichNbTree(
        pathList,
        fileTitle,
        #
        cleanedNbTree,
        #
        headings=nbHeadings,
        nbUrl=nbUrl,
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


def locateNotebooks(home='.', excludeDirs={'.ipynb_checkpoints', '.colab'}):

    NOTEBOOK_FILE_EXTENSION = '.ipynb'

    def _scanPath(pth=[],excludeDirs=excludeDirs):
        fullPth = os.path.join(home, *pth)
        everything = os.listdir(fullPth)
        dirs = [
            e
            for e in everything 
            if os.path.isdir(os.path.join(*([home]+pth+[e])))
            if e not in excludeDirs
        ]
        nbFiles = [
            e
            for e in everything
            if os.path.isfile(os.path.join(*([home]+pth+[e])))
            if len(e) >= len(NOTEBOOK_FILE_EXTENSION)
            if e.lower()[-len(NOTEBOOK_FILE_EXTENSION):] == NOTEBOOK_FILE_EXTENSION
        ]
        for f in nbFiles:
            yield pth, f
        for d in dirs:
            for pair in _scanPath(pth+[d],excludeDirs=excludeDirs):
                yield pair

    return _scanPath()

if __name__ == '__main__':
    for pathList, fileTitle in locateNotebooks():
        pathString = joinFilePath(pathList, fileTitle)
        if pathString not in suppressColabify:
            print(f'* Doing "{pathString}" ... ', end='')
            colabifyNotebook(pathList, fileTitle)
            print('done.')

