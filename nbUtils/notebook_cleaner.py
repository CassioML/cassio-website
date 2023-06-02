#!/bin/env python

import sys
import json

from nbmanipulate import cleanNb

CREATE_COPY = False  # True


def cleanFile(fname):
    ofname = fname if not CREATE_COPY else f'{fname}.copy'
    nbdata = json.load(open(fname))
    cleaned = cleanNb(nbdata)
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
