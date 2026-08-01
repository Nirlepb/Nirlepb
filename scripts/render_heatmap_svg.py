import json

# level 0 (no contributions) -> level 5 (max), recolored from GitHub green
# into the profile's purple -> magenta -> orange -> gold theme
PALETTE = ["#1a1f2e", "#4c1d95", "#a21caf", "#f97316", "#fbbf24", "#fde68a"]


def render_heatmap():
    with open("data/contributions.json", "r") as f:
        data = json.load(f)

    box_size = 11
    gap = 4
    svg_elements = []

    for i, day in enumerate(data):
        week = i // 7
        day_of_week = i % 7

        x = week * (box_size + gap)
        y = day_of_week * (box_size + gap)
        level = min(day["level"], 5)
        color = PALETTE[level]

        delay = (week + day_of_week) * 0.02

        rect = (
            f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'fill="{color}" rx="2" class="box" style="animation-delay: {delay}s"/>'
        )
        svg_elements.append(rect)

    grid_width = ((len(data) // 7) + 1) * (box_size + gap)
    card_width = max(860, grid_width + 40)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{card_width}" height="180" viewBox="0 -20 {card_width} 180">
      <defs>
        <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1e1033"/>
          <stop offset="50%" stop-color="#160f28"/>
          <stop offset="100%" stop-color="#0d1117"/>
        </linearGradient>
        <linearGradient id="borderGlow" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ff6ec4"/>
          <stop offset="33%" stop-color="#a21caf"/>
          <stop offset="66%" stop-color="#f97316"/>
          <stop offset="100%" stop-color="#fbbf24"/>
        </linearGradient>
        <style>
          .box {{ opacity: 0; transform: translateY(-10px); animation: dropIn 0.5s ease-out forwards; }}
          @keyframes dropIn {{ to {{ opacity: 1; transform: translateY(0); }} }}
          .heading {{ font-family: 'Segoe UI', sans-serif; font-weight: 700; font-size: 15px; fill: #fbbf24; }}
        </style>
      </defs>

      <rect x="1" y="-19" width="{card_width - 2}" height="178" rx="14" fill="url(#cardBg)" stroke="url(#borderGlow)" stroke-width="2"/>
      <text x="20" y="0" class="heading">✨ Contribution Activity</text>

      <g transform="translate(20, 20)">
        {''.join(svg_elements)}
      </g>

      <g transform="translate(20, 148)" font-family="monospace" font-size="10" fill="#9ca3af">
        <text x="0" y="0">Less</text>
        <rect x="35" y="-9" width="10" height="10" rx="2" fill="{PALETTE[0]}"/>
        <rect x="48" y="-9" width="10" height="10" rx="2" fill="{PALETTE[1]}"/>
        <rect x="61" y="-9" width="10" height="10" rx="2" fill="{PALETTE[2]}"/>
        <rect x="74" y="-9" width="10" height="10" rx="2" fill="{PALETTE[3]}"/>
        <rect x="87" y="-9" width="10" height="10" rx="2" fill="{PALETTE[4]}"/>
        <text x="102" y="0">More</text>
      </g>
    </svg>"""

    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg_content)
    print("Generated contrib-heatmap.svg successfully.")


if __name__ == "__main__":
    render_heatmap()
