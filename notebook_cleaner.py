#!/bin/env python

import sys
import json

CREATE_COPY = False  # True


def _cleanValue(value, path):
    # any list index becomes a '' in the path list
    if isinstance(value, list):
        return [
            _cleanValue(v, path=path+[''])
            for v in value
            if _keepValue(v, path=path+[''])
        ]
    elif isinstance(value, dict):
        return {
            k: _cleanValue(v, path=path+[k])
            for k, v in value.items()
            if _keepValue(v, path=path+[k])
        }
    else:
        return value


def _keepValue(value, path):
    path_str = '.'.join(path)
    if path_str == 'cells..id':
        return False
    elif path_str == 'cells..outputs.':
        if value.get('name') == 'stderr':
            return False
        else:
            return True
    elif path_str == 'metadata.language_info.version':
        return False
    else:
        return True


def cleanFile(fname):
    ofname = fname if not CREATE_COPY else f'{fname}.copy'
    nbdata = json.load(open(fname))
    cleaned = _cleanValue(nbdata, path=[])
    with open(ofname, 'w') as of:
        cleaned_json = json.dumps(
            cleaned,
            indent=1,
            ensure_ascii=False,
            sort_keys=True,
        )
        of.write(f'{cleaned_json}\n')
    return (json.dumps(
        nbdata, sort_keys=True,
    ) != json.dumps(
        cleaned, sort_keys=True,
    ))


if __name__ == '__main__':
    files = sys.argv[1:]
    for f in files:
        print(f'Cleaning "{f}" ... ', end='')
        changed = cleanFile(f)
        print(f'done {"[CHANGED]" if changed else ""}.')
