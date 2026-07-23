#!/usr/bin/env python3
"""Generate linked Hedy HTML twins (1440x900) 1:1 from the hedy_mobile codebase.

One self-contained page per screen/state, linked like a Figma prototype.
All icons/assets sourced from the repo, the app's Lucide glyph set
(lucide-static v0.525.0), or the app's shipped Material Icons font
(via glyphs.material). Only mock data (titles, timestamps, chat) is invented.
"""
import base64, os, re

from glyphs import material

TW = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TW)

DASH = "hedy-sessions-dashboard-light-1440.html"
DETAIL = "hedy-session-detail-light-1440.html"
DETAIL_NOTES = "hedy-session-detail-notes-light-1440.html"
DETAIL_HL = "hedy-session-detail-highlights-light-1440.html"
DETAIL_TRANS = "hedy-session-detail-transcript-light-1440.html"
DETAIL_SETTS = "hedy-session-detail-settings-light-1440.html"
TOPICS = "hedy-topics-light-1440.html"
TOPIC_DETAIL = "hedy-topic-detail-light-1440.html"
HIGHLIGHTS = "hedy-highlights-light-1440.html"
SETTINGS = "hedy-settings-light-1440.html"
SEARCH = "hedy-search-light-1440.html"
MERGE = "hedy-merge-sessions-light-1440.html"
MERGE_CONFIG = "hedy-merge-config-light-1440.html"
SHARE_MGMT = "hedy-share-management-light-1440.html"
CTX_INTRO = "hedy-context-intro-light-1440.html"
CTX_QUESTION = "hedy-context-question-light-1440.html"
CTX_STREAMING = "hedy-context-streaming-light-1440.html"
CTX_REVIEW = "hedy-context-review-light-1440.html"

# ---------- assets ----------
def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

logo_png = "data:image/png;base64," + b64(f"{REPO}/assets/images/hedy-glasses-logo-lovable.png")

glasses_white = open(f"{REPO}/assets/images/hedy-logo-image-glasses-white.svg", encoding="utf-8").read()
glasses_white = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", glasses_white, flags=re.S).strip()
glasses_white = glasses_white.replace("<svg ", '<svg style="height:24px;width:auto" ', 1)

session_play = open(f"{REPO}/assets/images/session-play.svg", encoding="utf-8").read()
session_play = session_play.replace('stroke="black"', 'stroke="currentColor"')
session_play = session_play.replace('width="24" height="24"', 'width="20" height="20"')

# Lucide: variable-weight font — w100..w600 => stroke-width 0.5..3.0 at 24px viewBox
def lucide(name, size, weight=400):
    src = open(f"{TW}/lucide/{name}.svg", encoding="utf-8").read()
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    src = re.sub(r'\s*class="[^"]*"', "", src)
    src = re.sub(r'width="24"', f'width="{size}"', src, count=1)
    src = re.sub(r'height="24"', f'height="{size}"', src, count=1)
    src = re.sub(r'stroke-width="2"', f'stroke-width="{weight/200:g}"', src, count=1)
    return re.sub(r">\s+<", "><", src).replace("\n", "").strip()

# ---------- fonts (Inter, as bundled in the app; embedded data URIs in fonts.css) ----------
fontfaces = open(f"{TW}/fonts.css", encoding="utf-8").read()

CAPTURE = '<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>'

