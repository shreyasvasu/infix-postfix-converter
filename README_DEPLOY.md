Run locally with Docker:

```bash
docker build -t postfix-studio:local .
docker run -p 5000:5000 postfix-studio:local
```

Deploy using GitHub Actions: push to `main` and the workflow will build and publish the image to GHCR as `ghcr.io/<owner>/<repo>:latest`.
