# BridgeNote Lab

BridgeNote Lab is a separate PulseArk pilot companion, derived from the BridgeNote workflow without altering the original BridgeNote AI app or repository.

It helps a music-outreach team:

- adapt a demo music session with the existing routine and safety-oriented prompt;
- record de-identified observations using simple, descriptive scales;
- document an inquiry cycle: question, hypothesis, adjustment, reflection;
- view descriptive program signals without making clinical claims; and
- generate a factual evidence-portfolio summary for project reflection.

## Privacy and scope

This prototype is not a medical, therapeutic, diagnostic, or clinical decision tool. Enter no names, medical records, recordings, contact details, or other identifying information. Use only within an approved consent and safeguarding process.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app writes local pilot records to `data/lab_observations.json` and `data/lab_inquiries.json`. Those files are ignored by Git and must not be committed.

