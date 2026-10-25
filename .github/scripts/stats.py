"""Generates local dark/light stats + contribution heatmap SVGs for a GitHub profile.
Uses only the Python standard library and the GitHub GraphQL API (token from GH_TOKEN)."""
import os, json, math, html, urllib.request, datetime as dt

THEMES = {
    "dark":  dict(card="#0d1117", border="#30363d", txt="#c9d1d9", mut="#8b949e", a1="#a78bfa", a2="#ec4899",
                  track="#21262d", lv=["#161b22", "#3b2a6b", "#6d3fd1", "#a78bfa", "#ec4899"]),
    "light": dict(card="#ffffff", border="#d0d7de", txt="#1f2328", mut="#57606a", a1="#7c3aed", a2="#db2777",
                  track="#eaeef2", lv=["#ebedf0", "#e9d5ff", "#c4b5fd", "#8b5cf6", "#db2777"]),
}
FALLBACK = ["#a78bfa", "#ec4899", "#38bdf8", "#f59e0b", "#22c55e", "#f97316"]
FONT = "font-family:'Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif"

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    pullRequests{totalCount}
    issues{totalCount}
    repositories(ownerAffiliations:OWNER, isFork:false, first:100, privacy:PUBLIC){
      totalCount
      nodes{ stargazerCount
        languages(first:6, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions
      contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount weekday } } }
    }
  }
}"""

def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": "bearer " + token, "Content-Type": "application/json", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
    if res.get("errors"):
        raise SystemExit(json.dumps(res["errors"]))
    u = res["data"]["user"]
    repos = u["repositories"]["nodes"]
    langs = {}
    for r_ in repos:
        for e in r_["languages"]["edges"]:
            n = e["node"]["name"]
            cur = langs.setdefault(n, [0, e["node"]["color"]])
            cur[0] += e["size"]
    total = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    lang_list = [(n, v[1] or FALLBACK[i % len(FALLBACK)], 100.0 * v[0] / total) for i, (n, v) in enumerate(top)]
    cal = u["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["date"], d["contributionCount"], d["weekday"]) for d in w["contributionDays"]] for w in cal["weeks"]]
    flat = sorted((d for w in weeks for d in w), key=lambda d: d[0])
    cur_streak = 0
    seq = [d[1] for d in flat]
    if seq and seq[-1] == 0:
        seq = seq[:-1]
    for c in reversed(seq):
        if c > 0: cur_streak += 1
        else: break
    longest = run = 0
    for d in flat:
        run = run + 1 if d[1] > 0 else 0
        longest = max(longest, run)
    return dict(
        stars=sum(r_["stargazerCount"] for r_ in repos),
        commits=u["contributionsCollection"]["totalCommitContributions"],
        prs=u["pullRequests"]["totalCount"], issues=u["issues"]["totalCount"],
        repos=u["repositories"]["totalCount"], followers=u["followers"]["totalCount"],
        langs=lang_list, total=cal["totalContributions"], current=cur_streak, longest=longest, weeks=weeks)

def esc(s): return html.escape(str(s), quote=True)

def render_stats(t, d):
    c = THEMES[t]
    W, H = 900, 312
    dash = "\u2014"
    g = (lambda k: f"{d[k]:,}") if d else (lambda k: dash)
    items = [("Stars", g("stars")), ("Commits \u00b7 past year", g("commits")), ("Pull requests", g("prs")),
             ("Issues", g("issues")), ("Public repos", g("repos")), ("Followers", g("followers"))]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub stats">',
         f'<defs><style>text{{{FONT}}}.v{{font-size:30px;font-weight:700}}.l{{font-size:13px;fill:{c["mut"]}}}'
         f'@keyframes up{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}'
         f'.i{{animation:up .7s both}}</style>'
         f'<clipPath id="bar"><rect x="510" y="76" width="350" height="10" rx="5"/></clipPath></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["card"]}" stroke="{c["border"]}" stroke-width="2"/>']
    for i, (lab, val) in enumerate(items):
        col, row = i % 2, i // 2
        x, y = 40 + col * 210, 56 + row * 62
        clr = c["a1"] if (row + col) % 2 == 0 else c["a2"]
        s.append(f'<g class="i" style="animation-delay:{i*0.08:.2f}s"><text class="l" x="{x}" y="{y}">{esc(lab)}</text>'
                 f'<text class="v" x="{x}" y="{y+32}" fill="{clr}">{esc(val)}</text></g>')
    s.append(f'<line x1="470" y1="36" x2="470" y2="216" stroke="{c["border"]}"/>')
    s.append(f'<text class="l" x="510" y="60" style="letter-spacing:1px;text-transform:uppercase">Top languages</text>')
    s.append(f'<rect x="510" y="76" width="350" height="10" rx="5" fill="{c["track"]}"/>')
    if d and d["langs"]:
        x = 510.0
        segs = []
        for n, col, pct in d["langs"]:
            w = 350.0 * pct / sum(p for _, _, p in d["langs"])
            segs.append(f'<rect x="{x:.1f}" y="76" width="{w:.1f}" height="10" fill="{esc(col)}"/>')
            x += w
        s.append('<g clip-path="url(#bar)">' + "".join(segs) + '</g>')
        for i, (n, col, pct) in enumerate(d["langs"]):
            cx, cy = 510 + (i % 2) * 180, 118 + (i // 2) * 30
            s.append(f'<circle cx="{cx+5}" cy="{cy-4}" r="5" fill="{esc(col)}"/>'
                     f'<text x="{cx+18}" y="{cy}" font-size="14" fill="{c["txt"]}">{esc(n)} '
                     f'<tspan fill="{c["mut"]}">{pct:.1f}%</tspan></text>')
    else:
        s.append(f'<text x="510" y="120" font-size="13" fill="{c["mut"]}">Fills in after the first workflow run</text>')
    s.append(f'<line x1="30" y1="240" x2="{W-30}" y2="240" stroke="{c["border"]}"/>')
    bottom = [("Contributions \u00b7 past year", g("total") if d else dash),
              ("Current streak", f'{d["current"]} day' + ('' if d["current"] == 1 else 's') if d else dash),
              ("Longest streak", f'{d["longest"]} day' + ('' if d["longest"] == 1 else 's') if d else dash)]
    for i, (lab, val) in enumerate(bottom):
        x = 150 + i * 300
        clr = [c["a1"], c["a2"], c["a1"]][i]
        s.append(f'<text x="{x}" y="276" text-anchor="middle" font-size="24" font-weight="700" fill="{clr}">{esc(val)}</text>'
                 f'<text x="{x}" y="298" text-anchor="middle" class="l">{esc(lab)}</text>')
    s.append('</svg>')
    return "\n".join(s)

def render_heatmap(t, d):
    c = THEMES[t]
    W, H = 900, 178
    pitch, cell, x0, y0 = 15, 12, 46, 38
    weeks = d["weeks"] if d else [[(None, 0, k) for k in range(7)] for _ in range(53)]
    mx = max([day[1] for w in weeks for day in w] + [1])
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribution heatmap">',
         f'<defs><style>text{{{FONT};font-size:11px;fill:{c["mut"]}}}@keyframes pop{{from{{opacity:0}}to{{opacity:1}}}}'
         f'.c{{animation:pop .5s both}}</style></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["card"]}" stroke="{c["border"]}" stroke-width="2"/>']
    for lab, wd in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        s.append(f'<text x="14" y="{y0 + wd*pitch + 10}">{lab}</text>')
    prev_m, last = None, -9
    for wi, w in enumerate(weeks):
        if w[0][0]:
            m = int(w[0][0][5:7])
            if m != prev_m:
                if wi - last >= 3:
                    s.append(f'<text x="{x0 + wi*pitch}" y="{y0-10}">{dt.date(2000, m, 1).strftime("%b")}</text>')
                    last = wi
                prev_m = m
        for (date, cnt, wd) in w:
            lvl = 0 if cnt <= 0 else max(1, min(4, math.ceil(4 * cnt / mx)))
            tip = f'<title>{cnt} contributions on {date}</title>' if date else ''
            s.append(f'<rect class="c" style="animation-delay:{wi*0.025:.2f}s" x="{x0 + wi*pitch}" y="{y0 + wd*pitch}" '
                     f'width="{cell}" height="{cell}" rx="3" fill="{c["lv"][lvl]}">{tip}</rect>')
    lx = W - 40 - 5 * pitch - 70
    s.append(f'<text x="{lx}" y="{H-14}">Less</text>')
    for k in range(5):
        s.append(f'<rect x="{lx+32+k*pitch}" y="{H-24}" width="{cell}" height="{cell}" rx="3" fill="{c["lv"][k]}"/>')
    s.append(f'<text x="{lx+32+5*pitch+4}" y="{H-14}">More</text>')
    s.append('</svg>')
    return "\n".join(s)

def write_all(d, outdir):
    os.makedirs(outdir, exist_ok=True)
    for t in THEMES:
        open(os.path.join(outdir, f"stats-{t}.svg"), "w", encoding="utf-8").write(render_stats(t, d))
        open(os.path.join(outdir, f"heatmap-{t}.svg"), "w", encoding="utf-8").write(render_heatmap(t, d))

if __name__ == "__main__":
    data = fetch(os.environ["GH_USER"], os.environ["GH_TOKEN"])
    write_all(data, os.environ.get("OUT_DIR", "assets"))
    print("stats written")