# ---------- shared CSS ----------
CSS = """
:root{
  --orange:#E26515; --ink:#26231A; --bg:#FBFAF9; --card:#FFFFFF;
  --border:#E8E4DE; --icon:#736359; --n40:#6F6F6F;
  --card-title:#2A2522; --card-meta:#8A7C75; --tb-fg:#2B2724;
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-font-smoothing:antialiased}
body{font-family:'Inter',sans-serif;color:var(--ink);width:1440px;height:900px;overflow:hidden;display:flex;position:relative;background:var(--bg)}
a{color:inherit;text-decoration:none}
/* Sidebar: 88px, hedyMenuBarColor #FBFAF9 (no background image — matches the app as Clara runs it) */
.rail{position:relative;z-index:1;width:88px;flex-shrink:0;background:var(--bg);border-right:1px solid rgba(232,228,222,.5);display:flex;flex-direction:column}
.logo{padding:8px 0;display:flex;justify-content:center}
.logo img{height:28px;width:auto}
.navwrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.nav{min-width:64px;margin:4px 8px;padding:8px;border-radius:8px;display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--icon);font-size:10px;line-height:1.2;text-align:center;border:1px solid transparent}
.nav.sel{background:#FFF5F0;border-color:#E8C4B8;color:#2B2724;font-weight:600}
.start{margin:8px;padding:16px 8px;border-radius:8px;background:var(--orange);color:#fff;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;font-weight:500;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.2)}
/* Main */
main{position:relative;z-index:1;flex:1;display:flex;flex-direction:column;min-width:0}
.topbar{min-height:56px;padding:10px 16px;display:flex;align-items:center;gap:8px}
.topbar h1{font-size:18px;font-weight:600;color:var(--ink)}
.count{width:24px;height:24px;border-radius:50%;background:#EEEEEE;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:600;color:var(--n40)}
.sp{flex:1}
.tbtn{display:inline-flex;align-items:center;gap:8px;min-height:36px;padding:8px 12px;border-radius:8px;background:rgba(240,237,233,.5);border:1px solid #E8E3DC;color:var(--tb-fg);font-size:13px;font-weight:500}
.content{flex:1;display:flex;min-height:0}
.listpane{width:300px;flex-shrink:0;display:flex;flex-direction:column;min-height:0}
.sort{padding:0 16px 8px;display:flex;align-items:center;color:var(--tb-fg);font-size:13px;font-weight:500}
.sort .si{margin-right:6px;display:flex}.sort .sc{margin-left:4px;display:flex}
.cards{flex:1;overflow:hidden;padding:0 16px}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;margin-bottom:12px;padding:17px 16px;display:flex;gap:20px;align-items:flex-start}
.card.sel{background:#FFF5F0;border-color:#FFD4C4}
.card .cicon{color:var(--icon);flex-shrink:0;padding-top:2px;display:flex;position:relative}
.icb{position:absolute;top:-4px;right:-4px;width:13px;height:13px;border-radius:50%;background:linear-gradient(180deg,#5BC8FF,#0A8EF0);border:1.5px solid var(--card);display:flex;align-items:center;justify-content:center;color:#fff}
.cc{flex:1;min-width:0}
.ct{font-size:13.3px;color:var(--card-title);line-height:1.4;margin-bottom:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cm{font-size:11.1px;color:var(--card-meta)}
.chip{margin-top:6px;display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:9999px;font-size:10px;font-weight:600}
.chip.amber{background:#FDE68A;color:#92400E}
.chip.peach{background:#FED7AA;color:#9A3412}
.chip.rose{background:#FFE4E6;color:#9F1239}
.chip.mint{background:rgba(16,185,129,.12);color:#059669}
.chip.sky{background:rgba(59,130,246,.12);color:#2563EB}
.year{font-size:14px;font-weight:600;color:var(--n40);padding:12px 0}
.seltopic{margin-top:6px;display:inline-flex;align-items:center;gap:2px;height:28px;padding:0 4px 0 8px;border-radius:6px;background:rgba(238,238,238,.6);border:1px solid #E0E0E0;font-size:11px;color:#757575}
.seltopic svg{margin-right:4px}
/* Empty detail state */
.empty{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px}
.empty .eicon{color:rgba(111,111,111,.5);display:flex}
.empty p{font-size:16px;color:var(--n40)}
/* Detail panel (frosted glass, two columns) */
.detail{flex:1;padding:16px;display:flex;min-width:0}
.glass{flex:1;display:flex;min-width:0;background:rgba(255,255,255,.75);border:1px solid rgba(232,228,222,.5);border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,.06);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);overflow:hidden}
.dleft{flex:1;display:flex;flex-direction:column;min-width:0}
.dhead{padding:12px 16px;display:flex;gap:12px;align-items:flex-start}
.dhead .hicon{color:var(--icon);flex-shrink:0;padding-top:4px;display:flex}
.dht{flex:1;min-width:0}
.dtitle{font-size:18px;font-weight:500;color:var(--ink);line-height:1.3}
.dmeta{margin-top:4px;display:flex;align-items:center;gap:6px;font-size:13px;color:var(--n40)}
.dmeta .chip{margin-top:0}
.mbtn{color:var(--ink);padding:4px;display:flex;align-items:center}
.dsep{height:1px;background:var(--border)}
.tabswrap{padding:12px 16px 0}
.tabs{display:inline-flex;padding:4px;background:rgba(240,237,233,.5);border:1px solid #E8E3DC;border-radius:8px}
.tab{padding:6px 16px;border-radius:6px;font-size:14px;font-weight:500;color:#8A817A}
.tab.sel{background:#FFFFFF;color:#2B2724;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.dbody{flex:1;overflow:hidden;padding:16px}
.pcard{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:16px}
.pchead{display:flex;align-items:center;gap:12px}
.pctitle{font-size:16px;font-weight:500;color:var(--ink)}
.picon{color:var(--ink);opacity:.8;display:flex}
.pcbody{margin-top:12px;font-size:14px;line-height:1.5;color:var(--ink)}
.pcbody p+p{margin-top:10px}
.todo{display:flex;align-items:flex-start;gap:10px;padding:7px 0;font-size:14px;color:var(--ink);line-height:1.4}
.cb{width:18px;height:18px;border-radius:4px;border:2px solid #A8A8A8;flex-shrink:0;margin-top:1px}
.cb.on{background:var(--orange);border-color:var(--orange);display:flex;align-items:center;justify-content:center;color:#fff}
.todo.done span{text-decoration:line-through;color:#9E9E9E}
.player{height:64px;flex-shrink:0;border-top:1px solid var(--border);background:var(--card);display:flex;align-items:center;gap:12px;padding:0 16px}
.ptime{font-size:12px;color:var(--n40);font-variant-numeric:tabular-nums}
.ptrack{flex:1;height:4px;border-radius:2px;background:#E8E4DE;position:relative}
.pfill{position:absolute;left:0;top:0;bottom:0;width:30%;background:var(--orange);border-radius:2px}
.pthumb{position:absolute;left:30%;top:50%;transform:translate(-50%,-50%);width:12px;height:12px;border-radius:50%;background:var(--orange)}
.pspeed{font-size:13px;font-weight:500;color:var(--ink)}
.dsplit{width:1px;flex-shrink:0;background:var(--border)}
.dchat{width:380px;flex-shrink:0;display:flex;flex-direction:column;background:var(--bg)}
.chathead{padding:12px 16px;display:flex;align-items:center;gap:8px}
.cht{font-size:16px;font-weight:600;color:var(--ink)}
.tctx{font-size:13px;color:var(--n40)}
.switch{width:34px;height:18px;border-radius:9px;background:var(--orange);position:relative;flex-shrink:0}
.switch::after{content:"";position:absolute;right:2px;top:2px;width:14px;height:14px;border-radius:50%;background:#fff}
.chatlog{flex:1;overflow:hidden;padding:16px;display:flex;flex-direction:column;gap:8px}
.bubble{max-width:85%;padding:12px 16px;border-radius:16px;font-size:14px;line-height:1.45}
.bubble.user{align-self:flex-end;background:var(--orange);color:#fff}
.bubble.hedy{align-self:flex-start;background:#EEEEEE;color:var(--ink)}
.chatin{padding:12px 16px 16px;display:flex;flex-direction:column;gap:10px}
.chiprow{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.qchip{display:inline-flex;align-items:center;gap:4px;padding:4px 8px;border-radius:16px;background:var(--card);border:1px solid var(--border);font-size:11px;color:var(--n40)}
.qmore{display:inline-flex;align-items:center;gap:4px;font-size:12px;color:var(--orange)}
.inbox{display:flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px 12px}
.inhint{flex:1;font-size:14px;color:var(--n40)}
.send{width:28px;height:28px;border-radius:50%;background:var(--orange);display:flex;align-items:center;justify-content:center;color:#fff;flex-shrink:0}
/* Session Notes tab (session_notes_tab.dart) */
.dbody.notes{display:flex;flex-direction:column}
.ntoolbar{display:flex;align-items:center;padding-bottom:8px}
.nibtn{width:30px;height:30px;border-radius:4px;display:flex;align-items:center;justify-content:center;color:#666666;margin-right:2px}
.nstatus{margin-left:auto;display:flex;align-items:center;gap:8px;font-size:12px}
.nsaved{color:#22C55E}.ncount{color:#808080}
.neditor{flex:1;padding:16px;border-radius:8px;background:var(--card);border:1px solid var(--border);font-size:16px;line-height:1.55;color:var(--ink);overflow:hidden}
.neditor p{margin-bottom:10px}.neditor ul,.neditor ol{margin:0 0 10px 22px}.neditor li{margin-bottom:4px}
/* Highlights tab (session detail) */
.dbody.hl{padding:16px;display:flex}
.hlwrap{flex:1;display:flex;border:1px solid var(--border);border-radius:12px;overflow:hidden}
.hllist{width:256px;flex-shrink:0;padding:12px;overflow:hidden}
.hlitem{margin-bottom:6px;padding:10px 12px;border-radius:8px;background:#F9F7F5;border:1px solid rgba(128,128,128,.2);display:flex;gap:10px;align-items:flex-start}
.hlitem.sel{background:#FFF5F0;border-color:#FFD4C4}
.hlitem .hlic{flex-shrink:0;color:#757575;display:flex;padding-top:1px}
.hlitem.sel .hlic{color:var(--orange)}
.hlt{font-size:14px;font-weight:500;color:var(--ink);line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.hltime{margin-top:6px;display:inline-flex;align-items:center;gap:4px;padding:4px 8px;border-radius:4px;background:rgba(226,101,21,.15);color:var(--orange);font-size:12px;font-weight:600}
.hldetail{flex:1;border:1px solid var(--border);border-radius:12px;background:var(--card);padding:16px;overflow:hidden;min-width:0}
.hldt{font-size:15px;font-weight:600;color:var(--ink);line-height:1.35;margin-bottom:12px}
.hlactions{display:flex;align-items:center;margin-bottom:16px}
.hlbtn{display:inline-flex;align-items:center;gap:4px;padding:4px 6px;border-radius:4px;font-size:12px;color:var(--n40)}
.hlbtn.del{color:#EF4444;margin-left:6px}
.hltime.sm{margin:0 0 0 auto;padding:3px 6px;font-size:11px}
.hlsec{display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:13px;font-weight:600;color:var(--ink)}
.hlsec svg{color:var(--orange)}
.hlbox{padding:12px;border-radius:8px;background:rgba(240,237,233,.2);font-size:14px;line-height:1.5;color:rgba(0,0,0,.87);margin-bottom:14px}
.hlbox.q{font-style:italic}
/* Transcript tab */
.dbody.trans{padding:16px;display:flex;flex-direction:column;position:relative}
.tdisc{display:flex;align-items:flex-start;gap:12px;padding:12px;margin-bottom:16px;border-radius:8px;border:1px solid rgba(226,101,21,.3);background:#F8F8F8;font-size:14px;color:var(--ink)}
.tdisc .ic{color:var(--orange);flex-shrink:0;display:flex}
.tdisc .cl{color:var(--n40);flex-shrink:0;display:flex;margin-left:8px}
.tbox{flex:1;border-radius:8px;border:1px solid var(--border);background:var(--card);padding:16px;font-size:14px;line-height:1.5;color:var(--ink);overflow:hidden}
.tbox p{margin-bottom:12px}
.fabs{position:absolute;right:28px;bottom:28px;display:flex;flex-direction:column;gap:8px}
.fab{width:40px;height:40px;border-radius:12px;background:var(--orange);color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.25)}
/* Session Settings tab */
.dbody.setts{padding:16px;overflow:hidden}
.scard{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:24px}
.scard h3{font-size:16px;font-weight:500;color:var(--ink);margin-bottom:16px}
.shead{display:flex;align-items:center;margin-bottom:8px}
.shead h3{margin-bottom:0}
.shead .hlp{margin-left:auto;color:var(--n40);display:flex}
.slabel{font-size:14px;font-weight:500;color:var(--ink);margin-bottom:8px}
.slabel.sm{font-size:12px;color:var(--n40)}
.sinput{padding:12px 16px;border-radius:8px;background:rgba(128,128,128,.1);font-size:14px;color:var(--ink);margin-bottom:16px}
.srow{display:flex;gap:16px}
.srow>div{flex:1}
.sfield{display:flex;align-items:center;padding:14px 12px;border-radius:8px;background:rgba(128,128,128,.1);font-size:14px;color:var(--ink)}
.sfield svg{margin-left:auto;color:var(--n40)}
.sdesc{font-size:14px;color:var(--n40);line-height:1.4;margin-bottom:16px}
.sdrop{display:flex;align-items:center;padding:12px 16px;border-radius:8px;background:rgba(128,128,128,.1);font-size:14px;color:var(--ink);margin-bottom:12px}
.sdrop svg{margin-left:auto;color:var(--n40)}
.sdesc.b{margin-bottom:0}
.danger{border:1px solid rgba(244,67,54,.3);border-radius:12px;background:rgba(244,67,54,.05);padding:16px}
.danger h3{font-size:16px;font-weight:600;color:#F44336;margin-bottom:8px}
.danger p{font-size:14px;color:var(--n40);margin-bottom:16px}
.delbtn{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:8px;background:#F44336;color:#fff;font-size:14px;font-weight:500}
/* PRO badge (pro_badge.dart) */
.pro{margin-left:8px;padding:2px 8px;border-radius:10px;background:linear-gradient(180deg,#FFAA6C,#E44D0D);color:#fff;font-size:10px;font-weight:700;letter-spacing:.5px;transform:rotate(-2.86deg);display:inline-block}
/* Topic tile (topic_list_tile.dart standard layout) */
.ttile{background:var(--card);border:1px solid var(--border);border-radius:8px;margin-bottom:12px;padding:12px 16px;display:flex;gap:12px;align-items:flex-start}
.ticon{padding:10px;border-radius:8px;display:flex;flex-shrink:0}
.tbody{flex:1;min-width:0}
.ttitle{font-size:16px;font-weight:700;color:var(--ink);line-height:1.3}
.tmeta{font-size:11.1px;color:var(--n40);margin-top:4px}
.tdesc{font-size:14px;color:var(--n40);margin-top:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.tctl{display:flex;gap:8px;align-items:center;flex-shrink:0}
.tpin{opacity:.75;display:flex}
.tmenu{color:var(--n40);display:flex}
/* Topic detail (topic_details_overlay_screen.dart wide layout) */
.tdpane{flex:1;padding:16px;display:flex;min-width:0}
.tdcard{flex:1;border:1px solid var(--border);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;min-width:0}
.tdtabsrow{display:flex;align-items:center;padding:8px 16px}
.tdmain{flex:1;display:flex;min-height:0}
.tdcontent{flex:1;overflow:hidden;padding:16px;min-width:0}
.ocard{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:24px;margin-bottom:16px}
.ohead{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
.otitle{font-size:18px;font-weight:600;color:var(--ink)}
.oicons{display:flex;gap:2px;color:var(--icon)}
.oicons span{padding:8px;display:flex;border-radius:6px}
.ocard p{font-size:14px;line-height:1.6;color:var(--ink);margin-bottom:12px}
.ogen{display:block;text-align:right;font-size:12px;color:#9E9E9E}
.irow{display:flex;gap:8px;align-items:flex-start;margin-bottom:12px}
.irow .iic{flex-shrink:0;display:flex;padding-top:1px}
.irow .iic.task{color:var(--orange)}
.irow .iic.note{color:var(--n40)}
.ibody{font-size:14px;line-height:1.45;color:var(--ink)}
.imeta{font-size:12px;color:var(--n40);margin-top:2px}
.ichip{display:inline-block;padding:2px 8px;border-radius:8px;background:rgba(226,101,21,.12);color:var(--orange);font-size:11px;font-weight:500;margin-bottom:4px}
/* Recording / paused rail states (adaptive_dashboard.dart) */
.nav.rec{background:#EFF8F0;border:.5px solid rgba(15,137,35,.4);color:#2B2724;font-weight:600}
.nav.pau{background:#FFF8E1;border:.5px solid rgba(245,158,11,.4);color:#2B2724;font-weight:600}
.recctl{margin:8px;display:flex;flex-direction:column;gap:4px}
.recrow{display:flex;gap:4px}
.recsq{flex:1;aspect-ratio:1;background:#005E10;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff}
.recbtn{padding:16px 8px;border-radius:8px;background:#005E10;color:#fff;display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;font-weight:500;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.2)}
.pausepill{margin:8px;padding:12px 8px 8px;border-radius:12px;background:#F59E0B;display:flex;flex-direction:column;align-items:center}
.pausecirc{width:36px;height:36px;border-radius:50%;background:#D97706;display:flex;align-items:center;justify-content:center;color:#fff}
.pauselbl{margin-top:6px;font-size:11px;font-weight:700;color:#fff;text-align:center}
.tbox .temp{color:rgba(38,35,26,.6)}
.tbox.live{font-size:16px}
/* Settings dialog (unified_settings_dialog.dart, 900x700) */
.ovl{position:absolute;inset:0;background:rgba(0,0,0,.54);display:flex;align-items:center;justify-content:center;z-index:5}
.ovl.blur{background:rgba(128,128,128,.2);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);align-items:flex-start;justify-content:center}
.sdlg{width:900px;height:700px;border-radius:8px;background:var(--card);display:flex;flex-direction:column;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.2)}
.sdhead{padding:16px;display:flex;align-items:center}
.sdhead h2{font-size:18px;font-weight:600;color:var(--ink)}
.sdhead .x{margin-left:auto;color:var(--ink);display:flex;padding:8px}
.sdbody{flex:1;display:flex;min-height:0;border-top:1px solid #E0E0E0}
.sdnav{width:200px;flex-shrink:0;background:#F5F5F5;padding:16px 12px;overflow:hidden}
.sditem{height:44px;margin-bottom:2px;padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;font-size:14px;color:#666666}
.sditem .ic{width:28px;height:28px;border-radius:8px;background:#F5F5F5;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sditem.sel{background:#FFFFFF;color:var(--orange);font-weight:500}
.sditem.sel .ic{background:rgba(226,101,21,.1);color:var(--orange)}
.sdcontent{flex:1;background:#FAFAFA;padding:32px;overflow:hidden}
.sdsec{font-size:18px;font-weight:600;color:var(--ink);margin-bottom:12px}
.sdcard{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:24px;margin-bottom:24px}
.sdrow{display:flex;gap:12px;align-items:center}
.sdinput{flex:1;padding:12px 16px;border-radius:8px;background:#F8F8F8;border:1px solid var(--border);font-size:14px;color:var(--ink)}
.obtn{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:8px;background:var(--orange);color:#fff;font-size:14px;font-weight:500}
.gbtn{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:8px;background:var(--card);border:1px solid var(--border);color:var(--ink);font-size:14px;font-weight:500}
.sdlabel{font-size:14px;font-weight:500;color:var(--ink);margin-bottom:6px}
.sddesc{font-size:14px;color:var(--n40);margin-bottom:12px}
.togrow{display:flex;align-items:center}
.togrow span{font-size:14px;color:var(--ink)}
.switch.off{background:#E0E0E0}
.switch.off::after{right:auto;left:2px}
.setrow{display:flex;align-items:flex-start;gap:16px}
.setrow+.setrow{margin-top:20px}
.setrow .sb{flex:1;min-width:0}
.setrow .st{font-size:14px;font-weight:500;color:var(--ink)}
.setrow .sd{font-size:13px;color:var(--n40);line-height:1.45;margin-top:4px}
.setrow .switch{margin-top:2px}
.hrow{display:flex;align-items:center;gap:12px;padding:12px 4px;font-size:14px;color:var(--ink)}
.hrow+.hrow{border-top:1px solid var(--border)}
.hrow .ic{color:var(--icon);display:flex}
.hrow .tr{margin-left:auto;color:var(--n40);display:flex}
.vfoot{margin-top:8px;text-align:center;font-size:12px;color:var(--n40);line-height:1.6}
/* Search overlay (search_overlay.dart) */
.swrap{margin-top:135px;width:600px;display:flex;flex-direction:column}
.sbox{background:var(--card);border:1px solid var(--border);border-radius:8px 8px 0 0;box-shadow:0 4px 20px rgba(0,0,0,.1);display:flex;align-items:center;padding:0 16px}
.sbox .si{color:#8D8D8D;display:flex;margin-right:12px}
.sbox .q{flex:1;font-size:16px;color:var(--ink);padding:16px 0}
.sbox .cx{color:#8D8D8D;display:flex;margin-left:8px}
.sres{background:var(--card);border:1px solid var(--border);border-top:none;border-radius:0 0 8px 8px;max-height:400px;overflow:hidden;padding-bottom:8px}
.ssec{padding:12px 16px 8px;display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;letter-spacing:.5px;color:var(--n40)}
.sitem{padding:10px 16px;display:flex;align-items:flex-start;gap:12px}
.sitem .ic{color:var(--orange);display:flex;padding-top:1px}
.sit{font-size:14px;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sis{font-size:12px;color:var(--n40);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* Onboarding (GradientBackground + centered column) */
.onbbody{flex-direction:column;background:linear-gradient(135deg,#F8EEE4,#FBFAF9)}
.oprog{padding:12px 16px;display:flex;align-items:center;gap:8px}
.oback{color:var(--ink);display:flex;padding:8px}
.otrack{flex:1;height:8px;border-radius:4px;background:#E0E0E0;position:relative;overflow:hidden}
.ofill{position:absolute;left:0;top:0;bottom:0;border-radius:4px;background:var(--orange)}
.osp{width:48px;flex-shrink:0}
.ocenter{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 24px;min-height:0}
.ocol{width:100%;max-width:500px;display:flex;flex-direction:column}
.ocol.narrow{max-width:400px}
.ohead{font-size:26px;font-weight:700;color:var(--ink);text-align:center;margin-bottom:28px}
.ohead.tight{margin-bottom:8px}
.wlogo{display:flex;justify-content:center;margin-bottom:16px}
.wtitle{font-size:32px;font-weight:700;color:var(--ink);text-align:center}
.wdesc{font-size:16px;color:var(--n40);line-height:1.5;text-align:center;margin-top:16px}
.wbtn{margin-top:48px;display:flex;align-items:center;justify-content:center;gap:8px;padding:16px;border-radius:8px;background:var(--orange);color:#fff;font-size:18px;font-weight:600;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.wlink{margin-top:12px;text-align:center;font-size:16px;font-weight:500;color:var(--n40);padding:12px 24px}
.lcard{display:flex;align-items:center;gap:16px;padding:16px;background:var(--card);border:1px solid #E0E0E0;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:6px}
.lflag{width:48px;height:48px;border-radius:8px;overflow:hidden;box-shadow:0 2px 4px rgba(0,0,0,.1);flex-shrink:0}
.lflag svg{width:48px;height:48px;display:block}
.lbody{flex:1;min-width:0}
.lname{font-size:17px;font-weight:700;color:var(--ink)}
.lsub{font-size:14px;color:var(--n40);margin-top:2px}
.lsub.sug{color:var(--orange);font-weight:500}
.lgo{width:36px;height:36px;border-radius:50%;background:rgba(226,101,21,.1);display:flex;align-items:center;justify-content:center;color:var(--orange);flex-shrink:0}
.nhelp{font-size:14px;color:var(--ink);text-align:center;margin-bottom:24px}
.ninput{background:var(--card);border:1px solid #E0E0E0;border-radius:12px;padding:14px 16px;font-size:20px;color:var(--ink)}
.ninput .ph{color:rgba(38,35,26,.3)}
.ucard{display:flex;align-items:center;gap:16px;padding:20px;background:var(--card);border:1px solid #E0E0E0;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:12px}
.uemoji{width:56px;height:56px;border-radius:8px;background:rgba(226,101,21,.1);display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0}
.uic{width:56px;height:56px;border-radius:8px;background:rgba(226,101,21,.1);display:flex;align-items:center;justify-content:center;color:var(--orange);flex-shrink:0}
.utitle{font-size:17px;font-weight:700;color:var(--ink)}
.udesc{font-size:14px;color:var(--n40);line-height:1.3;margin-top:4px}
.ccard{display:flex;align-items:center;gap:14px;padding:18px;background:var(--card);border:1px solid #E0E0E0;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.08);margin-bottom:12px}
.cic{width:48px;height:48px;border-radius:8px;background:rgba(226,101,21,.1);display:flex;align-items:center;justify-content:center;color:var(--orange);flex-shrink:0}
.cic.ink{color:var(--ink)}
.ctitle{font-size:16px;font-weight:600;color:var(--ink)}
.cdesc{font-size:13px;color:var(--n40);margin-top:3px}
.sagree{font-size:13px;color:var(--n40);line-height:1.4;text-align:center;margin-top:28px;padding:0 16px}
.sagree u{color:var(--orange)}
.shave{font-size:14px;color:var(--n40);text-align:center;margin-top:16px}
.shave b{color:var(--orange);font-weight:600}
/* Search empty + no-results states (search_overlay.dart) */
.sbox .q.ph{color:var(--n40)}
.shint{padding:32px 16px;text-align:center;font-size:14px;color:var(--n40)}
.snores{padding:32px 16px;display:flex;flex-direction:column;align-items:center;text-align:center}
.snores .ic{color:#8D8D8D;display:flex;margin-bottom:12px}
.snorest{font-size:16px;font-weight:500;color:var(--ink)}
.snoress{font-size:13px;color:var(--n40);margin-top:4px}
/* Merge sessions dialogs (merge_sessions_screen.dart / merge_configuration_screen.dart) */
.mdlg{width:500px;max-height:700px;border-radius:8px;background:var(--card);display:flex;flex-direction:column;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.2)}
.mdhead{padding:12px 8px;display:flex;align-items:center;border-bottom:1px solid #EBEBEB}
.mdhead .sp48{width:48px}
.mdhead h2{flex:1;text-align:center;font-size:18px;font-weight:600;color:var(--ink)}
.mdhead .ic{width:48px;display:flex;justify-content:center;color:var(--ink)}
.mdbody{padding:24px;overflow:hidden}
.minfo{display:flex;gap:12px;padding:16px;border-radius:8px;background:#F5F5F5;border:1px solid #EBEBEB;margin-bottom:20px}
.minfo .ic{color:var(--orange);display:flex;flex-shrink:0}
.minfo span{font-size:14px;color:#616161;line-height:1.4}
.mlabel{font-size:14px;font-weight:600;color:var(--ink);margin-bottom:8px}
.msel{padding:16px;border-radius:8px;background:var(--card);border:1px solid #E0E0E0;display:flex;gap:12px;align-items:center;margin-bottom:20px}
.msel.on{border:2px solid var(--orange);padding:15px}
.msel .ic{color:#757575;display:flex;flex-shrink:0}
.mst{font-size:14px;font-weight:500;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.msm{font-size:12px;color:#757575;margin-top:2px}
.mbtnrow{padding:0 24px 24px}
.mbig{display:flex;align-items:center;justify-content:center;padding:16px 20px;border-radius:8px;background:var(--orange);color:#fff;font-size:16px;font-weight:600}
.mdrop{padding:12px 16px;border-radius:6px;background:var(--card);border:1px solid rgba(226,101,21,.35);font-size:14px;color:var(--ink);display:flex;align-items:center;margin-bottom:16px}
.mdrop svg{margin-left:auto;color:var(--n40)}
.mlabel2{font-size:12px;color:#757575;margin-bottom:8px}
/* Share management (share_management_screen.dart) */
.smbar{padding:16px 16px 0;background:var(--card);border-bottom:1px solid var(--border)}
.smbar h1{font-size:20px;font-weight:600;color:var(--ink);padding:8px 0 12px;display:flex;align-items:center;gap:12px}
.smtabs{display:flex;gap:24px}
.smtab{padding:10px 4px;font-size:14px;font-weight:500;color:var(--n40);border-bottom:2px solid transparent}
.smtab.sel{color:var(--orange);border-bottom-color:var(--orange)}
.smlist{flex:1;overflow:hidden;padding:8px}
.smcard{display:flex;gap:16px;align-items:flex-start;padding:12px 16px;margin:4px 8px;background:var(--card);border:1px solid var(--border);border-radius:8px}
.smcard .ic{color:var(--orange);display:flex;flex-shrink:0;padding-top:2px}
.smt{font-size:16px;font-weight:700;color:var(--ink)}
.sms{font-size:12px;color:var(--n40);margin-top:3px}
.smcard .tr{margin-left:auto;color:#757575;display:flex}
/* Context creation flow */
.ctxcard{background:var(--card);border:1px solid #E0E0E0;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.08);padding:8px 16px;display:flex;align-items:center;gap:8px}
.ctxin{flex:1;font-size:20px;color:rgba(38,35,26,.3);padding:12px 0;text-align:left}
.ctxarrow{width:48px;height:48px;border-radius:50%;background:rgba(226,101,21,.1);display:flex;align-items:center;justify-content:center;color:var(--orange);flex-shrink:0}
.ctxskip{text-align:center;font-size:14px;font-weight:600;color:rgba(38,35,26,.7);margin-top:12px;padding:8px}
.qprog{text-align:center;font-size:12px;color:rgba(38,35,26,.5);padding-bottom:4px}
.steprow{display:flex;align-items:center;gap:12px;padding:8px 0;font-size:15px}
.steprow .ic{display:flex;width:24px;justify-content:center}
.steprow.done .ic{color:var(--orange)}
.steprow.done span,.steprow.active span{font-weight:500;color:var(--ink)}
.steprow.pending .ic{color:rgba(38,35,26,.25)}
.steprow.pending span{color:rgba(38,35,26,.4)}
.spin{width:20px;height:20px;border:2.5px solid rgba(226,101,21,.25);border-top-color:var(--orange);border-radius:50%}
.ctxeditor{background:var(--card);border:1px solid #E0E0E0;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.08);padding:16px;height:400px;font-size:14px;line-height:1.6;color:var(--ink);text-align:left;overflow:hidden}
/* Paywall (subscription_screen.dart desktop) */
.paywrap{flex:1;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#F8EEE4,#FBFAF9)}
.paycol{width:400px;display:flex;flex-direction:column;text-align:center}
.paycol h2{font-size:18px;font-weight:600;color:var(--ink);margin-bottom:16px}
.paycol p{font-size:14px;color:var(--ink);margin-bottom:24px;line-height:1.4}
.paycol .obtn{justify-content:center;margin-bottom:12px;padding:12px 16px}
.paylink{font-size:14px;font-weight:500;color:var(--orange);padding:8px}
/* Topic detail medium banner (_buildMediumScreenTopBar, shown <1280px) */
.tdbanner{display:none;padding:12px 16px;align-items:flex-start;background:linear-gradient(90deg,var(--bg),rgba(253,230,138,0.15))}
.tdback{width:32px;height:32px;border-radius:16px;background:var(--orange);color:#fff;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin:2px 12px 0 0}
.tdbicon{width:48px;height:48px;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin:2px 14px 0 0}
.tdbbody{flex:1;min-width:0}
.tdbtitle{font-size:18px;font-weight:600;color:var(--ink);line-height:1.3}
.tdbdesc{font-size:14px;color:var(--n40);margin-top:4px}
.tdbmeta{font-size:14px;color:#9E9E9E;margin-top:6px}
.tdbtabs{margin-top:12px;display:flex;align-items:center}
.tdbanner .tmenu{margin-top:2px;flex-shrink:0}
/* Session detail medium header (_buildDesktopTopBar with showBackButton, <1280px) */
.sdbanner{display:none;padding:12px 16px}
.sdbrow{display:flex;align-items:center}
.sdbrow .tdback{margin:0 12px 0 0}
.sdbicon{color:var(--n40);display:flex;margin-right:12px;flex-shrink:0}
.sdbody2{flex:1;min-width:0}
.sdbtitle{font-size:18px;font-weight:600;color:var(--ink);line-height:1.3}
.sdbmeta{margin-top:4px;display:flex;align-items:center;gap:12px;font-size:13px;color:var(--n40)}
.sdbmeta .chip{margin-top:0}
.sdbtabs{margin-top:12px}
/* Mobile (<768px): dashboard swaps to the phone layout (_buildMobileLayout) */
.mob{display:none}
@media (max-width:767px){
  body.page-sessions{width:100vw;height:100vh;min-width:390px;min-height:600px;background:linear-gradient(160deg,#F8EEE4,#FBFAF9)}
  body.page-sessions .rail,body.page-sessions main{display:none}
  body.page-sessions .mob{display:block;position:absolute;inset:0}
}
/* Medium breakpoint (768-1279px): per-screen medium layouts from the Dart
   _buildMediumScreenLayout builders. Wide (>=1280px) layouts are untouched. */
@media (max-width:1279px){
  body.page-topic-detail,body.page-session-detail,body.page-sessions,body.page-topics,
  body.page-highlights,body.page-settings,body.page-search,body.page-onb{
    width:100vw;height:100vh;min-width:768px;min-height:640px}
  /* detail overlays cover the toolbar at medium width */
  .page-topic-detail .topbar,.page-session-detail .topbar{display:none}
  /* topic detail: own page with banner header */
  .page-topic-detail .listpane{display:none}
  .page-topic-detail .tdpane{padding:0}
  .page-topic-detail .tdcard{border:none;border-radius:0}
  .page-topic-detail .tdtabsrow{display:none}
  .page-topic-detail .tdbanner{display:flex}
  /* session detail: own page with back-button header, no glass panel */
  .page-session-detail .listpane{display:none}
  .page-session-detail .detail{padding:0}
  .page-session-detail .glass{border:none;border-radius:0;box-shadow:none;background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none}
  .page-session-detail .dhead,.page-session-detail .tabswrap{display:none}
  .page-session-detail .sdbanner{display:block;border-bottom:1px solid var(--border)}
  /* responsive chat column (260-380px, _calculateChatWidth) */
  .page-topic-detail .dchat,.page-session-detail .dchat{width:clamp(260px,calc(260px + (100vw - 900px)*0.4),380px)}
  /* sessions dashboard + topics: list takes the full width */
  .page-sessions .listpane,.page-topics .listpane{width:auto;flex:1}
  .page-sessions .empty,.page-topics .empty{display:none}
  /* settings dialog + search overlay shrink with the window */
  .page-settings .sdlg{width:min(900px,calc(100vw - 32px));height:min(700px,calc(100vh - 64px))}
  .page-search .swrap{width:min(600px,calc(100vw - 48px))}
}
/* Topic detail: Sessions/Settings tabs, topics empty state, signin */
.tsitem{margin-bottom:6px;padding:12px;border-radius:8px;background:#F9F7F5;border:1px solid rgba(128,128,128,.2);display:flex;gap:10px;align-items:flex-start}
.tsitem.sel{background:#FFF5F0;border-color:#FFD4C4}
.tsitem .ic{color:#757575;display:flex;flex-shrink:0;padding-top:1px}
.tsitem.sel .ic{color:var(--orange)}
.tst{font-size:14px;font-weight:700;color:var(--ink);line-height:1.35}
.tsm{font-size:12px;color:var(--n40);margin-top:3px}
.tspanel{flex:1;border:1px solid var(--border);border-radius:12px;background:var(--card);min-width:0;display:flex;flex-direction:column;overflow:hidden}
.tsphead{padding:12px 16px 8px;display:flex;align-items:flex-start;gap:8px}
.tspt{flex:1;min-width:0}
.tsptitle{font-size:18px;font-weight:700;color:var(--ink);line-height:1.3}
.tspmeta{font-size:13px;color:var(--n40);margin-top:3px}
.cbtn{width:32px;height:32px;border-radius:16px;display:flex;align-items:center;justify-content:center;color:var(--icon);flex-shrink:0}
.tsptabs{padding:8px 16px}
.tsptabs .tab{padding:6px 10px;font-size:13px}
.tspbody{flex:1;overflow:hidden;padding:16px}
.sw{width:24px;height:24px;border-radius:50%;display:inline-block;margin-right:8px;border:2px solid transparent}
.sw.sel{border-color:var(--orange)}
.igrid{display:flex;gap:8px;margin-top:8px}
.igrid span{width:40px;height:40px;border-radius:8px;border:1px solid var(--border);display:flex;align-items:center;justify-content:center;color:var(--icon)}
.igrid span.sel{border-color:var(--orange);color:var(--orange);background:rgba(226,101,21,.08)}
.et{font-size:18px;font-weight:700;color:var(--ink)}
.ed{font-size:14px;color:var(--n40);line-height:1.5;text-align:center;max-width:420px;padding:0 32px}
.ebtn{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:8px;background:var(--orange);color:#fff;font-size:14px;font-weight:500}
.sifield{display:flex;align-items:center;gap:12px;background:var(--card);border:1px solid #E0E0E0;border-radius:8px;padding:16px;font-size:16px;color:var(--ink);margin-bottom:12px}
.sifield .ic{color:var(--n40);display:flex}
.sifield .ph{color:rgba(38,35,26,.4)}
.sibtn{display:flex;align-items:center;justify-content:center;padding:16px;border-radius:8px;background:var(--orange);color:#fff;font-size:17px;font-weight:600;margin-top:4px;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.silink{text-align:center;font-size:15px;font-weight:500;color:var(--orange);padding:8px 16px;margin-top:8px}
.sisub{text-align:center;font-size:16px;font-weight:500;color:var(--n40);margin-top:12px}
/* Highlights screen (highlights_screen.dart XL master-detail) */
.hlscreen{flex:1;display:flex;min-width:0}
.hlleft{flex:2;display:flex;flex-direction:column;min-width:0}
.hlcards{flex:1;overflow:hidden;padding:0 16px 16px}
.hlleft .hlitem{background:var(--card)}
.hlleft .hlitem.sel{background:#FFF0E8;border-color:#FFD4C4}
.hlright{flex:1;padding:8px 16px 16px 0;display:flex;flex-direction:column;min-width:0}
.hlright .hldetail{flex:1}
.hlright .empty{border:none}
"""

