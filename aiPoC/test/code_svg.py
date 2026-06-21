from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import logging

logging.getLogger("svglib").setLevel(logging.CRITICAL)

saved_image_path = 'test_png.png'
image_path = "./test.svg"

drawing = svg2rlg(image_path)
renderPM.drawToFile(drawing, saved_image_path, fmt="PNG")
