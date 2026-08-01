import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"

# how coarsely to bucket colors so runs of identical color group into
# a single <tspan> (keeps the SVG small instead of one tspan per pixel)
QUANT_STEP = 48


def _quantize_bgr(bgr):
    b, g, r = (int(c) for c in bgr)
    step = QUANT_STEP
    q = lambda c: min(255, (c // step) * step + step // 2)
    return q(b), q(g), q(r)


def _boost(bgr, sat_factor=1.35, val_factor=1.15):
    """Push saturation/value up a bit so the ascii art reads as vivid,
    not washed-out like a raw photo."""
    pixel = np.uint8([[bgr]])
    h, s, v = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0][0]
    s = min(255, int(s * sat_factor))
    v = min(255, int(v * val_factor))
    boosted = cv2.cvtColor(np.uint8([[[h, s, v]]]), cv2.COLOR_HSV2BGR)[0][0]
    return tuple(int(c) for c in boosted)


def _bgr_to_hex(bgr):
    b, g, r = bgr
    return f"#{r:02x}{g:02x}{b:02x}"


def _escape(ch):
    return {"<": "&lt;", ">": "&gt;", "&": "&amp;"}.get(ch, ch)


def make_ascii_svg(image_path="photo.jpg"):
    img = cv2.imread(image_path)  # color (BGR), not grayscale
    if img is None:
        print(f"Error: Could not read {image_path}. Make sure the file exists.")
        return

    img = cv2.resize(img, (100, 53))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    svg_lines = []
    for i in range(img.shape[0]):
        row_gray = gray[i]
        row_color = img[i]

        # build runs of (char, color) so identical consecutive pixels
        # collapse into one <tspan> instead of one per pixel
        runs = []
        for x in range(len(row_gray)):
            ramp_idx = int(((255 - int(row_gray[x])) / 255) * (len(RAMP) - 1))
            char = RAMP[ramp_idx]

            if char == " ":
                color_hex = None  # keep background showing through
            else:
                boosted = _boost(row_color[x])
                color_hex = _bgr_to_hex(_quantize_bgr(boosted))

            if runs and runs[-1][0] == char and runs[-1][1] == color_hex:
                runs[-1][2] += 1
            else:
                runs.append([char, color_hex, 1])

        tspans = []
        for char, color_hex, count in runs:
            text_chunk = _escape(char) * count
            fill = color_hex if color_hex else "#0d1117"
            tspans.append(f'<tspan fill="{fill}">{text_chunk}</tspan>')

        delay = i * 0.03
        svg_lines.append(
            f'<text class="line" x="0" y="{i * 7}" '
            f'style="animation-delay: {delay}s" xml:space="preserve">'
            f'{"".join(tspans)}</text>'
        )

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="370" height="370" viewBox="0 0 620 420">
      <defs>
        <linearGradient id="avatarBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e1033"/>
          <stop offset="50%" stop-color="#160f28"/>
          <stop offset="100%" stop-color="#0d1117"/>
        </linearGradient>
        <linearGradient id="avatarBorder" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ff6ec4"/>
          <stop offset="33%" stop-color="#7873f5"/>
          <stop offset="66%" stop-color="#4ade80"/>
          <stop offset="100%" stop-color="#fbbf24"/>
        </linearGradient>
        <style>
          .line {{
            font-family: monospace;
            font-size: 8px;
            opacity: 0;
            animation: type 0.15s forwards;
          }}
          @keyframes type {{
            to {{ opacity: 1; }}
          }}
        </style>
      </defs>
      <rect x="2" y="2" width="616" height="416" rx="16" fill="url(#avatarBg)" stroke="url(#avatarBorder)" stroke-width="2.5"/>

      <circle cx="580" cy="30" r="3" fill="#fbbf24">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2.3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="35" cy="390" r="2.5" fill="#4ade80">
        <animate attributeName="opacity" values="1;0.3;1" dur="2.8s" repeatCount="indefinite"/>
      </circle>

      <g transform="translate(30, 30)">
        {''.join(svg_lines)}
      </g>
    </svg>"""

    with open("avi-ascii.svg", "w") as f:
        f.write(svg_content)
    print("Generated avi-ascii.svg successfully.")


if __name__ == "__main__":
    make_ascii_svg()