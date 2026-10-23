# Kindly Later

Turn a folder of exported `.eml` messages into a calm, local reply queue. An open-weight model decides which messages need a response, writes a short draft, and points to a verbatim line in the original message. You review and copy the drafts; this tool never sends mail or connects to an inbox.

## Quick start

Requires Python 3.10+ and [Ollama](https://ollama.com/) with a local model. Gemma 3 is the recommended model, but `--model` can select any Ollama chat model.

```bash
ollama pull gemma3:4b
ollama serve
python3 kindly_later.py examples/mail --output reply-queue.html --model gemma3:4b
```

To inspect the interface without waiting for a model, run `python3 kindly_later.py examples/mail --sample-preview --output sample-preview.html`. The preview uses hand-written illustrative suggestions and is labeled accordingly; it is not evidence of model quality.

Open `reply-queue.html` in a browser. The sample messages are fictional. For your own mail, export individual messages as `.eml` into a folder and pass that folder instead. The tool reads only direct `.eml` children, caps each body at 12,000 characters, and makes requests only to `127.0.0.1:11434`.

Run `python3 -m unittest discover -s tests -v` for the offline tests. No Python packages or API keys are required.

## Why it is built this way

- The model has a narrow job: decide `reply`, `read`, or `ignore`, and draft a response. It must provide an exact quote from the source as evidence.
- Python validates the JSON, the decision, and the exact quote. Unsupported answers become `Review manually` rather than a confident suggestion.
- The HTML report is static. It stores no server-side data, makes no network requests, and has copy buttons for drafts. Original emails and generated suggestions stay on your computer.
- There is no send operation. The human chooses whether to use or edit each draft.

Limitations: this is a small local prototype, not an email client. It handles plain-text message bodies best; HTML-only email is converted to text conservatively. It does not understand attachments or threaded history. Model output can still be wrong even when it quotes a real line, so review every draft.

## Challenge note

Built for [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19). The lazy payoff is replacing repeated “open, decide, compose” passes with one review queue. Measure your own payoff by timing manual triage of the same messages versus reviewing the generated report; no time savings are claimed without that measurement.
