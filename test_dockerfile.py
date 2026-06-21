import unittest

from vulngraph import VulnGraph
from models import BaseNode, VersionNode, OS_Node
from generateDockerfile import makeDockerfile


class TestMakeDockerfile(unittest.TestCase):

    def setUp(self):
        self.graph = VulnGraph()

        # --------------------
        # CVE node
        # --------------------
        cve_node = BaseNode(
            id="CVE-TEST",
            type="CVE"
        )
        self.graph.addNode(cve_node)

        # --------------------
        # Version node
        # --------------------
        version_node = VersionNode(
            id="ver-1",
            type="VERSION",
            package="pydicom",
            versionNum="2.5.0"
        )
        self.graph.addNode(version_node)

        self.graph.g.nodes["ver-1"].update({
            "version_filter": [">=2.0.0,<3.0.2"],
            "pkg_n_version": {
                "product": "pydicom",
                "start_version": "2.0.0",
                "end_version": "3.0.2"
            },
            "ecosystems": ["py3", "py2.py3", "source"],
            "wheelFile": [
                "https://files.pythonhosted.org/.../pydicom-2.0.0.tar.gz",
                "https://files.pythonhosted.org/.../pydicom-2.0.0-py3-none-any.whl"
            ]  
        })

        # --------------------
        # Image node (IMPORTANT: add BEFORE edges)
        # --------------------
        image_node = BaseNode(
            id="python:3.11-slim",
            type="IMAGE"
        )
        self.graph.addNode(image_node)

        self.graph.g.nodes["python:3.11-slim"].update({
            "tag": "3.11-slim"
        })
        print(self.graph.g.nodes["python:3.11-slim"])
        # --------------------
        # OS node (runtime dependency)
        # --------------------
        os_node = OS_Node(
            id="Ubuntu:18.04",
            type="OS",
            distribution="Ubuntu"
        )
        self.graph.addNode(os_node)

        self.graph.g.nodes["Ubuntu:18.04"]["family"] = "debian"

        # --------------------
        # EDGES (must form a valid path)
        # --------------------
        self.graph.addEdge("CVE-TEST", "ver-1", relation="AFFECTS")
        self.graph.addEdge("ver-1", "python:3.11-slim", relation="INSTALLED_IN")
        self.graph.addEdge("python:3.11-slim", "Ubuntu:18.04", relation="RUNS_ON")

        # --------------------
        # Path used by function
        # --------------------
        self.path = [
            "CVE-TEST",
            "ver-1",
            "python:3.11-slim",
            "Ubuntu:18.04"
        ]

    def test_python_ecosystem_detected(self):
        result = makeDockerfile(self.graph, self.path)

        self.assertIsNotNone(result)
        self.assertTrue(result[0].startswith("FROM"))


if __name__ == "__main__":
    unittest.main()