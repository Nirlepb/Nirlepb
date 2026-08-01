import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

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
        
        rect = f'<rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" rx="2" class="box" style="animation-delay: {delay}s"/>'
        svg_elements.append(rect)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="150" viewBox="0 -20 860 150">
      <style>
        .box {{
          opacity: 0;
          transform: translateY(-10px);
          animation: dropIn 0.5s ease-out forwards;
        }}
        @keyframes dropIn {{
          to {{ opacity: 1; transform: translateY(0); }}
        }}
      </style>
      <g transform="translate(20, 20)">
        {''.join(svg_elements)}
      </g>
    </svg>"""

    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg_content)
    print("Generated contrib-heatmap.svg successfully.")

if __name__ == "__main__":
    render_heatmap()