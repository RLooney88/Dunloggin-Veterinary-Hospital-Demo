# CHECKPOINT-2026-06-06

## Project / Objective
Dunloggin Veterinary Hospital website demo: finish publishing the practice-specific veterinary demo site created from `Veterinary-Site-Template`, with the live placeholder URL `https://dvh.rclintegrated.com` smoke-tested and returning the Dunloggin content. This checkpoint is for the website project **Dunloggin Veterinary Hospital Demo**.

## Current Status (done vs in progress)
**Done**
- Practice-specific repo created: `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo`.
- GitHub repo created and pushed: `https://github.com/RLooney88/Dunloggin-Veterinary-Hospital-Demo`.
- Workbook created: `C:\Users\Roddy\.openclaw\workspace-nova\workbook\dunloggin-veterinary-hospital\SITE-WORKBOOK.md`.
- Refined scrape/config artifacts created for Dunloggin Veterinary Hospital.
- Local seed validation passed.
- Local frontend production build passed with only a pre-existing React hook warning in `src/hooks/useSurface.js`.
- Railway project created: `Dunloggin-Vet-Demo` / `db5513d2-4727-411f-a4cd-e5d6a154da8f`.
- Railway web service created: `Dunloggin-Veterinary-Hospital-Demo` / `bb704cbc-4b86-4503-bf3c-d598b21c1530`.
- Railway production environment id: `0bc44a43-960b-40eb-b97b-3b1db35d2f3c`.
- Cloudflare DNS record created for `dvh.rclintegrated.com` pointing to Railway target `f6l3slwb.up.railway.app`, proxied false.
- Railway custom domain showed DNS propagated for `dvh.rclintegrated.com`.
- Railway service-generated domain created: `dunloggin-veterinary-hospital-demo-production.up.railway.app`.
- Railway service config was updated to use Dockerfile path via current schema: `builder=RAILPACK`, `dockerfilePath=Dockerfile`, `railwayConfigFile=railway.json`.
- Git commit pushed: `711ffcc Allow SQLite fallback for demo deployments`.
- Required Railway env vars were set on the web service:
  - `JWT_SECRET` generated in Railway.
  - `ADMIN_EMAIL=admin@dvh.rclintegrated.com`.
  - `ADMIN_PASSWORD` generated; local sensitive copy is `C:\Users\Roddy\.openclaw\workspace-nova\tmp\dunloggin-admin-password.txt`.
  - `CORS_ORIGINS=*`.
  - `PUBLIC_SITE_URL=https://dvh.rclintegrated.com`.
  - `SEED_REFRESH_CONTENT=true`.
  - `EDIT_REQUEST_ENABLED=false`.
- Railway deploy `786b6134-7c4a-4573-99d3-39cfc1e96a1a` reached `SUCCESS` after env vars were set.

**In Progress**
- Publication is **not complete** because live smoke tests are still failing.
- Current live behavior:
  - `https://dvh.rclintegrated.com/` was returning Railway fallback / `Application not found` during tests.
  - `https://dunloggin-veterinary-hospital-demo-production.up.railway.app/` reached Railway service routing but returned `502 Application failed to respond`.
- Current suspected runtime blocker: SQLite fallback is active, but `backend/models.py` still imports and uses Postgres-specific `JSONB` and `UUID`, causing SQLite DDL compile errors during startup.
- Domain target port likely still needs correction: service-generated domain was created with `targetPort=8000`, while Railway runtime log showed Uvicorn on `0.0.0.0:8080`.

## Completed Work (key outputs + file paths)
- Website repo — `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo`
- GitHub repo — `https://github.com/RLooney88/Dunloggin-Veterinary-Hospital-Demo`
- Latest pushed commit — `711ffcc Allow SQLite fallback for demo deployments`
- Main config — `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo\site.config.json`
- Frontend config — `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo\frontend\src\site\site.config.json`
- Backend Dockerfile — `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo\Dockerfile`
- SQLite fallback patch location — `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo\backend\database.py`
- Current model blocker location — `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo\backend\models.py`
- Workbook — `C:\Users\Roddy\.openclaw\workspace-nova\workbook\dunloggin-veterinary-hospital\SITE-WORKBOOK.md`
- Refined profile JSON — `C:\Users\Roddy\.openclaw\workspace-nova\workbook\dunloggin-veterinary-hospital\practice-profile.refined.json`
- Railway debug/status helper — `C:\Users\Roddy\.openclaw\workspace-nova\tmp\railway_debug_dunloggin.py`
- Railway deploy status helper — `C:\Users\Roddy\.openclaw\workspace-nova\tmp\railway_deploy_status_dunloggin.py`
- Railway env-var helper — `C:\Users\Roddy\.openclaw\workspace-nova\tmp\railway_set_vars_redeploy_dunloggin.py`
- Generated admin password local copy, sensitive — `C:\Users\Roddy\.openclaw\workspace-nova\tmp\dunloggin-admin-password.txt`

