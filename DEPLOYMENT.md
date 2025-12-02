# Deployment options & steps — Desafio Positivo

This doc explains recommended deployment options and step-by-step instructions for deploying the `backend` to Render (recommended), Railway and Heroku. It also includes the GitHub Actions workflow that can trigger a Render deploy.

Overview — recommended order
- Render (recommended): Fast to go from GitHub to production using Docker, supports managed Postgres, and you can use `render.yaml` to declare infrastructure-as-code. Best balance for production-readiness and low ops.
- Railway: Quick prototyping. Great for demos and rapid iteration.
- Heroku: Known, easy to use, still works well. Many tools assume Heroku-style workflows.

1) Render — step-by-step (practical for production)

- In the Render dashboard create a new account (or signin) and choose **Create a new service** → **Import from GitHub**.
- During import, Render will detect `render.yaml` and create the web service + postgres based on the manifest. If it does not detect automatically, create the services manually and connect to the same repo + branch.
- Add the secret `DJANGO_SECRET_KEY` in Render's dashboard (Service → Environment → Secrets/Environment) and set it to a secure value.
- If you prefer to trigger deploys manually via GitHub Actions, set two repo secrets in GitHub:
  - `RENDER_API_KEY` — create an API key in Render account settings and paste here.
  - `RENDER_SERVICE_ID` — service id (from Render dashboard) for your web service.
- We provide `.github/workflows/deploy_to_render.yml` that will trigger a new Render deploy using the API when pushing to `main`. If you prefer, enable automatic deploys directly in Render when connecting GitHub.

Notes: The manifest `render.yaml` at the repo root describes two Render resources (web + Postgres) to make imports reproducible.

2) Railway — step-by-step (good for prototyping)

- Create a Railway account and link GitHub repo. Railway will detect the repo and allow you to set up a Postgres plugin.
- Configure environment variables in Railway (DATABASE_URL, DJANGO_SECRET_KEY, DJANGO_DEBUG, etc.)
- Railway can run migrations as part of the deploy or using one-off tasks.

3) Heroku — step-by-step (very known, still useful)

- Create a Heroku app and connect GitHub repo or push Docker image
- Add a Heroku Postgres add-on and configure `DATABASE_URL` environment variable.
- Add `DJANGO_SECRET_KEY` and other env vars on Heroku dashboard.

---

If you'd like I can proceed to:
- Create the Render services for you using the Render API (requires your Render API key and confirmation), or
- Configure GitHub Actions to also push container images to a registry and route a Render/Railway/Heroku deploy from there.

### Automated helper scripts

There are helper scripts in `scripts/` to assist you when working with the Render API locally:

- `scripts/render_list_services.sh` — lists services available in your Render account, helps you find the `service id`.
- `scripts/render_trigger_deploy.sh` — triggers a new deploy for a service using `RENDER_API_KEY` and `RENDER_SERVICE_ID` environment variables.

Usage example:

```bash
export RENDER_API_KEY=your_key_here
./scripts/render_list_services.sh
# find service id
export RENDER_SERVICE_ID=svc_xxx
./scripts/render_trigger_deploy.sh
```

Both scripts return JSON responses (they use `jq` for pretty output — install jq locally) and are meant to make manual testing/debugging easier.

### Create Render services automatically (script)

If you want me to automatically create the Postgres + Web service using the Render API, there's a local helper script you can run that will create a Postgres instance and a Git-backed web service connected to your repo and branch.

Run locally (Bash / WSL / Git Bash):

```bash
export RENDER_API_KEY=your_key_here
export GITHUB_REPO=https://github.com/<owner>/<repo>
# optional: BRANCH (defaults to main), WORKSPACE_NAME, REGION
./scripts/render_create_services.sh
```

The script will:
- choose your first workspace (or the one matching WORKSPACE_NAME) as the owner
- create a new Postgres instance
- create a new web service pointing to `$GITHUB_REPO` and `$BRANCH`, using `backend/Dockerfile`
- set basic DB env vars on the created service

### Manual GitHub Action to create services (secure)

If you prefer to run the creation from GitHub (so the API key never touches your local machine), you can set the secret `RENDER_API_KEY` on GitHub and use the manual workflow `Create Render services (manual)` in Actions.

Steps:

1. In your repo, go to Settings → Secrets → Actions and add `RENDER_API_KEY` with a Render API key you created in your Render Account Settings.
2. Open the repository Actions tab, find the `Create Render services (manual)` workflow and click Run workflow.
3. Provide `github_repo` (for this repository), optional `branch` and `workspace_name` and trigger the run.

The workflow will execute `scripts/render_create_services.sh` on GitHub Actions using the secret and will write the created service id(s) to the job logs. After a successful run, copy the web service id and set `RENDER_SERVICE_ID` as another secret (for the deploy workflows).


Notes & security:
- The script requires a valid `RENDER_API_KEY` and will echo responses from the Render API locally — do not paste your API key into public chat or commit it anywhere.
- If you prefer, run these same API requests manually in your own terminal or use the Render dashboard to import `render.yaml`.


### Build & Deploy workflow (image -> Render)

I added a GitHub Actions workflow `.github/workflows/build_and_deploy_render.yml` that:

1. Builds a Docker image from `backend/` and pushes it to GitHub Container Registry (GHCR) as `ghcr.io/<owner>/desafio-positivo-backend:<sha>`.
2. Calls Render API to create a new deploy for the configured `RENDER_SERVICE_ID`.

Before this workflow works, add these GitHub Secrets:

- `RENDER_API_KEY` — create this in Render Account Settings (API Keys). Do not commit it to source control.
- `RENDER_SERVICE_ID` — the target web service id in Render (found in dashboard or via `render_list_services.sh`).

Note: GHCR reuse — this workflow uses the repository `GITHUB_TOKEN` to authenticate with GHCR; if your org requires a PAT, replace `secrets.GITHUB_TOKEN` with a PAT stored in `secrets.GHCR_PAT`.

### Preview environments (pull requests)

This repository now supports PR preview deployments using GitHub Actions and Render's API. The flow is:

1. On a pull request, the `preview_deploy_render.yml` workflow builds a Docker image for the `backend/` and pushes it to GHCR with a tag tied to the PR number and commit SHA.
2. The workflow calls the Render API and requests a deploy using the pushed image for a preview environment. Render will create or reuse previews associated with the target service.

Required GitHub Secrets for previews:
- `RENDER_API_KEY` — Render API key
- `RENDER_SERVICE_ID` — Service ID of the Render web service which will receive the preview deploy (this can be a service configured to accept preview images)

Notes:
- Preview deploys are intended for short-lived PR previews. Be careful with the number of preview deploys on free plans.
- You can add other metadata (PR URL, author) to the metadata JSON sent to Render to make dashboards easier to navigate.


