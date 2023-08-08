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
    elif path_str == 'metadata.widgets':
        # for notebooks from colabs, these are widgets such as
        # those from gradio which make nbconvert complain of a KeyError
        # (see https://github.com/jupyter/nbconvert/issues/1731#issuecomment-1113451797)
        return False
    elif path_str == 'cells..metadata.colab':
        # for notebooks imported from colabs, there is a long list
        # of "associated widget IDs" here (+ other stuff) we don't care.
        return False
    elif path_str == 'cells..outputs.':
        if value.get('name') == 'stderr':
            return False
        elif value.get('name') == 'stdout' and options.get('stripStdoutOutput', False):
            # normally we want to keep the stdout chunks of output
            return False
        elif value.get('output_type') == 'execute_result':
            # this is immediate (implicit) output from the last cell command
            # At the moment it's an occasional image or text, we keep it
            return True
        elif value.get('output_type') == 'display_data':
            # this e.g. contains for massive "Audio widget" sounds,
            # base-64 encoded in the page.
            # Also: progress bars (tqdm stuff), gradio apps (...?)
            # We discard those, except for those with images, that we keep.
            _data = value.get('data') or {}
            _tps = str(_data.get('text/plain'))
            if 'PIL.Image.Image' in _tps:
                # it's harmless inline image stuff
                return True
            elif 'Figure size' in _tps:
                # other image stuff
                return True
            else:
                return False
        else:
            return True
    elif path_str == 'metadata.language_info.version':
        return False
    else:
        return True


def cleanNb(nbTree, options={}):
    return _cleanValue(nbTree, path=[], options=options)


def findNbHeadings(nbTree):
    """
    Assumption: if there is a "subtitle" i.e. a markdown regular pararaph,
    it is in the same cell as the one with the "# title" row.

    Returns (all keys can be None):
        {
            'title': ...
            'subtitle': ...
        }
    """
    cells = nbTree['cells']

    def _isTitleCell(cell):
        return any(
            len(line) > 1 and line[:2] == '# '
            for line in (
                _line.strip()
                for source in cell.get('source', [])
                for _line in source.split('\n')
            )
        )

    mdTitleCells = [
        cell
        for cell in cells
        if cell.get('cell_type') == 'markdown'
        if _isTitleCell(cell)
    ]

    if mdTitleCells:
        # take the first!
        mdTitleCell = mdTitleCells[0]
        titleRows = [
            line
            for line in (
                _line.strip()
                for source in mdTitleCell.get('source', [])
                for _line in source.split('\n')
            )
            if len(line) > 1 and line[:2] == '# '            
        ]
        titleString = titleRows[0][2:] 
        #
        subtitleRows = [
            line
            for line in (
                _line.strip()
                for source in mdTitleCell.get('source', [])
                for _line in source.split('\n')
            )
            if len(line) > 1 and line[:1] != '#'            
        ]
        if subtitleRows:
            subtitleString = ' '.join(subtitleRows)
        else:
            subtitleString = None
        #
        return {
            'title': titleString,
            'subtitle': subtitleString,
        }
    else:
        return {
            'title': None,
            'subtitle': None,
        }


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