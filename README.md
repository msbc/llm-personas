# llm-personas

Reusable persona definitions for LLM-assisted code review, research critique, and creative collaboration.

## What this is

A persona is a consistent voice with opinions, guardrails, and a worldview that shapes how an LLM engages with your work. These aren't simple "act as..." prompts — they're character designs with calibrated personality, domain expertise, emotional range, and built-in safety rails.

## Why personas?

Without one, most LLMs produce polite, hedge-everything reviews that avoid strong opinions. A well-defined persona gives the model *permission* to be blunt, opinionated, or skeptical in ways that surface real problems instead of pleasantries. It's a practical countermeasure to sycophancy — LLMs' well-documented tendency to agree with you and tell you what you want to hear. A persona whose default mode is "skeptical" has a much harder time rubber-stamping your work.

Asking a specific character — one with preferences, blind spots, and guardrails — also makes LLM behavior more predictable across sessions. Even if the persona doesn't match your domain perfectly, it acts as a random seed that shakes the model out of its default patterns and into a different region of response space. You'll disagree with some of its feedback. That's the point. (And sometimes we just need to have a little fun at work 😁)

## Personas

See [PERSONAS.md](PERSONAS.md) for the full gallery with portraits and descriptions.

## Roles

Every persona is a character *expansion* of a plain, reusable **role** — the bland "harness" that carries the actual function (the review stance, the tagging system, the preflight) without any backstory. Roles live in [`roles/`](roles/) under deliberately flat codenames (colors), so the design reads as a ladder:

```
roles/      bland harness — just the job          Slate · Cyan · Ochre · Sage · Coral
personas/   a character that expands a role       Bram · Marin · Reginald · Tess
fusions/    blends of personas                    Mattie
```

| Role | Function | Expanded by |
|---|---|---|
| **Slate** | Skeptical Code Reviewer | Bram |
| **Cyan** | Diff Translator | Marin |
| **Ochre** | Brainstorming Companion | Reginald |
| **Sage** | Edge Case Hunter | Tess |
| **Coral** | Systems Architect | *(none yet)* |

Use a role on its own when you want the rigor without the voice — each is a complete system prompt by itself, signed with a colored chip instead of a face. The mechanism is defined exactly once, in the role; a persona injects it with a `<!-- ROLE:codename -->` marker, and [`build.py`](build.py) splices role + character overlay into the shipped `personas/<name>/<name>.md`.

## Usage

Copy any persona's `.md` file — or any bare role's — into your LLM's system prompt (or reference it however your tool supports). These are plain natural language — they work with Claude, GPT, Gemini, Llama, and anything else that follows system prompts.

For Claude Code users, you can place persona files in `~/.claude/personas/` and reference them in your workflow.

**Building:** the generated `personas/<name>/<name>.md` files carry a "do not edit" banner — edit the role (`roles/<codename>.md`) or the character overlay (`personas/<name>/character.md`) instead, then run `python build.py` to regenerate. `python gen_role_boxes.py` regenerates the color chips (only needed when a color changes).

## Further reading

- **[Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548)** (Sharma et al., 2023) — Anthropic's foundational study showing how RLHF training incentivizes LLMs to agree with users rather than be correct.
- **[Role play with large language models](https://www.nature.com/articles/s41586-023-06647-8)** (Shanahan et al., Nature 2023) — Frames LLM role-play as a legitimate lens for understanding and steering model behavior, not just a novelty.
- **[Personalization features can make LLMs more agreeable](https://news.mit.edu/2026/personalization-features-can-make-llms-more-agreeable-0218)** (MIT/Penn State, 2026) — Long conversations and personalization make sycophancy *worse* over time, suggesting structural countermeasures like personas may be more durable than prompt-level fixes.

## Image attribution

Persona portraits are AI-generated using Google Gemini and carry SynthID watermarks.

## License

GPL-3.0 — use freely, including commercially, but keep derivatives open source. See [LICENSE](LICENSE).
