# AB-100 — Architecting Agentic AI Business Solutions · Student Portal

A static, single-page study portal for the Microsoft **AB-100 — Architecting Agentic AI Business Solutions** course. All eleven modules — recap, key concepts, architect cheat-sheet, practice quiz with explanations, and curated Microsoft Learn references — bundled into one HTML file with a left-sidebar nav.

## Live site

> Once GitHub Pages is enabled on this repo, the site is hosted at the URL shown under **Settings → Pages**.

## What's in here

| File | Purpose |
| --- | --- |
| `index.html` | Combined single-page portal — Overview + all 11 modules as left-sidebar tabs. **Generated** by `build_combined.py`. |
| `M01-quiz.html` … `M11-quiz.html` | Original per-module pages. Still work standalone — useful when you want one module in its own tab/print. |
| `build_combined.py` | Generator that extracts each module's content and assembles `index.html`. Re-run after editing any `Mxx-quiz.html`. |

## Modules

1. Introduction to Agentic AI Business Solution Architecture
2. Analyze requirements for AI-powered business solutions
3. Design overall AI strategy for business solutions
4. Evaluate the costs and benefits of an AI-powered business solution
5. Design AI and agents for business solutions
6. Design extensibility of AI solutions
7. Orchestrate configuration for prebuilt agents and apps
8. Analyze, monitor, and tune AI-powered business solutions
9. Manage the testing of AI-powered business solutions
10. Design the ALM process for AI-powered business solutions
11. Design responsible AI, security, governance, risk management, and compliance

Each module has: a recap, 6–8 key concepts, an architect "when…then" cheat sheet, an 8-question practice quiz with per-option explanations, and links back to Microsoft Learn for follow-up.

## Using it locally

It is a plain static site — no build step required to browse.

```powershell
# from this folder
python -m http.server 8000
# then open http://localhost:8000/
```

Or just double-click `index.html`.

## Regenerating the combined page

If you edit any `Mxx-quiz.html`, rebuild the combined page:

```powershell
python build_combined.py
```

## Progress & privacy

Quiz progress is stored in `localStorage` in your browser only. Nothing is sent anywhere. Clear it with each module's **Reset** button, or from devtools.

## Credits

Built around the Microsoft AB-100 trainer guide and the canonical Microsoft Learn references. Customer stories and product names belong to their owners; this is a study companion, not an official Microsoft asset.

---

## LinkedIn announcement — copy-ready

Optimized for LinkedIn's algorithm and reading patterns:

- **Hook in the first two lines** (above the "see more" fold on mobile, ~210 chars).
- **Unicode pseudo-bold** for the title (LinkedIn renders these characters natively; no plugin needed).
- **Short paragraphs and arrows** (`↳`) for high-scannability.
- **Specific differentiator** stated (per-option reasoning, not just the correct answer).
- **Mapped to the three official exam domains** with weighting — searchable terms.
- **High-intent hashtags** targeting AB-100 candidates, MCTs, and AI-architect role searchers.
- **Plain-text URL** (LinkedIn previews github.io reliably and ranks plain links better than wrapped ones).

Paste the block between the markers as-is:

```text
[BEGIN POST — do not include this line]

Prepping for AB-100 — Microsoft's new Agentic AI Business Solutions Architect Expert exam?

I just open-sourced a free single-page study portal that covers all 11 modules.

𝗔𝗕-𝟭𝟬𝟬 — 𝗔𝗿𝗰𝗵𝗶𝘁𝗲𝗰𝘁𝗶𝗻𝗴 𝗔𝗴𝗲𝗻𝘁𝗶𝗰 𝗔𝗜 𝗕𝘂𝘀𝗶𝗻𝗲𝘀𝘀 𝗦𝗼𝗹𝘂𝘁𝗶𝗼𝗻𝘀 — 𝗦𝘁𝘂𝗱𝗲𝗻𝘁 𝗣𝗼𝗿𝘁𝗮𝗹

Each module gives you:
↳ A recap of what to actually remember
↳ 6–8 key concepts you have to leave with
↳ An architect "when → then" cheat sheet
↳ An 8-question practice quiz with reasoning for EVERY option (not just the correct one)
↳ Direct links to the canonical Microsoft Learn pages

Coverage is mapped to the three official exam domains:
• Plan AI-powered business solutions — 25–30%
• Design AI-powered business solutions — 25–30%
• Deploy AI-powered business solutions — 40–45%

No login. No paywall. Progress saves in your browser. Works on mobile.

Try it: https://lostspace003.github.io/ab-100-quiz-architecting-agentic-ai-business-solutions/

I built this because the AI architect role doesn't fail on syntax — it fails on judgment. Multi-agent, agentic-first, ROI-defensible, responsibly-governed. Those decisions are what the exam tests, and they're what the quizzes drill.

If you're studying for AB-100 — or training your team for it — give it a spin and tell me what's missing. Feedback, corrections, and PRs welcome.

#AB100 #MicrosoftAI #AgenticAI #CopilotStudio #MicrosoftFoundry #AIArchitect #MicrosoftCertified #MCT #AzureAI #ExamPrep

[END POST — do not include this line]
```

### Two optional hooks (swap the opening line if you want a different tone)

**Credentials-first hook** (good if you want to reinforce authority):

```text
After 376+ hours on Microsoft Learn and 16 active Microsoft certifications, I kept hitting the same wall preparing for AB-100 — no consolidated portal for the architect's judgment calls. So I built one. Free. Open source.
```

**Trainer-first hook** (good for your MCT audience):

```text
I trained 80+ AI programs across 6 countries and the same question kept coming up: "where do we study for AB-100?" There was no single answer — so this weekend I built one and shipped it.
```

### Posting tips

- **Drop the link with the post.** Don't comment-link — github.io previews fine, and LinkedIn's algorithm now treats first-party links less harshly than it did in 2024.
- **Reply to every comment within the first hour.** That's the single biggest reach lever LinkedIn rewards.
- **Tag 1–2 people only** if they'd genuinely engage (over-tagging suppresses reach). Candidates: a colleague who's also pursuing AB-100, or a Microsoft Learn community account.
- **Repost in 7–10 days** with a "what people said" angle and one screenshot of the quiz UI — recycles the same audience without algorithm penalty.

