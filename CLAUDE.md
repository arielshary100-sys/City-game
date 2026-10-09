# עיר ללא חוקים 3D — notes for Claude

- The whole game is one self-contained HTML file. `index.html` here is the published copy.
- Live site (GitHub Pages, branch `main`, root): https://arielshary100-sys.github.io/City-game/
- The owner also has a Claude artifact of the same game; keep both in sync.

## Rule from the owner: every code change goes online

After ANY change to the game, in the same turn:
1. Syntax-check the main `<script>` (extract it and run `node --check`).
2. Republish the Claude artifact (if one is in use in the conversation).
3. Publish to GitHub Pages:
   `python3 scripts/publish.py <path-to-updated-game.html> "<short description of the change>"`
   End the commit message with the session attribution lines the system asks for.
4. Tell the owner it's live at the link above (it rebuilds in 1–2 minutes).

`publish.py` adds the home-screen tags and service worker automatically, so pass it the
plain game file. `sw.js` is network-first, so players get new versions on reload.
