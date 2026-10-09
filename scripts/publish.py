#!/usr/bin/env python3
"""Publish the game to GitHub Pages.

Usage:  python3 scripts/publish.py <path-to-game.html> ["commit message"]

Copies the single-file game into index.html, adds the home-screen
(PWA) tags and service worker registration, then commits and pushes
to main. GitHub Pages rebuilds automatically within a minute or two.
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEAD = """<meta name="theme-color" content="#1b1433">
<link rel="manifest" href="manifest.json">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
"""
SW = "<script>if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    msg = sys.argv[2] if len(sys.argv) > 2 else "Update game"
    if 'rel="manifest"' not in src:
        if "</head>" not in src:
            sys.exit("game file has no </head>")
        src = src.replace("</head>", HEAD + "</head>", 1)
    if "serviceWorker" not in src:
        src = src.replace("</body>", SW + "</body>", 1) if "</body>" in src else src + SW
    (ROOT / "index.html").write_text(src, encoding="utf-8")

    def git(*a):
        return subprocess.run(["git", "-C", str(ROOT), *a], check=True, capture_output=True, text=True).stdout

    git("add", "-A")
    if not git("status", "--porcelain").strip():
        print("No changes to publish.")
        return
    git("commit", "-q", "-m", msg)
    git("fetch", "-q", "origin", "+refs/heads/main:refs/remotes/origin/main")
    git("rebase", "-q", "origin/main")
    git("push", "-q", "origin", "HEAD:main")
    print("Published:", git("log", "--oneline", "-1").strip())
    print("Live in 1-2 min: https://arielshary100-sys.github.io/city-game/")


if __name__ == "__main__":
    main()
