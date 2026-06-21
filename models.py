from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class BaseNode:
    id: str
    type: str

@dataclass
class CVENode(BaseNode):
    #severity: str = ""
    description: str = ""
    type: str = "CVE"

@dataclass
class OS_Node(BaseNode):
    #type: str = "BASE"
    distribution: str =""
    type: str = "BASE"
    #version: str = ""

@dataclass
class PackageNode(BaseNode):
    package: str = ""
    ecosystem: str= ""
    type: str = "PACKAGE"
    #language: str ="" 

@dataclass
class VersionNode(BaseNode):
    package: str =""
    versionFilter: str = ""
    #filter: str = ""
    type: str = "VERSION"

@dataclass
class DependencyNode(BaseNode):
    installs: str = ""
    type: str = "DEPENDENCY"

@dataclass
class ExploitNode(BaseNode):
    url: str = ""
    type: str = "EXPLOIT"

@dataclass
class ArtifactNode(BaseNode):
    url: str = ""
    type: str = "ARTIFACT"

@dataclass
class LanguageFile(BaseNode):
    file: str = ""
    type: str = "FILE"
