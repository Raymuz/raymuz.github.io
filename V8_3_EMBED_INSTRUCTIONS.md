# V8.3 — Embedded Customer Churn and project navigation

- The main navigation label reads **Projects, AI Agents, & Models**.
- The featured Customer Churn section on the homepage has a collapsed **Try Customer Churn model on this website** interactive area.
- The full Customer Churn case-study page also includes an interactive embed.
- The embed uses a public Hugging Face Space metadata check and only inserts the iframe when the Space reports Public + RUNNING. An error, unknown status or private Space shows an explanatory fallback with retry.
- Public endpoint assumed: `https://raymuz-customer-churn-intelligence-lab.hf.space/ui/`. Confirm it responds after Space launch and that the Space allows iframe embedding.
- **Required before external visitors can use it:** set the Hugging Face Space visibility to Public, ensure Docker is running and `/ui/` works. Do not expose secrets or private customer data.
- The existing project catalogue, project/article pages, photos, Relevance AI notes, and GitHub workflows are preserved.
- No external authenticated deployment or live user-facing model testing was performed.
