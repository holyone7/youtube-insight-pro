# YouTube Insight Pro (Streamlit Demo)
This repository is a deployable Streamlit app that collects YouTube channel data, shows analytics, and generates a PDF report.

## Features
- YouTube Data API v3 integration
- Streamlit UI for channel input and visualization
- PDF report generation with `fpdf`
- Stripe checkout helper (uses environment variables; simulated URL when no key present)

## Local setup
1. Create a Python environment (recommended: venv)
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file (optional) with the following keys:
    - YOUTUBE_API_KEY=your_key
    - STRIPE_SECRET_KEY=sk_test_...
    - STRIPE_PUBLISHABLE_KEY=pk_test_...
    - SUCCESS_URL=https://your-domain.com/success
    - CANCEL_URL=https://your-domain.com/cancel
4. Run locally: `streamlit run app.py`

## Deploy to Streamlit Cloud
1. Push this repo to GitHub.
2. On Streamlit Cloud, create a new app pointing to this repo and set secret environment variables via the app settings.
3. Ensure `YOUTUBE_API_KEY` and `STRIPE_SECRET_KEY` are configured in Secrets.

## Notes & Next steps
- Add webhooks to handle Stripe checkout.succeeded events and trigger PDF generation + email delivery.
- Add user accounts / subscription model for recurring reports.
- Improve report aesthetics with ReportLab or HTML-to-PDF rendering.