# ---------- icons ----------
i_nav = {
    "Sessions": lucide("file-text", 20, 200),
    "Topics": lucide("folder-open", 20, 200),
    "Highlights": lucide("sparkles", 20, 200),
    "Settings": lucide("settings", 20, 200),
    "Search": lucide("search", 20, 200),
}
i_filters = lucide("sliders-horizontal", 18, 300)
i_merge = lucide("merge", 18, 300)
i_select = lucide("square-check", 18, 300)
i_refresh = lucide("refresh-cw", 18, 300)
i_import = lucide("download", 18, 300)
i_chev = lucide("chevron-down", 14, 400)
i_sortud = lucide("arrow-up-down", 14, 400)
i_filetext_card = lucide("file-text", 20, 300)
i_empty = lucide("file-text", 64, 100)

LUC = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICON_DOTS = f'<svg width="18" height="18" {LUC}><circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/></svg>'
ICON_SHARE = f'<svg width="18" height="18" {LUC}><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" x2="12" y1="2" y2="15"/></svg>'
ICON_CHECK = f'<svg width="12" height="12" {LUC} stroke-width="3"><path d="M20 6 9 17l-5-5"/></svg>'
ICON_SPARK = f'<svg width="10" height="10" {LUC} stroke-width="1.5"><path d="M12 3l1.9 5.8a2 2 0 0 0 1.28 1.28L21 12l-5.82 1.92a2 2 0 0 0-1.28 1.28L12 21l-1.9-5.8a2 2 0 0 0-1.28-1.28L3 12l5.82-1.92a2 2 0 0 0 1.28-1.28z"/></svg>'
ICON_SPARK12 = ICON_SPARK.replace('width="10" height="10"', 'width="12" height="12"')
ICON_UP = f'<svg width="14" height="14" {LUC} stroke-width="2.5"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>'
PLAY_FILL = '<svg width="40" height="40" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#E26515"/><path d="M9.8 8.2v7.6l6.4-3.8z" fill="#FFFFFF"/></svg>'

# ---------- shared shell pieces ----------
def navitem(label, sel=False, href=None):
    cls = "nav sel" if sel else "nav"
    inner = f'{i_nav[label]}<span>{label}</span>'
    if href:
        return f'<a class="{cls}" href="{href}">{inner}</a>'
    return f'<div class="{cls}">{inner}</div>'

NAV_HREF = {"Sessions": DASH, "Topics": TOPICS, "Highlights": HIGHLIGHTS,
            "Settings": SETTINGS, "Search": SEARCH}

def state_icon(name, size=20):
    src = open(f"{REPO}/assets/images/{name}.svg", encoding="utf-8").read()
    src = re.sub(r'stroke="#[0-9A-Fa-f]{6}"', 'stroke="currentColor"', src)
    src = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="currentColor"', src)
    src = src.replace('width="25" height="26"', f'width="{size}" height="{size + 1}"')
    return src.strip()

# Static frame of AudioLevelVisualizer (3 bars, audio_level_visualizer.dart)
WAVE_SVG = ('<svg width="24" height="24" viewBox="0 0 24 24">'
            '<rect x="0" y="7" width="4.8" height="10" fill="#fff"/>'
            '<rect x="9.6" y="2" width="4.8" height="20" fill="#fff"/>'
            '<rect x="19.2" y="5.5" width="4.8" height="13" fill="#fff"/></svg>')

def rail(active="Sessions", mode="default"):
    rows = []
    for label in ["Sessions", "Topics", "Highlights", "Settings", "Search"]:
        if label == "Sessions" and mode in ("recording", "paused"):
            cls = "nav rec" if mode == "recording" else "nav pau"
            icon = state_icon("session-active-icon" if mode == "recording" else "session-paused-icon")
            rows.append(f'<a class="{cls}" href="{NAV_HREF[label]}">{icon}<span>{label}</span></a>')
        else:
            rows.append(navitem(label, sel=(label == active), href=NAV_HREF[label]))
    items = "\n    ".join(rows)
    if mode == "recording":
        bottom = f'''<div class="recctl">
    <div class="recrow"><span class="recsq">{WAVE_SVG}</span><span class="recsq">{lucide("mic", 18, 100)}</span></div>
    <div class="recbtn">{glasses_white}<span>Listening</span></div>
  </div>'''
    elif mode == "paused":
        bottom = f'''<div class="pausepill">
    <span class="pausecirc">{material("pause_rounded", 20)}</span>
    <span class="pauselbl">Session<br>Paused</span>
  </div>'''
    else:
        bottom = f'<div class="start">{glasses_white}<span>Start Session</span></div>'
    return f'''<aside class="rail">
  <div class="logo"><img src="{logo_png}" alt="Hedy"></div>
  <div class="navwrap">
    {items}
  </div>
  {bottom}
</aside>'''

PRO_BADGE = '<span class="pro">PRO</span>'

def topbar(title="Sessions", count="14", pro=False, buttons=None):
    if buttons is None:
        buttons = (f'<span class="tbtn">{i_filters}Filters</span>'
                   f'<a class="tbtn" href="{MERGE}">{i_merge}Merge Sessions</a>'
                   f'<span class="tbtn">{i_select}Select</span>'
                   f'<span class="tbtn">{i_refresh}Refresh</span>'
                   f'<span class="tbtn">{i_import}Import {i_chev}</span>')
    return f'''<div class="topbar">
  <h1>{title}</h1><span class="count">{count}</span>{PRO_BADGE if pro else ""}<span class="sp"></span>
  {buttons}
</div>'''

SESSIONS = [
    ("Q1 Strategy Review with Leadership Team", "Today, 4:58 PM &bull; 42 minutes &bull; Business Meeting", True, '<span class="chip amber">Acme Corp</span>'),
    ("Product Roadmap Planning for Q4", "Today, 2:30 PM &bull; 45 minutes &bull; Group Brainstorm", False, '<span class="chip peach">Roadmap</span>'),
    ("Interview: Sarah Chen, VP Engineering", "Yesterday, 11:15 AM &bull; 38 minutes &bull; Job Interview", True, ""),
    ("Weekly Team Standup", "Yesterday, 9:00 AM &bull; 12 minutes &bull; Business Meeting", False, '<span class="chip amber">Acme Corp</span>'),
    ("Cardiology Follow-up &mdash; Questions for Dr. Reyes", "Mon, Jun 30, 10:40 AM &bull; 22 minutes &bull; Medical Consultation", True, '<span class="chip rose">Health</span>'),
    ("Negotiation Prep: Vendor Contract Renewal", "Sun, Jun 29, 3:05 PM &bull; 31 minutes &bull; Negotiation", False, ""),
    ("Customer Discovery: Beacon Health", "Fri, Jun 27, 2:15 PM &bull; 34 minutes &bull; Business Meeting", True, ""),
    ("Renewal Pricing Sync", "Tue, Jun 24, 1:30 PM &bull; 18 minutes &bull; Business Meeting", False, '<span class="chip amber">Acme Corp</span>'),
]

def cards(selected_first=False):
    out = ['<div class="sort"><span class="si">' + i_sortud + '</span><span>Date</span><span class="sc">' + i_chev + "</span></div>", '<div class="cards">']
    for k, (title, meta, audio, chip) in enumerate(SESSIONS):
        icon = session_play if audio else i_filetext_card
        icb = f'<span class="icb">{material("cloud_done", 8)}</span>' if audio else ""
        if not chip:
            chip = f'<span class="seltopic">Select Topic {material("keyboard_arrow_down", 14)}</span>' 
        sel = " sel" if (selected_first and k == 0) else ""
        href = DASH if (selected_first and k == 0) else DETAIL
        out.append(f'''<a class="card{sel}" href="{href}" data-t="{title}"><span class="cicon">{icon}{icb}</span><div class="cc">
<div class="ct">{title}</div><div class="cm">{meta}</div>{chip}</div></a>''')
    out.append('<div class="year">2025</div></div>')
    return '<div class="listpane">' + "\n".join(out) + "</div>"

def page(title, body, active="Sessions", bar=None, mode="default", cls=""):
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=1440">
<title>{title}</title>
{CAPTURE}
<style>
{fontfaces}
{CSS}
</style>
</head><body{f' class="{cls}"' if cls else ""}>
{rail(active, mode)}
<main>
{bar if bar is not None else topbar()}
<div class="content">
{body}
</div>
</main>
</body></html>'''

# ---------- dashboard (empty detail state) ----------
empty = f'''<div class="empty"><span class="eicon">{i_empty}</span><p>Select a session to view details</p></div>'''
dash_html = page("Hedy — Sessions Dashboard (Light, 1440)", cards(selected_first=False) + "\n" + empty,
                 cls="page-sessions")

# ---------- session detail (shared shell, one page per tab) ----------
DETAIL_TABS = [("Details", DETAIL), ("Session Notes", DETAIL_NOTES),
               ("Highlights", DETAIL_HL), ("Transcript", DETAIL_TRANS),
               ("Settings", DETAIL_SETTS)]

def detail_shell(active_tab, dbody):
    tabs = "\n".join(
        f'<a class="tab{" sel" if label == active_tab else ""}" href="{href}">{label}</a>'
        for label, href in DETAIL_TABS)
    banner = f'''<div class="sdbanner">
      <div class="sdbrow">
        <a class="tdback" href="{DASH}">{material("arrow_back", 16)}</a>
        <span class="sdbicon">{session_play}</span>
        <div class="sdbody2">
          <div class="sdbtitle">Q1 Strategy Review with Leadership Team</div>
          <div class="sdbmeta"><span>Tuesday, July 7, 2026 &bull; 4:58 PM &bull; 42 min</span><span class="chip amber">Acme Corp</span></div>
        </div>
        <span class="mbtn">{ICON_DOTS}</span>
      </div>
      <div class="sdbtabs"><div class="tabs">
{tabs}
      </div></div>
    </div>'''
    return f'''<div class="detail"><div class="glass">
  <div class="dleft">
    {banner}
    <div class="dhead">
      <span class="hicon">{session_play}</span>
      <div class="dht">
        <div class="dtitle">Q1 Strategy Review with Leadership Team</div>
        <div class="dmeta"><span>Tuesday, July 7, 2026 &bull; 4:58 PM &bull; 42 min</span><span class="chip amber">Acme Corp</span></div>
      </div>
      <span class="mbtn">{ICON_DOTS}</span>
    </div>
    <div class="dsep"></div>
    <div class="tabswrap"><div class="tabs">
{tabs}
    </div></div>
    {dbody}
    <div class="player">
      {PLAY_FILL}
      <span class="ptime">12:41</span>
      <div class="ptrack"><div class="pfill"></div><div class="pthumb"></div></div>
      <span class="ptime">42:10</span>
      <span class="pspeed">1.0&times;</span>
    </div>
  </div>
  <div class="dsplit"></div>
  <div class="dchat">
    <div class="chathead"><span class="cht">Chat</span><span class="sp"></span><span class="tctx">Topic context</span><span class="switch"></span></div>
    <div class="dsep"></div>
    <div class="chatlog">
      <div class="bubble user">What concerns were raised about the Q3 roadmap?</div>
      <div class="bubble hedy">Sarah flagged that the Q3 roadmap timeline may be at risk given current engineering load. She suggested re-scoping two initiatives or shifting the ship date by about three weeks. The team agreed to follow up before the next monthly review.</div>
      <div class="bubble user">Who owns the follow-up?</div>
      <div class="bubble hedy">The follow-up with Sarah on Q3 roadmap risks is on your to-do list &mdash; no other owner was assigned during the meeting.</div>
    </div>
    <div class="chatin">
      <div class="chiprow">
        <span class="qchip">Summarize key points {ICON_SPARK}</span>
        <span class="qchip">Key decisions {ICON_SPARK}</span>
        <span class="qchip">What are the action items? {ICON_SPARK}</span>
        <span class="qmore">More {ICON_SPARK12}</span>
      </div>
      <div class="inbox"><span class="inhint">How can I help?</span><span class="send">{ICON_UP}</span></div>
    </div>
  </div>
</div></div>'''

details_body = f'''<div class="dbody">
      <div class="pcard">
        <div class="pchead"><span class="pctitle">Summary</span><span class="sp"></span><span class="picon">{ICON_DOTS}</span></div>
        <div class="pcbody">
          <p>The leadership team reviewed Q1 performance against plan and aligned on priorities heading into Q2. Revenue closed at 104% of target, driven primarily by the enterprise segment, while self-serve growth slowed for the second consecutive quarter.</p>
          <p>Key discussion points:<br>&bull; Enterprise pipeline is strong, but onboarding capacity is the limiting factor for Q2.<br>&bull; Marketing will shift budget from paid acquisition toward lifecycle campaigns.<br>&bull; The hiring plan was approved for two additional customer success roles.<br>&bull; Sarah raised concerns about the Q3 roadmap timeline given current engineering load.</p>
          <p>The team agreed to revisit pricing for the annual plan at the next monthly review.</p>
        </div>
      </div>
      <div class="pcard" style="margin-top:24px">
        <div class="pchead"><span class="pctitle">Your Todos</span><span class="sp"></span><span class="picon">{ICON_SHARE}</span></div>
        <div class="pcbody" style="margin-top:8px">
          <div class="todo done"><span class="cb on">{ICON_CHECK}</span><span>Send updated Q2 capacity model to leadership</span></div>
          <div class="todo"><span class="cb"></span><span>Schedule pricing review for annual plans</span></div>
          <div class="todo"><span class="cb"></span><span>Share onboarding hiring plan with recruiting</span></div>
          <div class="todo"><span class="cb"></span><span>Follow up with Sarah on Q3 roadmap risks</span></div>
        </div>
      </div>
    </div>'''

# ---------- session notes tab (lib/widgets/session_notes_tab.dart) ----------
i_fmt = {n: lucide(n, 16) for n in ["bold", "italic", "underline", "list", "list-ordered", "clock"]}
notes_body = f'''<div class="dbody notes">
      <div class="ntoolbar">
        <span class="nibtn">{i_fmt["bold"]}</span>
        <span class="nibtn">{i_fmt["italic"]}</span>
        <span class="nibtn">{i_fmt["underline"]}</span>
        <span class="nibtn">{i_fmt["list"]}</span>
        <span class="nibtn">{i_fmt["list-ordered"]}</span>
        <span class="nstatus"><span class="nsaved">Saved</span><span class="ncount">1,247 / 5000 chars</span></span>
      </div>
      <div class="neditor">
        <p><strong>Prep &amp; open questions</strong></p>
        <p>Walk in with the Q2 capacity model on screen &mdash; leadership will ask about onboarding first.</p>
        <ul>
          <li>Enterprise pipeline looks strong; confirm CS hiring timeline with recruiting</li>
          <li>Ask Sarah for the re-scoped Q3 roadmap options before the monthly review</li>
          <li>Marketing budget shift: what happens to the paid-acquisition experiments already running?</li>
        </ul>
        <p><strong>Decisions to capture</strong></p>
        <ol>
          <li>Two additional customer success roles approved</li>
          <li>Annual-plan pricing review scheduled for next monthly</li>
        </ol>
      </div>
    </div>'''

# ---------- highlights tab (session_details_overlay_screen.dart _buildHighlightsTab) ----------
i_spark_hl = lucide("sparkles", 18, 300)
i_clock12 = lucide("clock", 12)
i_share14 = lucide("share", 14)
i_trash14 = lucide("trash-2", 14)
i_bulb = lucide("lightbulb", 16, 300)
i_quote = lucide("quote", 16, 300)
i_chart = lucide("chart-no-axes-column-increasing", 16, 300)

HL_TAB_DATA = [
    ("Q3 roadmap timeline is at risk", "35m", True),
    ("Two customer success hires approved", "27m", False),
    ("Budget shifts to lifecycle campaigns", "18m", False),
    ("Onboarding capacity is the Q2 bottleneck", "12m", False),
    ("Revenue closed at 104% of target", "3m", False),
]

def hl_items():
    out = []
    for title, t, sel in HL_TAB_DATA:
        out.append(f'''<div class="hlitem{" sel" if sel else ""}" data-t="{title}" data-time="{t}"><span class="hlic">{i_spark_hl}</span>
