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

# NOTE: currently you HAVE to mirror these changes
# to a list in overrides/main.html to suppress
# the 'open in colab' button!
suppressColabify = [
    'prompt-templates-feast',
    'another-notebook-not-colabified', 
]
