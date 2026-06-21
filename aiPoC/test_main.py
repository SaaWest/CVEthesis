from poc_generator import *
from make_files import *
from parser import *

def main():
    parse = exploitPoC("https://github.com/deeplook/svglib/issues/229")
    #mid = len(parse) // 2
    context = {
        "cveID": "CVE-2020-10799",
        "pkg": "svglib",
        "version": "0.9.3",
        "ref": [
            "https://github.com/deeplook/svglib/issues/229"
        ],
        "ref_text": parse
    }
    
    result = pocGenerator(context=context)

    writeFile(dir="./test", files=result["files"])

if __name__=="__main__":
    main()
