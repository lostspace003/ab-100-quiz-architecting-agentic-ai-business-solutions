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

Brought to you by **[Gennoor Tech · AI Academy](https://gennoor.com/academy)** — live, instructor-led AI architect tracks.

