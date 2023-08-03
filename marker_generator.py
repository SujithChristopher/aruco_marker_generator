import cv2
import numpy as np
from svgwrite import Drawing, rgb

import cv2
import numpy as np
from svgwrite import Drawing, rgb
from cv2 import aruco

def generate_aruco_marker(marker_id, output_filename, size=189, border=1):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_MIP_36H12)
    marker = aruco_dict.generateImageMarker(marker_id, size)
    marker = np.array(marker)
    h, w = marker.shape
    marker = cv2.resize(marker, (w, h+2), interpolation=cv2.INTER_NEAREST)
    h, w = marker.shape
    
    # Convert the marker to an SVG image
    svg_image = Drawing(filename=output_filename, size=(f"{w}px", f"{h}px"))
    for y in range(h):
        for x in range(w):
            color = "black" if marker[y][x] == 0 else "white"
            svg_image.add(svg_image.rect(insert=(x, y), size=(1, 1), fill=color))

    svg_image.save()

if __name__ == "__main__":
    marker_ids = [12, 88, 89]
    
    marker_sizes = [4,5]
    
    for marker_id in marker_ids:      
        for marker_size in marker_sizes:
            output_filename = f"MIP_AR_ID{marker_id}_{marker_size}cm.svg"
            px = marker_size / ((1/96.5) * 2.54)
            px = int(px)
            generate_aruco_marker(marker_id, output_filename, size=px)
            print(f"ArUco marker {marker_id} saved as '{output_filename}'")

    

