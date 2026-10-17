# V6 — Repository architecture and automatic application registration

## Where files go

- `raymuz.github.io`: the personal homepage, articles, and automatically generated project pages. Do **not** push model Python code into this repository.
- `churn-intelligence-lab-site`: your existing standalone Churn marketing site, optional to retain or redirect.
- `churn-intelligence-lab`: the model training notebook, Docker application, evaluation, and a `portfolio.json` registration file.
- Hugging Face Space: your actual app backend and frontend, e.g. `raymuz/Customer_Churn_Intelligence_Lab`.

## Automatic discovery, no cross-repo PAT required

1. Deploy the app successfully to an **accessible public Hugging Face Space**. Private apps are deliberately not embedded.
2. In its **public GitHub code repository** add `portfolio.json` at the root, modeled on `templates/portfolio.json`. Match `slug` to an existing portfolio project or choose a safe new slug.
3. The portfolio's daily scheduled GitHub Action (or `Actions → Build and deploy ... → Run workflow`) scans only public repositories owned by `raymuz` and only those that explicitly opt in via `portfolio.json`.
4. It checks public Space metadata for RUNNING and verifies the app root URL responds with HTTP 200. Then it creates or updates the project page, preserving your custom Churn HTML page, and rebuilds the catalogue.
5. Changes to a summary in `portfolio.json` are reflected after the next successful scan. Missing, private, or failed Spaces are skipped, and existing links stay until edited/reviewed (not automatically deleted).

### Note on embedding

The live Hugging Face frontend is embedded using its public `.hf.space` hostname, when that host allows iframes. GitHub Pages does not host or proxy the model backend, and this mechanism never exposes private tokens. An iframe can still fail due to browser/service policies: the **Open live app** link remains available.

### Private applications

Keep NTM and other restricted agents private. Do not store backend credentials in the portfolio. Publish a restricted-access or description-only project page instead. Access to a private Space cannot be granted through a public iframe.

### Deployment-triggered immediate updates (optional)

Existing `repository_dispatch` receives event `portfolio_project_deployed`. For the Churn project the incoming client_payload must contain `slug`, `repo`, `live`, `embed`. The source repository is allowlisted in `scripts/update_deployment.py`, but this event **also requires a one-time safely stored cross-repository token** with permission to dispatch to the portfolio repository. Run that event **only after** the Hugging Face deployment is healthy and public, and verify the intended URLs. Other repos can be allowlisted explicitly after review. Do not reuse unrestricted personal access tokens. The scheduled scan provides a simpler no-PAT alternative.

### Articles

Add or update `articles/<slug>/index.html` in the portfolio repository. GitHub Actions indexes it on each commit; ResearchGate does not automatically synchronize papers with this workflow.

### First deployment

Use your existing fixed Colab website publisher, but upload **this V6 ZIP**. The built-in GitHub Actions workflow will then be published to the portfolio repository. To trigger public app scanning manually after publishing, open portfolio repository **Actions → Build and deploy → Run workflow**.
