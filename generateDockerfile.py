from pathlib import Path
import subprocess
import re

def makeDockerfile(graph, path, error=False, installs=[]):
    #print("PathFile exist b4 if ", pathFile.exists())
    print("PATH: ")
    print(len(path))
    print(path)
    base = []
    pathFile = Path("requirements.txt")
    ## TODO: REDO conditionals for file creation 6/07/26
    for id in path:
        node = graph.g.nodes[id]

    if len(path) > 5: #and ("source" in eco):
        print("PATH ", path)
        #image = path[-1]
        #print("Image node: ", image)
        #PYTHON DOCKERFILE SETUP
        pkg, filter, os, ecoVer, whl = setup(path, graph)
            
        #pathFile = Path("requirements.txt")
        base.append(f"FROM {os.lower()}")
        base.append(f"ENV DEBIAN_FRONTEND=noninteractive\n")

        #if any("py" in e for e in eco):
        #if any("py" in e for e in eco): #or (float(e) > 3) for e in eco):
            #remove 'source' from eco
        
        
        #if any(float(e) >= 3.0 for e in eco): #or ("py3" in e for e in eco)):
        if castFloat(ecoVer):
            print("PathFile exist in cast Float if ", pathFile.exists())
            #print("IF ", pathFile.exists())
            pyfloat_template(base, pathFile, os, ecoVer, pkg, filter)
        else:
            #print("Else ", pathFile.exists())
            pyStr_template(base, pathFile, os, ecoVer, pkg, filter)
            #print(pyStr_template(base, pathFile, os, eco, pkg, filter))
            
    else:
        ##TODO: change conditional from artifact:0
        if "artifact:0" in path:
            pos = path.index("artifact:0")
            whl = graph.g.nodes[path[pos]]["url"]
            base.append(f"FROM ubuntu:18.04\n")
            base.append("RUN apt-get update && apt-get install -y python3 python3-pip")
            base.append("WORKDIR /\n")
            if pathFile.exists():
                base.append("COPY requirements.txt .\n")
                base.append("RUN pip3 install --no-cache-dir -r requirements.txt")
            else:
                base.append("RUN apt-get update && apt-get install -y " \
                "python " \
                "python-dev " \
                "python-pip " \
                "build-essential"
                )
        base.append("\nCOPY poc.py .\n")
        #LATER may need to implement file/module groups i.e. bash, python3 -m package.module,scan multiple file heuristics, repo-packages python3 -m package, or simply copy a folder and run from CLI: docker run -it image bash
        base.append("\nCMD [\"python3\", \"poc.py\"]")
    
    #base.append("\nCOPY poc.py .")

    #if any("py" in e for e in eco):
        #if "py3" in eco:
            #base.append("\nCMD [\"python3\", \"poc.py\"]")
        #else:
            #base.append("\nCMD [\"python\", \"poc.py\"]")
    file = "\n".join(base)
    print(file)
    with open("Dockerfile", "w") as dock:
        dock.write(file)
    
    return base 

def setup(path, graph):
    versionNode = path[2]

    #tag = graph.g.nodes[image]

    #image_node = graph.g.nodes[image]
    version_node = graph.g.nodes[versionNode]
    #print(f"Version_node: ", version_node)

    #tag = image_node["tag"]
    pkg = version_node["package"]
    print(pkg)
    filter = version_node["versionFilter"][0]
    
    os = graph.g.nodes[path[3]]["distribution"]
    #print("Path", path[4])
    print("OS ", len(os))
    eco = graph.g.nodes[path[1]]["ecosystem"]
    ecoVer = eco[0] if len(eco) != 0 else ''
    
    print("OS: ", os)
    print("ECO: ", eco)
    whl = graph.g.nodes[path[-1]]["url"]
    print("WHL: ", whl)
    #print("Version Node: ", versionNode)
    if os.endswith(":LTS"):
        os = os[:-4]
    return pkg, filter, os, ecoVer, whl

def castFloat(eco):
    try:
        float(eco)
        return True
    except ValueError:
        return False

