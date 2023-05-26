"""
Very simple utility to manage the choice of LLM service
"""

import os


def suggestLLMProvider():
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        return 'VertexAI'
    elif 'OPENAI_API_KEY' in os.environ:
        return 'OpenAI'
    else:
        raise ValueError('No available credentials for LLMs')
