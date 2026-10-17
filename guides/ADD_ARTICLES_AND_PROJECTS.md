# Automatic article and project updates — Dr. Adamou Musa portfolio

## Already automated
The existing `.github/workflows/publish.yml` workflow runs after each commit to `main`. It executes `scripts/build_portfolio.py`, which discovers `articles/<slug>/index.html` and `projects/<slug>/index.html`, generates `articles.json` and `projects.json`, then publishes the built site using GitHub Pages.

You do not upload the entire website ZIP for each new article or project.

## New article (GitHub web UI)
1. Open https://github.com/Raymuz/raymuz.github.io and click Add file > Create new file.
2. Set the filename to `articles/my-new-article/index.html` (lowercase, numbers, hyphens; use a unique slug).
3. Copy `NEW_ARTICLE_TEMPLATE.html` from the repository and replace TITLE, `portfolio:description`, `portfolio:date`, article summary, and relevant reading link.
4. Commit directly to `main` or open a pull request, review, and merge it.
5. Wait for the Actions workflow `Build and deploy Dr. Adamou Musa portfolio` to succeed, then visit https://raymuz.github.io/#articles .

For an article already on ResearchGate, include a normal `https://www.researchgate.net/...` link in the body; upload full text only if you have the rights to do so. Use accurate publication metadata.

## New project (GitHub web UI)
1. Add a new file named `projects/my-new-model/index.html` using `NEW_PROJECT_TEMPLATE.html`.
2. Set `portfolio:title`, `portfolio:description`, `portfolio:category`, `portfolio:status`, and `portfolio:tags`.
3. Set `portfolio:repo` to the public GitHub repository URL, `portfolio:live` to the live model URL, and `portfolio:embed` to the public `https://YOUR-APP.hf.space` embed URL when available. Leave unavailable links blank.
4. Commit to `main`, wait for green Actions check, and visit https://raymuz.github.io/#projects .

## Update an existing entry
Edit `articles/<slug>/index.html` or `projects/<slug>/index.html` on GitHub and commit. The same workflow republishes the updated catalogue. This is the simplest reliable workflow for changing a project summary or its links.

## Updates triggered by another repository
The portfolio also includes `scripts/update_deployment.py` and a `repository_dispatch` handler. This is not automatic merely from uploading to Hugging Face; each application repository must be configured once to send a validated deployment notification with credentials and allowed repository identity. Do not add secrets to a public web page. Follow README instructions, test on one project, and then enable for other applications.

## If the new entry does not appear
Verify correct path and filename (`articles/<slug>/index.html` or `projects/<slug>/index.html`), lowercase slug, valid UTF-8, commit on `main`, and GitHub Actions green status. A browser hard-refresh may help after successful deployment.
