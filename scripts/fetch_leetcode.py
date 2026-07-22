#!/usr/bin/env python3
"""Fetch LeetCode stats for a user and regenerate the DSA card SVGs.
Exits non-zero and writes nothing on failure (never clobbers good cards)."""
import json, os, sys, urllib.request

USER = os.environ.get("LEETCODE_USER", "JothishKamal")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
GQL = "https://leetcode.com/graphql"

DARK = {"bg": "#0D1117", "panel": "#161B22", "border": "#30363D",
        "text": "#E6EDF3", "muted": "#8B949E", "accent": "#00ADD8", "signal": "#3FB950"}
LIGHT = {"bg": "#FFFFFF", "panel": "#F6F8FA", "border": "#D0D7DE",
         "text": "#1F2328", "muted": "#636C76", "accent": "#0969DA", "signal": "#1A7F37"}


def query(q, variables):
    body = json.dumps({"query": q, "variables": variables}).encode()
    req = urllib.request.Request(GQL, data=body,
        headers={"Content-Type": "application/json", "Referer": "https://leetcode.com",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]


def fetch():
    q = """query($u:String!){matchedUser(username:$u){
      submitStatsGlobal{acSubmissionNum{difficulty count}}
      userCalendar{streak totalActiveDays}}}"""
    d = query(q, {"u": USER})["matchedUser"]
    nums = {x["difficulty"]: x["count"] for x in d["submitStatsGlobal"]["acSubmissionNum"]}
    cal = d["userCalendar"]
    return {"all": nums["All"], "easy": nums["Easy"], "medium": nums["Medium"],
            "hard": nums["Hard"], "streak": cal["streak"], "active": cal["totalActiveDays"]}


def render(s, t):
    def stat(x, label, value, color):
        return (f'<text x="{x}" y="98" font-size="26" fill="{color}" '
                f'font-family="ui-monospace,monospace">{value}</text>'
                f'<text x="{x}" y="118" font-size="11" fill="{t["muted"]}" '
                f'font-family="ui-monospace,monospace">{label}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 150" width="440" height="150" role="img" aria-label="LeetCode DSA stats">
  <rect x="1" y="1" width="438" height="148" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
  <text x="24" y="36" font-size="14" fill="{t['muted']}" font-family="ui-monospace,monospace">DSA <tspan fill="{t['border']}">/</tspan> LeetCode</text>
  <text x="24" y="66" font-size="30" fill="{t['text']}" font-family="ui-monospace,monospace">{s['all']}<tspan font-size="14" fill="{t['muted']}"> solved</tspan></text>
  {stat(24, "Medium", s['medium'], t['accent'])}
  {stat(150, "Hard", s['hard'], t['text'])}
  {stat(250, "Active Days", s['active'], t['text'])}
  {stat(370, "Streak", s['streak'], t['signal'])}
</svg>
'''


def main():
    try:
        s = fetch()
    except Exception as e:
        print(f"leetcode fetch failed: {e}", file=sys.stderr)
        return 1
    for name, t in (("dark", DARK), ("light", LIGHT)):
        path = os.path.normpath(os.path.join(OUT, f"leetcode-{name}.svg"))
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(s, t))
        print("wrote", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