## Blockers / Failures (what failed, why, what was tried)
1. **Initial publish stopped too early**
   - What failed:
     - The first response reported local build/config completion, but the site was not published/live.
   - Why:
     - The vet-template onboarding playbook requires commit, push, Railway deploy, custom domain, DNS, and smoke tests unless user says local-only.
   - What was tried:
     - Resumed publish flow after Roddy corrected expectation: “Does the playbook not say publish it?”

2. **Railway deploy crashed from missing `DATABASE_URL`**
   - What failed:
     - App import crashed on `os.environ["DATABASE_URL"]` in `backend/database.py`.
   - Why:
     - Railway Postgres was not successfully provisioned/wired through the available API path; CLI rejected the account token for project mutation.
   - What was tried:
     - Attempted Railway CLI `railway add --database postgres`, but CLI returned unauthorized/invalid token for that path.
     - Patched `backend/database.py` to use Postgres when `DATABASE_URL` exists and fallback to SQLite at `/tmp/vet-demo.sqlite3` for demo deployments.
     - Added `aiosqlite==0.21.0` to `backend/requirements.txt`.
     - Committed and pushed fix as `711ffcc`.

3. **GitHub push required non-interactive token path**
   - What failed:
     - `git push` failed because shell could not prompt: `fatal: could not read Username for 'https://github.com'`.
     - `gh auth status` showed stale/invalid GitHub CLI auth.
   - Why:
     - GitHub CLI token was invalid and interactive prompts are unavailable in this runtime.
   - What was tried:
     - Located indexed GitHub token metadata in secret index.
     - Used stored classic PAT at `C:\Users\Roddy\.openclaw\workspace\secrets\roddy\github-token.json` through a temporary askpass helper without printing token value.

4. **Railway did not auto-deploy after push**
   - What failed:
     - Pushed commit `711ffcc` did not automatically create a new Railway deployment.
   - Why:
     - Existing Railway source/deploy trigger did not fire for the manual source-created service.
   - What was tried:
     - Triggered deployment via GraphQL `serviceInstanceDeployV2`.
     - `githubRepoDeploy` returned a generic Railway API error.

5. **Railway builder/config mismatch**
   - What failed:
     - A manual deploy initially used `RAILPACK` and became stuck/building.
   - Why:
     - Current Railway schema no longer exposes old `DOCKERFILE` builder enum; builder enum values were `HEROKU`, `NIXPACKS`, `PAKETO`, `RAILPACK`.
   - What was tried:
     - Introspected `ServiceInstanceUpdateInput` and `Builder` enum.
     - Updated service instance using `builder=RAILPACK`, `dockerfilePath=Dockerfile`, `railwayConfigFile=railway.json`.
     - Cancelled stuck deployment and redeployed. Later deploys showed `builder=DOCKERFILE` in manifest and reached `SUCCESS`.

6. **Railway deploy crashed from missing auth env vars**
   - What failed:
     - Runtime crashed on `JWT_SECRET = os.environ["JWT_SECRET"]` in `backend/auth.py`.
   - Why:
     - Required env vars were missing from the web service.
   - What was tried:
     - Set `JWT_SECRET`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `CORS_ORIGINS`, `PUBLIC_SITE_URL`, `SEED_REFRESH_CONTENT`, `EDIT_REQUEST_ENABLED` with `variableCollectionUpsert`.
     - Redeployed; deploy reached `SUCCESS`.

7. **SQLite fallback incompatible with Postgres-specific model types**
   - What failed:
     - Runtime logs showed SQLAlchemy compile error: SQLite compiler cannot render `JSONB` in table `visitor_sessions`, column `intent_scores`.
   - Why:
     - `backend/models.py` imports `JSONB, UUID` from `sqlalchemy.dialects.postgresql` and uses them throughout models. SQLite fallback cannot render `JSONB` and may also have trouble with Postgres UUID type.
   - What was tried:
     - Confirmed all `JSONB`/`UUID` occurrences in `backend/models.py` with `Select-String`.
   - Still needed:
     - Patch models to use portable SQLAlchemy `JSON` and compatible string UUID columns for SQLite/demo mode, or provision real Postgres and set `DATABASE_URL`.

