"""
Very simple utility to manage the choice of LLM service
"""

import os

# functions from env var map to boolean (whereby True means valid)
providerValidator = {
    'VertexAI': lambda envMap: 'GOOGLE_APPLICATION_CREDENTIALS' in envMap,
    'OpenAI': lambda envMap: 'OPENAI_API_KEY' in envMap,
}

def suggestLLMProvider():
    #
    preferredProvider = os.environ.get('PREFERRED_LLM_PROVIDER')
    if preferredProvider and providerValidator[preferredProvider](os.environ):
        return preferredProvider
    else:
        for pName, pValidator in providerValidator.items():
            if pValidator(os.environ):
                return pName
        raise ValueError('No available credentials for LLMs')
