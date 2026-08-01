import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"

def make_ascii_svg(image_path="photo.jpg"):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not read {image_path}. Make sure the file exists.")
        return
        
    img = cv2.resize(img, (100, 53))
    
    svg_lines = []
    for i, row in enumerate(img):
        line_chars = []
        for pixel in row:
            ramp_idx = int(((255 - pixel) / 255) * (len(RAMP) - 1))
            char = RAMP[ramp_idx]
            
            if char == '<': char = '&lt;'
            elif char == '>': char = '&gt;'
            elif char == '&': char = '&amp;'
            line_chars.append(char)
            
        line_str = "".join(line_chars)
        delay = i * 0.05  
        
        svg_lines.append(f'<text class="line" x="0" y="{i*7}" style="animation-delay: {delay}s" xml:space="preserve">{line_str}</text>')
        
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="370" height="370" viewBox="0 0 600 400">
      <style>
        .line {{
          font-family: monospace;
          font-size: 8px;
          fill: #c9d1d9; 
          opacity: 0;
          animation: type 0.1s forwards;
        }}
        @keyframes type {{
          to {{ opacity: 1; }}
        }}
      </style>
      <rect width="100%" height="100%" fill="#0d1117" />
      <g transform="translate(10, 20)">
        {''.join(svg_lines)}
      </g>
    </svg>"""
    
    with open("avi-ascii.svg", "w") as f:
        f.write(svg_content)
    print("Generated avi-ascii.svg successfully.")

if __name__ == "__main__":
    make_ascii_svg()