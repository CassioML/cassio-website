import os


def getColabifiedFileCoordinates(pathList, fileTitle):
    assert(fileTitle[-6:].lower() == '.ipynb')
    colabFileTitle = f'colab_{fileTitle}'
    return pathList + ['.colab'], colabFileTitle


def joinDirs(pathList):
    return os.path.join(*pathList)


def joinFilePath(pathList, fileTitle):
    return os.path.join(*(pathList + [fileTitle]))


def mkDirP(dName):
    """Mimic 'mkdir -p DIRNAME' in creating the full path."""
    nDir = os.path.normpath(os.path.abspath(dName))
    if not os.path.isdir(nDir):
        pth, last = os.path.split(nDir)
        mkDirP(pth)
        os.mkdir(nDir)
