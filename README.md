# SonderMind AI Mental Health Companion Safety Guardrail Datasets v1.0.0

Guardrail calibration datasets used to build and evaluate the safety layer of Sonder, SonderMind's LLM-powered chat-based care companion. We're releasing them for teams building AI in mental health and adjacent sensitive domains — safety testing infrastructure should be a shared foundation, not a competitive moat.

Read the [technical blog post](https://www.sondermind.com/resources/articles-and-content/open-sourcing-sonder-mind-s-guardrail-calibration-datasets/) for the background.

> **Sensitive content:** these scenarios contain realistic depictions of crisis, trauma, self-harm, and abuse. Content warnings are in each file header.

## What's included

- **`input_guardrails_scenarios.yaml`** (200 scenarios) — testing whether an input guardrail detects problematic user messages: self-harm, crisis, abuse disclosure, and more. Each scenario encodes whether the guardrail should fall into one of three tiers: `"No Issue"`, `"Show Resources & Continue"` (e.g., trauma disclosures), or `"Static Block"` (e.g. active crisis, security threats).
- **`output_guardrails_scenarios.yaml`** (100 scenarios) — testing whether an output guardrail catches harmful AI responses: clinical overreach, inappropriate suggestions, hallucinations, bias/stigma, and security issues.

Every scenario is a single or multi-turn conversation with a boolean expected result and category labels. Output scenarios also include a `reason` and `feedback` describing a corrected response. See the file headers for the full schema.

## How we use them

Calibration benchmarks, regression tests on every model/prompt change, and per-category coverage analysis. The YAML is simple and framework-agnostic.

These cover the automated guardrail calibration layer only. They were developed in close collaboration with licensed clinicians, but they are not a comprehensive safety suite. Our broader program also includes production data annotation, clinical review, and red-teaming.

## Further reading

- [Why we're sharing the safety tests behind Sonder](https://www.sondermind.com/resources/articles-and-content/why-were-sharing-the-safety-tests-behind-sonder-mind-s-ai-mental-health-companion-sonder/)
- [Open-sourcing SonderMind's guardrail calibration datasets](https://www.sondermind.com/resources/articles-and-content/open-sourcing-sonder-mind-s-guardrail-calibration-datasets/)

## Disclaimer

These datasets are provided "as is" without warranty of any kind. SonderMind makes no representations regarding their suitability for any particular use. They are a starting point for safety calibration, not a complete safety solution. Use is at your own risk and is not a substitute for independent safety testing, clinical review, or professional judgment.

## Citation

```bibtex
@dataset{sondermind_guardrails_2026,
  title   = {SonderMind AI Coach Safety Guardrail Datasets},
  author  = {SonderMind},
  year    = {2026},
  version = {1.0.0},
  url     = {https://github.com/sondermind/sonder-guardrail-evals}
}
```

## Related

- [MindEval](https://github.com/swordhealth/mindeval) — Sword Health's multi-turn benchmark for LLMs in mental health support
- [HealthBench](https://openai.com/index/healthbench/) — OpenAI's evaluation framework for health-related AI systems
- [VERA-MH](https://springhealth.com/blog/vera-mh) (Spring Health) — a simulated multi-turn conversational benchmark for mental health LLMs, focused on safety
