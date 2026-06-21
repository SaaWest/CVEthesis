import requests
from sys import argv
#from json import loads
import json
import subprocess
import re
import pathlib

#CACHE_ECOSystem = []

def makeNISTrequest():#cve: str):
    """
    This program returns a request from NIST in json format

    Output:
    returns a json response from NIST
    """
    #RESTORE VARIABLE cve after testing
    cve = argv[1].upper()
    #cve =cve.upper()
    api = f'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}'
    #print(api)
    response = requests.get(api)
    nistResponse = response.json()
    return nistResponse

def makeOSV_EcosystemRequest(product):
    #global CACHE_ECOSystem
    """
    Searches for Ecosystems by making request to OSV. Save results to a global list
    Input: 
        Takes version variable from cpeParser.parse_product()
            - ex 2.0.0
        Takes ProductName from cpeParser.parse_product()
    Output:
        json file of ecosystems
    """
    name = product.get("product")
    startVer = product.get("start_version")
    endVer = product.get("end_version")
    #name.
    url = "https://api.osv.dev/v1/query"
    payload = {
        "version": startVer if startVer else endVer,
        "package": {
            "name": name,
            "ecosystem": ""
        }
    }
    print("Payload ", payload)
    req = requests.post(url, json=payload)
    #print(req.text + '\n')
    responseJson = req.json()

    vulns = responseJson.get("vulns", [])
    #CACHE_ECOSystem = [
    ecosystemList = [
        affected.get("package", {}).get("ecosystem")
        for vuln in vulns
        for affected in vuln.get("affected", [])
        if affected.get("package", {}).get("ecosystem")
    ]
    #print("Ecosystems ", ecosystemList)
    #return ecosystemList
    return ecosystemList #CACHE_ECOSystem

    #cve = argv[1].upper()
    #api = f'https://osv.dev/list?q={lib.upper()}&ecosystem={eco.upper()}-{cve}'
    #print(api)
    #response = requests.get(api)
    #osvResponse = response.json()
    #return osvResponse

def makePyPi_aptRequest(product_name):
    """
    Function to get request python version (for pip dependency)
    """
    name = product_name.get("product")
    if "python" in name:
        name = name.replace("python-", "")
    getReq = f"https://pypi.org/pypi/{name}/json"
    print('\n')
    print("\nREQUEST PYPI ", getReq)
    res = requests.get(getReq)
    data = res.json()
    print("\nRELEASES: ", data["releases"])
    #print("\n")
    return data["releases"]

def getPythonVersion_Pypi(whlReleases, product_name, ecoProductSysVersion):
    print("\nPYPI PRODUCT NAME ", whlReleases)

    version = product_name.get("start_version")
    print(f"\nVERSION for Python: {version}\n")
    #print("\n\n\nwheel release ITEMS ", whlReleases.values())
    if version in whlReleases:
        release_list = whlReleases[version]
        try:
            pyVer = [
                item["python_version"]
                #for release_list in whlReleases.values()
                for item in release_list
                if "python_version" in item
            ]
            whlURL = [
                item["url"]
                #for release_list in whlReleases.values()
                for item in release_list
                if "url" in item
            ]
            pyVer = [i for i in pyVer if i != "source"]
            whlURL = [i for i in whlURL if (".exe" not in i) or ("win" not in i)]
            print("WHL URLs: ", list(set(whlURL)))
            return list(set(pyVer)), list(set(whlURL))
        except:
            print("EEROR: Possibly no python versions from PyPI")
            return None


def compare_osvEcosys_DockHubImages(product):
    """
    About:
    Comapares the ecosystems found in OSV request to the available Docker Containers 
    using get_tags() cli results. Removes item from cache to prevent using the same variables.
    
    Included error handling (if unable to create image).
    
    Output:
    Returns either a tuple for OS and version or version or OS or nothing if unable to find a 
    possible valid image.
    """
    approvedOS = ("Debian", "Ubuntu")
    print("OSV PRODUCT ", product)
    osList = [
        x.removesuffix(":LTS") if x else x
        for x in set(makeOSV_EcosystemRequest(product))
    ]
    #osList = list(set(makeOSV_EcosystemRequest(product)))
    for i in osList[:]:
        dockhub_tags = {"tags": []}
        if ":" in i:
            sw = i.split(":")[0]
            version = i.split(":")[1]
            result = get_tags(sw.lower())
            if not isinstance(result, dict):
                continue
            dockhub_tags = result
            tags = dockhub_tags["tags"]
            if version not in tags:
                osList.remove(i)
        elif i is not None:
            result = get_tags(i.lower())
            if not isinstance(result, dict):
                continue
            dockhub_tags = result
            tags = dockhub_tags["tags"]
            if i not in tags:
                osList.remove(i)
        else:
            continue
    osList[:] = [item for item in osList if 'pypi' not in item.lower()]
    if len(osList) == 0:
        osList.append("Ubuntu:18.04")
    osList = [i for i in osList if any(i.startswith(a) for a in approvedOS)]
    #if len(osList) == 0:
        #osList.append("Ubuntu:18.04")
    print("OS ", osList)
    return osList        
            


