"""Story types and opening lines, shared with hookmaker.py.

One source of truth: the data lives in story_types.py (references/lines.md is generated from it).
studio.py imports this module name, so it simply re-exports story_types.
"""
from story_types import *  # noqa: F401,F403
from story_types import TYPES, count, find, numbered, line_no, matches  # noqa: F401