<div><div class="hlt">{title}</div><span class="hltime">{i_clock12}{t}</span></div></div>''')
    return "\n".join(out)

hl_body = f'''<div class="dbody hl"><div class="hlwrap">
      <div class="hllist">
{hl_items()}
      </div>
      <div class="hldetail">
        <div class="hldt">Q3 roadmap timeline is at risk</div>
        <div class="hlactions">
          <span class="hlbtn">{i_share14}Share</span>
          <span class="hlbtn del">{i_trash14}Delete</span>
          <span class="hltime sm">{i_clock12}35:12</span>
        </div>
        <div class="hlsec">{i_bulb}Main Idea</div>
        <div class="hlbox">The Q3 roadmap timeline may slip because current engineering load leaves no slack for the two largest initiatives.</div>
        <div class="hlsec">{i_quote}Original Context</div>
        <div class="hlbox q">&ldquo;If we keep both initiatives scoped as they are, I don&rsquo;t see how we hit the September date &mdash; we either re-scope or we move the ship date by about three weeks.&rdquo;</div>
        <div class="hlsec">{i_chart}Analysis</div>
        <div class="hlbox">This is the second quarter in a row where engineering capacity has been raised as a delivery risk. Re-scoping now would protect the September launch while keeping the pricing review on schedule.</div>
      </div>
    </div></div>'''

# ---------- transcript tab ----------
mi_info = material("info_outline", 20)
mi_close = material("close", 20)
mi_edit = material("edit", 20)
mi_copy = material("content_copy", 20)
mi_down = material("download", 20)
mi_wand = material("auto_awesome", 20)

trans_body = f'''<div class="dbody trans">
      <div class="tdisc"><span class="ic">{mi_info}</span><span style="flex:1">Transcripts are generated automatically and may contain mistakes. Audio is the source of truth.</span><span class="cl">{mi_close}</span></div>
      <div class="tbox">
        <p>Alright, let&rsquo;s get started. First on the agenda is the Q1 close. Revenue landed at 104 percent of target, and the enterprise segment carried most of that overage. Self-serve growth slowed again, which is the second consecutive quarter we&rsquo;ve seen that pattern.</p>
        <p>On the pipeline side, enterprise looks strong going into Q2, but I want to flag that onboarding capacity is the limiting factor right now. If we close everything currently in stage four, we simply don&rsquo;t have the customer success coverage to onboard them on time.</p>
        <p>That&rsquo;s why the hiring plan in front of you includes two additional customer success roles. Recruiting says a six-to-eight-week fill time is realistic if we open the reqs this week.</p>
        <p>Moving to marketing &mdash; we&rsquo;re proposing to shift budget from paid acquisition toward lifecycle campaigns. Paid CAC has been creeping up for three quarters, and lifecycle has been outperforming on activation.</p>
        <p>One concern from my side: the Q3 roadmap timeline. Given the current engineering load, if we keep both initiatives scoped as they are, I don&rsquo;t see how we hit the September date. We either re-scope or we move the ship date by about three weeks.</p>
        <p>Fair point. Let&rsquo;s take that offline and revisit before the next monthly review. Last item &mdash; annual plan pricing. We agreed to revisit it next month once the Q1 cohort data is in.</p>
      </div>
      <div class="fabs">
        <span class="fab">{mi_edit}</span>
        <span class="fab">{mi_copy}</span>
        <span class="fab">{mi_down}</span>
        <span class="fab">{mi_wand}</span>
      </div>
    </div>'''

# ---------- session settings tab ----------
i_cal16 = lucide("calendar", 16)
i_clock16 = lucide("clock", 16)
mi_help = material("help_outline", 20)
mi_delout = material("delete_outline", 18)

setts_body = f'''<div class="dbody setts">
      <div class="scard">
        <h3>Session Settings</h3>
        <div class="slabel">Session Title</div>
        <div class="sinput">Q1 Strategy Review with Leadership Team</div>
        <div class="srow">
          <div><div class="slabel sm">Date</div><div class="sfield">Jul 7, 2026 {i_cal16}</div></div>
          <div><div class="slabel sm">Time</div><div class="sfield">4:58 PM {i_clock16}</div></div>
        </div>
      </div>
      <div class="scard">
        <div class="shead"><h3>Session Type</h3><span class="hlp">{mi_help}</span></div>
        <div class="sdesc">The session type controls how Hedy summarizes this session and which suggestions you get in real time.</div>
        <div class="sdrop">Business Meeting {i_chev}</div>
      </div>
      <div class="danger">
        <h3>Danger Zone</h3>
        <p>Delete this session permanently. This cannot be undone.</p>
        <span class="delbtn">{mi_delout}Delete Session</span>
      </div>
    </div>'''

# ---------- topics (topics_screen.dart + topic_list_tile.dart) ----------
def asset_svg(name, size, color):
    src = open(f"{REPO}/assets/images/{name}.svg", encoding="utf-8").read()
    src = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", src, flags=re.S).strip()
    src = src.replace('fill="#000000"', f'fill="{color}"')
    src = src.replace('width="800px" height="800px"', f'width="{size}" height="{size}"')
    return src

pin_outline = asset_svg("pin-outline", 16, "#BDBDBD")
pin_fill = asset_svg("pin-fill", 16, "#FFB800")
mi_morevert = material("more_vert", 18)

# Wallpaper presets from lib/utils/topic_color_palette.dart (gradient alpha 0.6, 135deg)
WALLPAPERS = {
    "gold":  ("#FDE68A", "#FEF9C3", "#FCD34D", "#92400E", "#FDE68A"),
    "rose":  ("#FECDD3", "#FCE7F3", "#FDA4AF", "#9F1239", "#FECDD3"),
    "peach": ("#FED7AA", "#FFE4E6", "#FDBA74", "#BF360C", "#FED7AA"),
    "mint":  ("#A7F3D0", "#CCFBF1", "#6EE7B7", "#065F46", "#A7F3D0"),
    "sky":   ("#BFDBFE", "#E0F2FE", "#93C5FD", "#1E40AF", "#BFDBFE"),
}

def _rgba(hexcol, a):
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    return f"rgba({r},{g},{b},{a})"

TOPICS_DATA = [
    ("Acme Corp", "gold", "work_outline", "8 sessions &bull; Jul 7, 2026", True,
     "Client meetings and account planning"),
    ("Health", "rose", "medical_services_outlined", "3 sessions &bull; Jun 30, 2026", False, ""),
    ("Product Roadmap", "sky", "folder", "5 sessions &bull; Jun 28, 2026", False,
     "Quarterly planning and launch decisions"),
    ("Hiring", "mint", "people_outline", "4 sessions &bull; Jun 24, 2026", False, ""),
    ("Learning", "peach", "school_outlined", "2 sessions &bull; Jun 12, 2026", False, ""),
]

def topic_tiles(selected=None):
    out = [f'<div class="sort"><span class="si">{i_sortud}</span><span>Last Activity</span><span class="sc">{i_chev}</span></div>',
           '<div class="cards">']
    for name, wp, icon, meta, starred, desc in TOPICS_DATA:
        g1, g2, g3, txt, banner = WALLPAPERS[wp]
        grad = f"background:linear-gradient(135deg,{_rgba(g1,.6)},{_rgba(g2,.6)},{_rgba(g3,.6)})"
        sel = name == selected
        selstyle = f';background:{_rgba(banner,.08)};border-color:{_rgba(banner,.2)}' if sel else ""
        pin = pin_fill if starred else pin_outline
        desc_html = f'<div class="tdesc">{desc}</div>' if desc else ""
        href = TOPIC_DETAIL if not sel else TOPICS
        out.append(f'''<a class="ttile" href="{href}" style="{selstyle[1:] if sel else ""}" data-t="{name}" data-d="{desc}" data-m="{meta}">
<span class="ticon" style="{grad}"><span style="color:{txt};display:flex">{material(icon, 28)}</span></span>
<div class="tbody"><div class="ttitle">{name}</div><div class="tmeta">{meta}</div>{desc_html}</div>
<span class="tctl"><span class="tpin">{pin}</span><span class="tmenu">{mi_morevert}</span></span></a>''')
    out.append("</div>")
    return '<div class="listpane">' + "\n".join(out) + "</div>"

topics_bar = topbar("Topics", "5", pro=True,
                    buttons=(f'<span class="tbtn">{i_refresh}Refresh</span>'
                             f'<span class="tbtn">{lucide("plus", 18, 300)}New Topic</span>'))

i_folder_empty = lucide("folder-open", 64, 100)
topics_empty = f'''<div class="empty"><span class="eicon">{i_folder_empty}</span><p>Select a topic to view details</p></div>'''
topics_html = page("Hedy — Topics (Light, 1440)", topic_tiles() + "\n" + topics_empty,
                   active="Topics", bar=topics_bar, cls="page-topics")

# ---------- topic detail (wide layout: tabs row + overview + chat) ----------
mi_ios_share = material("ios_share", 16)
mi_refresh16 = material("refresh", 16)
mi_task = material("assignment_outlined", 18)
mi_note = material("sticky_note_2_outlined", 18)

_gold_banner = _rgba("#FDE68A", .1)
_gold_grad = f"background:linear-gradient(135deg,{_rgba('#FDE68A',.6)},{_rgba('#FEF9C3',.6)},{_rgba('#FCD34D',.6)})"
TD_SESSIONS = "hedy-topic-detail-sessions-light-1440.html"
TD_HIGHLIGHTS = "hedy-topic-detail-highlights-light-1440.html"
TD_SETTINGS = "hedy-topic-detail-settings-light-1440.html"
TD_TABS = [("Overview", TOPIC_DETAIL), ("Sessions", TD_SESSIONS),
           ("Highlights", TD_HIGHLIGHTS), ("Settings", TD_SETTINGS)]

def td_tabs_html(active):
    return "\n".join(
        f'<a class="tab{" sel" if label == active else ""}" href="{href}">{label}</a>'
        for label, href in TD_TABS)

TOPIC_CHAT = None  # filled below

def td_shell(active, content):
    return f'''<div class="tdpane"><div class="tdcard">
  <div class="tdbanner">
    <a class="tdback" href="{TOPICS}">{material("arrow_back", 16)}</a>
    <span class="tdbicon" style="{_gold_grad}"><span style="color:#92400E;display:flex">{material("work_outline", 32)}</span></span>
    <div class="tdbbody">
      <div class="tdbtitle">Acme Corp</div>
      <div class="tdbdesc">Client meetings and account planning</div>
      <div class="tdbmeta">Jul 7 &bull; 8 sessions</div>
      <div class="tdbtabs"><div class="tabs">
{td_tabs_html(active)}
      </div></div>
    </div>
    <span class="tmenu">{mi_morevert}</span>
  </div>
  <div class="tdtabsrow" style="background:linear-gradient(90deg,transparent,{_gold_banner})">
    <div class="tabs">
{td_tabs_html(active)}
    </div>
    <span class="sp"></span>
    <span class="tmenu">{mi_morevert}</span>
  </div>
  <div class="dsep"></div>
  <div class="tdmain">
    {content}
    <div class="dsplit"></div>
    {TOPIC_CHAT}
  </div>
</div></div>'''

overview_content = f'''<div class="tdcontent">
      <div class="ocard">
        <div class="ohead"><span class="otitle">Topic Overview</span>
          <span class="oicons"><span>{mi_ios_share}</span><span>{mi_refresh16}</span></span></div>
        <p>Acme Corp is your most active client topic, covering eight sessions since March. Recent work has centered on the Q1 strategy review, contract renewal preparation, and the expansion of the customer success team supporting their account.</p>
        <p>The relationship is in good shape overall: revenue targets were exceeded last quarter and the renewal conversation is on track. The main open risks are onboarding capacity for Q2 and the Q3 roadmap timeline raised in the most recent leadership review.</p>
        <span class="ogen">Last generated: Jul 7, 2026</span>
      </div>
      <div class="ocard">
        <div class="ohead"><span class="otitle">Action Items</span></div>
        <div class="irow"><span class="iic task">{mi_task}</span><div>
          <span class="ichip">High priority</span>
          <div class="ibody">Send updated Q2 capacity model to leadership</div>
          <div class="imeta">Q1 Strategy Review &bull; Jul 7</div></div></div>
        <div class="irow"><span class="iic task">{mi_task}</span><div>
          <div class="ibody">Schedule pricing review for annual plans</div>
          <div class="imeta">Q1 Strategy Review &bull; Jul 7</div></div></div>
        <div class="irow"><span class="iic task">{mi_task}</span><div>
          <div class="ibody">Confirm renewal terms with procurement before Aug 1</div>
          <div class="imeta">Negotiation Prep &bull; Jun 29</div></div></div>
      </div>
      <div class="ocard">
        <div class="ohead"><span class="otitle">Key Decisions</span></div>
        <div class="irow"><span class="iic note">{mi_note}</span><div>
          <div class="ibody">Two additional customer success roles approved for the account team</div>
          <div class="imeta">Q1 Strategy Review &bull; Jul 7</div></div></div>
      </div>
    </div>'''

TOPIC_CHAT = f'''<div class="dchat">
      <div class="chathead"><span class="cht">Chat</span></div>
      <div class="dsep"></div>
      <div class="chatlog">
        <div class="bubble user">What are the open risks on this account?</div>
        <div class="bubble hedy">Two risks are open right now: onboarding capacity for Q2 &mdash; the current customer success team can&rsquo;t absorb the stage-four pipeline &mdash; and the Q3 roadmap timeline, which Sarah flagged as at risk in the July 7 leadership review.</div>
      </div>
      <div class="chatin">
        <div class="chiprow">
          <span class="qchip">Summarize this topic {ICON_SPARK}</span>
          <span class="qchip">Open action items {ICON_SPARK}</span>
          <span class="qmore">More {ICON_SPARK12}</span>
        </div>
        <div class="inbox"><span class="inhint">How can I help?</span><span class="send">{ICON_UP}</span></div>
      </div>
    </div>'''

topic_detail_pane = td_shell("Overview", overview_content)
topic_detail_html = page("Hedy — Topic Detail (Light, 1440)",
                         topic_tiles(selected="Acme Corp") + "\n" + topic_detail_pane,
                         active="Topics", bar=topics_bar, cls="page-topic-detail")

# --- topic detail: Sessions tab (_buildSessionsTabWideScreen) ---
TD_SESS_LIST = [
    ("Q1 Strategy Review with Leadership Team", "Today, 4:58 PM &bull; 42 min", True, True),
    ("Weekly Team Standup", "Yesterday, 9:00 AM &bull; 12 min", False, False),
    ("Negotiation Prep: Vendor Contract Renewal", "Sun, Jun 29, 3:05 PM &bull; 31 min", True, False),
    ("Renewal Pricing Sync", "Tue, Jun 24, 1:30 PM &bull; 18 min", False, False),
]
def td_sess_items():
    out = []
    for title, meta, audio, sel in TD_SESS_LIST:
        icon = session_play if audio else i_filetext_card
        out.append(f'''<div class="tsitem{" sel" if sel else ""}"><span class="ic">{icon}</span>
<div><div class="tst">{title}</div><div class="tsm">{meta}</div></div></div>''')
    return "\n".join(out)

td_sessions_content = f'''<div class="tdcontent" style="padding:16px;display:flex;overflow:hidden">
      <div class="hlwrap">
        <div class="hllist">
{td_sess_items()}
        </div>
        <div class="tspanel">
          <div class="tsphead">
            <div class="tspt">
              <div class="tsptitle">Q1 Strategy Review with Leadership Team</div>
              <div class="tspmeta">Tuesday, July 7, 2026 &bull; 4:58 PM &bull; 42 min</div>
            </div>
            <span class="cbtn">{lucide("link", 16, 300)}</span>
            <span class="cbtn">{mi_morevert}</span>
          </div>
          <div class="tsptabs"><div class="tabs">
            <span class="tab sel">Details</span><span class="tab">Highlights</span><span class="tab">Transcript</span><span class="tab">Settings</span>
          </div></div>
          <div class="tspbody">
            <div class="pcard">
              <div class="pchead"><span class="pctitle">Summary</span><span class="sp"></span><span class="picon">{ICON_DOTS}</span></div>
              <div class="pcbody">
                <p>The leadership team reviewed Q1 performance against plan and aligned on priorities heading into Q2. Revenue closed at 104% of target, driven primarily by the enterprise segment.</p>
                <p>The team agreed to revisit pricing for the annual plan at the next monthly review.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>'''

# --- topic detail: Highlights tab (wide) ---
td_highlights_content = f'''<div class="tdcontent" style="padding:16px;display:flex;overflow:hidden">
      <div class="hlwrap">
        <div class="hllist">
{hl_items()}
        </div>
        <div class="hldetail">
          <div class="hldt">Q3 roadmap timeline is at risk</div>
          <div class="hlactions">
            <span class="hlbtn">{i_share14}Share</span>
            <span class="hlbtn del">{i_trash14}Delete</span>
            <span class="hltime sm">{i_clock12}35:12</span>
          </div>
          <div class="hlsec">{i_bulb}Main Idea</div>
          <div class="hlbox">The Q3 roadmap timeline may slip because current engineering load leaves no slack for the two largest initiatives.</div>
          <div class="hlsec">{i_quote}Original Context</div>
          <div class="hlbox q">&ldquo;If we keep both initiatives scoped as they are, I don&rsquo;t see how we hit the September date &mdash; we either re-scope or we move the ship date by about three weeks.&rdquo;</div>
          <div class="hlsec">{i_chart}Analysis</div>
          <div class="hlbox">This is the second quarter in a row where engineering capacity has been raised as a delivery risk.</div>
        </div>
      </div>
    </div>'''

# --- topic detail: Settings tab ---
_swatches = "".join(
    f'<span class="sw{" sel" if c == "#FDE68A" else ""}" style="background:{c}"></span>'
    for c in ["#FDE68A", "#FED7AA", "#FECDD3", "#A7F3D0", "#BFDBFE"])
_icon_opts = "".join(
    f'<span{" class=sel" if ic == "work_outline" else ""}>{material(ic, 20)}</span>'
    for ic in ["folder", "work_outline", "medical_services_outlined", "school_outlined", "people_outline", "event_outlined"])
td_settings_content = f'''<div class="tdcontent">
      <div class="scard">
        <h3>Basic Information</h3>
        <div class="slabel">Name</div>
        <div class="sinput">Acme Corp</div>
        <div class="slabel">Description</div>
        <div class="sinput" style="min-height:64px">Client meetings and account planning</div>
      </div>
      <div class="scard">
        <h3>Appearance</h3>
        <div class="slabel">Color</div>
        <div style="margin-bottom:16px">{_swatches}</div>
        <div class="slabel">Icon</div>
        <div class="tabs"><span class="tab sel">Icons</span><span class="tab">Emojis</span></div>
        <div class="igrid">{_icon_opts}</div>
      </div>
      <div class="danger">
        <h3>Danger Zone</h3>
        <p>Delete this topic permanently. Sessions in this topic are not deleted.</p>
        <span class="delbtn">{mi_delout}Delete Topic</span>
      </div>
    </div>'''

td_sessions_html = page("Hedy — Topic Detail Sessions (Light, 1440)",
                        topic_tiles(selected="Acme Corp") + "\n" + td_shell("Sessions", td_sessions_content),
                        active="Topics", bar=topics_bar, cls="page-topic-detail")
td_highlights_html = page("Hedy — Topic Detail Highlights (Light, 1440)",
                          topic_tiles(selected="Acme Corp") + "\n" + td_shell("Highlights", td_highlights_content),
                          active="Topics", bar=topics_bar, cls="page-topic-detail")
td_settings_html = page("Hedy — Topic Detail Settings (Light, 1440)",
                        topic_tiles(selected="Acme Corp") + "\n" + td_shell("Settings", td_settings_content),
                        active="Topics", bar=topics_bar, cls="page-topic-detail")

# --- topics empty state (topics_screen.dart lines 583-627) ---
TOPICS_EMPTY = "hedy-topics-empty-light-1440.html"
topics_empty_body = f'''<div class="empty">
  <span class="eicon">{i_folder_empty}</span>
  <div class="et">No topics yet</div>
  <div class="ed">Organize your sessions by theme. Create topics to group related conversations, track ideas across meetings, and get AI-powered overviews of everything discussed.</div>
  <a class="ebtn" href="{TOPICS}">{lucide("plus", 18, 300)}Add Topic</a>
</div>'''
topics_empty_html = page("Hedy — Topics Empty (Light, 1440)", topics_empty_body,
                         active="Topics",
                         bar=topbar("Topics", "0", pro=True,
                                    buttons=(f'<span class="tbtn">{i_refresh}Refresh</span>'
                                             f'<span class="tbtn">{lucide("plus", 18, 300)}New Topic</span>')))

# ---------- highlights screen (highlights_screen.dart, flat view) ----------
HL_SCREEN = [
    ("Q3 roadmap timeline is at risk", "35m", True),
    ("Two customer success hires approved", "27m", False),
    ("Budget shifts to lifecycle campaigns", "18m", False),
    ("Onboarding capacity is the Q2 bottleneck", "12m", False),
    ("Revenue closed at 104% of target", "3m", False),
    ("Sarah recommends re-scoping two initiatives", "9m", False),
    ("Renewal terms need procurement sign-off by Aug 1", "22m", False),
    ("Lifecycle campaigns outperform paid on activation", "14m", False),
]

def hl_screen_items():
    out = []
    for title, t, sel in HL_SCREEN:
        out.append(f'''<div class="hlitem{" sel" if sel else ""}" data-t="{title}" data-time="{t}"><span class="hlic">{i_spark_hl}</span>
<div><div class="hlt">{title}</div><span class="hltime">{i_clock12}{t}</span></div></div>''')
    return "\n".join(out)

highlights_bar = topbar("Highlights", "8", pro=True,
                        buttons=f'<span class="tbtn">{i_refresh}Refresh</span>')

highlights_body = f'''<div class="hlscreen">
  <div class="hlleft">
    <div class="sort"><span class="si">{i_sortud}</span><span>Highlights</span><span class="sc">{i_chev}</span></div>
    <div class="hlcards">
{hl_screen_items()}
    </div>
  </div>
  <div class="hlright">
    <div class="hldetail">
      <div class="hldt">Q3 roadmap timeline is at risk</div>
      <div class="hlactions">
        <span class="hlbtn">{i_share14}Share</span>
        <span class="hlbtn del">{i_trash14}Delete</span>
        <span class="hltime sm">{i_clock12}35:12</span>
      </div>
      <div class="hlsec">{i_bulb}Main Idea</div>
      <div class="hlbox">The Q3 roadmap timeline may slip because current engineering load leaves no slack for the two largest initiatives.</div>
      <div class="hlsec">{i_quote}Original Context</div>
      <div class="hlbox q">&ldquo;If we keep both initiatives scoped as they are, I don&rsquo;t see how we hit the September date &mdash; we either re-scope or we move the ship date by about three weeks.&rdquo;</div>
      <div class="hlsec">{i_chart}Analysis</div>
      <div class="hlbox">This is the second quarter in a row where engineering capacity has been raised as a delivery risk. Re-scoping now would protect the September launch while keeping the pricing review on schedule.</div>
    </div>
  </div>