def get_exploits(nist_json):
    """
    About:
    This program will return all urls in the reference section of a NIST CVE page
    and return any that have a exploit tag.

    Input:
    Takes the json list from makeNISTrequest()
    
    Output:
    A list of all url references with exploits
    """
    # get refernces for exploits 
    references = nist_json['vulnerabilities'][0]['cve']['references']
    # look for urls with exploit tag
    matches = [url['url'] for url in references if 'tags' in url and 'Exploit' in url['tags']]
    return matches

#description = lambda nist_json: ['vulnerabilities'][0]['cve']['descriptions'][0]['value']
# Just in case get description
def get_descript(nist_json):
    """
    About:
    This parses the description from NIST API
    
    Input:
    Takes the json list from makeNISTrequest()

    Output:
    Returns a string
    """
    description = nist_json['vulnerabilities'][0]['cve']['descriptions'][0]['value']
    return description


def get_versions(nist_json):
    """
    About:
    This function will search and retrieve
    data from NIST JSON based on if the keys
    (criteria, versionStartIncluding, or versionEndExcluding)
    Returns a JSON of all software CPE

    Input:
    Takes the json list from makeNISTrequest()

    Output:
    a list of distionaries or a list of lists
    """
    results = []

    keys = {
        "criteria",
        "versionStartIncluding",
        "versionStartExcluding",
        "versionEndIncluding",
        "versionEndExcluding"
    }

    if isinstance(nist_json, dict):

        # Check if this dict contains ANY relevant key
        if any(k in nist_json for k in keys):
            # Keep only relevant fields (or keep full dict if you prefer)
            filtered = {k: nist_json.get(k) for k in keys if k in nist_json}
            results.append(filtered)
        else:
            for v in nist_json.values():
                results.extend(get_versions(v))

    elif isinstance(nist_json, list):
        for item in nist_json:
            results.extend(get_versions(item))

    return results

def get_tags(image):
    """
    About:
    Gets valid tags from docker using regctl
    
    Input:
    String: name of an OS (lowercase)

    Returns: 
    JSON of tags
    """
    cmd = ["regctl", "tag", "ls", image.lower(), "--format", "{{json .}}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    #print(result)

    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        #print(f"Error: {result.stderr}")
        return None
    
def getPython(version):
    '''
    Function to retrieve the compressed file for python versions based on PyPI versions that label each package
    version with language version.
    '''
    print("VERSION ", version)
    ver = version[0].split(".")
    query = ["curl", "-s", f"https://www.python.org/ftp/python/"]
    output = subprocess.run(query, capture_output=True, text=True)
    print(output.stdout)
    dirs = set(re.findall(r'href="([^"]+)/"', output.stdout))
    if version[0] in dirs:
        cmd = ["curl", "-L", "-O", f"https://www.python.org/ftp/python/{version[0]}/Python-{version[0]}.tgz"]
        print("CMD for getPython ", cmd)
        subprocess.run(cmd, check=True)
        return f"Python-{version[0]}.tgz"

    else:
        print("VER ", ver)
        if len(ver) < 3:
            ver.append("0")
        ver = ".".join(ver)
        if ver in dirs:
            print("VER ", ver)
            print("Version ", version[0])
            cmd = ["curl", "-L", "-O", f"https://www.python.org/ftp/python/{ver}/Python-{ver}.tgz"]
            print("CMD for getPython ", cmd)
            subprocess.run(cmd, check=True)
            return f"Python-{ver}.tgz"
        else:
            print("None Found")
            return None