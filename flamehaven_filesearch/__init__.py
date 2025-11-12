"""
FLAMEHAVEN FileSearch
=====================

Open source semantic document search powered by Google Gemini
Fast, simple, and transparent file search for developers
"""

__version__ = "1.0.0"
__author__ = "FLAMEHAVEN"
__license__ = "MIT"

from .core import FlamehavenFileSearch
from .config import Config

__all__ = ["FlamehavenFileSearch", "Config"]