def pyfloat_template(base, pathFile, os, eco, pkg, filter):
    if float(eco) >= 3.0:
        base.append("RUN apt-get update && apt-get install -y " \
        "python3 " \
        "python3-dev " \
        "python3-pip " \
        "python3-venv " \
        "curl " \
        "wget " \
        "build-essential"
        )
        print("Float ", pathFile.exists())
        if pathFile.exists():
            base.append("COPY requirements.txt .")
            if float(os.split(":")[1]) > 23.04: 
                base.append("RUN python3 -m venv /venv\n" \
                            "ENV PATH=\"/venv/bin:$PATH\"")
                base.append("RUN python3 -m pip install --no-cache-dir -r requirements.txt")
                base.append("\nCOPY poc.py .")
                base.append("\nCMD [\"python3\", \"poc.py\"]") 
            else:
                base.append("RUN python3 -m pip install --no-cache-dir -r requirements.txt")
                base.append("\nCOPY poc.py .")
                base.append("\nCMD [\"python3\", \"poc.py\"]") 
        else:
            base.append(f"RUN python3 -m pip install {pkg}{filter}")
            base.append("\nCOPY poc.py .")
            base.append("\nCMD [\"python3\", \"poc.py\"]") 
    else:
        base.append("RUN apt-get update && apt-get install -y " \
                    "python " \
                    "python-dev " \
                    "python-pip " \
                    "build-essential"
                    )
        base.append("\nCOPY poc.py .")
        base.append(f"RUN python -m pip install {pkg}{filter}")
        base.append("\nCMD [\"python\", \"poc.py\"]")
               
    return base

def pyStr_template(base, pathFile, os, eco, pkg, filter):
    if "py3" in eco:
        base.append("RUN apt-get update && apt-get install -y " \
        "python3 " \
        "python3-dev " \
        "python3-pip " \
        "python3-venv " \
        "curl " \
        "wget " \
        "build-essential"
        )
        print("Str ", pathFile.exists())
        if pathFile.exists():
            base.append("COPY requirements.txt .")
            if float(os.split(":")[1]) > 23.04: 
                base.append("RUN python3 -m venv /venv\n" \
                            "ENV PATH=\"/venv/bin:$PATH\"")
                base.append("RUN python3 -m pip install --no-cache-dir -r requirements.txt")
                base.append("\nCOPY poc.py .")
                base.append("\nCMD [\"python3\", \"poc.py\"]") 
            else:
                base.append("RUN python3 -m pip install --no-cache-dir -r requirements.txt")
                base.append("\nCOPY poc.py .")
                base.append("\nCMD [\"python3\", \"poc.py\"]") 
        else:
            base.append(f"RUN python3 -m pip install {pkg}{filter}")
            base.append("\nCOPY poc.py .")
            base.append("\nCMD [\"python3\", \"poc.py\"]") 
    else:
        base.append("RUN apt-get update && apt-get install -y " \
                    "python " \
                    "python-dev " \
                    "python-pip " \
                    "build-essential"
                    )
        base.append("\nCOPY poc.py .")
        base.append(f"RUN python -m pip install {pkg}{filter}")
        base.append("\nCMD [\"python\", \"poc.py\"]")
               
    return base

def requirementsErrors(installs):
    '''
    About: Function to handle errors if test build file is not successful
    Input: Reads in parse error data from build and applies changes to requirements.txt
    Output: Dependency appended to requirements.txt 
    '''
    _, error = installs
    print("Errors ", error)
    if Path("requirements.txt").exists():
        try:
            with open("requirements.txt", "r") as df:
                req = df.read().lower()
        except:
            req = ""
        mod = [re.search(r"named\s+'(.+?)'", i).group(1) for i in error if re.search(r"named\s+'(.+?)'", i)]
        print("MOD ", mod)
        for i in mod:
            print(i)
            if i not in req:
                with open("requirements.txt", "a") as file:
                    if req and not req.endswith('\n'):
                        file.write('\n')
                    file.write(f"{i}\n")
        print("REQUIRE", Path("requirements.txt").read_text())

def build_Dockerfile(name):
    cmd = ["docker", "build", "--no-cache", "-t", f"{name.lower()}:latest", "."]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        #print("Dockerfile built successfully")
        return True
    else:
        errors = [i for i in result.stderr.split('\n')]
        return False, errors
    
def run_Image(name):
    cmd = ["docker", "run", "--rm", "-it", f"{name.lower()}:latest"]
    print(cmd)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Dockerfile success")
        return True
    else:
        errors = [i for i in result.stdout.split('\n') if "ModuleNotFoundError:" in i]
        #return False, errors
        #print("returncode:", result.returncode)
        #print("stdout:", repr(result.stdout))
        #print("stderr:", repr(result.stderr))
        return False, errors

def makeRequirements(path, graph):
        if "artifact:0" in path:
            pos = path.index("artifact:0")
            whl = graph.g.nodes[path[pos]]["url"]
            fileExtn = (".whl", "tar.gz")
            if whl is not None and whl.endswith(fileExtn):
                #print("\nFOR LOOP\n")
                with open("requirements.txt", "w") as f:
                    f.write(whl)
            print(Path("requirements.txt").read_text())