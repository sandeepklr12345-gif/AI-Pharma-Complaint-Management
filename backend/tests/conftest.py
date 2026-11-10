"""Test setup: no network, no Postgres, no model downloads.

The app reads settings and builds a DB engine at import time, and the graph nodes load a
SentenceTransformer, so we provide dummy env vars and stub the heavy/remote libraries first.
"""
import os
import sys
import types

os.environ.setdefault("GROQ_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "sqlite://")

# Never download the embedding model in tests (the real one is ~90 MB and needs torch).
st = types.ModuleType("sentence_transformers")


class _FakeEmbedder:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, text, **kwargs):
        return text


st.SentenceTransformer = _FakeEmbedder
st.util = types.SimpleNamespace(cos_sim=lambda a, b: [[0.0]])
sys.modules["sentence_transformers"] = st

# groq is only needed to construct a client object; skip it if it is not installed.
try:
    import groq  # noqa: F401
except ImportError:
    groq_stub = types.ModuleType("groq")
    groq_stub.Groq = lambda *args, **kwargs: types.SimpleNamespace()
    sys.modules["groq"] = groq_stub
