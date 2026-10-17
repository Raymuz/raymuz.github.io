# Dr. Adamou Musa — AI / Cybersecurity Portfolio

A **single, free GitHub Pages website** with automatically discovered project pages and embedded demonstrations for separately hosted AI/ML apps.

## Publish (one-time)

1. At GitHub, create the public repository **`raymuz.github.io`**. This is separate from `churn-intelligence-lab-site`; do not delete the current working site.
2. Extract the website ZIP and upload the **contents of the `Dr_Adamou_Musa_Portfolio` folder**, keeping `index.html`, `assets/`, `projects/`, `scripts/`, `tests/` and `.github/workflows/publish.yml` in place. For GitHub's browser upload, hidden `.github` folders can be awkward to upload; the simplest reliable option is `git clone`, copying the extracted contents including hidden files, then `git add . && git commit ... && git push`. Alternatively upload a few folders in batches and create `.github/workflows/publish.yml` using GitHub's **Add file → Create new file**. Do not upload the ZIP as a single file.
3. Under repository **Settings → Pages → Build and deployment**, choose **GitHub Actions** (not “Deploy from a branch” for THIS NEW portfolio repository).
4. Go to **Actions → Build and deploy Dr. Adamou Musa portfolio** to verify green build/deployment jobs. Your website will be `https://raymuz.github.io/`.
5. The existing Churn GitHub Pages website can stay available. It also has a copy in `projects/churn-intelligence-lab/`.

## Adding a new project automatically

Create `projects/my-new-model/index.html` and commit to `main`. The workflow runs `scripts/build_portfolio.py`; it discovers ALL `projects/*/index.html` files and generates the catalogue automatically. You do NOT modify the homepage. The new card will appear after a successful GitHub Actions deployment.

To have a useful title and category, place these tags inside the new project's `<head>`:

```html
<meta name="portfolio:title" content="My New Model">
<meta name="portfolio:description" content="Short, accurate public description of the project.">
<meta name="portfolio:category" content="Machine Learning">
<meta name="portfolio:status" content="In development">
<meta name="portfolio:tags" content="Python, XGBoost, Docker">
<meta name="portfolio:repo" content="">
<meta name="portfolio:live" content="">
<meta name="portfolio:embed" content="">
```

If these are omitted, the generator uses a readable folder name and `Other Projects` category.

## Embedding a *working* machine-learning application

**GitHub Pages cannot execute Python models**. Train/deploy your app separately in Hugging Face Spaces or a supported API host. Once your Hugging Face Space actually runs and has a public embed URL, edit that project's `<head>`:

```html
<meta name="portfolio:repo" content="https://github.com/raymuz/my-new-model">
<meta name="portfolio:live" content="https://huggingface.co/spaces/ACCOUNT/SPACE">
<meta name="portfolio:embed" content="https://ACCOUNT-SPACE.hf.space">
```

These are **examples, not functioning user URLs**. Copy the real embed address from the Space's menu; some subdomain patterns differ. `portfolio:embed` accepts only HTTPS `*.hf.space` addresses to reduce accidental unsafe iframes. The shared `assets/project.js` uses the metadata to show a live iframe and buttons. The automatic registry uses `portfolio:live` to add a "Use live app" action on the homepage. **Do not paste API keys, tokens, service secrets or private customer data into public HTML.** A protected/authenticated Space may restrict access; a private one cannot be embedded publicly.

### Important: special case for Churn Intelligence Lab

The previously published Churn HTML is preserved in `projects/churn-intelligence-lab/index.html` with its original design. After deploying the Python app, update only the three `portfolio:repo`, `portfolio:live`, `portfolio:embed` `<meta>` tags near the top of that page. The Churn page now reads those metadata fields automatically; no second JavaScript edit is needed. Then its embedded app and the homepage live/demo actions will appear. The initial bundle intentionally leaves all live URLs blank until verified.

## Hosting and account permissions

- This portfolio is entirely public static HTML, CSS and JS; GitHub Pages is free for public repositories within normal usage limits.
- GitHub Actions for the *website* uses GitHub's built-in workflow token. You don't need to create a new personal access token to publish this site manually; token setup from Colab is only needed for separate app repositories/Spaces.
- Public interactive inference services may have resource limits and can sleep or incur charges depending on host and workload.
- Never host a production app with private customer, financial or health data on an open public demo. For restricted NTM applications, publish a sanitized read-only demo or link to its authenticated site.

## Local preview and tests

From the extracted folder:

```bash
python -m unittest discover -s tests -v
python scripts/build_portfolio.py --out dist
cd dist && python -m http.server 8000
```

Visit http://localhost:8000. The static home loads `projects.json`, which the build script creates. Double-clicking the original `index.html` file will not load the catalogue reliably due to browser file security.

## CV and privacy

The public pages are summarized from the supplied CV. The raw CV is **not** included, nor are its private phone number, personal email or clearance information. Project listings reflect descriptions in the CV and **do not imply all projects have working deployments**. Review status labels and wording before publishing.

## V2: Portrait, social profiles, articles, and automatic external deployment updates

- The profile picture is `assets/profile-photo.png`.
- LinkedIn, Facebook and Handshake links appear under **Contact**.
- Add articles at `articles/<slug>/index.html` using `NEW_ARTICLE_TEMPLATE.html`. Their metadata automatically appears on the homepage after a successful Pages build.
- External app deployments can notify the portfolio through the GitHub `repository_dispatch` event type `portfolio_project_deployed`.
- For security, first approve each app repository in `scripts/update_deployment.py` in `ALLOWED`, for example `"churn-intelligence-lab":"raymuz/churn-intelligence-lab"`. The action rejects unapproved projects.
- In each application repository, store a fine-grained token as the secret `PORTFOLIO_DISPATCH_TOKEN` scoped to the `raymuz.github.io` repository (Contents read/write permission). Send a POST to `https://api.github.com/repos/raymuz/raymuz.github.io/dispatches` with `event_type` `portfolio_project_deployed` and `client_payload` containing `slug`, `repo`, `live`, and `embed`. Only trigger this *after* the app deployment is confirmed successful; GitHub alone cannot verify Hugging Face readiness.
- A notification can update only a known portfolio project and an allowlisted GitHub repo. It does not deploy, authenticate, or expose a private backend. Verify `Actions` is green before assuming the page updated.
- Articles uploaded elsewhere are **not** discovered automatically; to add them, publish a corresponding article HTML or metadata file in this repository.

### Public model and competition profiles
- Hugging Face: https://huggingface.co/raymuz
- Kaggle: https://www.kaggle.com/raymuz


## V6 automatic app discovery
Read [automatic project integration](guides/AUTO_DEPLOY_INTEGRATION.md). Opt-in template: `templates/portfolio.json`.
