NAVY = "#16263F"; PAPER = "#F6F3EC"; PAPER2 = "#EAE5D8"; RUST = "#A3471F"; TEAL = "#1F6466"; AMBER = "#E9B872"
INK = "#3D4A5C"; MUTED = "#5E6B7A"; LINE = "#D8D1BF"
CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1920px;height:1080px;overflow:hidden}}
body{{font-family:Inter,sans-serif;background:{PAPER};color:{NAVY};-webkit-font-smoothing:antialiased}}
body.dark{{background:{NAVY};color:{PAPER}}}
.wrap{{position:absolute;inset:0;padding:96px 128px 120px;display:flex;flex-direction:column}}
.kicker{{font-size:26px;font-weight:700;letter-spacing:.14em;color:{RUST};margin-bottom:18px}}
.dark .kicker{{color:{AMBER}}}
h1{{font-family:Lora,serif;font-size:92px;line-height:1.08;font-weight:600;max-width:1560px}}
h2{{font-family:Lora,serif;font-size:66px;line-height:1.1;font-weight:600}}
.lead{{font-size:38px;line-height:1.4;color:{INK};margin-top:30px;max-width:1500px}}
.dark .lead{{color:#C9D3E0}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;padding-top:24px}}
.quote{{font-family:Lora,serif;font-size:70px;line-height:1.2;max-width:1560px}}
.cite{{font-size:30px;line-height:1.4;color:{MUTED};max-width:1450px}}
.dark .cite{{color:#9FB0C6}}
.grid{{display:grid;gap:32px}}
.card{{background:{PAPER2};border-radius:20px;padding:40px 36px;display:flex;flex-direction:column;gap:14px}}
.dark .card{{background:#22375A}}
.num{{font-family:Lora,serif;font-size:64px;font-weight:600;line-height:1;color:{RUST}}}
.card h3{{font-size:42px;font-weight:700;line-height:1.15}}
.card p{{font-size:32px;line-height:1.35;color:{INK}}}
.dark .card p{{color:#C9D3E0}}
.strong{{font-size:38px;line-height:1.35;font-weight:600}}
.row{{font-size:36px;line-height:1.3;color:{INK};padding:22px 0;border-top:2px solid {LINE};display:flex;gap:28px;align-items:baseline}}
.row b{{color:{NAVY};min-width:430px;font-weight:700}}
.pill{{display:inline-block;font-size:24px;font-weight:700;letter-spacing:.06em;color:#fff;padding:8px 16px;border-radius:8px}}
.round{{background:{PAPER2};border-radius:20px;padding:32px 36px;display:flex;flex-direction:column;gap:20px}}
.round span{{font-size:26px;font-weight:700;letter-spacing:.14em;color:{MUTED}}}
.chips{{display:flex;gap:18px}}
.chip{{font-size:52px;font-weight:700;color:#fff;padding:22px 34px;border-radius:14px;line-height:1}}
.arrow{{font-size:56px;color:{RUST};align-self:center;font-weight:700}}
.stat{{border-top:8px solid {RUST};padding-top:24px}}
.stat .n{{font-family:Lora,serif;font-size:150px;font-weight:600;line-height:1}}
.stat p{{font-size:34px;line-height:1.35;color:{INK};margin-top:10px}}
.foot{{position:absolute;left:128px;right:128px;bottom:48px;font-size:22px;color:{MUTED};display:flex;justify-content:space-between}}
.dark .foot{{color:#9FB0C6}}
"""

# additions for this video
CSS += f"""
.arch{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px 24px}}
.wrap.tight{{padding:72px 128px 104px}}
.wrap.tight .main{{justify-content:flex-start;padding-top:28px}}
.box{{border:3px solid {LINE};border-radius:16px;padding:14px 24px;background:{PAPER};display:flex;flex-direction:column;gap:6px;transition:none}}
.box h4{{font-size:30px;font-weight:700;line-height:1.15}}
.box p{{font-size:24px;line-height:1.3;color:{INK}}}
.box.on{{border-color:{TEAL};background:#DCEBEA}}
.box.ai.on{{border-color:{TEAL};background:#DCEBEA}}
.box.dim{{opacity:.38}}
.span3{{grid-column:1 / span 3}}
.span2{{grid-column:1 / span 2}}
.c3{{grid-column:3}}
.down{{text-align:center;color:{MUTED};font-size:30px;line-height:1;margin:-12px 0}}
.clock{{display:flex;align-items:center;gap:34px;padding:26px 0;border-top:2px solid {LINE}}}
.clock .n{{font-family:Lora,serif;font-size:96px;font-weight:600;min-width:250px;line-height:1}}
.clock .u{{font-size:32px;color:{INK};min-width:330px}}
.clock .s{{font-size:30px;color:{MUTED}}}
.clock.win .n{{color:{RUST}}}
.tick{{font-size:31px;line-height:1.3;color:{INK};padding:20px 0;border-top:2px solid {LINE};display:flex;gap:26px;align-items:baseline}}
.tick b{{color:{NAVY};min-width:640px;font-weight:700}}
.tick .st{{margin-left:auto;font-size:26px;font-weight:700;letter-spacing:.06em;color:{RUST};white-space:nowrap}}
"""
CSS += ".wide b{min-width:540px !important}"
