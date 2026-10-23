# Kindly Later: a local reply queue for the emails I keep postponing

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19).* 

## What I Built

I do not dread writing email as much as I dread deciding which email needs writing. A mixed folder of receipts, updates, and actual questions makes every “quick inbox check” a series of tiny decisions.

Kindly Later takes exported `.eml` messages and turns them into a single review queue. It asks a locally running open weight model to mark each message as “reply,” “read,” or “ignore,” and to write a short reply draft when one is needed. Each suggestion includes an exact quote from the original message, so I can see why it was made without reopening the email. The app never sends mail. The user reviews the drafts and copies only the useful ones.

The goal is modest: spend one intentional pass reviewing suggestions instead of repeatedly reopening the same messages.

## Demo

**Interface preview:** [Add public screenshot or short demo video before publishing]. The repository includes `sample-preview.html`, a static example with four fictional emails. Its suggestions are hand written so readers can inspect the interface without installing a model; it is clearly labeled as an illustration.

**Real model run:** [Add a recorded run and measured results before publishing]. The local Ollama service on the development machine timed out during verification, so I am not claiming that the sample preview proves model accuracy or speed.

## Code

**Repository:** [Add public GitHub repository URL before publishing]

The project is MIT licensed and has no Python package dependencies. The key command is:

```bash
ollama pull gemma3:4b
ollama serve
python3 kindly_later.py examples/mail --output reply-queue.html --model gemma3:4b
```

The model name is configurable. The local build was also attempted with an installed `llama3.1:latest` model. Both attempted runs timed out on this machine, so the current verified results are the offline tests and the illustrative UI preview.

## How I Built It

Python's standard `email` package parses exported messages. The app sends only the sender, subject, and a capped text body to Ollama on `127.0.0.1`. A system prompt asks for JSON with a decision, a reason, a verbatim evidence quote, and an optional draft. Python validates the fields and checks that the quote occurs in the source body. If validation fails or the model times out, the message goes into a “Review manually” lane. The report is static HTML with no network requests and no send action.

The trust boundary is the interesting part. An email can contain instructions aimed at an assistant. One fictional test message includes such an instruction. The email is passed as data, and model output is validated before it appears as a suggestion. An exact quote does not guarantee a correct decision, so human review remains the last step.

## Why Does Open Innovation Matter?

Email is personal. Using a local open weight model means the app can process exported messages without sending their content to an external AI service. Ollama provides a model interface that can be swapped: a small model for a low power machine or a stronger model when accuracy matters more. There is no per message API charge. The code and the output format can be inspected and changed by anyone.

This design also makes the safety behavior visible. The model suggests; the Python program verifies a narrow set of invariants; the person decides whether to use the result.

## The Lazy Payoff

I have not measured time saved yet. A fair test is to time a manual triage of the same exported messages, then time review of the generated queue, counting corrections. I will add those numbers after a successful real model run.

## Prize Categories

This project is entered for the overall Hacktoberfest Open-Source AI Challenge Week 3 prize.

It is not currently claiming a partner category. The code supports Ollama models locally, but a partner category should be listed only after that partner technology is used successfully in the working demo. For example, the Gemma category would require a verified run with Gemma.

## Before Publishing

- Run Ollama successfully on the four fictional sample messages and record the actual decisions, drafts, and elapsed time.
- Publish the code in a public repository and add its URL above.
- Host a screenshot or short video and add its URL above.
- If entering a partner category, use that technology in the working build and describe its role accurately. Do not claim the Gemma category until a real Gemma run succeeds.
- Use the challenge tags `#devchallenge` and `#hf26challenge` when publishing on DEV.
