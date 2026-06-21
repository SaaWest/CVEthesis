import json
from graph import VulnGraph
from nodes import (
    CVENode,
    PackageNode,
    VersionNode,
    ExploitNode,
    OS_Node
)

def build_graph_from_json(json_file, cve_id):
    graph = VulnGraph()

    with open(json_file, "r") as f:
        data = json.load(f)

    # -------------------------
    # Create CVE node
    # -------------------------
    cve = CVENode(
        id=cve_id,
        description=f"Vulnerability affecting {data['pkg_n_version']['product']}"
    )

    graph.addNode(cve)

    # -------------------------
    # Package node
    # -------------------------
    pkg_name = data["pkg_n_version"]["product"]

    pkg_node = PackageNode(
        id=f"pkg:{pkg_name}",
        package=pkg_name,
        ecosystem="PyPI"
    )

    graph.addNode(pkg_node)

    graph.addEdge(cve.id, pkg_node.id, "affects")

    # -------------------------
    # Version node
    # -------------------------
    version = data["pkg_n_version"]["start_version"]

    version_node = VersionNode(
        id=f"{pkg_name}:{version}",
        package=pkg_name,
        versionNum=version
    )

    graph.addNode(version_node)

    graph.addEdge(pkg_node.id, version_node.id, "has_version")

    # CVE directly affects version
    graph.addEdge(cve.id, version_node.id, "affects_version")

    # -------------------------
    # OS/Ecosystem nodes
    # -------------------------
    for os_name in data.get("os_list", []):
        os_node = OS_Node(
            id=f"os:{os_name}",
            distribution=os_name
        )

        graph.addNode(os_node)

        graph.addEdge(version_node.id, os_node.id, "runs_on")

    # -------------------------
    # Exploit nodes
    # -------------------------
    for i, url in enumerate(data.get("exploit", [])):
        exploit_node = ExploitNode(
            id=f"exploit:{i}",
            url=url
        )

        graph.addNode(exploit_node)

        graph.addEdge(exploit_node.id, cve.id, "targets")

    # -------------------------
    # Artifact/Image node
    # -------------------------
    for i, wheel_url in enumerate(data.get("wheelFile", [])):

        image_node = {
            "id": f"image:{i}",
            "type": "IMAGE",
            "url": wheel_url
        }

        graph.g.add_node(image_node["id"], **image_node)

        graph.addEdge(version_node.id, image_node["id"], "downloads")

    return graph