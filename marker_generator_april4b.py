import cv2
import numpy as np
from svgwrite import Drawing, rgb

import cv2
import numpy as np
from cv2 import aruco

def generate_aruco_marker(marker_id, output_filename_base, size=189, scale_factor=10):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36H11)
    marker = aruco_dict.generateImageMarker(marker_id, size)
    marker = np.array(marker)
    h, w = marker.shape
    marker = cv2.resize(marker, (w, h+2), interpolation=cv2.INTER_NEAREST)
    h, w = marker.shape

    # Generate SVG file
    svg_filename = output_filename_base.replace('.svg', '') + '.svg'
    svg_image = Drawing(filename=svg_filename, size=(f"{w}px", f"{h}px"))
    for y in range(h):
        for x in range(w):
            color = "black" if marker[y][x] == 0 else "white"
            svg_image.add(svg_image.rect(insert=(x, y), size=(1, 1), fill=color))

    svg_image.save()

    # Generate PNG file
    png_filename = output_filename_base.replace('.svg', '') + '.png'
    # Normalize marker to 0-255 range
    marker_normalized = (marker.astype(np.float32) / marker.max() * 255).astype(np.uint8)
    # Scale up the marker for better visibility in PNG
    marker_scaled = cv2.resize(marker_normalized, (w * scale_factor, h * scale_factor), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(png_filename, marker_scaled)

if __name__ == "__main__":
    marker_ids = [4,8,12, 14, 20]
    
    marker_sizes = [5]
    
    for marker_id in marker_ids:      
        for marker_size in marker_sizes:
            output_filename = f"APRIL_36_ID{marker_id}_{marker_size}cm.svg"
            px = marker_size / ((1/96.5) * 2.54)
            px = int(px)
            generate_aruco_marker(marker_id, output_filename, size=px)
            print(f"ArUco marker {marker_id} saved as '{output_filename}'")

    

