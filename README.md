# Kuku AI Generalist Assignment — Problem 2: Build an AI Lawyer

A small text-based prototype for three narrowly scoped everyday problems in India:
1. RTI application / delayed response
2. UPI or online payment fraud
3. Unpaid salary / full-and-final dues

It is **not a lawyer and must not be used as legal advice**. The legal notes in `kb.json` are explicitly marked `unverified`; verify every rule, deadline, fee and forum against current official central/state/bank sources before using a generated draft. The tool intentionally leaves unknown facts as `[PLACEHOLDERS]` rather than inventing them.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open the local Gradio URL printed in the terminal. Text input is implemented; voice input is not implemented and is an acknowledged limitation.

## Optional model explanation

Set one provider's API key before running. The default is Anthropic:

```powershell
$env:ANTHROPIC_API_KEY="your_key"
```

Or use an OpenAI-compatible provider:

```powershell
$env:LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your_key"
```

Model configuration is swappable through `LLM_PROVIDER`, `LLM_MODEL` and `LLM_BASE_URL`. Without a key, routing, date rules and draft templates still run; model explanations are unavailable.

## Tests

```bash
python run_tests.py --tag final_offline
```

The offline tests check keyword routing, date calculations and the citation guard. A passing guard only means its configured pattern checks passed; it does **not** prove that legal advice is correct. Model output quality requires a separately run and manually scored model test; no model-quality score is claimed in this submission.

## Files

- `app.py` — Gradio interface and input collection
- `engine.py` — routing, date calculations, templates, model adapter and citation guard
- `kb.json` — legal notes and source URLs; currently unverified
- `tests.json`, `run_tests.py` — offline test suite
- `test_cases.md` — test plan
- `raw_outputs/` — unedited test outputs
- `Solution_Doc_Problem2.pdf` — two-page solution note

## Known limitations

- Keyword routing can miss paraphrases and can misclassify ambiguous stories.
- The date calculations are indicative, ignore public holidays and must be checked against current rules and facts.
- The citation guard detects selected patterns; it cannot detect every false legal statement.
- The notes have not been independently verified; state-specific law and procedure are not comprehensively covered.
- Voice input, document upload, authentication and lawyer review workflow are not implemented.
- Generated drafts contain placeholders and must be checked by the user / qualified professional before sending.
