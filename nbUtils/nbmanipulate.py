def _cleanValue(value, path, options):
    # any list index becomes a '' in the path list
    if isinstance(value, list):
        return [
            _cleanValue(v, path=path+[''], options=options)
            for v in value
            if _keepValue(v, path=path+[''], options=options)
        ]
    elif isinstance(value, dict):
        return {
            k: _cleanValue(v, path=path+[k], options=options)
            for k, v in value.items()
            if _keepValue(v, path=path+[k], options=options)
        }
    else:
        return value


def _keepValue(value, path, options):
    path_str = '.'.join(path)
    if path_str == 'cells..id':
        if options.get('stripCellIds', False):
            return False
        else:
            # For notebooks aimed at jupyter,
            # unfortunately we cannot strip the id field as its absence
            # will become a hard error in future nbformat versions.
            return True
    elif path_str == 'cells..outputs.':
        if value.get('name') == 'stderr':
            return False
        elif value.get('name') == 'stdout' and options.get('stripStdoutOutput', False):
            # normally we want to keep the stdout chunks of output
            return False
        else:
            return True
    elif path_str == 'metadata.language_info.version':
        return False
    else:
        return True


def cleanNb(nbTree, options={}):
    return _cleanValue(nbTree, path=[], options=options)


def findNbTitle(nbTree):
    cells = nbTree['cells']
    mdTitleRows = [
        line
        for line in (
            _line.strip()
            for cell in cells
            if cell.get('cell_type') == 'markdown'
            for source in cell.get('source', [])
            for _line in source.split('\n')
        )
        if len(line) > 1 and line[:2] == '# '
    ]
    if mdTitleRows:
        return mdTitleRows[0][2:]
    else:
        return None


nbUrlPrefix = 'https://cassio.org/'
nbExtension = '.ipynb'
def findNbUrl(pathList, fileTitle):
    assert(pathList[0] == 'docs')
    assert(fileTitle.lower()[-len(nbExtension):] == nbExtension)
    filePathComponent = fileTitle[:-len(nbExtension)]
    return f'{nbUrlPrefix}{"/".join(pathList[1:])}/{filePathComponent}/'


def _replaceNbCodeLine(line, replacements):
    for oldB, newL in replacements:
        if line.find(oldB) > -1:
            return newL
    return line


def _replaceNbCodeInCodeBlock(block, replacements):
    # block is a list of strings, all but the last one ending in "\n"
    strippedLines = [
        line if len(line) < 1 or line [-1:] != '\n' else line[:-1]
        for line in block
    ]
    cleanedStrippedLines = [
        newLine
        for newLine in (
            _replaceNbCodeLine(_line, replacements)
            for _line in strippedLines
        )
        if newLine is not None
    ]
    #
    numLines = len(cleanedStrippedLines)
    restoredLines = [
        lin if lini + 1 == numLines else f'{lin}\n'
        for lini, lin in enumerate(cleanedStrippedLines)
    ]
    return restoredLines


def _replaceNbCodeInCell(cell, replacements):
    if cell.get('cell_type') == 'code':
        return {
            k: (
                v
                if k != 'source'
                else _replaceNbCodeInCodeBlock(v, replacements)
            )
            for k, v in cell.items()
        }
    else:
        return cell


def replaceNbCodeLines(nbTree, replacements):
    return {
        k: (
            v
            if k != 'cells'
            else [
                _replaceNbCodeInCell(cell, replacements)
                for cell in v
            ]
        )
        for k, v in nbTree.items()
    }