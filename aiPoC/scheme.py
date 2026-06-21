from dataclasses import dataclass
from typing import List

@dataclass
class References:
    url: str
    source: str
    content: str

@dataclass
class CVEcontent:
    cveID: str
    pkg: str
    eco: str
    versions: str
    ref: List[References]

@dataclass
class GeneratedFiles:
    path: str
    content: str

@dataclass
class PoCresult:
    success: bool
    stdout: str
    stderr: str
    exitCode: int