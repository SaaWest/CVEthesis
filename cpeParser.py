import requestAPI
import semver
import json

def get_cpeVersions(tags):
    # Use this function if dockerCPE_versions fails
    #versions = []
    print(tags)
    print(type(tags))
    #for item in tags:
    start = [i.get('versionStartIncluding')for i in tags if i.get('versionStartIncluding') != None]
    endExc = [i.get('versionEndExcluding') for i in tags if i.get('versionEndExcluding') != None]
        #endInc = item.get('versionEndIncluding')
    endInc = [i.get('versionEndIncluding') for i in tags if i.get('versionEndIncluding') != None]#item.get('versionEndIncluding')]
    #print(endInc)
        #if start or endExc or endInc:
    versions = {
        "start": start if len(start) != 0 else ' ',
        "endExclude": endExc if len(endExc) != 0 else ' ',
        "endInclude": endInc if len(endInc) != 0 else ' '
        }
    print("Versions", versions)
    return versions

def decrementVersion(version):
    #saefely decrement versions
    #print(len(version))
    if len(version) <= 3:
        version += ".0"
    print("Version ", version)
    ver = semver.VersionInfo.parse(version)
    
    if ver.patch > 0:
        # standard decrement: 1.2.3 -> 1.2.2
        return ver.replace(patch=ver.patch - 1)
    elif ver.major > 0 and ver.minor > 0:
        # roll back minor: 1.1.0 -> 1.0.9
        return ver.replace(minor=ver.minor - 1, patch=9)    
    elif ver.major > 0:
        # roll back major: 3.0.0 -> 2.9.9
        return ver.replace(major=ver.major - 1, minor=9, patch=9)
    elif ver.major == 0 and ver.minor > 0:
        # roll back minor: 0.5.0 -> 0.4.9
        return ver.replace(minor=ver.minor-1, patch=9)
    
    raise ValueError("Cannot decrement version")

def cpe_filterVersions(tags):
    print("tags in DcoekrCPE_version ",tags)
    start= tags.get('start')[0]#, end, endInclude = tags#item.get('versionStartIncluding')
    endExc = tags.get('endExclude')[0]#end = item.get('versionEndExcluding')
    endInc = tags.get('endInclude')[0]#endInclude = item.get('versionEndIncluding')
    #endExclude = item.get('versionEndExcluding')
    print(start)
    print(endExc)
    print(endInc)
    versions = []
    cpeString = ""
    #for item in tags:
    if (start != ' ') and (endExc != ' '):
        cpeString = f">={start},<{endExc}"
        versions.append(cpeString)
    elif start != ' ' and endExc == ' ':
        cpeString = f"=={start}"
        versions.append(cpeString)
    elif (start != ' ') and (endInc != ' '):
        cpeString = f">={start},={endInc}"
        versions.append(cpeString)
    #elif (endInc and not start) and (endInc and not endExc) and (endInc != ' '):
        #cpeString = f"=={endInc}"
        #versions.append(cpeString)
    elif (start == ' ') and (endExc == ' ') and (endInc != ' '):
        cpeString = f"<={endInc}"
        versions.append(cpeString)
    elif endExc and start == ' ' and endInc == ' ':
        #ver = decrementVersion(end)
        #cpeString = f"=={str(ver)}"
        cpeString = f"<{endExc}"
        versions.append(cpeString)
    return versions


def get_startDefault(tags):
    startVer = [item.get('versionStartIncluding') for item in tags if 'versionStartIncluding' in item]
    return startVer

def get_endDefault(tags):
    startVer = [item.get('versionEndIncluding') for item in tags if 'versionEndIncluding' in item]
    return startVer

def parse_productAndVersion(tags, versionList):
    """
    USE THIS IN OSV API CALL
    """
    criteria = [item.get('criteria') for item in tags if 'criteria' in item]
    start = ""
    end = ""
    endInclude= ""
    for item in versionList:
        if ">=" in item and ",<" in item:
            parts = item.split(",")
            start = parts[0].replace(">=", "").strip()
            end = parts[1].replace("<", "").strip()

        elif ">=" in item and ",=" in item:
            parts = item.split(",")
            start = parts[0].replace(">=", "").strip()
            end = parts[1].replace("=", "").strip()

        elif "==" in item:
            version = item.replace("==", "").strip()
            start = version
            end = version
        elif "<=" in item:
            version = item.replace("<=", "").strip()
            start = version
            end = version
        elif "<" in item:
            version = item.replace("<", "").strip()
            start = str(decrementVersion(version))[:3]
            end = version
            print("START ", start)
    for i in criteria:
        parts = i.split(':')
        print("PARTS ", parts)
        return {
            "product": parts[4].replace("python-", "") if "python-" in parts[4] else parts[4],
            "start_version": start if start else "",
            "end_version": end if end else ""
        }

def combineAPIJsonFile(osList, prdNver, allVer, filterVer, expoilt, whl, langFile):
    print("\nCPE combineAPIfiles: ", whl)
    print("\n")
    allData = {
        "os_list" : osList,
        "pkg_n_version": prdNver,
        "ecosystems": allVer,
        "version_filter": filterVer,
        "exploit": expoilt,
        "wheelFile": whl,
        "languageFile": langFile
    }
    print("\nallData", allData)
    with open("data.json", "w") as f:
        json.dump(allData, f)