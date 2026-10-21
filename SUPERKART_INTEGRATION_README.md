# SuperKart — Main Portfolio Integration

Page: `projects/superkart-sales-forecasting/index.html`
Hugging Face Space: https://huggingface.co/spaces/raymuz/SUPERKART_SALES_FORECASTING
Current status: Space created; Gradio application not independently verified live.

## Publishing
Use existing binary-safe portfolio publisher and this entire ZIP as full website release. The page and menu entry live in the root source; GitHub Actions rebuilds `dist/`.

## App deployment (separate action)
In Hugging Face Space Files, upload `app.py`, `requirements.txt`, and a properly configured `README.md` SDK header from the previously created SuperKart Gradio application package. Confirm Space `Running` and test it on Hugging Face before assessing the iframe.

## Warning
The prototype uses demonstration forecasting logic and is not yet a trained validated XGBoost predictor.
