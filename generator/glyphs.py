"""Extract Material Icons glyphs as SVG paths from the app's tree-shaken release font.

The OTF at build/macos/.../MaterialIcons-Regular.otf contains exactly the 211 glyphs
the shipped app uses, so every icon extracted here is 1:1 with the real app.
Codepoints resolve via the Flutter SDK's icons.dart (Icons.* names).
"""
import functools, re

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

OTF = ("/Users/claramunro/Documents/GitHub/hedy_mobile/build/macos/Build/Products/"
       "Release/App.framework/Versions/A/Resources/flutter_assets/fonts/MaterialIcons-Regular.otf")
# Full SDK font: fallback for icons referenced in code newer than the last release build.
OTF_FULL = ("/Users/claramunro/Documents/GitHub/flutter/bin/cache/artifacts/"
            "material_fonts/MaterialIcons-Regular.otf")
ICONS_DART = "/Users/claramunro/Documents/GitHub/flutter/packages/flutter/lib/src/material/icons.dart"


@functools.lru_cache(maxsize=2)
def _font(path=OTF):
    return TTFont(path)


@functools.lru_cache(maxsize=1)
def _name_to_cp():
    src = open(ICONS_DART, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"static const IconData (\w+) = IconData\(\s*0x(\w+)", src):
        out.setdefault(m.group(1), int(m.group(2), 16))
    return out


@functools.lru_cache(maxsize=None)
def material_path(name):
    """SVG path data for Icons.<name>, normalized to a 24x24 viewBox (y-down)."""
    font = _font()
    cp = _name_to_cp()[name]
    cmap = font.getBestCmap()
    if cp not in cmap:
        font = _font(OTF_FULL)
        cmap = font.getBestCmap()
    if cp not in cmap:
        raise KeyError(f"Icons.{name} (U+{cp:04X}) not in either Material font")
    glyph_set = font.getGlyphSet()
    pen = SVGPathPen(glyph_set)
    glyph_set[cmap[cp]].draw(pen)
    d = pen.getCommands()
    upem = font["head"].unitsPerEm  # font units, y-up; flip and scale to 24px
    ascender = font["hhea"].ascent
    s = 24 / upem
    return d, s, ascender


def material(name, size, cls=""):
    """Inline SVG for Icons.<name> at `size`px, filled with currentColor."""
    d, s, asc = material_path(name)
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" fill="currentColor" '
            f'xmlns="http://www.w3.org/2000/svg"><path transform="scale({s:g},-{s:g}) '
            f'translate(0,-{asc})" d="{d}"/></svg>')


if __name__ == "__main__":
    for n in ["info_outline", "more_vert", "edit", "content_copy", "download",
              "auto_awesome", "close", "delete_outline", "help_outline", "arrow_downward"]:
        try:
            svg = material(n, 20)
            print(n, "ok", len(svg), "bytes")
        except KeyError as e:
            print(n, "MISSING:", e)
