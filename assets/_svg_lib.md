# SVG conventions

Tokens (dark): bg #0D1117, panel #161B22, border #30363D, text #E6EDF3,
muted #8B949E, accent #00ADD8, signal #3FB950.
Tokens (light): bg #FFFFFF, panel #F6F8FA, border #D0D7DE, text #1F2328,
muted #636C76, accent #0969DA, signal #1A7F37.

Font: font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace"

Reusable node box (12px radius, hairline border, label centered):
```svg
<g>
  <rect x="X" y="Y" width="150" height="44" rx="8" fill="{panel}" stroke="{border}"/>
  <text x="X+75" y="Y+27" text-anchor="middle" font-size="13" fill="{text}"
        font-family="ui-monospace,'SF Mono','Cascadia Code','JetBrains Mono',monospace">LABEL</text>
</g>
```

Arrow marker (define once per file in <defs>):
```svg
<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
        markerHeight="7" orient="auto-start-reverse">
  <path d="M0 0 L10 5 L0 10 z" fill="{accent}"/>
</marker>
```
Connector: <line ... stroke="{accent}" stroke-width="1.5" marker-end="url(#arw)"/>