</div>'''

highlights_html = page("Hedy — Highlights (Light, 1440)", highlights_body,
                       active="Highlights", bar=highlights_bar, cls="page-highlights")

# ---------- settings dialog (lib/dialogs/unified_settings_dialog.dart) ----------
SETTINGS_ACCOUNT = "hedy-settings-account-light-1440.html"
SETTINGS_SESSIONS = "hedy-settings-sessions-light-1440.html"
SETTINGS_PRIVACY = "hedy-settings-privacy-light-1440.html"
SETTINGS_HELP = "hedy-settings-help-light-1440.html"

SETTINGS_SPEECH = "hedy-settings-speech-light-1440.html"
SETTINGS_PERSONAL = "hedy-settings-personalization-light-1440.html"
SETTINGS_AUTOMATION = "hedy-settings-automation-light-1440.html"

SETT_CATS = [
    ("Profile", "settings_outlined", SETTINGS),
    ("Account", "person_outline", SETTINGS_ACCOUNT),
    ("Sessions", "mic_outlined", SETTINGS_SESSIONS),
    ("Speech & AI", "description_outlined", SETTINGS_SPEECH),
    ("Personalization", "tune_outlined", SETTINGS_PERSONAL),
    ("Automation & Data", "auto_awesome_outlined", SETTINGS_AUTOMATION),
    ("Privacy", "shield_outlined", SETTINGS_PRIVACY),
    ("Help", "help_outline", SETTINGS_HELP),
]

def sett_nav(selected="Profile"):
    out = []
    for label, icon, href in SETT_CATS:
        sel = " sel" if label == selected else ""
        inner = f'<span class="ic">{material(icon, 16)}</span><span>{label}</span>'
        if href and label != selected:
            out.append(f'<a class="sditem{sel}" href="{href}">{inner}</a>')
        else:
            out.append(f'<div class="sditem{sel}">{inner}</div>')
    return "\n".join(out)

def sett_dialog(selected, content):
    return f'''<div class="ovl"><div class="sdlg">
  <div class="sdhead"><h2>Settings</h2><a class="x" href="{DASH}">{material("close", 24)}</a></div>
  <div class="sdbody">
    <div class="sdnav">
{sett_nav(selected)}
    </div>
    <div class="sdcontent">
{content}
    </div>
  </div>
</div></div>'''

mi_lock = material("lock_outline", 18)
mi_email = material("email_outlined", 18)
mi_x24 = material("close", 24)

profile_content = f'''      <div class="sdsec">Personal Information</div>
      <div class="sdcard">
        <div class="sdlabel">First Name</div>
        <div class="sdrow"><span class="sdinput">Clara</span><span class="obtn">Save</span></div>
        <div class="sdrow" style="margin-top:16px;gap:8px">
          <span class="gbtn">{mi_lock}Change Password</span>
          <span class="gbtn">{mi_email}Change Email</span>
        </div>
      </div>
      <div class="sdsec">Language Preferences</div>
      <div class="sdcard">
        <div class="sdlabel">Meeting Language</div>
        <div class="sddesc">The language spoken in your sessions.</div>
        <div class="sdrow"><span class="sdinput">English {i_chev}</span></div>
        <div class="sdlabel" style="margin-top:16px">Hedy Chat Language</div>
        <div class="sddesc">The language Hedy uses to chat with you.</div>
        <div class="sdrow"><span class="sdinput">English {i_chev}</span></div>
      </div>
      <div class="sdsec">Theme</div>
      <div class="sdcard">
        <div class="togrow"><span>Dark Mode</span><span class="sp"></span><span class="switch off"></span></div>
      </div>'''

settings_html = page("Hedy — Settings Dialog (Light, 1440)",
                     cards(selected_first=False) + "\n" + empty + "\n" + sett_dialog("Profile", profile_content),
                     active="Settings", cls="page-settings")

def _toggle_row(title, desc, on):
    return (f'<div class="setrow"><div class="sb"><div class="st">{title}</div>'
            f'<div class="sd">{desc}</div></div>'
            f'<span class="switch{"" if on else " off"}"></span></div>')

def _hrow(icon, label, trailing="arrow_forward_ios"):
    return (f'<div class="hrow"><span class="ic">{material(icon, 18)}</span><span>{label}</span>'
            f'<span class="tr">{material(trailing, 14)}</span></div>')

account_content = f'''      <div class="sdsec">Hedy Pro License</div>
      <div class="sdcard">
        <div class="setrow"><div class="sb"><div class="st">License Status</div>
          <div class="sd">Hedy Pro &mdash; active</div></div>
          <span class="gbtn">{mi_lock}Activate License Code</span></div>
      </div>
      <div class="sdsec">Share Management <span class="pro">PRO</span></div>
      <div class="sdcard">
        <div class="sddesc">View and manage all your shared content in one place.</div>
        <div class="tabs"><a class="tab sel" href="{SHARE_MGMT}">My Shares</a><a class="tab" href="{SHARE_MGMT}">Shared with Me</a><a class="tab" href="{SHARE_MGMT}">Share Links</a></div>
      </div>
      <div class="sdsec">Account</div>
      <div class="sdcard">
        <div class="setrow"><div class="sb"><div class="st">Email</div><div class="sd">clara@example.com</div></div></div>
        <div class="setrow"><div class="sb"><div class="st">Sign Out</div></div>
          <span class="gbtn">{material("logout", 18)}Sign Out</span></div>
        <div class="setrow"><div class="sb"><div class="st" style="color:#F44336">Danger Zone</div></div>
          <span class="delbtn">{material("delete_forever", 18)}Delete Account</span></div>
      </div>
      <div class="vfoot">Hedy 2.14.3 (482)<br>&copy; 2026 Hedy AI LLC</div>'''

sessions_content = f'''      <div class="sdsec">Auto-Pause After Inactivity</div>
      <div class="sdcard">
        {_toggle_row("Enable auto-pause", "Automatically pause the session if no speech is detected for 5 minutes.", False)}
      </div>
      <div class="sdsec">Save Session Audio</div>
      <div class="sdcard">
        {_toggle_row("Enable Audio Recording", "Never miss a detail. Save session audio to revisit key moments and ensure accurate records. (Remember to always get consent from participants before recording.)", True)}
      </div>
      <div class="sdsec">Automatic Suggestions</div>
      <div class="sdcard">
        <div class="sddesc">Get real-time suggestions during your conversations without having to ask Hedy first.</div>
        <div class="tabs"><span class="tab">Off</span><span class="tab">Selective</span><span class="tab sel">Balanced</span><span class="tab">Frequent</span></div>
      </div>
      <div class="sdsec">Session Type</div>
      <div class="sdcard">
        <div class="sddesc">Get the most relevant support for every conversation. Choose a session type and Hedy will provide insights and suggestions perfectly tailored to that scenario, helping you achieve your specific goals.</div>
        <div class="sdrow"><span class="sdinput">Business Meeting {i_chev}</span></div>
      </div>'''

privacy_content = f'''      <div class="sdsec">Privacy Preferences</div>
      <div class="sdcard">
        {_toggle_row("Cloud Sync", "Upload new sessions to access from any device", True)}
        {_toggle_row("Disable Cloud AI Analysis", "Transcription-only mode. This disables Hedy&rsquo;s core AI features: summaries, highlights, meeting notes, and chat will not be available. Recommended only if you have very strict privacy requirements and don&rsquo;t need Hedy&rsquo;s AI analysis.", False)}
      </div>
      <div class="sdsec">Desktop Settings</div>
      <div class="sdcard">
        {_toggle_row("Show System Tray Icon", "Access Hedy instantly. Keep the Hedy icon in your system tray for one-click access to start, pause, or manage your sessions.", True)}
        {_toggle_row("Launch at Login", "Ensure Hedy is always ready. Automatically start Hedy when you log in, so it&rsquo;s prepared to capture insights from your very first meeting of the day.", False)}
        <div class="setrow"><div class="sb"><div class="st">Quit App</div>
          <div class="sd">Close the application completely.</div></div>
          <span class="gbtn">{material("logout", 18)}Quit App</span></div>
      </div>'''

help_content = f'''      <div class="sdsec">Help &amp; Support</div>
      <div class="sdcard">
        {_hrow("play_circle_outline", "Watch Tutorial")}
        {_hrow("help_outline", "Questions? Check out our Help Center", "open_in_new")}
        {_hrow("email_outlined", "support@hedy.bot", "open_in_new")}
      </div>
      <div class="sdsec">Legal</div>
      <div class="sdcard">
        {_hrow("gpp_good_outlined", "Trust Center")}
        {_hrow("article_outlined", "Terms of Use", "open_in_new")}
        {_hrow("privacy_tip_outlined", "Privacy Policy", "open_in_new")}
        {_hrow("copyright_outlined", "Open Source Licenses", "open_in_new")}
      </div>'''

speech_content = f'''      <div class="sdsec">Speech Recognition Options</div>
      <div class="sdcard">
        <div class="sdlabel">Transcription Method</div>
        <div class="sddesc">Optimize transcription for your needs</div>
        <div class="sdrow"><span class="sdinput">Local (Whisper) {i_chev}</span></div>
      </div>
      <div class="sdcard">
        <div class="sdlabel">Model Selection</div>
        <div class="sddesc">Enhance transcription quality by selecting the best speech recognition model for your needs. The standard model offers a balance of speed and accuracy, while the larger model provides superior accuracy for non-English languages.</div>
        <div class="tabs"><span class="tab">{material("compress_outlined", 16)} Small</span><span class="tab sel">{material("balance_outlined", 16)} Regular</span><span class="tab">{material("expand_outlined", 16)} Large</span></div>
        <div style="height:20px"></div>
        {_toggle_row("Enable voice activity detection", "Automatically pause transcription when no speech is detected. Adjust sensitivity to control how aggressively silence is filtered.", True)}
        <div class="sdrow" style="margin-top:12px;align-items:center">
          <div class="ptrack" style="flex:1"><div class="pfill" style="width:50%"></div><div class="pthumb" style="left:50%"></div></div>
          <span class="hltime" style="margin:0">0.6</span>
        </div>
        <div style="height:20px"></div>
        <div class="sdlabel">Transcript Speed <span class="pro" style="background:linear-gradient(180deg,#8D8D8D,#525252)">{material("science_outlined", 10)} EXPERIMENTAL</span></div>
        <div class="sddesc">Balance real-time updates with battery life. Choose how frequently your transcript updates: &lsquo;Faster&rsquo; for near-instant updates (uses more power), or &lsquo;Normal&rsquo;/&lsquo;Slower&rsquo; for optimized battery and processing.</div>
        <div class="tabs"><span class="tab">Slower</span><span class="tab sel">Normal</span><span class="tab">Faster</span></div>
      </div>'''

personal_content = f'''      <div class="sdsec">Session Contexts <span class="pro">PRO</span></div>
      <div class="sdcard">
        <div class="sddesc">Get smarter, more personalized insights from Hedy. By providing context &ndash; like your role, company details, or project goals &ndash; Hedy can tailor its analysis and suggestions to be far more relevant and impactful for you. You can also include specific instructions, such as advice you want Hedy to give you during the session, or a preferred format for the summary. Pro users can save and switch between multiple context profiles.</div>
        {_hrow("psychology_outlined", "Account lead — Acme Corp")}
        {_hrow("psychology_outlined", "Default")}
      </div>
      <div class="sdsec">Custom Prompts</div>
      <div class="sdcard">
        <div class="sddesc">Instantly access your go-to questions and commands. Create custom prompts (e.g., &lsquo;Summarize action items for me&rsquo;) to get the information you need, faster, in any session.</div>
        {_hrow("edit_note_outlined", "Summarize action items for me")}
        {_hrow("edit_note_outlined", "What did I commit to?")}
      </div>
      <div class="sdsec">Custom Vocabulary</div>
      <div class="sdcard">
        {_toggle_row("Enable Custom Vocabulary", "Teach Hedy your specific terms, company names, and technical jargon. These terms improve real-time transcription accuracy and are automatically corrected during transcript cleanup.", True)}
        <div class="sdrow" style="margin-top:16px"><span class="sdinput" style="color:var(--n40)">Add a term&hellip;</span><span class="obtn">Add</span></div>
        <div class="chiprow" style="margin-top:12px">
          <span class="qchip">Acme Corp {lucide("x", 14)}</span>
          <span class="qchip">Portkey {lucide("x", 14)}</span>
          <span class="qchip">NREMT {lucide("x", 14)}</span>
        </div>
        <div class="sdrow" style="margin-top:16px;gap:8px">
          <span class="gbtn">{material("upload_outlined", 18)}Import</span>
          <span class="gbtn">{material("download_outlined", 18)}Export</span>
          <span class="gbtn" style="color:#F44336">{mi_delout}Clear All</span>
        </div>
      </div>'''

automation_content = f'''      <div class="sdsec">Auto Recap Email</div>
      <div class="sdcard">
        {_toggle_row("Enable Auto Recap Email", "Keep everyone informed effortlessly. Automatically send key takeaways and a session summary via email after each meeting. (Note: Emails are sent unencrypted; please consider conversation confidentiality.)", False)}
      </div>
      <div class="sdsec">Auto Meeting Minutes <span class="pro">PRO</span></div>
      <div class="sdcard">
        {_toggle_row("Enable Auto Detailed Notes", "Save time and ensure nothing is missed. Hedy can automatically create comprehensive detailed notes at the end of each session, ready for review or sharing.", False)}
      </div>
      <div class="sdsec">Export Data</div>
      <div class="sdcard">
        {_hrow("download_outlined", "Export Data")}
        <div class="sddesc" style="margin:8px 0 0">Download your sessions, topics, and highlights</div>
      </div>
      <div class="sdsec">API Access <span class="pro">PRO</span></div>
      <div class="sdcard">
        <div class="sddesc">Automate your workflows and integrate Hedy with your favorite tools. Generate an API key to connect Hedy data to Zapier, CRMs, and more, streamlining how you use your meeting insights. (Cloud Sync must be active).</div>
        <div class="sdrow"><span class="obtn">Generate API Key</span></div>
        <div class="setrow" style="margin-top:16px"><div class="sb"><div class="st">API Endpoint</div>
          <div class="sd" style="font-family:ui-monospace,monospace;font-size:12px">https://api.hedy.bot/v1</div></div>
          <span class="cbtn">{material("content_copy_rounded", 16)}</span></div>
        {_toggle_row("Auto Export Todos", "Streamline your task management. Automatically send all your Hedy-generated To-Dos to your connected tools (via webhook) after each session, ensuring action items flow directly into your workflow.", False)}
        <div class="sdrow" style="margin-top:16px"><span class="gbtn">{material("webhook_outlined", 18)}Manage Webhooks</span></div>
      </div>'''

_sett_bg = cards(selected_first=False) + "\n" + empty
settings_account_html = page("Hedy — Settings Account (Light, 1440)",
                             _sett_bg + "\n" + sett_dialog("Account", account_content),
                             active="Settings", cls="page-settings")
settings_sessions_html = page("Hedy — Settings Sessions (Light, 1440)",
                              _sett_bg + "\n" + sett_dialog("Sessions", sessions_content),
                              active="Settings", cls="page-settings")
settings_privacy_html = page("Hedy — Settings Privacy (Light, 1440)",
                             _sett_bg + "\n" + sett_dialog("Privacy", privacy_content),
                             active="Settings", cls="page-settings")
settings_help_html = page("Hedy — Settings Help (Light, 1440)",
                          _sett_bg + "\n" + sett_dialog("Help", help_content),
                          active="Settings", cls="page-settings")
settings_speech_html = page("Hedy — Settings Speech AI (Light, 1440)",
                            _sett_bg + "\n" + sett_dialog("Speech & AI", speech_content),
                            active="Settings", cls="page-settings")
settings_personal_html = page("Hedy — Settings Personalization (Light, 1440)",
                              _sett_bg + "\n" + sett_dialog("Personalization", personal_content),
                              active="Settings", cls="page-settings")
settings_automation_html = page("Hedy — Settings Automation (Light, 1440)",
                                _sett_bg + "\n" + sett_dialog("Automation & Data", automation_content),
                                active="Settings", cls="page-settings")

# ---------- search overlay (lib/components/search_overlay.dart) ----------
i_search20 = lucide("search", 20)
i_x18 = lucide("x", 18)
i_ft14 = lucide("file-text", 14, 300)
i_folder14 = lucide("folder", 14)
i_spark14 = lucide("sparkles", 14, 300)
i_ft16 = lucide("file-text", 16, 300)
i_folder16 = lucide("folder", 16)
i_spark16 = lucide("sparkles", 16, 300)

search_overlay = f'''<div class="ovl blur"><div class="swrap">
  <div class="sbox"><span class="si">{i_search20}</span><span class="q">roadmap</span><span class="cx">{i_x18}</span></div>
  <div class="sres">
    <div class="ssec">{i_ft14}SESSIONS</div>
    <div class="sitem"><span class="ic">{i_ft16}</span><div style="min-width:0;flex:1">
      <div class="sit">Product Roadmap Planning for Q4</div>
      <div class="sis">&hellip;shift budget from paid acquisition toward lifecycle campaigns&hellip;</div></div></div>
    <div class="sitem"><span class="ic">{i_ft16}</span><div style="min-width:0;flex:1">
      <div class="sit">Q1 Strategy Review with Leadership Team</div>
      <div class="sis">&hellip;concerns about the Q3 roadmap timeline given current engineering load&hellip;</div></div></div>
    <div class="ssec">{i_folder14}TOPICS</div>
    <div class="sitem"><span class="ic">{i_folder16}</span><div style="min-width:0;flex:1">
      <div class="sit">Product Roadmap</div></div></div>
    <div class="ssec">{i_spark14}HIGHLIGHTS</div>
    <div class="sitem"><span class="ic">{i_spark16}</span><div style="min-width:0;flex:1">
      <div class="sit">Q3 roadmap timeline is at risk</div></div></div>
  </div>
</div></div>'''

search_html = page("Hedy — Search Overlay (Light, 1440)",
                   cards(selected_first=False) + "\n" + empty + "\n" + search_overlay,
                   active="Search", cls="page-search")

SEARCH_EMPTY = "hedy-search-empty-light-1440.html"
SEARCH_NORES = "hedy-search-noresults-light-1440.html"
i_searchx48 = lucide("search-x", 48)

search_empty_overlay = f'''<div class="ovl blur"><div class="swrap">
  <div class="sbox"><span class="si">{i_search20}</span><a class="q ph" href="{SEARCH}" style="display:block">Search</a></div>
  <div class="sres"><div class="shint">Search sessions, topics, highlights...</div></div>
</div></div>'''
search_empty_html = page("Hedy — Search Empty (Light, 1440)",
                         cards(selected_first=False) + "\n" + empty + "\n" + search_empty_overlay,
                         active="Search", cls="page-search")

search_nores_overlay = f'''<div class="ovl blur"><div class="swrap">
  <div class="sbox"><span class="si">{i_search20}</span><span class="q">xylophone</span><a class="cx" href="{SEARCH_EMPTY}">{i_x18}</a></div>
  <div class="sres"><div class="snores">
    <span class="ic">{i_searchx48}</span>
    <div class="snorest">No matches</div>
    <div class="snoress">Try searching with different keywords</div>
  </div></div>
</div></div>'''
search_nores_html = page("Hedy — Search No Results (Light, 1440)",
                         cards(selected_first=False) + "\n" + empty + "\n" + search_nores_overlay,
                         active="Search", cls="page-search")

# ---------- paywall (lib/screens/subscription_screen.dart desktop) ----------
PAYWALL = "hedy-paywall-light-1440.html"
paywall_html = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=1440">
<title>Hedy — Subscription (Light, 1440)</title>
{CAPTURE}
<style>
{fontfaces}
{CSS}
</style>
</head><body class="page-onb">
<div class="paywrap">
  <div class="paycol">
    <h2>Manage Your Subscription</h2>
    <p>Subscriptions are managed through our secure billing portal.</p>
    <span class="obtn">Open Billing Portal</span>
    <span class="paylink">Not now</span>
  </div>
</div>
</body></html>'''

# ---------- recording + paused states ----------
RECORDING = "hedy-recording-light-1440.html"
PAUSED = "hedy-recording-paused-light-1440.html"
mi_lockout = material("lock_outline", 20)

