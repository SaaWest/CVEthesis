import requestAPI
import cpeParser
import sys
import json

from vulngraph import VulnGraph
from models import BaseNode, VersionNode, OS_Node, CVENode, PackageNode, ExploitNode, ArtifactNode, LanguageFile
from generateDockerfile import makeDockerfile, requirementsErrors, build_Dockerfile, run_Image, makeRequirements

request = requestAPI
response = request.makeNISTrequest()
#print(response)
exploit = requestAPI.get_exploits(response)
#print("tags", tags)
versions = requestAPI.get_versions(response)
#print("\nVersions: ", versions)
#criteria = cpeParser.parse_product(versions)
#versionStart = parse_json.get_startDefault(versions)
allVersions = cpeParser.get_cpeVersions(versions)
print("ALL VERSIONS", allVersions)
#tags = requestAPI.get_tags()
verList = cpeParser.cpe_filterVersions(allVersions)
#print("dockerCPE_Versions", verList)
#startVer = cpeParser.get_startDefault(versions)
#endVer = cpeParser.get_endDefault(versions)
product = cpeParser.parse_productAndVersion(versions, versionList=verList)
print("\nLibrary \n", product)
eco = requestAPI.makeOSV_EcosystemRequest(product)
#print(verionList)
print("\nMake OSV", eco)
compareOS = requestAPI.compare_osvEcosys_DockHubImages(product)
#print(f"Compare List ", compareOS)

whlFile = requestAPI.makePyPi_aptRequest(product)
#print("Wheel File ", whlFile)

whlVersion, whlURL = requestAPI.getPythonVersion_Pypi(whlFile, product, eco)
print("Wheel Version ", whlVersion)
print("WHEEL URL ", whlURL )
downloadPython = requestAPI.getPython(whlVersion)
print("downloadeding Python file ", downloadPython)
#filter = parse_json.filter_versions(versions, allVersions)
#print(filter)

dataJson = cpeParser.combineAPIJsonFile(compareOS, product, whlVersion, verList, exploit, whlURL, downloadPython)
print("dataJson for WhlURL: ", dataJson)
# json file for graph
with open('data.json', 'r') as f:
    dataFile = json.load(f)
    print("dataJson for WhlURL: ", dataFile)
    
path = []
#Test graph
graph = VulnGraph()
cveNode = CVENode(id=f"cve:{sys.argv[1].upper()}", description=requestAPI.get_descript(response))
graph.addNode(cveNode)
path.append(cveNode.id)

pkgNode = PackageNode(id=f"pkg:{dataFile['pkg_n_version']['product']}", package=dataFile["pkg_n_version"]["product"], ecosystem=dataFile["ecosystems"])
graph.addNode(pkgNode)
graph.addEdge(cveNode.id, pkgNode.id, "affects")
path.append(pkgNode.id)

versionNode = VersionNode(id=f"version:{dataFile['pkg_n_version']['product']}:{dataFile["pkg_n_version"]["start_version"]}", package=dataFile["pkg_n_version"]["product"], versionFilter=dataFile.get("version_filter"))
graph.addNode(versionNode)
graph.addEdge(pkgNode.id, versionNode.id, "has_version")
path.append(versionNode.id)

graph.addEdge(cveNode.id, versionNode.id, "affected_version")

for os in dataFile.get("os_list", []):
    print(os)
    osNode = OS_Node(id=f"os:{os}", distribution=os)
    graph.addNode(osNode)
    graph.addEdge(versionNode.id, osNode.id, "runs_on")
    path.append(osNode.id)
    break

for i, url in enumerate(dataFile.get("exploit", [])):
    exploitNode = ExploitNode(id=f"exploit:{i}", url=url)
    graph.addNode(exploitNode)
    graph.addEdge(exploitNode.id, cveNode.id, "targets")
    path.append(exploitNode.id)
    break

for i, whlURL in enumerate(dataFile.get("wheelFile", [])):
    artifactNode = ArtifactNode(id=f"artifact:{i}", url=whlURL)
    graph.addNode(artifactNode)
    graph.addEdge(artifactNode.id, versionNode.id, "downloads")
    path.append(artifactNode.id)
    break

languageFile = LanguageFile(id=f"LangFile:{dataFile["languageFile"]}", file=dataFile["languageFile"])

graph.addNode(languageFile)
graph.addEdge(languageFile.id, cveNode.id, "is_file")
path.append(languageFile.id)

#path = [cveNode.id, versionNode.id, ]

## TODO: Stills needs an exit for applications that have flask or others; remove  -it and handle errors some other way
## make the Dockerfile
#makeRequirements(graph=graph, path=path)
#makeDockerfile(graph=graph, path=path)
#
#build image
#builder = build_Dockerfile(sys.argv[1])
#print(builder)
#run image
#runner = run_Image(sys.argv[1])
#print(runner)
## error handling
#if len(runner) > 1:
    #req = requirementsErrors(runner)
    #print(req)
    #builder = build_Dockerfile(sys.argv[1])
    #runner = run_Image(sys.argv[1])
#else:
    #print("Build and Run success")

#graph.g.nodes[sys.argv[1].upper()].update(dataFile)

#baseNode = BaseNode(id="attempt-1", type="IMAGE")
