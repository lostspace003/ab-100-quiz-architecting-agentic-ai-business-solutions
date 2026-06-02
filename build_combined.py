"""Build a single combined index.html from M01-quiz.html..M11-quiz.html.

Left-sidebar nav (Overview + 11 modules). Per-module quiz progress in localStorage.
Original per-module files stay untouched.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent

MODULE_TITLES_FALLBACK = {
    1: "Introduction to Agentic AI Business Solution Architecture",
    2: "Analyze requirements for AI-powered business solutions",
    3: "Design overall AI strategy for business solutions",
    4: "Evaluate the costs and benefits of an AI-powered business solution",
    5: "Design AI and agents for business solutions",
    6: "Design extensibility of AI solutions",
    7: "Orchestrate configuration for prebuilt agents and apps",
    8: "Analyze, monitor, and tune AI-powered business solutions",
    9: "Manage the testing of AI-powered business solutions",
    10: "Design the ALM process for AI-powered business solutions",
    11: "Design responsible AI, security, governance, risk management, and compliance",
}

MODULE_SUMMARIES = {
    1: "The architect is the bridge between business strategy and AI delivery.",
    2: "Requirements + data quality determine whether the AI project can ever work.",
    3: "The biggest module — set the strategy that the rest of the course decorates with detail.",
    4: "If you can&#x27;t defend the business case, the project never ships.",
    5: "Heaviest design module. Designing the agents themselves — Copilot, Foundry agents, agent flows.",
    6: "Stretch the platform — when out-of-the-box isn&#x27;t enough.",
    7: "Configure what already exists in Dynamics 365, M365 Copilot, and Power Platform before you build anything custom.",
    8: "Operate and improve. The metrics that prove the agents work.",
    9: "AI testing is different — non-deterministic outputs require new strategies.",
    10: "Agents and prompts are production assets — they need ALM like any other workload.",
    11: "The hardest topic and the most important. Where the architect anchors ethics.",
}


def extract_one(n: int) -> dict:
    src = (HERE / f"M{n:02d}-quiz.html").read_text(encoding="utf-8")

    m = re.search(r"<title>AB-100\s*[—–-]\s*Module\s*\d+\s*[—–-]\s*(.+?)</title>", src)
    title = m.group(1).strip() if m else MODULE_TITLES_FALLBACK[n]

    m = re.search(r'<p class="frame">(.*?)</p>', src, re.S)
    frame = m.group(1).strip() if m else ""

    m = re.search(r'<ul class="recap-list">(.*?)</ul>', src, re.S)
    recap_inner = m.group(1).strip() if m else ""

    m = re.search(r'<div class="concepts">(.*?)</div>\s*</section>', src, re.S)
    concepts_inner = m.group(1).strip() if m else ""

    m = re.search(r'<div class="cheat">(.*?)</div>\s*</section>', src, re.S)
    cheat_inner = m.group(1).strip() if m else ""

    # Question blocks
    q_blocks = []
    for qm in re.finditer(
        r'<div class="q" id="q-(\d+)" data-locked="0">.*?<div class="explain"[^>]*></div>\s*</div>',
        src,
        re.S,
    ):
        block = qm.group(0)
        block = re.sub(r'id="q-(\d+)"', rf'id="m{n}-q-\1"', block)
        block = re.sub(
            r'onclick="pickOption\((\d+),\s*(\d+)\)"',
            rf'onclick="pickOption({n}, \1, \2)"',
            block,
        )
        q_blocks.append(block)
    questions_html = "\n\n".join(q_blocks)

    # Refs — grab the anchors inside the refs card (after the <h2>...</h2>)
    rm = re.search(
        r'<section class="card refs">.*?<h2>.*?</h2>(.*?)</section>', src, re.S
    )
    refs_inner = rm.group(1).strip() if rm else ""

    qm = re.search(r"const QUIZ_DATA\s*=\s*(\{.*?\});\s*\n", src, re.S)
    quiz_data = json.loads(qm.group(1)) if qm else {"questions": []}

    return {
        "n": n,
        "title": title,
        "frame": frame,
        "recap_inner": recap_inner,
        "concepts_inner": concepts_inner,
        "cheat_inner": cheat_inner,
        "questions_html": questions_html,
        "refs_inner": refs_inner,
        "quiz_data": quiz_data,
        "num_q": len(quiz_data.get("questions", [])),
    }


def short_summary(n: int) -> str:
    return MODULE_SUMMARIES.get(n, "")


def stat_counts(mod: dict) -> str:
    """Best-effort stat row counts from extracted HTML."""
    recap_count = mod["recap_inner"].count("<li")
    concepts_count = mod["concepts_inner"].count('class="concept"')
    return (
        f'<span class="stat">📋 {recap_count} recap points</span>'
        f'<span class="stat">📚 {concepts_count} key concepts</span>'
        f'<span class="stat">❓ {mod["num_q"]} questions</span>'
    )


def build():
    modules = [extract_one(n) for n in range(1, 12)]

    # ---------- shared CSS ----------
    css = r"""