def live_shell(paused=False):
    temp = ('' if paused else
            ' <span class="temp">and if we look at the stage-four pipeline, the two accounts most likely to close this month are</span>')
    tabs = "\n".join(
        f'<span class="tab{" sel" if label == "Transcript" else ""}">{label}</span>'
        for label, _ in DETAIL_TABS)
    banner = f'''<div class="sdbanner">
      <div class="sdbrow">
        <a class="tdback" href="{DASH}">{material("arrow_back", 16)}</a>
        <span class="sdbicon">{state_icon("session-paused-icon" if paused else "session-active-icon")}</span>
        <div class="sdbody2">
          <div class="sdbtitle">Current Session</div>
          <div class="sdbmeta"><span>Tuesday, July 7, 2026 &bull; 4:58 PM &bull; 12 min</span><span class="chip amber">Acme Corp</span></div>
        </div>
        <span class="mbtn">{ICON_DOTS}</span>
      </div>
      <div class="sdbtabs"><div class="tabs">
{tabs}
      </div></div>
    </div>'''
    return f'''<div class="detail"><div class="glass">
  <div class="dleft">
    {banner}
    <div class="dhead">
      <span class="hicon">{session_play}</span>
      <div class="dht">
        <div class="dtitle">Current Session</div>
        <div class="dmeta"><span>Tuesday, July 7, 2026 &bull; 4:58 PM &bull; 12 min</span><span class="chip amber">Acme Corp</span></div>
      </div>
      <span class="mbtn">{ICON_DOTS}</span>
    </div>
    <div class="dsep"></div>
    <div class="tabswrap"><div class="tabs">
{tabs}
    </div></div>
    <div class="dbody trans">
      <div class="tbox live">
        <p>Alright, let&rsquo;s get started. First on the agenda is the Q1 close. Revenue landed at 104 percent of target, and the enterprise segment carried most of that overage. Self-serve growth slowed again, which is the second consecutive quarter we&rsquo;ve seen that pattern.</p>
        <p>On the pipeline side, enterprise looks strong going into Q2, but I want to flag that onboarding capacity is the limiting factor right now.{temp}</p>
      </div>
      <div class="fabs">
        <span class="fab">{mi_copy}</span>
        <span class="fab">{mi_lockout}</span>
      </div>
    </div>
  </div>
  <div class="dsplit"></div>
  <div class="dchat">
    <div class="chathead"><span class="cht">Chat</span><span class="sp"></span><span class="tctx">Topic context</span><span class="switch"></span></div>
    <div class="dsep"></div>
    <div class="chatlog">
      <div class="bubble user">What did they say about self-serve growth?</div>
      <div class="bubble hedy">Self-serve growth slowed for the second consecutive quarter, while the enterprise segment carried the revenue overage &mdash; Q1 closed at 104% of target.</div>
    </div>
    <div class="chatin">
      <div class="chiprow">
        <span class="qchip">Summarize so far {ICON_SPARK}</span>
        <span class="qchip">What should I ask next? {ICON_SPARK}</span>
        <span class="qmore">More {ICON_SPARK12}</span>
      </div>
      <div class="inbox"><span class="inhint">How can I help?</span><span class="send">{ICON_UP}</span></div>
    </div>
  </div>
</div></div>'''

recording_html = page("Hedy — Recording (Light, 1440)",
                      cards(selected_first=True) + "\n" + live_shell(False), mode="recording",
                      cls="page-session-detail")
paused_html = page("Hedy — Recording Paused (Light, 1440)",
                   cards(selected_first=True) + "\n" + live_shell(True), mode="paused",
                   cls="page-session-detail")

# ---------- onboarding flow ----------
ONB = {i: f"hedy-onboarding-{s}-light-1440.html" for i, s in enumerate(
    ["welcome", "language", "name", "meeting-language", "usecase",
     "challenge", "signup", "cloud-sync"], 1)}

glasses_logo_svg = open(f"{REPO}/assets/images/hedy-glasses-logo-lovable.svg", encoding="utf-8").read()
glasses_logo_svg = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", glasses_logo_svg, flags=re.S).strip()
glasses_logo_svg = glasses_logo_svg.replace("<svg ", '<svg style="height:180px;width:auto" ', 1)

def flag(code):
    src = open(f"{REPO}/assets/images/language-icons/{code}.svg", encoding="utf-8").read()
    return re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", src, flags=re.S).strip()

mi_back = material("arrow_back_rounded", 24)
mi_fwd = material("arrow_forward_rounded", 20)

def onb_doc(fname, title, body, step=None, back_href=None):
    if step is not None:
        pct = round(step / 7 * 100)
        back = (f'<a class="oback" href="{back_href}">{mi_back}</a>' if back_href
                else f'<span class="oback" style="opacity:.3">{mi_back}</span>')
        prog = (f'<div class="oprog">{back}'
                f'<div class="otrack"><div class="ofill" style="width:{pct}%"></div></div>'
                f'<span class="osp"></span></div>')
    else:
        prog = ""
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=1440">
<title>{title}</title>
{CAPTURE}
<style>
{fontfaces}
{CSS}
</style>
</head><body class="onbbody page-onb">
{prog}
<div class="ocenter">
{body}
</div>
</body></html>'''

def lang_cards(next_href):
    langs = [("en", "English", "Suggested for you", True),
             ("es", "Español", "Spanish", False),
             ("fr", "Français", "French", False),
             ("de", "Deutsch", "German", False),
             ("pt", "Português", "Portuguese", False)]
    out = []
    for code, native, sub, sug in langs:
        out.append(f'''<a class="lcard" href="{next_href}"><span class="lflag">{flag(code)}</span>
<div class="lbody"><div class="lname">{native}</div><div class="lsub{" sug" if sug else ""}">{sub}</div></div>
<span class="lgo">{mi_fwd}</span></a>''')
    return "\n".join(out)

onb_pages = {}

onb_pages[ONB[1]] = onb_doc(ONB[1], "Hedy — Onboarding: Welcome (Light, 1440)", f'''
<div class="ocol narrow">
  <div class="wlogo">{glasses_logo_svg}</div>
  <div class="wtitle">Hi, I&rsquo;m Hedy</div>
  <div class="wdesc">I&rsquo;m your personal meeting coach. I&rsquo;ll listen to your conversations, help you stay focused, and give you insights to communicate more effectively.</div>
  <a class="wbtn" href="{ONB[2]}">Let&rsquo;s Get Started {mi_fwd}</a>
  <a class="wlink" href="{ONB[7]}">I already have an account</a>
</div>''')

onb_pages[ONB[2]] = onb_doc(ONB[2], "Hedy — Onboarding: Hedy Language (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead">What language would you like me to use?</div>
{lang_cards(ONB[3])}
</div>''', step=1, back_href=ONB[1])

onb_pages[ONB[3]] = onb_doc(ONB[3], "Hedy — Onboarding: Name (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead tight">What should I call you?</div>
  <div class="nhelp">This is how I&rsquo;ll address you when we chat!</div>
  <a class="ninput" href="{ONB[4]}">Clara</a>
</div>''', step=2, back_href=ONB[2])

onb_pages[ONB[4]] = onb_doc(ONB[4], "Hedy — Onboarding: Meeting Language (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead">Nice to meet you, Clara! What language are your meetings in?</div>
{lang_cards(ONB[5])}
</div>''', step=3, back_href=ONB[3])

USECASES = [
    ("💼", "Professional Meetings", "Become the most insightful voice in every discussion"),
    ("📚", "Learning &amp; Development", "Master complex knowledge and accelerate your growth"),
    ("🧠", "Personal Support", "Remember everything important, and inspire ideas, effortlessly"),
    ("✍️", "Content &amp; Creative Work", "Create extraordinary work through deeper insights"),
]
uc_cards = "\n".join(
    f'''<a class="ucard" href="{ONB[6]}"><span class="uemoji">{e}</span>
<div><div class="utitle">{t}</div><div class="udesc">{d}</div></div></a>'''
    for e, t, d in USECASES)
onb_pages[ONB[5]] = onb_doc(ONB[5], "Hedy — Onboarding: Use Case (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead">Clara, what brings you to Hedy?</div>
{uc_cards}
</div>''', step=4, back_href=ONB[4])

CHALLENGES = [
    ("psychology_outlined", "Too many meetings, need to focus on participation",
     "Contribute brilliant ideas while everything gets captured"),
    ("person_outline", "Client details get lost between calls",
     "Be the professional who remembers every commitment"),
    ("checklist_outlined", "Team action items don&rsquo;t get completed",
     "Drive task completion across your entire team"),
    ("translate_outlined", "International calls in multiple languages",
     "Lead confidently across cultures and languages"),
]
ch_cards = "\n".join(
    f'''<a class="ccard" href="{ONB[7]}"><span class="cic">{material(ic, 24)}</span>
<div><div class="ctitle">{t}</div><div class="cdesc">{d}</div></div></a>'''
    for ic, t, d in CHALLENGES)
onb_pages[ONB[6]] = onb_doc(ONB[6], "Hedy — Onboarding: Challenge (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead">How can I support you the best?</div>
{ch_cards}
</div>''', step=5, back_href=ONB[5])

google_svg = open(f"{REPO}/assets/images/google-icon-logo.svg", encoding="utf-8").read()
google_svg = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", google_svg, flags=re.S).strip()
google_svg = re.sub(r'width="[^"]*" height="[^"]*"', 'width="24" height="24"', google_svg, count=1)

onb_pages[ONB[7]] = onb_doc(ONB[7], "Hedy — Onboarding: Sign Up (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead">To help you excel at work, let&rsquo;s create your account</div>
  <a class="ccard" href="{ONB[8]}"><span class="cic">{google_svg}</span><div><div class="ctitle">Continue with Google</div></div></a>
  <a class="ccard" href="{ONB[8]}"><span class="cic ink">{material("apple", 28)}</span><div><div class="ctitle">Continue with Apple</div></div></a>
  <a class="ccard" href="{ONB[8]}"><span class="cic">{material("email_outlined", 24)}</span><div><div class="ctitle">Sign up with email</div></div></a>
  <div class="sagree">By signing up, you agree to our <u>Terms of Use</u> and <u>Privacy Policy</u>.</div>
  <div class="shave">Already have an account? <b>Sign In</b></div>
</div>''', step=6, back_href=ONB[6])

onb_pages[ONB[8]] = onb_doc(ONB[8], "Hedy — Onboarding: Cloud Sync (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead tight">One Last Thing</div>
  <div class="nhelp">Where should I keep your conversation history? Cloud sync lets me help you across all your devices. You can change this anytime in settings.</div>
  <a class="ucard" href="{CTX_INTRO}"><span class="uic">{material("cloud_done", 28)}</span>
<div><div class="utitle">Sync Across Devices</div><div class="udesc">I&rsquo;ll remember everything across your phone, tablet, and computer. Your data is encrypted and backed up.</div></div></a>
  <a class="ucard" href="{CTX_INTRO}"><span class="uic">{material("phone_iphone", 28)}</span>
<div><div class="utitle">Keep It Private on This Device</div><div class="udesc">I&rsquo;ll only store data on this device. Perfect if privacy is your top priority.</div></div></a>
</div>''', step=7, back_href=ONB[7])

# --- sign in (signin_screen.dart) ---
SIGNIN = "hedy-signin-light-1440.html"
mi_email24 = material("email_outlined", 24)
mi_lockr = material("lock_outline_rounded", 24)
signin_html = onb_doc(SIGNIN, "Hedy — Sign In (Light, 1440)", f'''
<div class="ocol narrow">
  <div class="ohead" style="font-size:28px;margin-bottom:24px">Welcome back!</div>
  <a class="ccard" href="{DASH}"><span class="cic">{google_svg}</span><div><div class="ctitle">Continue with Google</div></div></a>
  <a class="ccard" href="{DASH}"><span class="cic ink">{material("apple", 28)}</span><div><div class="ctitle">Continue with Apple</div></div></a>
  <div style="height:12px"></div>
  <div class="sifield"><span class="ic">{mi_email24}</span><span class="ph">Email address</span></div>
  <div class="sifield"><span class="ic">{mi_lockr}</span><span class="ph">Password</span></div>
  <a class="sibtn" href="{DASH}">Login</a>
  <span class="silink">Forgot password?</span>
  <a class="sisub" href="{ONB[7]}">Don&rsquo;t have an account? <span style="color:var(--orange)">Sign Up</span></a>
</div>''')

# --- merge sessions flow (merge_sessions_screen.dart + merge_configuration_screen.dart) ---
mi_desc24 = material("description_outlined", 24)

def _msession(title, meta, on=False):
    return (f'<div class="msel{" on" if on else ""}"><span class="ic">{mi_desc24}</span>'
            f'<div style="min-width:0;flex:1"><div class="mst">{title}</div>'
            f'<div class="msm">{meta}</div></div></div>')

merge_dialog = f'''<div class="ovl"><div class="mdlg">
  <div class="mdhead"><span class="sp48"></span><h2>Merge Sessions</h2><a class="ic" href="{DASH}">{material("close", 20)}</a></div>
  <div class="mdbody">
    <div class="minfo"><span class="ic">{mi_info}</span><span>Select two sessions to merge. The merged session will combine audio, transcripts, and chats from both sessions.</span></div>
    <div class="mlabel">First Session</div>
    {_msession("Q1 Strategy Review with Leadership Team", "Jul 7, 2026 &bull; 4:58 PM &bull; 42 minutes", on=True)}
    <div class="mlabel">Second Session</div>
    {_msession("Weekly Team Standup", "Jul 6, 2026 &bull; 9:00 AM &bull; 12 minutes", on=True)}
  </div>
  <div class="mbtnrow"><a class="mbig" href="{MERGE_CONFIG}">Continue</a></div>
</div></div>'''
merge_html = page("Hedy — Merge Sessions (Light, 1440)",
                  cards(selected_first=False) + "\n" + empty + "\n" + merge_dialog,
                  cls="page-settings")

merge_config_dialog = f'''<div class="ovl"><div class="mdlg">
  <div class="mdhead"><a class="ic" href="{MERGE}">{material("arrow_back", 20)}</a><h2>Merge Configuration</h2><a class="ic" href="{DASH}">{material("close", 20)}</a></div>
  <div class="mdbody">
    <div class="mlabel">Sessions to Merge</div>
    {_msession("Q1 Strategy Review with Leadership Team", "Jul 7, 2026 &bull; 4:58 PM &bull; 42 minutes")}
    {_msession("Weekly Team Standup", "Jul 6, 2026 &bull; 9:00 AM &bull; 12 minutes")}
    <div class="mlabel" style="margin-top:4px">Merge Settings</div>
    <div class="mlabel2">Session Type</div>
    <div class="mdrop">Business Meeting {i_chev}</div>
    <div class="mlabel2">Session Context</div>
    <div class="mdrop">Account lead &mdash; Acme Corp {i_chev}</div>
    <div class="mlabel2">Topics</div>
    <div class="mdrop">Acme Corp {i_chev}</div>
  </div>
  <div class="mbtnrow"><a class="mbig" href="{DASH}">Merge Sessions</a></div>
</div></div>'''
merge_config_html = page("Hedy — Merge Configuration (Light, 1440)",
                         cards(selected_first=False) + "\n" + empty + "\n" + merge_config_dialog,
                         cls="page-settings")

# --- share management (share_management_screen.dart) ---
def _smcard(icon, title, line1, line2, menu=True):
    tr = f'<span class="tr">{mi_morevert}</span>' if menu else f'<span class="tr">{material("visibility", 20)}</span>'
    return (f'<div class="smcard"><span class="ic">{material(icon, 24)}</span>'
            f'<div style="min-width:0;flex:1"><div class="smt">{title}</div>'
            f'<div class="sms">{line1}</div><div class="sms">{line2}</div></div>{tr}</div>')

share_mgmt_html = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=1440">
<title>Hedy — Share Management (Light, 1440)</title>
{CAPTURE}
<style>
{fontfaces}
{CSS}
</style>
</head><body style="flex-direction:column">
<div class="smbar">
  <h1><a class="tdback" href="{SETTINGS_ACCOUNT}">{material("arrow_back", 16)}</a> Invites</h1>
  <div class="smtabs">
    <span class="smtab sel">Shared by Me</span>
    <span class="smtab">Shared with Me</span>
    <span class="smtab">Invite Links</span>
  </div>
</div>
<div class="smlist">
  {_smcard("description_rounded", "Q1 Strategy Review with Leadership Team", "Invited sarah.chen@acme.com", "Jul 8, 2026")}
  {_smcard("folder_copy_outlined", "Acme Corp", "Invited julian@hedy.bot", "Jul 5, 2026")}
  {_smcard("description_rounded", "Negotiation Prep: Vendor Contract Renewal", "Invited procurement@acme.com", "Jun 30, 2026")}
</div>
</body></html>'''

# --- context creation flow (context_creation_*.dart) ---
glasses_logo_100 = glasses_logo_svg.replace("height:180px", "height:100px")

ctx_intro_html = onb_doc(CTX_INTRO, "Hedy — Context Intro (Light, 1440)", f'''
<div class="ocol narrow">
  <div class="wlogo">{glasses_logo_100}</div>
  <div class="ohead" style="font-size:26px;margin-bottom:16px">Let me get to know you!</div>
  <div class="wdesc" style="margin-top:0">A few quick questions about your work so I can give you more relevant insights during your meetings.</div>
  <a class="sibtn" href="{CTX_QUESTION}" style="margin-top:60px">Let&rsquo;s go!</a>
  <a class="ctxskip" href="{DASH}">Maybe later</a>
</div>''')

ctx_question_html = onb_doc(CTX_QUESTION, "Hedy — Context Question (Light, 1440)", f'''
<div class="ocol narrow">
  <div class="qprog">Question 1 of 4</div>
  <div class="ohead" style="font-size:26px;margin-bottom:20px">How do colleagues refer to you in meetings?</div>
  <div class="ctxcard">
    <span class="ctxin">Sarah, Dr. Smith, etc.</span>
    <a class="ctxarrow" href="{CTX_STREAMING}">{material("arrow_forward_rounded", 24)}</a>
  </div>
  <a class="ctxskip" href="{CTX_STREAMING}">Skip</a>
</div>''', step=1, back_href=CTX_INTRO)

ctx_streaming_html = onb_doc(CTX_STREAMING, "Hedy — Context Streaming (Light, 1440)", f'''
<div class="ocol narrow">
  <div class="wlogo">{glasses_logo_100}</div>
  <div class="ohead" style="font-size:26px;margin-bottom:24px">Getting to know you...</div>
  <div style="align-self:center">
    <div class="steprow done"><span class="ic">{material("check_circle", 24)}</span><span>Analyzing your answers...</span></div>
    <div class="steprow active"><span class="ic"><span class="spin"></span></span><span>Building your profile...</span></div>
    <div class="steprow pending"><span class="ic">{material("circle_outlined", 24)}</span><span>Personalizing your experience...</span></div>
  </div>
  <a class="ctxskip" href="{CTX_REVIEW}" style="margin-top:32px;opacity:.7">Skip for now</a>
</div>''')

ctx_review_html = onb_doc(CTX_REVIEW, "Hedy — Context Review (Light, 1440)", f'''
<div class="ocol">
  <div class="ohead" style="font-size:26px;margin-bottom:8px">Your personal context is ready! &#x2728;</div>
  <div class="nhelp" style="color:rgba(38,35,26,.6)">A context tells me who you are and what you need, so I can be a better assistant. You can edit this anytime in Settings.</div>
  <div class="ctxeditor">Clara is an account lead working with enterprise clients, primarily Acme Corp. In meetings, colleagues call her Clara.

Her work centers on quarterly strategy reviews, contract renewals, and coordinating customer success capacity. She wants Hedy to track commitments made in meetings, flag delivery risks early, and keep summaries focused on decisions and action items.

Preferred summary format: short overview paragraph followed by bulleted decisions and to-dos with owners.</div>
  <a class="sibtn" href="{DASH}" style="margin-top:24px">Save &amp; Get Started</a>
  <a class="ctxskip" href="{DASH}">Skip for now</a>
