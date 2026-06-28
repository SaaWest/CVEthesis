import networkx as nx

class SecurityGraph:
    def __init__(self):
        self.g = nx.DiGraph()

    # ---------- Nodes ----------

    def add_os(self, name, version, safe=True):
        node_id = f"{name}:{version}"

        self.g.add_node(
            node_id,
            type="os",
            name=name,
            version=version,
            cve_safe=safe
        )

        return node_id

    def add_runtime(self, runtime, version):
        node_id = f"{runtime}:{version}"

        self.g.add_node(
            node_id,
            type="runtime",
            name=runtime,
            version=version
        )

        return node_id

    def add_package(self, ecosystem, name, version):
        node_id = f"{ecosystem}:{name}:{version}"

        self.g.add_node(
            node_id,
            type="package",
            ecosystem=ecosystem,
            name=name,
            version=version
        )

        return node_id

    #def add_cve(self, cve_id, severity=None, exploited=False):
        #node_id = f"{cve_id}"

        #self.g.add_node(
            #node_id,
            #type="cve",
            #severity=severity,
            #exploited=exploited
        #)

        #return node_id

    # ---------- Relationships ----------

    def add_dependency(self, parent, dependency):
        self.g.add_edge(
            parent,
            dependency,
            relation="depends_on"
        )

    def add_cve_affect(self, cve, package):
        self.g.add_edge(
            cve,
            package,
            relation="affects"
        )

    def add_runtime_requirement(self, package, runtime):
        self.g.add_edge(
            package,
            runtime,
            relation="requires"
        )

    def add_os_relationship(self, runtime, os_node):
        self.g.add_edge(
            runtime,
            os_node,
            relation="runs_on"
        )