8. **Domain/service routing and target port mismatch**
   - What failed:
     - `dvh.rclintegrated.com` returned Railway fallback `404 Application not found`.
     - Service domain returned `502 Application failed to respond`.
   - Why:
     - Custom domain was attached/provisioned but app routing was not yet healthy; service domain was created with `targetPort=8000`, while logs showed Uvicorn running on `0.0.0.0:8080`.
   - What was tried:
     - Created service domain `dunloggin-veterinary-hospital-demo-production.up.railway.app` with id `f47e5120-5c07-437f-9b4b-ba1aedec3bac`.
     - Attempted one inline PowerShell/Python GraphQL update for target ports, but the shell mangled `$` in GraphQL and produced syntax errors. Use a `.py` script file for future GraphQL calls, not inline command strings.

## Next Actions (ordered, executable steps)
1. Patch `backend/models.py` for SQLite/demo compatibility:
   - Replace or alias `JSONB` to portable `JSON` when SQLite fallback is active.
   - Replace or alias Postgres `UUID(as_uuid=False)` to a portable `String(36)` UUID column when SQLite fallback is active.
   - Keep Postgres behavior intact when `DATABASE_URL` points to Postgres.
2. Validate locally:
   - `python backend\validate_seed.py`
   - From repo root, run the backend startup with no `DATABASE_URL` and required local env vars to verify SQLite tables can create and seed.
   - If available, run frontend build or at least confirm no config regression.
3. Commit and push the model compatibility fix:
   - `git status --short`
   - `git add backend\models.py` plus any required supporting file.
   - `git commit -m "Make demo SQLite fallback compatible with model types"`
   - Push with stored GitHub token helper if normal `git push` fails.
4. Trigger Railway deploy via GraphQL `serviceInstanceDeployV2` for the new commit SHA.
5. Poll Railway deploy status with `C:\Users\Roddy\.openclaw\workspace-nova\tmp\railway_deploy_status_dunloggin.py` until latest deploy is terminal `SUCCESS` or failed.
6. Pull fresh runtime logs with `C:\Users\Roddy\.openclaw\workspace-nova\tmp\railway_debug_dunloggin.py`; verify no startup tracebacks and that Uvicorn is running.
7. Update Railway service/custom domain target ports using a Python script file, not inline shell, if routes still fail:
   - Custom domain id observed earlier: `b6b3d6ba-8aa5-4bf0-84df-4a64bf744298` for `dvh.rclintegrated.com`.
   - A later inline attempt referenced `370c9016-8616-464d-b59d-cb451f7fb535`, but that id is uncertain because the command failed before useful output. Re-query domains first and use the authoritative id from Railway.
   - Service domain id: `f47e5120-5c07-437f-9b4b-ba1aedec3bac`.
   - Target port should likely be `8080` if Railway continues running Uvicorn on `$PORT=8080`; verify from logs.
8. Re-query Railway domains and Cloudflare DNS:
   - Confirm Railway required DNS value for `dvh.rclintegrated.com`.
   - Confirm Cloudflare CNAME still matches Railway required value and remains unproxied.
9. Run live smoke tests and do not report complete until they pass:
   - `curl.exe -I https://dvh.rclintegrated.com/ --max-time 30`
   - `curl.exe -sS https://dvh.rclintegrated.com/api/health --max-time 30`
   - `curl.exe -sS https://dvh.rclintegrated.com/api/surfaces/home_hero/content --max-time 30`
   - `curl.exe -sS https://dvh.rclintegrated.com/api/surfaces/inline_cta/content --max-time 30`
   - Verify returned content is Dunloggin-specific and status is 200.
10. After publish succeeds, update workbook/publish status and clean non-sensitive scratch scripts if no longer useful. Keep or securely handle `dunloggin-admin-password.txt` according to Roddy’s preference.

## Restart Instructions (what to read/run first after reset)
1. Read: `C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo\CHECKPOINT-2026-06-06.md`
2. Run: `cd C:\Users\Roddy\.openclaw\workspace\repos\Dunloggin-Veterinary-Hospital-Demo; git status --short; git log --oneline -5`
3. Verify: `Select-String -Path backend\models.py -Pattern "JSONB|UUID"` still shows the unpatched Postgres-specific model types before applying the next fix.
4. Then continue at “Next Actions” step 1: patch `backend/models.py` for SQLite/demo compatibility, or alternatively provision Railway Postgres and set a real `DATABASE_URL` if that path is preferred.