</div>''')

# ---------- dark set (systematic light->dark transform, values from colors.dart etc.) ----------
logo_png_dark = "data:image/png;base64," + b64(f"{REPO}/assets/images/hedy-glasses-logo-lovable-dark.png")

DARK_MAP = {
    # base tokens (colors.dart HedyThemeColors + theme_config.dart)
    "#FBFAF9": "#1A1A1A", "#26231A": "#F8F8F8", "#E8E4DE": "#333333",
    "#736359": "#C6C6C6", "#6F6F6F": "#C6C6C6", "#2A2522": "#F8F8F8",
    "#8A7C75": "#C6C6C6", "#2B2724": "#FFFFFF", "#8A817A": "#8A8A8A",
    "rgba(240,237,233,.5)": "#2A2A2A", "#E8E3DC": "#3A3A3A",
    "rgba(232,228,222,.5)": "rgba(51,51,51,.5)",
    "rgba(255,255,255,.75)": "rgba(42,42,42,.75)",
    # selection tints (enhanced_nav_button.dart, topic_details, highlights_screen)
    "#FFF5F0": "#3D2E25", "#E8C4B8": "#5A4035", "#FFD4C4": "#5A4035",
    # mobile scaffold (adaptive_dashboard.dart mobile nav)
    "rgba(251,250,249,.95)": "rgba(50,50,50,.95)",
    "#D8D2CC": "rgba(255,255,255,.1)", "#FFF0E5": "#3D3530",
    "#FFF0E8": "#4A3328", "#F9F7F5": "#2D2D2D",
    "#EFF8F0": "#1E3225", "#FFF8E1": "#3D3520",
    # neutrals / fills
    "#EEEEEE": "#424242", "#E0E0E0": "#3D3D3D", "#F8F8F8": "#323232",
    "#F5F5F5": "#2A2A2A", "#FAFAFA": "#1A1A1A", "#F8EEE4": "#222222",
    "#666666": "#A3A3A3", "#757575": "#BDBDBD",
    "rgba(128,128,128,.1)": "rgba(255,255,255,.05)",
    "rgba(128,128,128,.2)": "rgba(255,255,255,.1)",
    "rgba(240,237,233,.2)": "rgba(255,255,255,.05)",
    "rgba(0,0,0,.87)": "rgba(255,255,255,.7)",
    "rgba(38,35,26,.6)": "rgba(248,248,248,.6)",
    "rgba(38,35,26,.3)": "rgba(248,248,248,.3)",
    "rgba(111,111,111,.5)": "rgba(141,141,141,.5)",
    "rgba(253,230,138,0.1)": "rgba(253,230,138,0.2)",
    "rgba(253,230,138,0.15)": "rgba(253,230,138,0.25)",
    # rail logo
    logo_png: logo_png_dark,
}

# Component-specific dark values that share a light color with something else
DARK_OVERRIDES = """<style>
:root{--card:#2A2A2A}
.rail{background:#323232}
.dchat{background:#222222}
.mni{background:#3A3A3A}
.seltopic{background:rgba(66,66,66,.5);border-color:#616161;color:#BDBDBD}
.bubble.hedy{background:#323232;color:#F8F8F8}
.tab.sel{background:#3D3D3D;color:#FFFFFF}
.sditem.sel{background:#3A3A3A}
.hlleft .hlitem.sel{background:#4A3328;border-color:#6B4A3A}
.sbox,.sres,.sdlg{background:#2C2C2C}
.sdinput{background:#383838}
.ovl.blur{background:rgba(0,0,0,.5)}
.ssec,.sis{color:#8D8D8D}
.sbox .si,.sbox .cx{color:#8D8D8D}
.card{background:#2A2A2A}
.card.sel{background:#3D2E25;border-color:#5A4035}
</style>"""

_dark_re = re.compile("|".join(re.escape(k) for k in
                               sorted(DARK_MAP, key=len, reverse=True)))

def darken(html):
    out = _dark_re.sub(lambda m: DARK_MAP[m.group(0)], html)
    out = out.replace("-light-1440.html", "-dark-1440.html")
    out = out.replace("(Light, 1440)", "(Dark, 1440)")
    out = out.replace("</head>", DARK_OVERRIDES + "\n</head>")
    return out

# ---------- mobile pages (390x844, from _buildMobileLayout / non-XL branches @ dbb0f260c) ----------
MOB_DASH = "hedy-sessions-dashboard-mobile-light-390.html"

MOBILE_UI_CSS = """
.mstatus{height:47px}
.mscroll{position:absolute;top:47px;bottom:90px;left:0;right:0;overflow:hidden;padding:0 16px 8px}
.mtopbar{min-height:56px;padding:10px 0;display:flex;align-items:center;background:#FBFAF9}
.mtopbar h1{font-size:18px;font-weight:600;color:#26231A}
.mcount{width:24px;height:24px;border-radius:50%;background:#EEEEEE;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:600;color:#6F6F6F;margin-left:8px}
.msp{flex:1}
.mfilters{display:inline-flex;align-items:center;gap:8px;min-height:36px;padding:8px 12px;border-radius:8px;background:rgba(240,237,233,.5);border:1px solid #E8E3DC;color:#2B2724;font-size:13px;font-weight:500}
.mmore{padding:8px;margin-left:4px;color:#26231A;display:flex}
.msort{padding:6px 4px 8px;display:flex;align-items:center;color:#2B2724;font-size:13px;font-weight:500}
.msort .si{margin-right:6px;display:flex}.msort .sc{margin-left:4px;display:flex}
.mcard{background:#FFFFFF;border:1px solid #E8E4DE;border-radius:8px;margin-bottom:12px;padding:17px 16px;display:flex;gap:20px;align-items:flex-start}
.mcard .cicon{color:#736359;flex-shrink:0;padding-top:2px;display:flex;position:relative}
.micb{position:absolute;top:-4px;right:-4px;width:13px;height:13px;border-radius:50%;background:linear-gradient(180deg,#5BC8FF,#0A8EF0);border:1.5px solid #FFFFFF;display:flex;align-items:center;justify-content:center;color:#fff}
.mcc{flex:1;min-width:0}
.mct{font-size:13.3px;color:#26231A;line-height:1.4;margin-bottom:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.mcm{font-size:11.1px;color:#6F6F6F}
.mchip{margin-top:6px;display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:9999px;font-size:10px;font-weight:600}
.mchip.amber{background:#FDE68A;color:#92400E}
.mchip.peach{background:#FED7AA;color:#9A3412}
.mchip.rose{background:#FFE4E6;color:#9F1239}
.seltopic{margin-top:6px;display:inline-flex;align-items:center;gap:2px;height:28px;padding:0 4px 0 8px;border-radius:6px;background:rgba(238,238,238,.6);border:1px solid #E0E0E0;font-size:11px;color:#757575}
.seltopic svg{margin-right:4px}
.myear{font-size:14px;font-weight:600;color:#6F6F6F;padding:12px 0}
/* bottom nav (adaptive_dashboard.dart:669) */
.mnav{position:absolute;left:0;right:0;bottom:0;height:90px;padding:12px 12px 34px;background:rgba(251,250,249,.95);border-top:1px solid #E8E4DE;display:flex;align-items:center;justify-content:space-around}
.mstart{width:56px;height:56px;border-radius:12px;background:#E26515;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.2)}
.mni{width:44px;height:44px;border-radius:10px;background:#F5F5F5;border:0.5px solid #D8D2CC;display:flex;align-items:center;justify-content:center;color:#736359}
.mni.sel{background:#FFF0E5;color:#E26515}
"""

MOBILE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-font-smoothing:antialiased}
body{font-family:'Inter',sans-serif;width:390px;height:844px;overflow:hidden;position:relative;
background:linear-gradient(160deg,#F8EEE4,#FBFAF9);color:#26231A}
""" + MOBILE_UI_CSS

def mobile_page(title, body):
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=390">
<title>{title}</title>
{CAPTURE}
<style>
{fontfaces}
{MOBILE_CSS}
</style>
</head><body>
{body}
</body></html>'''

glasses_white_24 = glasses_white.replace("height:24px", "height:24px")
i_mfilters = lucide("sliders-horizontal", 18, 300)
mi_morevert24 = material("more_vert", 24)
_mnav_icons = {
    "Sessions": lucide("file-text", 20, 300), "Topics": lucide("folder-open", 20, 300),
    "Highlights": lucide("sparkles", 20, 300), "Search": lucide("search", 20, 300),
    "Settings": lucide("settings", 20, 300)}

def mobile_nav(active="Sessions"):
    items = [f'<span class="mstart">{glasses_white_24}</span>']
    for label, ic in _mnav_icons.items():
        items.append(f'<span class="mni{" sel" if label == active else ""}">{ic}</span>')
    return '<div class="mnav">' + "".join(items) + '</div>'

def mobile_cards():
    out = []
    for title, meta, audio, chip in SESSIONS:
        icon = session_play if audio else i_filetext_card
        icb = f'<span class="micb">{material("cloud_done", 8)}</span>' if audio else ""
        chip_m = chip.replace('class="chip', 'class="mchip')
        if not chip_m:
            chip_m = f'<span class="seltopic">Select Topic {material("keyboard_arrow_down", 14)}</span>' 
        out.append(f'''<div class="mcard"><span class="cicon">{icon}{icb}</span><div class="mcc">
<div class="mct">{title}</div><div class="mcm">{meta}</div>{chip_m}</div></div>''')
    return "\n".join(out)

mob_dash_body = f'''<div class="mstatus"></div>
<div class="mscroll">
  <div class="mtopbar"><h1>Sessions</h1><span class="mcount">14</span><span class="msp"></span>
    <span class="mfilters">{i_mfilters}Filters</span><span class="mmore">{mi_morevert24}</span></div>
  <div class="msort"><span class="si">{i_sortud}</span><span>Most Recent</span><span class="sc">{i_chev}</span></div>
{mobile_cards()}
  <div class="myear">2025</div>
</div>
{mobile_nav("Sessions")}'''

dash_html = dash_html.replace("</body>",
    f'<style>{MOBILE_UI_CSS}</style>\n<div class="mob">\n{mob_dash_body}\n</div>\n</body>')
dash_html = dash_html.replace('<meta name="viewport" content="width=1440">',
                              '<meta name="viewport" content="width=device-width, initial-scale=1">')

mob_dash_html = mobile_page("Hedy — Sessions Dashboard (Light, Mobile 390)", mob_dash_body)
open(f"{TW}/{MOB_DASH}", "w", encoding="utf-8").write(mob_dash_html)
mob_dash_dark = darken(mob_dash_html).replace("-mobile-light-390.html", "-mobile-dark-390.html").replace("(Light, Mobile 390)", "(Dark, Mobile 390)")
open(f"{TW}/hedy-sessions-dashboard-mobile-dark-390.html", "w", encoding="utf-8").write(mob_dash_dark)

# ---------- index hub ----------
def index_page(entries):
    rows = "\n".join(
        f'<a class="ix" href="{fname}"><span class="ixn">{label}</span><span class="ixf">{fname}</span></a>'
        for label, fname in entries)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Hedy App Twins — Index</title>
