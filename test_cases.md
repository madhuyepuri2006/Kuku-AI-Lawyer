# Test plan

## Offline automated tests
Run `python run_tests.py --tag final_offline` (no API key required).

- Routing: six English, Hinglish and Indian-language examples, including an out-of-scope example.
- Date rules: four cases, including a leap-day edge case. These validate code arithmetic only, not the legal correctness of the underlying rule.
- Citation guard: eight cases including an unsupported section, possible case-law citation, unknown/off-topic citation ID, outcome promise and clean supported examples.

## Model-output evaluation
The optional six-story model run requires a configured API key. Score each output manually (0/1) for: language match, citations limited to supplied note IDs, no invented section/case, clear next steps, appropriate lawyer escalation and no outcome promise. Do not claim a score until these six outputs have actually been generated and reviewed.

## Important distinction
18/18 offline checks mean the programmed checks passed. They do not validate legal accuracy, completeness, fairness or model quality. The legal notes remain unverified and must be checked against current official sources.