:root {
  --ink: #0b1530;
  --ink-soft: #2a3450;
  --muted: #5b6478;
  --line: #e6ebf4;
  --bg: #f5f7fb;
  --bg-card: #ffffff;
  --brand: #1f3a68;
  --brand-soft: #2c4f8c;
  --accent: #0078d4;
  --good: #1f7e3a;
  --good-soft: #e7f5ec;
  --bad: #b03030;
  --bad-soft: #fbeaea;
  --warn: #b06000;
  --warn-soft: #fff5e0;
  --shadow: 0 6px 24px rgba(15, 29, 58, 0.08);
  --shadow-strong: 0 12px 36px rgba(15, 29, 58, 0.14);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  margin: 0; padding: 0; background: var(--bg); color: var(--ink); line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

/* ------- Layout: sidebar + main ------- */
.layout {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 0;
  min-height: 100vh;
  max-width: 1400px;
  margin: 0 auto;
}
.sidebar {
  position: sticky; top: 0; align-self: start;
  height: 100vh; overflow-y: auto;
  background: white; border-right: 1px solid var(--line);
  padding: 22px 16px 28px;
}
.sidebar-brand {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 12px; background: var(--brand); color: white;
  font-size: 11px; font-weight: 700; letter-spacing: .6px; border-radius: 999px; text-transform: uppercase;
  margin-bottom: 18px;
}
.sidebar-brand::before { content: ""; width: 8px; height: 8px; border-radius: 999px; background: #6ec1ff; }
.nav-section-label {
  font-size: 11px; font-weight: 700; letter-spacing: .8px; color: var(--muted);
  text-transform: uppercase; margin: 14px 8px 6px;
}
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 10px; cursor: pointer;
  font-size: 14px; color: var(--ink-soft); font-weight: 500;
  background: transparent; border: none; width: 100%; text-align: left;
  transition: background .12s ease, color .12s ease;
}
.nav-item:hover { background: #eef3fb; color: var(--brand); }
.nav-item.active { background: var(--brand); color: white; font-weight: 600; box-shadow: var(--shadow); }
.nav-item.active .nav-num { background: rgba(255,255,255,0.22); color: white; }
.nav-num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 26px; height: 26px; background: #eef3fb; color: var(--brand);
  border-radius: 7px; font-size: 12px; font-weight: 800; flex-shrink: 0;
}
.nav-label { flex: 1; line-height: 1.35; }
.nav-check {
  width: 16px; height: 16px; border-radius: 50%; flex-shrink: 0;
  background: var(--line);
  display: inline-flex; align-items: center; justify-content: center;
  color: white; font-size: 10px; font-weight: 800;
}
.nav-item.done .nav-check { background: var(--good); }
.nav-item.done .nav-check::after { content: "✓"; }
.nav-item.active .nav-check { background: rgba(255,255,255,0.5); }
.nav-item.active.done .nav-check { background: white; color: var(--good); }

.sidebar-foot { margin-top: 18px; font-size: 11.5px; color: var(--muted); padding: 0 8px; line-height: 1.5; }

.main { padding: 28px 32px 80px; min-width: 0; }

/* ------- Hero ------- */
.hero {
  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-soft) 60%, #3b6cae 100%);
  color: white; border-radius: 20px; padding: 32px 32px; box-shadow: var(--shadow-strong);
  margin-bottom: 24px; position: relative; overflow: hidden;
}
.hero::after {
  content: ""; position: absolute; right: -80px; top: -80px; width: 280px; height: 280px;
  border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,0.18), transparent 60%);
}
.hero-mod {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.18); padding: 5px 12px; border-radius: 999px;
  font-size: 12px; font-weight: 700; letter-spacing: .5px; text-transform: uppercase;
  backdrop-filter: blur(4px);
}
.hero h1 { margin: 12px 0 6px; font-size: 28px; line-height: 1.2; font-weight: 700; }
.hero .frame { font-size: 15px; opacity: 0.92; max-width: 680px; margin: 0; }

/* ------- Scorebar ------- */
.scorebar {
  position: sticky; top: 12px; z-index: 20;
  background: white; border-radius: 14px; box-shadow: var(--shadow);
  padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;
  font-size: 14px; margin-bottom: 22px; gap: 12px; flex-wrap: wrap;
}
.scorebar .progress { color: var(--muted); }
.scorebar .progress strong { color: var(--ink); }
.scorebar .score { font-weight: 700; color: var(--brand); }
.scorebar .pct { font-weight: 700; color: var(--accent); }

/* ------- Cards ------- */
section.card {
  background: var(--bg-card); border-radius: 18px; box-shadow: var(--shadow);
  padding: 26px 28px; margin-bottom: 22px;
}
section.card h2 {
  font-size: 19px; color: var(--brand); margin: 0 0 16px;
  display: flex; align-items: center; gap: 10px;
}
section.card h2 .icon {
  width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #e3ecf9, #d0deef);
  display: inline-flex; align-items: center; justify-content: center; color: var(--brand);
  font-size: 15px; font-weight: 800;
}

/* Recap */
.recap-list { padding-left: 20px; margin: 0; }
.recap-list li { margin: 8px 0; }
.recap-list li::marker { color: var(--accent); font-weight: 700; }

/* Key concepts grid */
.concepts {
  display: grid; gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}
