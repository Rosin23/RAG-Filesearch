"""
SovDef FileSearch Lite
======================

MVP용 경량 파일 검색 시스템
Google File Search 수준 편의성 + 기본 품질 보장
"""

__version__ = "1.0.0"
__author__ = "SovDef"
__license__ = "MIT"

from .core import SovDefLite
from .config import Config

__all__ = ["SovDefLite", "Config"]
