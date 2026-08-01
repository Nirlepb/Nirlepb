import os


def generate_info_card():
    svg_template = """<svg xmlns="http://www.w3.org/2000/svg" width="490" height="370" viewBox="0 0 490 370">
  <defs>
    <linearGradient id="cardBg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e1033"/>
      <stop offset="50%" stop-color="#160f28"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="borderGlow2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff6ec4"/>
      <stop offset="33%" stop-color="#7873f5"/>
      <stop offset="66%" stop-color="#4ade80"/>
      <stop offset="100%" stop-color="#fbbf24"/>
    </linearGradient>
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff6ec4"/>
      <stop offset="100%" stop-color="#7873f5"/>
    </linearGradient>
    <style>
      .text { font-family: 'Segoe UI', sans-serif; font-size: 15px; fill: #e6edf3; opacity: 0; animation: fadeIn 0.5s forwards; }
      .label { font-weight: 700; }
      .val { fill: #c9d1d9; }
      @keyframes fadeIn { to { opacity: 1; transform: translateX(0); } }
      .row-1 { animation-delay: 0.2s; }
      .row-2 { animation-delay: 0.4s; }
      .row-3 { animation-delay: 0.6s; }
      .row-4 { animation-delay: 0.8s; }
      .chip { opacity: 0; animation: pop 0.4s forwards; }
      @keyframes pop { to { opacity: 1; } }
    </style>
  </defs>

  <rect x="2" y="2" width="486" height="366" rx="18" fill="url(#cardBg2)" stroke="url(#borderGlow2)" stroke-width="2.5"/>

  <circle cx="455" cy="30" r="3" fill="#fbbf24">
    <animate attributeName="opacity" values="0.2;1;0.2" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="30" cy="335" r="2.5" fill="#4ade80">
    <animate attributeName="opacity" values="1;0.3;1" dur="2.8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="470" cy="200" r="2" fill="#ff6ec4">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite"/>
  </circle>

  <text x="30" y="48" font-family="'Segoe UI', sans-serif" font-weight="800" font-size="24" fill="url(#titleGrad)">👋 Hey, I'm Nirlep</text>
  <text x="30" y="70" font-family="'Segoe UI', sans-serif" font-size="13" fill="#9ca3af">nirlepb · github.com/nirlepb</text>

  <line x1="30" y1="86" x2="460" y2="86" stroke="#30363d" stroke-width="1"/>

  <g class="text row-1" transform="translate(30, 118)">
    <circle cx="-11" cy="-6" r="14" fill="#7873f5" opacity="0.2"/>
    <text x="-16" y="0" font-size="16">💼</text>
    <text x="20" y="-2" class="label" fill="#a78bfa">Role</text>
    <text x="20" y="18" class="val">Java Developer · Full-Stack &amp; AI</text>
  </g>

  <g class="text row-2" transform="translate(30, 178)">
    <circle cx="-11" cy="-6" r="14" fill="#4ade80" opacity="0.2"/>
    <text x="-16" y="0" font-size="16">🎓</text>
    <text x="20" y="-2" class="label" fill="#4ade80">Education</text>
    <text x="20" y="18" class="val">B.Tech CSE @ Amrita Vishwa</text>
  </g>

  <g class="text row-3" transform="translate(30, 238)">
    <circle cx="-11" cy="-6" r="14" fill="#f97316" opacity="0.2"/>
    <text x="-16" y="0" font-size="16">⚡</text>
    <text x="20" y="-2" class="label" fill="#fb923c">Skills</text>
    <g transform="translate(20, 12)">
      <rect class="chip" x="0" y="0" width="52" height="24" rx="12" fill="#1f2937" stroke="#f97316" style="animation-delay: 0.9s"/>
      <text class="chip" x="26" y="16" font-size="12" fill="#fdba74" text-anchor="middle" style="animation-delay: 0.9s">Java</text>
      <rect class="chip" x="60" y="0" width="48" height="24" rx="12" fill="#1f2937" stroke="#ff6ec4" style="animation-delay: 1.0s"/>
      <text class="chip" x="84" y="16" font-size="12" fill="#f9a8d4" text-anchor="middle" style="animation-delay: 1.0s">DSA</text>
      <rect class="chip" x="116" y="0" width="66" height="24" rx="12" fill="#1f2937" stroke="#4ade80" style="animation-delay: 1.1s"/>
      <text class="chip" x="149" y="16" font-size="12" fill="#86efac" text-anchor="middle" style="animation-delay: 1.1s">Python</text>
    </g>
  </g>

  <g class="text row-4" transform="translate(30, 312)">
    <circle cx="-11" cy="-6" r="14" fill="#fbbf24" opacity="0.2"/>
    <text x="-16" y="0" font-size="16">🏆</text>
    <text x="20" y="-2" class="label" fill="#fde047">Certification</text>
    <text x="20" y="18" class="val">Oracle Java Foundations</text>
  </g>
</svg>"""

    with open("info-card.svg", "w") as f:
        f.write(svg_template)
    print("Generated info-card.svg successfully.")


if __name__ == "__main__":
    generate_info_card()