.concept {
  border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px;
  background: linear-gradient(180deg, #fbfcff 0%, #f3f6fc 100%);
  transition: transform .12s ease, box-shadow .12s ease;
}
.concept:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.concept .term { font-weight: 700; color: var(--brand); margin-bottom: 4px; font-size: 14px; }
.concept .def  { color: var(--ink-soft); font-size: 13.5px; }

/* Cheat sheet */
.cheat { display: grid; gap: 10px; }
.cheat-row {
  display: grid; grid-template-columns: 1fr; gap: 8px; align-items: start;
  background: linear-gradient(180deg, #fffaf0 0%, #fff5e0 100%);
  border-left: 4px solid #c8a040; border-radius: 12px; padding: 12px 14px;
  font-size: 14px; color: var(--ink-soft);
}
.cheat-row strong { color: var(--ink); }

/* Quiz */
.q-meta { color: var(--muted); font-size: 13.5px; margin: 0 0 16px; }
.q { padding: 4px 0 6px; }
.q + .q { border-top: 1px dashed var(--line); margin-top: 18px; padding-top: 16px; }
.q-stem { font-weight: 600; color: var(--ink); margin: 0 0 12px; line-height: 1.5; }
.q-num {
  display: inline-block; background: #eef3fb; color: var(--brand); padding: 3px 10px;
  border-radius: 999px; font-size: 12px; font-weight: 700; margin-right: 8px; vertical-align: 2px;
}
.options { display: flex; flex-direction: column; gap: 8px; }
.option {
  display: flex; align-items: flex-start; gap: 10px;
  border: 1.5px solid var(--line); border-radius: 12px; padding: 12px 14px;
  cursor: pointer; background: #fafbff; transition: all .15s ease;
  font-size: 14.5px; line-height: 1.5;
}
.option:hover:not(.locked) {
  border-color: var(--brand); background: #f1f5fc; transform: translateY(-1px);
}
.option .letter {
  display: inline-flex; align-items: center; justify-content: center;
  width: 24px; height: 24px; border-radius: 6px; background: white; border: 1px solid var(--line);
  font-weight: 700; font-size: 12px; color: var(--brand); flex-shrink: 0;
}
.option.locked { cursor: default; }
.option.correct { border-color: var(--good); background: var(--good-soft); color: #0c4a1c; }
.option.correct .letter { background: var(--good); color: white; border-color: var(--good); }
.option.wrong { border-color: var(--bad); background: var(--bad-soft); color: #6c1414; }
.option.wrong .letter { background: var(--bad); color: white; border-color: var(--bad); }
.option.disabled { opacity: 0.55; }

.explain {
  margin-top: 12px; padding: 14px 16px; border-radius: 12px;
  background: #f3f6fc; font-size: 14px;
  border-left: 4px solid var(--brand);
}
.explain.right { background: var(--good-soft); border-left-color: var(--good); }
.explain.wrong { background: var(--bad-soft); border-left-color: var(--bad); }
.explain .verdict {
  font-weight: 800; margin-right: 6px; text-transform: uppercase;
  font-size: 12px; letter-spacing: .5px;
}
.explain.right .verdict { color: var(--good); }
.explain.wrong .verdict { color: var(--bad); }
.explain details { margin-top: 10px; }
.explain summary {
  cursor: pointer; font-size: 13px; color: var(--brand); font-weight: 600;
  padding: 4px 0; outline: none;
}
.explain summary:hover { text-decoration: underline; }
.explain ul { padding-left: 20px; margin: 6px 0 0; }
.explain li { margin: 4px 0; font-size: 13px; line-height: 1.5; }
.explain li strong { color: var(--ink); }

/* Buttons */
.btn {
  padding: 9px 16px; border-radius: 10px; border: 1.5px solid var(--brand);
  background: var(--brand); color: white; font-weight: 600; cursor: pointer;
  font-size: 13.5px; transition: all .14s ease;
}
.btn:hover { background: #163056; transform: translateY(-1px); box-shadow: var(--shadow); }
.btn.ghost { background: white; color: var(--brand); }
.btn.ghost:hover { background: #eef3fb; }
.btn.danger { border-color: var(--bad); background: var(--bad); }
.btn.danger:hover { background: #821e1e; }

/* Banner */
.success-banner {
  background: linear-gradient(135deg, #1f7e3a 0%, #14572a 100%); color: white;
  border-radius: 16px; padding: 22px 26px; margin-bottom: 22px; display: none;
  box-shadow: var(--shadow-strong);
}
.success-banner.show { display: block; }
.success-banner h3 { margin: 0 0 6px; font-size: 22px; }
.success-banner p { margin: 4px 0 0; opacity: 0.95; font-size: 14px; }

/* Refs */
.refs a {
  display: block; padding: 11px 14px; border: 1px solid var(--line); border-radius: 10px;
  margin: 8px 0; color: var(--brand); text-decoration: none; font-weight: 600; font-size: 14px;
  background: linear-gradient(180deg, #fbfcff, #f4f7fc);
  transition: all .14s ease;
}
.refs a:hover { border-color: var(--brand); transform: translateX(3px); box-shadow: var(--shadow); }
.refs a::after { content: "  →"; color: var(--accent); }
.refs a small { display: block; color: var(--muted); font-weight: 400; font-size: 12px; margin-top: 2px; word-break: break-all; }

/* Footer */
footer.foot {
  color: var(--muted); font-size: 12px; text-align: center; margin-top: 32px;
  padding-top: 18px; border-top: 1px solid var(--line);
}

/* Overview pane */
.intro {
  background: var(--bg-card); padding: 28px 32px; border-radius: 20px;
  box-shadow: var(--shadow); margin-bottom: 22px;
  border-left: 6px solid var(--accent);
}
.intro h1 { margin: 4px 0 8px; font-size: 28px; color: var(--ink); line-height: 1.2; }
.intro p { margin: 0 0 6px; color: var(--ink-soft); }
.intro .intro-sub { color: var(--ink-soft); font-size: 15px; margin: 0 0 12px; }
.intro .intro-sub strong { color: var(--brand); }
.intro .exam-code {
  display: inline-block; background: var(--accent); color: white;
  font-size: 11px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase;
  padding: 5px 12px; border-radius: 999px;
}
.exam-meta {
  display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px;
}
.meta-pill {
  display: inline-flex; align-items: center; gap: 6px;
  background: #eef3fb; border: 1px solid var(--line); border-radius: 999px;
  padding: 5px 12px; font-size: 12.5px;
}
.meta-pill .meta-key { color: var(--muted); font-weight: 500; }
.meta-pill .meta-val { color: var(--brand); font-weight: 700; }

.domain-grid {
  display: grid; gap: 12px; margin-top: 4px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}
.domain {
  border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px;
  background: linear-gradient(180deg, #f9fbff 0%, #eef3fb 100%);
}
.domain-pct {
  display: inline-block; background: var(--brand); color: white;
  font-weight: 800; font-size: 13px; padding: 4px 10px; border-radius: 8px;
  margin-bottom: 8px;
}
.domain-name { font-weight: 700; color: var(--ink); font-size: 14.5px; margin-bottom: 4px; line-height: 1.3; }
.domain-mods { color: var(--muted); font-size: 12.5px; }
.exam-note {
  margin-top: 14px; padding: 10px 14px; border-radius: 10px;
  background: var(--warn-soft); border-left: 3px solid var(--warn);
  font-size: 13px; color: var(--ink-soft);
}
.modules-grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
.mod-card {
  display: block; text-decoration: none; color: inherit; cursor: pointer;
  background: var(--bg-card); border-radius: 16px; box-shadow: var(--shadow);
  padding: 22px 24px; transition: transform .14s ease, box-shadow .14s ease;
  border: 1px solid var(--line);
  position: relative; overflow: hidden;
}
.mod-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-strong); }
.mod-card .num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; background: var(--brand); color: white; border-radius: 8px;
  font-size: 13px; font-weight: 800;
}
.mod-card h3 { font-size: 17px; font-weight: 700; margin: 12px 0 6px; color: var(--ink); }
.mod-card .summary { color: var(--muted); font-style: italic; font-size: 13.5px; line-height: 1.5; }
.mod-card .stat-row {
  display: flex; gap: 12px; margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--line);
  font-size: 12px; color: var(--muted); flex-wrap: wrap;
}
.mod-card .stat-row .stat { display: inline-flex; align-items: center; gap: 4px; }
.completion {
  display: none; position: absolute; top: 14px; right: 14px;
  background: var(--good); color: white; padding: 4px 10px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: .5px;
}
.mod-card.done .completion { display: inline-block; }
.mod-card.done { border-color: var(--good); }
.tot-progress {
  background: white; border-radius: 14px; box-shadow: var(--shadow); padding: 14px 18px; margin-bottom: 18px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  font-size: 14px;
}
.tot-progress .bar-wrap { flex: 1; background: var(--line); border-radius: 999px; overflow: hidden; height: 10px; }
.tot-progress .bar-fill { height: 100%; background: linear-gradient(90deg, var(--accent) 0%, var(--good) 100%); transition: width .4s ease; }
.tot-progress .label { color: var(--muted); white-space: nowrap; }
.tot-progress .label strong { color: var(--ink); }

/* Panes */
.pane { display: none; }
.pane.active { display: block; }

/* Top promo strip — Gennoor AI Academy */
.promo-strip {
  background: linear-gradient(135deg, #0b1530 0%, #1f3a68 60%, #2c4f8c 100%);
  color: white; padding: 10px 18px; font-size: 13.5px;
  position: sticky; top: 0; z-index: 50;
  box-shadow: 0 2px 8px rgba(15,29,58,0.18);
}
.promo-strip a {
  color: white; text-decoration: none;
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap; justify-content: center;
  max-width: 1200px; margin: 0 auto;
}
.promo-strip .promo-tag {
  background: rgba(255,255,255,0.18); padding: 4px 11px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase;
  flex-shrink: 0;
}
.promo-strip .promo-text { opacity: 0.92; }
.promo-strip .promo-cta {
  font-weight: 700; padding: 4px 12px; border-radius: 999px;
  background: rgba(255,255,255,0.16); transition: background .15s ease;
  white-space: nowrap;
}
.promo-strip a:hover .promo-cta { background: white; color: var(--brand); }

/* Bottom CTA card — full Gennoor AI Academy block on Overview */
.cta-card {
  background: linear-gradient(135deg, #0b1530 0%, #1f3a68 55%, #3b6cae 100%);
  color: white; border-radius: 20px; padding: 32px 36px; margin: 28px 0 8px;
  box-shadow: var(--shadow-strong); position: relative; overflow: hidden;
}
.cta-card::after {
  content: ""; position: absolute; right: -90px; top: -90px; width: 320px; height: 320px;
  border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,0.16), transparent 65%);
}
.cta-card .cta-tag {
  display: inline-block; background: rgba(255,255,255,0.18); padding: 5px 12px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase;
}
.cta-card h2 {
  margin: 12px 0 8px; font-size: 24px; line-height: 1.25; color: white;
  position: relative; z-index: 1;
}
.cta-card p { margin: 0 0 16px; opacity: 0.95; max-width: 720px; font-size: 14.5px; position: relative; z-index: 1; }
.cta-card .cta-stats {
  display: flex; gap: 18px; flex-wrap: wrap; margin: 0 0 18px;
  font-size: 13px; opacity: 0.9; position: relative; z-index: 1;
}
.cta-card .cta-stats span strong { color: white; font-weight: 800; }
.cta-card .cta-btn {
  display: inline-block; background: white; color: var(--brand);
  padding: 11px 22px; border-radius: 10px; font-weight: 700; text-decoration: none;
  font-size: 14.5px; transition: transform .15s ease, box-shadow .15s ease;
  position: relative; z-index: 1;
}
.cta-card .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.18); }

.sidebar-credit {
  display: block; margin-top: 6px; color: var(--muted);
  font-size: 11.5px; text-decoration: none;
}
.sidebar-credit:hover { color: var(--brand); text-decoration: underline; }
.sidebar-credit strong { color: var(--brand); font-weight: 700; }

/* Mobile nav toggle */
.mobile-nav-bar { display: none; }

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar {
    position: relative; height: auto; max-height: 0; overflow: hidden;
    padding: 0 16px; border-right: none; border-bottom: 1px solid var(--line);
    transition: max-height .25s ease, padding .25s ease;
  }
  .sidebar.open { max-height: 80vh; overflow-y: auto; padding: 18px 16px; }
  .main { padding: 18px 18px 80px; }
  .promo-strip { font-size: 12.5px; padding: 9px 14px; }
  .promo-strip a { gap: 8px; }
  .promo-strip .promo-text { font-size: 12px; }
  .cta-card { padding: 24px 22px; }
  .cta-card h2 { font-size: 19px; }
  .mobile-nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 16px; background: white; border-bottom: 1px solid var(--line);
    position: sticky; top: 0; z-index: 30;
  }
  .mobile-nav-bar .brand-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 12px; background: var(--brand); color: white;
    font-size: 11px; font-weight: 700; letter-spacing: .6px; border-radius: 999px; text-transform: uppercase;
  }
  .mobile-nav-bar .brand-pill::before { content: ""; width: 8px; height: 8px; border-radius: 999px; background: #6ec1ff; }
  .menu-btn {
    background: transparent; border: 1.5px solid var(--line); color: var(--brand);
    padding: 7px 12px; border-radius: 10px; font-weight: 600; cursor: pointer; font-size: 13px;
  }
  .hero h1 { font-size: 22px; }
  .hero { padding: 24px 22px; }
  .scorebar { font-size: 13px; padding: 12px 14px; }
  section.card { padding: 22px 20px; }
  .intro { padding: 22px 22px; }
  .intro h1 { font-size: 22px; }
}

@media print {
  body { background: white; }
  .sidebar, .mobile-nav-bar, .scorebar, .btn, .success-banner { display: none !important; }
  .layout { grid-template-columns: 1fr; }
  .main { padding: 0; }
  .pane { display: block !important; page-break-before: always; }
  .pane:first-of-type { page-break-before: auto; }
  section.card { box-shadow: none; border: 1px solid var(--line); page-break-inside: avoid; }
  .hero { background: var(--brand); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .explain { display: block !important; }
}
"""

    # ---------- sidebar ----------
    sidebar_items = [
        '<button class="nav-item" data-target="overview" type="button">'
        '<span class="nav-num">★</span><span class="nav-label">Overview</span><span class="nav-check"></span></button>'
    ]
    for mod in modules:
        sidebar_items.append(
            f'<button class="nav-item" data-target="m{mod["n"]}" data-modnum="{mod["n"]}" type="button">'
            f'<span class="nav-num">{mod["n"]}</span>'
            f'<span class="nav-label">{mod["title"]}</span>'
            f'<span class="nav-check"></span></button>'
        )
    sidebar_html = "\n".join(sidebar_items)

    # ---------- overview pane ----------
    mod_cards = []
    for mod in modules:
        summary = short_summary(mod["n"])
        stats = stat_counts(mod)
        mod_cards.append(
            f'<a class="mod-card" data-target="m{mod["n"]}" data-modnum="{mod["n"]}" href="#m{mod["n"]}">'
            f'<span class="completion">Complete</span>'
            f'<span class="num">{mod["n"]}</span>'
            f'<h3>{mod["title"]}</h3>'
            f'<div class="summary">{summary}</div>'
            f'<div class="stat-row">{stats}</div>'
            f'</a>'
        )
    overview_pane = f"""
<div class="pane active" id="pane-overview">
  <div class="intro">
    <div class="exam-code">Exam AB-100 · Microsoft Certifications</div>
    <h1>AB-100 — Architecting Agentic AI Business Solutions</h1>
    <p class="intro-sub">Path to the <strong>Agentic AI Business Solutions Architect Expert</strong> certification.</p>
    <div class="exam-meta">
      <span class="meta-pill"><span class="meta-key">Exam code</span><span class="meta-val">AB-100</span></span>
      <span class="meta-pill"><span class="meta-key">Passing score</span><span class="meta-val">700 / 1000</span></span>
      <span class="meta-pill"><span class="meta-key">Domains</span><span class="meta-val">3 · weighted</span></span>
      <span class="meta-pill"><span class="meta-key">Format</span><span class="meta-val">Proctored</span></span>
    </div>
    <p style="margin-top:14px;">Eleven modules — each with a recap, the key concepts you need to leave with, an architect cheat-sheet, a practice quiz with retry, and the canonical Microsoft Learn pages for follow-up.</p>
    <p style="margin-top:6px;color:var(--muted);font-size:13.5px;">Pick any module to start. Progress is saved in your browser — close the tab and come back.</p>
  </div>

  <section class="card">
    <h2><span class="icon">i</span>About AB-100</h2>
    <p style="margin:0 0 12px;color:var(--ink-soft);font-size:14.5px;">
      AB-100 validates that you can architect AI-powered business solutions across the Microsoft stack —
      Microsoft 365 Copilot, Copilot Studio, Microsoft Foundry &amp; Foundry Tools, Dynamics 365, and Power Platform.
      The audience is an experienced solution architect who designs <strong>agentic-first, multi-agent, secure, ROI-defensible</strong>
      solutions and champions responsible AI. Passing AB-100 plus a prerequisite associate certification earns the
      <em>Agentic AI Business Solutions Architect Expert</em> credential.
    </p>

    <div class="domain-grid">
      <div class="domain">
        <div class="domain-pct">25–30%</div>
        <div class="domain-name">Plan AI-powered business solutions</div>
        <div class="domain-mods">Modules 2 · 3 · 4</div>
      </div>
      <div class="domain">
        <div class="domain-pct">25–30%</div>
        <div class="domain-name">Design AI-powered business solutions</div>
        <div class="domain-mods">Modules 5 · 6 · 7</div>
      </div>
      <div class="domain">
        <div class="domain-pct">40–45%</div>
        <div class="domain-name">Deploy AI-powered business solutions</div>
        <div class="domain-mods">Modules 8 · 9 · 10 · 11</div>
      </div>
    </div>

    <p class="exam-note">
      Module 1 is the architect-role primer that frames the whole course; it is not a separate exam domain.
    </p>

    <div class="refs" style="margin-top:18px;">
      <a href="https://learn.microsoft.com/credentials/certifications/resources/study-guides/ab-100" target="_blank" rel="noopener">Official AB-100 study guide<small>learn.microsoft.com/credentials/certifications/resources/study-guides/ab-100</small></a>
      <a href="https://learn.microsoft.com/credentials/certifications/agentic-ai-business-solutions-architect/" target="_blank" rel="noopener">Agentic AI Business Solutions Architect — certification page<small>learn.microsoft.com/credentials/certifications/agentic-ai-business-solutions-architect/</small></a>
      <a href="https://learn.microsoft.com/credentials/certifications/exams/AB-100" target="_blank" rel="noopener">Exam AB-100 — schedule &amp; details<small>learn.microsoft.com/credentials/certifications/exams/AB-100</small></a>
      <a href="https://learn.microsoft.com/credentials/certifications/agentic-ai-business-solutions-architect/practice/assessment?assessment-type=practice&amp;assessmentId=1815645847&amp;practice-assessment-type=certification" target="_blank" rel="noopener">Free official practice assessment<small>learn.microsoft.com/.../practice/assessment</small></a>
    </div>
  </section>

  <div class="tot-progress">
    <span class="label"><strong id="totDone">0</strong> of 11 modules completed</span>
    <div class="bar-wrap"><div class="bar-fill" id="totBar" style="width:0%"></div></div>
    <span class="label"><strong id="totScore">0</strong> total points</span>
  </div>

  <div class="modules-grid">
{chr(10).join(mod_cards)}
  </div>

  <section class="cta-card">
    <span class="cta-tag">Gennoor Tech · AI Academy</span>
    <h2>Take it further — live, hands-on AI architect tracks.</h2>
    <p>Built and delivered by an MCT with 14+ years of practice and 80+ enterprise programs shipped across six countries — covering AB-100 prep, Copilot Studio, Microsoft Foundry, multi-agent design, and responsible AI for leadership and engineering teams.</p>
    <div class="cta-stats">
      <span><strong>14+</strong> years</span>
      <span><strong>80+</strong> enterprise programs</span>
      <span><strong>6+</strong> countries</span>
      <span><strong>16</strong> active Microsoft certs</span>
    </div>
    <a class="cta-btn" href="https://gennoor.com/academy" target="_blank" rel="noopener">Explore the AI Academy on gennoor.com →</a>
  </section>

  <footer class="foot">Microsoft AB-100 ILT companion · Use it before, during, or after the trainer-led delivery.<br>
  Built around the Microsoft Learn references in the official decks · Brought to you by <a href="https://gennoor.com/academy" target="_blank" rel="noopener" style="color:var(--brand);font-weight:600;text-decoration:none;">Gennoor Tech · AI Academy</a>.</footer>
</div>
"""

    # ---------- module panes ----------
    module_panes = []
    for mod in modules:
        n = mod["n"]
        pane = f"""
<div class="pane" id="pane-m{n}">
  <div class="hero">
    <span class="hero-mod">Module {n} of 11</span>
    <h1>{mod["title"]}</h1>
    <p class="frame">{mod["frame"]}</p>
  </div>

  <div class="scorebar">
    <span class="progress" id="m{n}-progress-text"><strong>0</strong> of {mod["num_q"]} answered</span>
    <span class="score" id="m{n}-score-text">Score: 0/{mod["num_q"]}</span>
    <span class="pct" id="m{n}-pct-text">0%</span>
    <button class="btn danger" onclick="resetAll({n})">Reset</button>
  </div>

  <div id="m{n}-success-banner" class="success-banner">
    <h3>Quiz complete</h3>
    <p id="m{n}-banner-text"></p>
  </div>

  <section class="card">
    <h2><span class="icon">R</span>Recap — what to remember</h2>
    <ul class="recap-list">{mod["recap_inner"]}</ul>
  </section>

  <section class="card">
    <h2><span class="icon">K</span>Key concepts</h2>
    <div class="concepts">{mod["concepts_inner"]}</div>
  </section>

  <section class="card">
    <h2><span class="icon">C</span>Cheat sheet — when…then</h2>
    <div class="cheat">{mod["cheat_inner"]}</div>
  </section>

  <section class="card">
    <h2><span class="icon">Q</span>Practice quiz · {mod["num_q"]} questions</h2>
    <p class="q-meta">Tap an option to lock your answer. You'll see the right answer, why your pick is wrong (if it is), and reasoning for every option. Use <em>Reset</em> at the top to start the quiz over. Your progress saves automatically.</p>
    {mod["questions_html"]}
  </section>

  <section class="card refs">
    <h2><span class="icon">→</span>Further reading on Microsoft Learn</h2>
    {mod["refs_inner"]}
  </section>

  <footer class="foot">
    AB-100 — Architecting agentic AI business solutions · Microsoft customer stories used as use cases.<br>
    Self-paced — open this page as many times as you want. Progress is saved in your browser.
  </footer>
</div>
"""
        module_panes.append(pane)

    # ---------- quiz data JSON for runtime ----------
    quiz_runtime = {
        str(mod["n"]): mod["quiz_data"] for mod in modules
    }
    quiz_runtime_json = json.dumps(quiz_runtime)

    # ---------- script ----------
    script = """
const QUIZ_BY_MOD = __QUIZ_RUNTIME__;
const TOTAL_MODS = 11;
const state = {}; // modnum -> { answered, correct, userAnswers }

function storeKey(n) { return "ab100-progress-mod-" + n; }
const ALL_KEY = "ab100-progress-all";

function saveProgress(n) {
  try {
    const s = state[n];
    const totalQ = QUIZ_BY_MOD[n].questions.length;
    const p = { answered: s.answered, correct: s.correct, totalQ, userAnswers: s.userAnswers, savedAt: Date.now() };
    localStorage.setItem(storeKey(n), JSON.stringify(p));
    const all = JSON.parse(localStorage.getItem(ALL_KEY) || "{}");
    all["m" + n] = { score: s.correct, total: totalQ, answered: s.answered, complete: s.answered === totalQ, at: Date.now() };
    localStorage.setItem(ALL_KEY, JSON.stringify(all));
  } catch(e) {}
}

function loadProgressForMod(n) {
  state[n] = { answered: 0, correct: 0, userAnswers: {} };
  try {
    const raw = localStorage.getItem(storeKey(n));
    if (!raw) return;
    const p = JSON.parse(raw);
    if (!p || !p.userAnswers) return;
    state[n].userAnswers = p.userAnswers || {};
    Object.keys(state[n].userAnswers).forEach(k => {
      const qi = parseInt(k);
      const oi = state[n].userAnswers[k];
      applyAnswerVisuals(n, qi, oi, /*fromLoad*/true);
    });
  } catch(e) {}
}

function applyAnswerVisuals(n, qi, oi, fromLoad) {
  const q = QUIZ_BY_MOD[n].questions[qi];
  const block = document.getElementById('m' + n + '-q-' + qi);
  if (!block || block.dataset.locked === '1') return;
  block.dataset.locked = '1';
  const opts = block.querySelectorAll('.option');
  opts.forEach((el, i) => {
    el.classList.add('locked');
    if (i === q.correct) el.classList.add('correct');
    else if (i === oi) el.classList.add('wrong');
    else el.classList.add('disabled');
  });
  const expl = block.querySelector('.explain');
  expl.style.display = 'block';
  const isRight = oi === q.correct;
  expl.classList.remove('right', 'wrong');
  expl.classList.add(isRight ? 'right' : 'wrong');
  let out = '';
  out += '<div><span class="verdict">' + (isRight ? 'Correct' : 'Not quite') + '</span>' + q.explanations[q.correct] + '</div>';
  if (!isRight) {
    out += '<div style="margin-top:10px;"><strong>Why your pick is wrong:</strong> ' + q.explanations[oi] + '</div>';
  }
  out += '<details><summary>See reasoning for every option</summary><ul>';
  for (let i = 0; i < q.options.length; i++) {
    const tag = (i === q.correct) ? ' (correct)' : '';
    out += '<li><strong>' + String.fromCharCode(65+i) + ')' + tag + '</strong> ' + q.explanations[i] + '</li>';
  }
  out += '</ul></details>';
  expl.innerHTML = out;
  state[n].answered += 1;
  if (isRight) state[n].correct += 1;
  renderScorebar(n);
}

function pickOption(n, qi, oi) {
  const block = document.getElementById('m' + n + '-q-' + qi);
  if (block.dataset.locked === '1') return;
  applyAnswerVisuals(n, qi, oi);
  state[n].userAnswers[qi] = oi;
  saveProgress(n);
  renderOverview();
  renderSidebar();
}

function resetAll(n) {
  if (!confirm("Reset this quiz? All your answers will be cleared.")) return;
  const totalQ = QUIZ_BY_MOD[n].questions.length;
  for (let i = 0; i < totalQ; i++) {
    const block = document.getElementById('m' + n + '-q-' + i);
    if (block && block.dataset.locked === '1') {
      block.dataset.locked = '0';
      block.querySelectorAll('.option').forEach(el => { el.className = 'option'; });
      const expl = block.querySelector('.explain');
      expl.style.display = 'none';
      expl.classList.remove('right', 'wrong');
      expl.innerHTML = '';
    }
  }
  state[n] = { answered: 0, correct: 0, userAnswers: {} };
  saveProgress(n);
  const banner = document.getElementById('m' + n + '-success-banner');
  if (banner) banner.classList.remove('show');
  renderScorebar(n);
  renderOverview();
  renderSidebar();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderScorebar(n) {
  const totalQ = QUIZ_BY_MOD[n].questions.length;
  const s = state[n];
  const pt = document.getElementById('m' + n + '-progress-text');
  const st = document.getElementById('m' + n + '-score-text');
  const ct = document.getElementById('m' + n + '-pct-text');
  if (!pt) return;
  pt.innerHTML = '<strong>' + s.answered + '</strong> of ' + totalQ + ' answered';
  st.textContent = 'Score: ' + s.correct + '/' + totalQ;
  const pct = totalQ ? Math.round((s.correct/totalQ)*100) : 0;
  ct.textContent = pct + '%';
  if (s.answered === totalQ) {
    const banner = document.getElementById('m' + n + '-success-banner');
    banner.classList.add('show');
    let msg = '';
    if (s.correct === totalQ) msg = 'Perfect run. You know this module cold.';
    else if (s.correct >= totalQ * 0.75) msg = 'Strong pass. Skim the explanations and you are ready.';
    else if (s.correct >= totalQ * 0.5) msg = 'Halfway home. Re-read the recap and try again.';
    else msg = 'Slow down — go back to the recap and key concepts before retrying.';
    document.getElementById('m' + n + '-banner-text').textContent =
      'You scored ' + s.correct + '/' + totalQ + ' (' + pct + '%). ' + msg;
  }
}

function renderOverview() {
  try {
    const all = JSON.parse(localStorage.getItem(ALL_KEY) || "{}");
    let done = 0, score = 0;
    document.querySelectorAll(".mod-card").forEach(card => {
      const n = card.getAttribute("data-modnum");
      const r = all["m" + n];
      card.classList.remove("done");
      if (r) {
        score += r.score || 0;
        if (r.complete) { done++; card.classList.add("done"); }
      }
    });
    document.getElementById("totDone").textContent = done;
    document.getElementById("totScore").textContent = score;
    document.getElementById("totBar").style.width = ((done/TOTAL_MODS)*100) + "%";
  } catch(e) {}
}

function renderSidebar() {
  try {
    const all = JSON.parse(localStorage.getItem(ALL_KEY) || "{}");
    document.querySelectorAll(".nav-item[data-modnum]").forEach(btn => {
      const n = btn.getAttribute("data-modnum");
      const r = all["m" + n];
      btn.classList.toggle("done", !!(r && r.complete));
    });
  } catch(e) {}
}

function showPane(target) {
  document.querySelectorAll('.pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
  const pane = document.getElementById('pane-' + target);
  if (pane) pane.classList.add('active');
  const navBtn = document.querySelector('.nav-item[data-target="' + target + '"]');
  if (navBtn) navBtn.classList.add('active');
  // close mobile sidebar after pick
  const sb = document.getElementById('sidebar');
  if (sb) sb.classList.remove('open');
  window.scrollTo({ top: 0, behavior: 'instant' in window ? 'instant' : 'auto' });
  // update hash without jump
  if (history.replaceState) history.replaceState(null, '', '#' + target);
}

function initFromHash() {
  let target = (location.hash || '#overview').slice(1);
  if (target !== 'overview' && !target.match(/^m([1-9]|1[01])$/)) target = 'overview';
  showPane(target);
}

document.addEventListener('DOMContentLoaded', () => {
  // load all module state
  for (let n = 1; n <= TOTAL_MODS; n++) loadProgressForMod(n);
  // wire nav
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => showPane(btn.getAttribute('data-target')));
  });
  document.querySelectorAll('.mod-card').forEach(card => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      showPane(card.getAttribute('data-target'));
    });
  });
  const menu = document.getElementById('menu-toggle');
  if (menu) menu.addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
  });
  window.addEventListener('hashchange', initFromHash);
  renderOverview();
  renderSidebar();
  // render scorebars for all modules (so initial state is consistent even before viewing)
  for (let n = 1; n <= TOTAL_MODS; n++) renderScorebar(n);
  initFromHash();
});
"""
    script = script.replace("__QUIZ_RUNTIME__", quiz_runtime_json)

    # ---------- assemble ----------
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AB-100 — Architecting Agentic AI Business Solutions · Student Portal</title>
<style>{css}</style>
</head>
<body>

<div class="promo-strip">
  <a href="https://gennoor.com/academy" target="_blank" rel="noopener">
    <span class="promo-tag">Gennoor Tech · AI Academy</span>
    <span class="promo-text">Live, instructor-led AI architect tracks · taught by an MCT with 80+ enterprise programs shipped globally</span>
    <span class="promo-cta">Explore courses →</span>
  </a>
</div>

<div class="mobile-nav-bar">
  <span class="brand-pill">AB-100 · Student Portal</span>
  <button class="menu-btn" id="menu-toggle" type="button">☰ Modules</button>
</div>

<div class="layout">
  <aside class="sidebar" id="sidebar">
    <span class="sidebar-brand">AB-100 · Student Portal</span>
    <a class="sidebar-credit" href="https://gennoor.com/academy" target="_blank" rel="noopener">by <strong>Gennoor Tech · AI Academy</strong></a>
    <div class="nav-section-label">Course</div>
    {sidebar_html}
    <div class="sidebar-foot">Microsoft AB-100 · Architecting Agentic AI Business Solutions. Progress is saved in your browser.</div>
  </aside>

  <main class="main">
    {overview_pane}
    {"".join(module_panes)}
  </main>
</div>

<script>{script}</script>
</body>
</html>
"""
    (HERE / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote index.html ({len(html):,} chars, {len(modules)} modules)")


if __name__ == "__main__":
    build()
