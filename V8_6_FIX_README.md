# V8.6 GoogleSaada source fix

The older project page was retained at `projects/googlesaada/index.html` while the updated iframe version existed only in `dist/projects/googlesaada/index.html`. GitHub Actions regenerates dist from source every time. This archive synchronizes both pages and rebuilds dist.

Use the *full website* publishing workflow of your existing Colab publisher. Verify `.github/workflows/publish.yml` succeeds, then open https://raymuz.github.io/projects/googlesaada/. Public HF application must be running and frame-embeddable.
