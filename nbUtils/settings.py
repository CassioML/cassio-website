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