<style>
{fontfaces}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;background:#FBFAF9;color:#26231A;padding:48px;max-width:760px}}
h1{{font-size:24px;font-weight:700;margin-bottom:4px}}
p{{font-size:13px;color:#6F6F6F;margin-bottom:28px}}
.ix{{display:flex;align-items:baseline;gap:12px;padding:10px 14px;margin-bottom:6px;border:1px solid #E8E4DE;border-radius:8px;background:#fff;text-decoration:none;color:inherit}}
.ixn{{font-size:14px;font-weight:600}}
.ixf{{font-size:11px;color:#8D8D8D;margin-left:auto}}
h2{{font-size:14px;font-weight:600;color:#6F6F6F;margin:20px 0 10px}}
</style></head><body>
<h1>Hedy App Twins</h1>
<p>Static 1:1 HTML twins of the Hedy macOS app, 1440&times;900. Each page is self-contained and Figma-capturable.</p>
{rows}
</body></html>'''

# ---------- write pages ----------
PAGES = [
    (DASH, "Hedy — Sessions Dashboard (Light, 1440)", None, None),
    (DETAIL, "Hedy — Session Detail (Light, 1440)", "Details", details_body),
    (DETAIL_NOTES, "Hedy — Session Notes (Light, 1440)", "Session Notes", notes_body),
    (DETAIL_HL, "Hedy — Session Highlights (Light, 1440)", "Highlights", hl_body),
    (DETAIL_TRANS, "Hedy — Session Transcript (Light, 1440)", "Transcript", trans_body),
    (DETAIL_SETTS, "Hedy — Session Settings Tab (Light, 1440)", "Settings", setts_body),
]

sizes = []
for fname, title, tab, body in PAGES:
    if tab is None:
        html = dash_html
    else:
        html = page(title, cards(selected_first=True) + "\n" + detail_shell(tab, body),
                    cls="page-session-detail")
    open(f"{TW}/{fname}", "w", encoding="utf-8").write(html)
    sizes.append(f"{fname}={len(html) // 1024}K")

extra_pages = [(TOPICS, topics_html), (TOPIC_DETAIL, topic_detail_html),
               (TD_SESSIONS, td_sessions_html), (TD_HIGHLIGHTS, td_highlights_html),
               (TD_SETTINGS, td_settings_html), (TOPICS_EMPTY, topics_empty_html),
               (SIGNIN, signin_html),
               (HIGHLIGHTS, highlights_html), (SETTINGS, settings_html),
               (SETTINGS_ACCOUNT, settings_account_html),
               (SETTINGS_SESSIONS, settings_sessions_html),
               (SETTINGS_PRIVACY, settings_privacy_html),
               (SETTINGS_HELP, settings_help_html),
               (SETTINGS_SPEECH, settings_speech_html),
               (SETTINGS_PERSONAL, settings_personal_html),
               (SETTINGS_AUTOMATION, settings_automation_html),
               (SEARCH, search_html),
               (SEARCH_EMPTY, search_empty_html), (SEARCH_NORES, search_nores_html),
               (MERGE, merge_html), (MERGE_CONFIG, merge_config_html),
               (SHARE_MGMT, share_mgmt_html),
               (CTX_INTRO, ctx_intro_html), (CTX_QUESTION, ctx_question_html),
               (CTX_STREAMING, ctx_streaming_html), (CTX_REVIEW, ctx_review_html),
               (PAYWALL, paywall_html),
               (RECORDING, recording_html), (PAUSED, paused_html)]
extra_pages += list(onb_pages.items())
for fname, html in extra_pages:
    open(f"{TW}/{fname}", "w", encoding="utf-8").write(html)
    sizes.append(f"{fname}={len(html) // 1024}K")

# dark set: transform every light page
light_files = [f for f, *_ in PAGES] + [f for f, _ in extra_pages]
for fname in light_files:
    html = open(f"{TW}/{fname}", encoding="utf-8").read()
    dark_fname = fname.replace("-light-1440.html", "-dark-1440.html")
    open(f"{TW}/{dark_fname}", "w", encoding="utf-8").write(darken(html))
sizes.append(f"dark set: {len(light_files)} pages")

INDEX_ENTRIES = [
    ("Sessions Dashboard (Light)", DASH),
    ("Session Detail — Details (Light)", DETAIL),
    ("Session Detail — Session Notes (Light)", DETAIL_NOTES),
    ("Session Detail — Highlights (Light)", DETAIL_HL),
    ("Session Detail — Transcript (Light)", DETAIL_TRANS),
    ("Session Detail — Settings (Light)", DETAIL_SETTS),
    ("Topics (Light)", TOPICS),
    ("Topics — Empty (Light)", TOPICS_EMPTY),
    ("Topic Detail (Light)", TOPIC_DETAIL),
    ("Topic Detail — Sessions (Light)", TD_SESSIONS),
    ("Topic Detail — Highlights (Light)", TD_HIGHLIGHTS),
    ("Topic Detail — Settings (Light)", TD_SETTINGS),
    ("Sign In (Light)", SIGNIN),
    ("Highlights (Light)", HIGHLIGHTS),
    ("Settings Dialog (Light)", SETTINGS),
    ("Settings — Account (Light)", SETTINGS_ACCOUNT),
    ("Settings — Sessions (Light)", SETTINGS_SESSIONS),
    ("Settings — Privacy (Light)", SETTINGS_PRIVACY),
    ("Settings — Help (Light)", SETTINGS_HELP),
    ("Settings — Speech & AI (Light)", SETTINGS_SPEECH),
    ("Settings — Personalization (Light)", SETTINGS_PERSONAL),
    ("Settings — Automation & Data (Light)", SETTINGS_AUTOMATION),
    ("Search Overlay (Light)", SEARCH),
    ("Search — Empty (Light)", SEARCH_EMPTY),
    ("Search — No Results (Light)", SEARCH_NORES),
    ("Merge Sessions (Light)", MERGE),
    ("Merge Configuration (Light)", MERGE_CONFIG),
    ("Share Management (Light)", SHARE_MGMT),
    ("Context Creation 1 — Intro (Light)", CTX_INTRO),
    ("Context Creation 2 — Question (Light)", CTX_QUESTION),
    ("Context Creation 3 — Generating (Light)", CTX_STREAMING),
    ("Context Creation 4 — Review (Light)", CTX_REVIEW),
    ("Subscription / Paywall (Light)", PAYWALL),
    ("Recording (Light)", RECORDING),
    ("Recording — Paused (Light)", PAUSED),
    ("Onboarding 1 — Welcome (Light)", ONB[1]),
    ("Onboarding 2 — Hedy Language (Light)", ONB[2]),
    ("Onboarding 3 — Name (Light)", ONB[3]),
    ("Onboarding 4 — Meeting Language (Light)", ONB[4]),
    ("Onboarding 5 — Use Case (Light)", ONB[5]),
    ("Onboarding 6 — Challenge (Light)", ONB[6]),
    ("Onboarding 7 — Sign Up (Light)", ONB[7]),
    ("Onboarding 8 — Cloud Sync (Light)", ONB[8]),
]
# ---------- app.html: single-page prototype (client-side nav + theme toggle) ----------
def _extract_body(html):
    m = re.search(r"<body([^>]*)>(.*)</body></html>", html, flags=re.S)
    attrs, inner = m.group(1), m.group(2)
    cm = re.search(r'class="([^"]*)"', attrs)
    return (cm.group(1) if cm else ""), inner.strip()

def _dark_css(css):
    out = _dark_re.sub(lambda m: DARK_MAP[m.group(0)], css)
    return out + "\n" + DARK_OVERRIDES.replace("<style>", "").replace("</style>", "")

app_templates = []
route_meta = {}
for fname in [f for f, *_ in PAGES] + [f for f, _ in extra_pages]:
    html = open(f"{TW}/{fname}", encoding="utf-8").read()
    cls, inner = _extract_body(html)
    slug = fname.replace("hedy-", "").replace("-light-1440.html", "")
    route_meta[fname] = {"slug": slug, "cls": cls}
    app_templates.append(f'<template id="t-{slug}" data-file="{fname}" data-cls="{cls}">\n{inner}\n</template>')

ROUTES_JSON = "{" + ",".join(
    f'"{meta["slug"]}":{{"file":"{f}","cls":"{meta["cls"]}"}}' for f, meta in route_meta.items()) + "}"

MENUS = {
    "sort-sessions": [{"t": "Most Recent", "sel": True}, {"t": "Oldest"}, {"t": "Grouped by date"}],
    "sort-topics": [{"t": "Last Activity", "sel": True}, {"t": "Name (A-Z)"},
                    {"t": "Most Active"}, {"t": "Recently Created"}, {"t": "Starred"}],
    "sort-highlights": [{"t": "Highlights", "sel": True}, {"t": "By Session"}, {"t": "By Topic"}],
    "import": [{"ic": material("audio_file_outlined", 20), "t": "Import Audio File"},
               {"ic": material("play_circle_outline", 20), "t": "Import Online Video"},
               {"ic": material("text_snippet_outlined", 20), "t": "Create Session from Transcript"}],
    "session-menu": [
        {"ic": material("link", 20), "t": "Copy link to session"},
        {"ic": material("person_add", 20), "t": "Invite to Session"},
        {"ic": material("outgoing_mail", 20), "t": "Send Recap Email"},
        {"ic": material("webhook", 20), "t": "Export to Webhook"},
        {"ic": material("ios_share", 20), "t": "Share"}],
    "topic-menu": [
        {"ic": material("edit", 20), "t": "Edit"},
        {"ic": material("person_add", 20), "t": "Invite to Topic"},
        {"ic": material("delete", 20), "t": "Delete", "red": True, "modal": "del-topic"}],
    "share-menu": [
        {"ic": material("content_copy", 20), "t": "Copy Link"},
        {"ic": material("block", 20), "t": "Revoke Access", "red": True, "modal": "revoke"}],
    "type": [{"t": "Business Meeting", "sel": True}, {"t": "Group Brainstorm"},
             {"t": "Job Interview"}, {"t": "Medical Consultation"}, {"t": "Negotiation"}],
    "topics": [
        {"t": "Acme Corp", "dot": "#FDE68A", "chip": "amber"},
        {"t": "Health", "dot": "#FECDD3", "chip": "rose"},
        {"t": "Roadmap", "dot": "#FED7AA", "chip": "peach"},
        {"t": "Hiring", "dot": "#A7F3D0", "chip": "mint"},
        {"t": "Learning", "dot": "#BFDBFE", "chip": "sky"}],
    "lang": [{"t": "English", "sel": True}, {"t": "Español"}, {"t": "Français"},
             {"t": "Deutsch"}, {"t": "Português"}],
    "stt": [{"t": "Local (Whisper)", "sel": True}, {"t": "Deepgram"}],
}
MODALS = {
    "del-session": {"title": "Delete Session",
                    "body": "Are you sure you want to delete this session?",
                    "actions": [{"t": "Cancel"}, {"t": "Delete", "red": True, "go": "sessions-dashboard"}]},
    "del-topic": {"title": "Delete Topic",
                  "body": "Are you sure you want to delete this topic?",
                  "actions": [{"t": "Cancel"}, {"t": "Delete", "red": True, "go": "topics"}]},
    "del-account": {"title": "Delete Account",
                    "body": "Are you sure you want to delete your account? This action cannot be undone.",
                    "actions": [{"t": "Cancel"}, {"t": "Delete", "red": True}]},
    "revoke": {"title": "Revoke Access",
               "body": "Are you sure you want to revoke access? The recipient will no longer be able to view this content.",
               "actions": [{"t": "Cancel"}, {"t": "Revoke Access", "red": True}]},
    "type-help": {"title": "Session Type",
                  "body": "Get the most relevant support for every conversation. Choose a session type and Hedy will provide insights and suggestions perfectly tailored to that scenario, helping you achieve your specific goals.",
                  "actions": [{"t": "OK", "primary": True}]},
    "forgot": {"title": "Forgot Password",
               "body": "Enter your email address and we&rsquo;ll send you a link to reset your password.",
               "field": "Email address",
               "actions": [{"t": "Send Password Reset Link", "primary": True}]},
    "new-topic": {"title": "New Topic", "body": "",
                  "field": "Topic Name", "field2": "Topic Description",
                  "actions": [{"t": "Cancel"}, {"t": "Create", "primary": True}]},
}
import json as _json
MENUS_JSON = _json.dumps(MENUS)
MODALS_JSON = _json.dumps(MODALS)

APP_JS = """
const ROUTES = __ROUTES__;
const MENUS = __MENUS__;
const MODALS = __MODALS__;
const FILE2SLUG = {}; for (const [s, r] of Object.entries(ROUTES)) FILE2SLUG[r.file] = s;
const LOGO = {light: '__LOGO_LIGHT__', dark: '__LOGO_DARK__'};
const root = document.getElementById('root');
let dark = false;
let pendingPatch = null;

function applyTheme() {
  document.getElementById('css-light').media = dark ? 'not all' : 'all';
  document.getElementById('css-dark').media = dark ? 'all' : 'not all';
  const logo = root.querySelector('.logo img');
  if (logo) logo.src = dark ? LOGO.dark : LOGO.light;
  const sw = root.querySelector('.togrow .switch');
  if (sw) sw.classList.toggle('off', !dark);
}

function go(slug, push = true) {
  const t = document.getElementById('t-' + slug);
  if (!t) return;
  closeMenu(); closeModal();
  root.innerHTML = t.innerHTML;
  document.body.className = 'app ' + (ROUTES[slug].cls || '');
  if (push) history.pushState(null, '', '#/' + slug);
  if (pendingPatch) {
    const p = pendingPatch; pendingPatch = null;
    for (const [sel, txt] of p) root.querySelectorAll(sel).forEach(n => { n.textContent = txt; });
  }
  applyTheme();
}

/* ---- dropdown menus ---- */
let openMenu = null;
function closeMenu() { if (openMenu) { openMenu.remove(); openMenu = null; } }
function showMenu(trigger, key, onPick) {
  closeMenu();
  const m = document.createElement('div');
  m.className = 'popmenu';
  const search = key === 'topics' ? '<input class="pms" placeholder="Search topics...">' : '';
  m.innerHTML = search + MENUS[key].map((it, i) =>
    `<div class="pmi${it.red ? ' red' : ''}${it.sel ? ' on' : ''}" data-i="${i}">` +
    (it.dot ? `<span class="pdot" style="background:${it.dot}"></span>` : '') +
    (it.ic || '') + `<span>${it.t}</span></div>`).join('');
  document.body.appendChild(m);
  const inp = m.querySelector('.pms');
  if (inp) {
    inp.addEventListener('input', () => {
      const q = inp.value.toLowerCase();
      m.querySelectorAll('.pmi').forEach(n => { n.style.display = n.textContent.toLowerCase().includes(q) ? '' : 'none'; });
    });
    setTimeout(() => inp.focus(), 0);
  }
  const r = trigger.getBoundingClientRect();
  m.style.left = Math.min(r.left, innerWidth - m.offsetWidth - 12) + 'px';
  m.style.top = Math.min(r.bottom + 4, innerHeight - m.offsetHeight - 12) + 'px';
  m.addEventListener('click', (e) => {
    const item = e.target.closest('.pmi');
    if (!item) return;
    const it = MENUS[key][+item.dataset.i];
    closeMenu();
    if (it.modal) showModal(it.modal);
    else if (onPick) onPick(it.t);
    e.stopPropagation();
  });
  openMenu = m;
}

/* ---- modals ---- */
let openDlg = null;
function closeModal() { if (openDlg) { openDlg.remove(); openDlg = null; } }
function showModal(key) {
  closeModal(); closeMenu();
  const d = MODALS[key];
  const dlg = document.createElement('div');
  dlg.className = 'modalovl';
  dlg.innerHTML = `<div class="modal"><h3>${d.title}</h3>` +
    (d.body ? `<p>${d.body}</p>` : '') +
    (d.field ? `<div class="mfield">${d.field}</div>` : '') +
    (d.field2 ? `<div class="mfield" style="min-height:64px">${d.field2}</div>` : '') +
    `<div class="mact">` + d.actions.map((a, i) =>
      `<span class="ma${a.red ? ' red' : ''}${a.primary ? ' primary' : ''}" data-i="${i}">${a.t}</span>`).join('') +
    `</div></div>`;
  document.body.appendChild(dlg);
  dlg.addEventListener('click', (e) => {
    const btn = e.target.closest('.ma');
    if (btn) {
      const a = d.actions[+btn.dataset.i];
      closeModal();
      if (a.go) go(a.go);
      return;
    }
    if (e.target === dlg) closeModal();
  });
  openDlg = dlg;
}

document.addEventListener('click', (e) => {
  if (openMenu && !e.target.closest('.popmenu')) closeMenu();

  /* theme + session flow */
  const sw = e.target.closest('.togrow .switch');
  if (sw) { dark = !dark; applyTheme(); return; }
  const tgl = e.target.closest('.setrow .switch');
  if (tgl) { tgl.classList.toggle('off'); return; }
  const start = e.target.closest('.start');
  if (start) { go('recording'); return; }
  const stop = e.target.closest('.recbtn');
  if (stop) { go('sessions-dashboard'); return; }
  const resume = e.target.closest('.pausepill');
  if (resume) { go('recording'); return; }
  const mute = e.target.closest('.recsq:last-child');
  if (mute && root.querySelector('.recctl')) {
    mute.classList.toggle('muted'); return;
  }
  const close = e.target.closest('.sdhead .x');
  if (close) { go('sessions-dashboard'); return; }

  /* dropdown triggers */
  const sort = e.target.closest('.sort');
  if (sort) {
    const key = document.body.className.includes('page-topics') ? 'sort-topics'
      : document.body.className.includes('page-highlights') ? 'sort-highlights' : 'sort-sessions';
    showMenu(sort, key, (t) => { sort.querySelector('span:nth-child(2)').textContent = t; });
    return;
  }
  const imp = e.target.closest('.tbtn');
  if (imp && imp.textContent.includes('Import')) { showMenu(imp, 'import'); return; }
  const mbtn = e.target.closest('.mbtn, .picon');
  if (mbtn) { e.preventDefault(); showMenu(mbtn, 'session-menu'); return; }
  const tmenu = e.target.closest('.tmenu');
  if (tmenu) { e.preventDefault(); showMenu(tmenu, 'topic-menu'); return; }
  const tpin = e.target.closest('.tpin');
  if (tpin) { e.preventDefault(); tpin.classList.toggle('starred'); return; }
  const smtr = e.target.closest('.smcard .tr');
  if (smtr) { showMenu(smtr, 'share-menu'); return; }
  const drop = e.target.closest('.sdrop, .mdrop, .sdinput, .sfield');
  if (drop && drop.querySelector('svg')) {
    const txt = drop.textContent.trim();
    const key = txt.includes('English') || txt.includes('Español') ? 'lang'
      : txt.includes('Whisper') || txt.includes('Deepgram') ? 'stt' : 'type';
    if (key === 'type' && !(txt.includes('Meeting') || txt.includes('Brainstorm') || txt.includes('Interview') || txt.includes('Consultation') || txt.includes('Negotiation') || txt.includes('Acme') || txt.includes('Corp'))) return;
    showMenu(drop, key, (t) => { drop.childNodes[0].textContent = t + ' '; });
    return;
  }

  /* topic assignment dropdown: Select Topic + assigned chips */
  const tchip = e.target.closest('.seltopic, .cc .chip, .mcc .mchip');
  if (tchip && !e.target.closest('.pms')) {
    e.preventDefault();
    showMenu(tchip, 'topics', (t) => {
      const it = MENUS.topics.find(x => x.t === t);
      const mobile = tchip.classList.contains('mchip');
      const span = document.createElement('span');
      span.className = (mobile ? 'mchip ' : 'chip ') + it.chip;
      span.textContent = t;
      tchip.replaceWith(span);
    });
    return;
  }
  /* modal triggers */
  const del = e.target.closest('.delbtn');
  if (del) {
    const t = del.textContent;
    showModal(t.includes('Account') ? 'del-account' : t.includes('Topic') ? 'del-topic' : 'del-session');
    return;
  }
  const hlp = e.target.closest('.hlp');
  if (hlp) { showModal('type-help'); return; }
  const forgot = e.target.closest('.silink');
  if (forgot) { showModal('forgot'); return; }
  const newtopic = e.target.closest('.tbtn, .ebtn');
  if (newtopic && (newtopic.textContent.includes('New Topic') || newtopic.textContent.includes('Add Topic'))) {
    e.preventDefault(); showModal('new-topic'); return;
  }

  /* segmented pills (non-link tabs) */
  const pill = e.target.closest('.tabs span.tab');
  if (pill) {
    pill.parentElement.querySelectorAll('.tab').forEach(t => t.classList.remove('sel'));
    pill.classList.add('sel');
    return;
  }
  /* todo checkboxes */
  const todo = e.target.closest('.todo');
  if (todo) {
    const cb = todo.querySelector('.cb');
    todo.classList.toggle('done');
    cb.classList.toggle('on');
    cb.innerHTML = cb.classList.contains('on') ? document.querySelector('#cksvg').innerHTML : '';
    return;
  }
  /* vocabulary chips: x removes */
  const chipx = e.target.closest('.qchip svg');
  if (chipx && document.body.className.includes('page-settings')) {
    chipx.closest('.qchip').remove(); return;
  }
  /* highlight list selection */
  const hli = e.target.closest('.hlitem[data-t]');
  if (hli) {
    const wrap = hli.closest('.hllist, .hlcards');
    if (wrap) {
      wrap.querySelectorAll('.hlitem').forEach(n => n.classList.remove('sel'));
      hli.classList.add('sel');
      const pane = wrap.parentElement.querySelector('.hldetail') || root.querySelector('.hldetail');
      if (pane) {
        pane.querySelector('.hldt').textContent = hli.dataset.t;
        const tm = pane.querySelector('.hltime.sm');
        if (tm) tm.lastChild.textContent = hli.dataset.time.replace('m', ':00');
      }
    }
    return;
  }

  /* links + per-card data patching */
  const a = e.target.closest('a[href]');
  if (a) {
    const slug = FILE2SLUG[a.getAttribute('href')];
    if (slug) {
      e.preventDefault();
      if (a.dataset.t && a.classList.contains('card'))
        pendingPatch = [['.dtitle', a.dataset.t], ['.sdbtitle', a.dataset.t]];
      if (a.dataset.t && a.classList.contains('ttile'))
        pendingPatch = [['.tdbtitle', a.dataset.t], ['.tdbdesc', a.dataset.d || ''], ['.tdbmeta', a.dataset.m || '']];
      go(slug);
    }
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (openDlg) { closeModal(); return; }
    if (openMenu) { closeMenu(); return; }
    if (root.querySelector('.ovl')) go('sessions-dashboard');
  }
});

window.addEventListener('popstate', () => {
  const slug = location.hash.replace('#/', '') || 'sessions-dashboard';
  if (ROUTES[slug]) go(slug, false);
});

go(location.hash.replace('#/', '') || 'sessions-dashboard', false);
"""

# ---------- modal chunk pages (each modal = its own Figma artboard) ----------
CHUNK_CSS_EXTRA = """
body.chunk{width:auto;height:auto;min-width:0;min-height:0;overflow:visible;display:block;padding:40px;background:var(--bg)}
.chunk .modal{width:400px;background:var(--card);border-radius:12px;padding:24px;box-shadow:0 8px 32px rgba(0,0,0,.25)}
.chunk .modal h3{font-size:18px;font-weight:600;color:var(--ink);margin-bottom:12px}
.chunk .modal p{font-size:14px;color:var(--n40);line-height:1.5;margin-bottom:8px}
.chunk .mfield{margin-top:12px;padding:12px 16px;border-radius:8px;background:rgba(128,128,128,.1);font-size:14px;color:var(--n40)}
.chunk .mact{display:flex;justify-content:flex-end;gap:8px;margin-top:20px}
.chunk .ma{padding:10px 16px;border-radius:8px;font-size:14px;font-weight:500;color:var(--orange)}
.chunk .ma.red{background:#D32F2F;color:#fff}
.chunk .ma.primary{background:var(--orange);color:#fff}
.chunk .mdlg{box-shadow:0 8px 32px rgba(0,0,0,.25)}
"""

def modal_chunk_html(title, inner):
    return f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{CAPTURE}
<style>
{fontfaces}
{CSS}
{CHUNK_CSS_EXTRA}
</style>
</head><body class="chunk">
{inner}
</body></html>'''

CHUNK_FILES = []
for slug, d in MODALS.items():
    body = f'<div class="modal"><h3>{d["title"]}</h3>'
    if d.get("body"): body += f'<p>{d["body"]}</p>'
    if d.get("field"): body += f'<div class="mfield">{d["field"]}</div>'
    if d.get("field2"): body += f'<div class="mfield" style="min-height:64px">{d["field2"]}</div>'
    body += '<div class="mact">' + "".join(
        f'<span class="ma{" red" if a.get("red") else ""}{" primary" if a.get("primary") else ""}">{a["t"]}</span>'
        for a in d["actions"]) + '</div></div>'
    fname = f"hedy-modal-{slug}-light.html"
    html = modal_chunk_html(f'Hedy — Modal · {d["title"]} (Light)', body)
    open(f"{TW}/{fname}", "w", encoding="utf-8").write(html)
    dk = darken(html).replace("(Light)", "(Dark)")
    open(f"{TW}/hedy-modal-{slug}-dark.html", "w", encoding="utf-8").write(dk)
    CHUNK_FILES.append((d["title"], fname))

# merge dialogs as chunks (strip the page overlay wrapper)
for slug, title, dlg in [("merge-sessions", "Merge Sessions", merge_dialog),
                         ("merge-config", "Merge Configuration", merge_config_dialog)]:
    inner = dlg.replace('<div class="ovl">', '').rsplit('</div>', 1)[0]
    fname = f"hedy-modal-{slug}-light.html"
    html = modal_chunk_html(f'Hedy — Modal · {title} (Light)', inner)
    open(f"{TW}/{fname}", "w", encoding="utf-8").write(html)
    dk = darken(html).replace("(Light)", "(Dark)")
    open(f"{TW}/hedy-modal-{slug}-dark.html", "w", encoding="utf-8").write(dk)
    CHUNK_FILES.append((title, fname))

app_html = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hedy — App Prototype</title>
<style>
{fontfaces}
</style>
<style id="css-light">
{CSS}
</style>
<style id="css-dark" media="not all">
{_dark_css(CSS)}
</style>
<style>
body{{width:100vw !important;height:100vh !important;min-width:390px;min-height:600px}}
#root{{display:contents}}
.start,.recbtn,.pausepill,.togrow .switch,.sdhead .x,.recsq{{cursor:pointer}}
a{{cursor:pointer}}
/* Prototype: panes scroll like the real app (static capture pages stay clipped) */
.cards,.dbody,.dbody.setts,.tbox,.neditor,.chatlog,.hllist,.hldetail,.tdcontent,.hlcards,.sdcontent,.sres{{overflow-y:auto}}
.dbody.trans,.dbody.notes,.dbody.hl{{overflow:hidden}}
/* Prototype: dropdown menus + modal dialogs (popup styling per app menus) */
.popmenu{{position:fixed;z-index:60;min-width:200px;background:var(--card);border:1px solid var(--border);border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.15);padding:4px;overflow:hidden}}
.pmi{{display:flex;align-items:center;gap:10px;padding:0 14px;height:44px;border-radius:6px;font-size:14px;color:var(--ink);cursor:pointer;white-space:nowrap}}
.pmi:hover{{background:#FFF0E5}}
.pmi.on{{color:var(--orange);font-weight:600}}
.pmi.red,.pmi.red svg{{color:#D32F2F}}
.pmi svg{{color:var(--icon);flex-shrink:0}}
.pms{{display:block;margin:4px;padding:8px 10px;border-radius:6px;border:1px solid var(--border);background:var(--bg);font-size:13px;color:var(--n40);font-family:'Inter',sans-serif;width:calc(100% - 8px);outline:none}}
.pdot{{width:14px;height:14px;border-radius:4px;flex-shrink:0}}
.modalovl{{position:fixed;inset:0;z-index:70;background:rgba(0,0,0,.54);display:flex;align-items:center;justify-content:center}}
.modal{{width:400px;background:var(--card);border-radius:12px;padding:24px;box-shadow:0 8px 32px rgba(0,0,0,.25)}}
.modal h3{{font-size:18px;font-weight:600;color:var(--ink);margin-bottom:12px}}
.modal p{{font-size:14px;color:var(--n40);line-height:1.5;margin-bottom:8px}}
.mfield{{margin-top:12px;padding:12px 16px;border-radius:8px;background:rgba(128,128,128,.1);font-size:14px;color:var(--n40)}}
.mact{{display:flex;justify-content:flex-end;gap:8px;margin-top:20px}}
.ma{{padding:10px 16px;border-radius:8px;font-size:14px;font-weight:500;color:var(--orange);cursor:pointer}}
.ma.red{{background:#D32F2F;color:#fff}}
.ma.primary{{background:var(--orange);color:#fff}}
.recsq.muted{{background:#D32F2F !important}}
.sort,.tbtn,.mbtn,.picon,.tmenu,.smcard .tr,.sdrop,.mdrop,.sdinput,.sfield,.delbtn,.hlp,.silink,.ebtn,.tabs span.tab,.todo,.hlitem{{cursor:pointer}}
</style>
</head><body class="app">
<div id="root"></div>
<div id="cksvg" style="display:none">{ICON_CHECK}</div>
{chr(10).join(app_templates)}
<script>
{APP_JS.replace("__ROUTES__", ROUTES_JSON).replace("__MENUS__", MENUS_JSON).replace("__MODALS__", MODALS_JSON).replace("__LOGO_LIGHT__", logo_png).replace("__LOGO_DARK__", logo_png_dark)}
</script>
</body></html>'''
open(f"{TW}/app.html", "w", encoding="utf-8").write(app_html)
sizes.append(f"app.html={len(app_html) // 1024}K ({len(app_templates)} screens)")

INDEX_ENTRIES.append(("Sessions Dashboard (Light, Mobile 390)", MOB_DASH))
INDEX_ENTRIES.append(("Sessions Dashboard (Dark, Mobile 390)", "hedy-sessions-dashboard-mobile-dark-390.html"))
dark_entries = [(label.replace("(Light)", "(Dark)"),
                 fname.replace("-light-1440.html", "-dark-1440.html"))
                for label, fname in INDEX_ENTRIES]
open(f"{TW}/index.html", "w", encoding="utf-8").write(
    index_page([("▶ Interactive App Prototype (responsive, light/dark)", "app.html")]
               + INDEX_ENTRIES + dark_entries))
print("\n".join(sizes))
