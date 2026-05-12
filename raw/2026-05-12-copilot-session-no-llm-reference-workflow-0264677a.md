---
title: "Copilot Session Checkpoint: No-LLM Reference Workflow"
type: text
captured: 2026-05-12T19:44:50.731189Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, mempalace, agents]
checkpoint_class: durable-workflow
checkpoint_class_rule: "title:workflow"
retention_mode: retain
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** No-LLM Reference Workflow
**Session ID:** `85ff364b-9e65-41e4-9a65-bcf9f7d72341`
**Checkpoint file:** `/home/jbl/.copilot/session-state/85ff364b-9e65-41e4-9a65-bcf9f7d72341/checkpoints/001-no-llm-reference-workflow.md`
**Checkpoint timestamp:** 2026-05-12T19:43:02.822641Z
**Exported:** 2026-05-12T19:44:50.731189Z
**Checkpoint class:** `durable-workflow` (rule: `title:workflow`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user asked to fully implement `Spatial-Design-Studio/plans/no-llm-reference-asset-production-plan.md`, using a branch/commit/push/PR/merge cycle after each phase, then deploy to the homelab and validate. The implementation followed the written no-LLM plan: deterministic OpenCV/Pillow/Tesseract/QR reference processing, review-first calibration/acceptance, editable 2D/3D objects, product candidates, and an internal homelab worker with no cloud/LLM runtime path.
</overview>

<history>
1. User requested plan implementation, phased GitHub PRs/merges, homelab deploy, and validation.
   - Loaded required skills: `task-observer`, `executing-plans`, `subagent-driven-development`, `using-git-worktrees`, `homelab-deploy`.
   - Loaded MemPalace context and inspected plan/repo/homelab state.
   - Created SQL todos for Stage 0 through Stage 7 plus final deploy.

2. Stage 0: UI/docs no-AI copy.
   - Created worktree/branch `no-llm-reference-stage-0`.
   - Added `apps/web/app/__tests__/reference-language.test.ts`.
   - Updated user-facing copy from AI-first language to reference-first language in `AiJobsPanel.tsx` and `studio-shell.tsx`.
   - Validated web test/typecheck.
   - Opened and merged PR #3: “Clarify deterministic reference workflow”.

3. Stage 1: deterministic reference job wiring.
   - Branch `no-llm-reference-stage-1`.
   - Added Spatial reference settings to API config.
   - Added `ReferenceMode`.
   - Updated `/spaces/{space_id}/assets` to accept `reference_mode` and queue local `reference-analysis` jobs with cloud/LLM flags hard false.
   - Added `apps/api/tests/test_reference_workflow.py`.
   - Validated API tests.
   - Opened and merged PR #4: “Add deterministic reference job wiring”.

4. Stage 2: local image artifacts.
   - Branch `no-llm-reference-stage-2`.
   - Added `opencv-python-headless`.
   - Created `spatial_api/reference/` package with quality, geometry, and proposal output modules.
   - Routed `reference-analysis` jobs in `ai_runner.py` to deterministic processing instead of detached AI.
   - Added `GET /ai/jobs/{job_id}`.
   - Validated API tests.
   - Opened and merged PR #5: “Generate deterministic reference artifacts”.

5. Stage 3: OCR/QR extraction.
   - Branch `no-llm-reference-stage-3`.
   - Added `pytesseract` and Docker apt packages: `tesseract-ocr libgl1 libglib2.0-0`.
   - Added OCR and URL/QR extraction modules.
   - Extended reference output with `ocrSnippets`, `productLinkCandidates`, and `ocrTextPath`.
   - Tests initially failed because local Tesseract was unavailable/unstable for a geometry-only test; resolved by monkeypatching OCR to empty for that test and separately monkeypatching OCR for URL/dimension extraction.
   - Validated API tests.
   - Opened and merged PR #6: “Extract product links from reference images”.

6. Stage 4: calibration and candidate acceptance.
   - Branch `no-llm-reference-stage-4`.
   - Added `reference/calibration.py` with `pixels_per_unit()` and `convert_rectangle_to_scene_object()`.
   - Added `scene.objects` and `add_scene_object()`.
   - Added `ReferenceCalibration` and `ReferenceCandidateAccept`.
   - Added endpoint `POST /reference/jobs/{job_id}/candidates/{candidate_id}/accept`.
   - Validated API tests.
   - Opened and merged PR #7: “Convert calibrated traces to scene objects”.

7. Stage 5: editable object transforms in API/UI/3D.
   - Branch `no-llm-reference-stage-5`.
   - Extended `ProductInstanceUpdate` with width/depth/height/unit so per-instance dimensions can be edited without changing product library specs.
   - Added `SceneObjectUpdate` and scene object update/duplicate/delete helpers/endpoints.
   - Added frontend `SceneObject` types.
   - Updated `Plan2D.tsx` to render/select/drag reference objects.
   - Updated `Scene3D.tsx` to render primitive reference objects.
   - Added `ObjectTransformPanel.tsx`.
   - Updated `studio-shell.tsx` to support object selection and transform actions.
   - Validated API tests, web typecheck, and web tests.
   - Opened and merged PR #8: “Add editable reference object transforms”.

8. Stage 6: product candidates.
   - Branch `no-llm-reference-stage-6`.
   - Refactored product creation in API into reusable `_create_imported_product()`.
   - Added URL candidate acceptance endpoint: `POST /reference/jobs/{job_id}/product-candidates/{candidate_id}/accept`.
   - Added manual product candidate endpoint: `POST /reference/product-candidates/manual`.
   - Added schemas `ReferenceProductCandidateAccept` and `ManualProductCandidateCreate`.
   - Added `ProductCandidatePanel.tsx` and wired it into `studio-shell.tsx`.
   - Validated API tests and web typecheck.
   - Opened and merged PR #9: “Create products from deterministic reference candidates”.

9. Stage 7: homelab worker deployment.
   - Created homelab worktree/branch `spatial-reference-worker`.
   - Added Spatial reference env vars to `homelab/.env.example`.
   - Added `spatial-design-studio-reference-worker` to `compose/compose.web.yml` with 2 CPU/2GB limits, shared Spatial data volume, no Caddy labels, and hard false cloud/LLM flags.
   - Added setup dir creation for `/opt/homelab/data/spatial-design-studio/reference-jobs`.
   - Updated `docs/05-service-guide.md` with no-LLM worker behavior.
   - Validated Docker Compose config.
   - Opened and merged homelab PR #10: “Add deterministic Spatial reference worker”.

10. Deploy/validate.
   - Pulled `main` in both `Spatial-Design-Studio` and `homelab`.
   - Added non-secret `SPATIAL_REFERENCE_*` flags to real `homelab/.env` because they were missing.
   - Ran final local validation: API tests, web typecheck, web tests, web build, compose config.
   - `bash scripts/ops/setup.sh` failed during broad Riven mount `chown` with “Function not implemented” on virtual media files, after creating the needed Spatial reference directory. Treated as unrelated to Spatial worker.
   - Ran `bash scripts/ops/deploy.sh web`; deploy exited 0.
   - Initial service validation showed API and web healthy, but `spatial-design-studio-reference-worker` was restarting with `ModuleNotFoundError: No module named 'spatial_api'`.
   - Created hotfix branch `spatial-worker-pythonpath`, added `PYTHONPATH=/app/apps/api` to the worker service, opened and merged homelab PR #11: “Fix Spatial reference worker module path”.
   - Redeployed web stack again; deploy exited 0. Compaction occurred before post-hotfix service validation was completed.
</history>

<work_done>
Files updated in `Spatial-Design-Studio`:
- `apps/api/spatial_api/config.py`: added deterministic reference settings and reference-jobs data dir creation.
- `apps/api/spatial_api/schemas.py`: added reference modes, calibration/candidate schemas, object update schemas, product/manual candidate schemas, and per-instance product dimension patch fields.
- `apps/api/spatial_api/main.py`: added asset `reference_mode` job queueing, job lookup, reference candidate acceptance, object transform endpoints, product candidate endpoints, and reusable product creation helpers.
- `apps/api/spatial_api/ai_runner.py`: routed `reference-analysis` jobs to deterministic local processing and avoided detached AI.
- `apps/api/spatial_api/worker.py`: used by the deployed worker.
- `apps/api/spatial_api/reference/__init__.py`, `quality.py`, `geometry.py`, `proposals.py`, `ocr.py`, `links.py`, `calibration.py`: new deterministic reference processing package.
- `apps/api/requirements.txt`: added `opencv-python-headless==4.12.0.88` and `pytesseract==0.3.13`.
- `apps/api/Dockerfile`: added Tesseract/OpenCV runtime apt packages.
- `apps/api/tests/test_reference_workflow.py`: new comprehensive tests for reference upload/job queueing, artifact output, OCR URL extraction, calibration, scene object transforms, URL candidate import, and dimension gating.
- `apps/web/app/__tests__/reference-language.test.ts`: new no-AI wording guard.
- `apps/web/app/components/inspector/AiJobsPanel.tsx`: renamed user-facing copy to reference workflow language.
- `apps/web/app/components/inspector/ObjectTransformPanel.tsx`: new object transform panel.
- `apps/web/app/components/inspector/ProductCandidatePanel.tsx`: new candidate review/manual product panel.
- `apps/web/app/components/planner/Plan2D.tsx`: renders/selects/drags reference objects.
- `apps/web/app/components/three/Scene3D.tsx`: renders reference objects as primitives.
- `apps/web/app/studio-shell.tsx`: wired object/product candidate UI and API actions.
- `apps/web/app/types.ts`: added SceneObject and looser deterministic job output typing.

Files updated in `homelab`:
- `.env.example`: added `SPATIAL_REFERENCE_*` variables.
- `.env`: added real non-secret `SPATIAL_REFERENCE_*` values locally. Do not commit this.
- `compose/compose.web.yml`: added reference worker and later hotfixed `PYTHONPATH=/app/apps/api` for worker.
- `scripts/ops/setup.sh`: creates `reference-jobs` directory.
- `docs/05-service-guide.md`: documented deterministic no-LLM workflow and worker.

Completed PRs:
- Spatial PR #3: Stage 0
- Spatial PR #4: Stage 1
- Spatial PR #5: Stage 2
- Spatial PR #6: Stage 3
- Spatial PR #7: Stage 4
- Spatial PR #8: Stage 5
- Spatial PR #9: Stage 6
- Homelab PR #10: Stage 7
- Homelab PR #11: worker PYTHONPATH hotfix

Most recent state:
- Web stack redeploy after PR #11 completed with exit code 0.
- Need to validate worker post-hotfix; this was in progress when compaction occurred.
</work_done>

<technical_details>
- Spatial app stack: FastAPI backend + Next.js frontend. API package lives under `/app/apps/api` in the Docker image. Running `python -m spatial_api.worker` requires `PYTHONPATH=/app/apps/api` in compose.
- Deterministic reference workflow constraints:
  - No local LLM/VLM.
  - No Copilot/Codex/Claude runtime dependency.
  - No paid cloud vision.
  - No reverse image search.
  - `SPATIAL_REFERENCE_ALLOW_CLOUD=false` and `SPATIAL_REFERENCE_ALLOW_LLM=false` are hard-false in homelab compose for API and worker.
- Worker:
  - Service name/container: `spatial-design-studio-reference-worker`.
  - Command: `python -m spatial_api.worker --interval 2 --limit 1`.
  - Internal-only, no Caddy labels.
  - Currently attached to `proxy` network only because API and shared volume are enough; it has no ingress labels.
  - Resource limit: memory `2G`, cpus `2.0`.
- Reference processing:
  - Upload with `reference_mode=deterministic` or `extract_links` queues an `ai_jobs` row with `type='reference-analysis'`, `provider='local'`, `model='deterministic-reference-0'`.
  - Artifacts go under `${SPATIAL_DATA_DIR}/reference-jobs/{job_id}`.
  - Output includes normalized preview, edge overlay, optional OCR text path, candidates, OCR snippets, product link candidates, and calibration requirements.
- Existing `ai_jobs` DB table intentionally remains; user-facing copy changed to “Reference jobs”.
- The `run_ai_job()` path no longer creates render rows for `reference-analysis`; normal AI critique jobs still do.
- Tesseract may not exist in local dev environments, so tests monkeypatch `pytesseract.image_to_string` where deterministic OCR output matters or is irrelevant.
- Homelab setup script issue:
  - `scripts/ops/setup.sh` currently fails on `sudo chown -R "$PUID:$PGID" "$RIVEN_MOUNT"` because the Riven FUSE/virtual media mount does not support ownership changes. This is unrelated to Spatial and occurred after the new Spatial reference directory had already been created.
  - Do not treat this as a Spatial deploy failure, but it is a homelab setup-script bug worth future cleanup.
- PR merge via `gh pr merge` from a worktree repeatedly printed `fatal: 'main' is already used by worktree...` after successful merges in Spatial repo. The PRs were merged despite local cleanup errors.
- Homelab worktree created from origin/main showed pre-existing dirty files (`PROGRESS.md`, `compose/compose.runtime-test.yml`) probably from smudge/line-ending or generated changes. They were ignored and not committed.
- Validation completed before deploy:
  - Spatial API tests: 13 passed.
  - Web tests: 45 passed.
  - Web typecheck passed.
  - Web production build passed.
  - Homelab compose config passed.
- Deploy command:
  - Use `cd /home/jbl/projects/homelab && bash scripts/ops/deploy.sh web`.
  - `./scripts/ops/deploy.sh` may not be executable; running with `bash` works.
</technical_details>

<important_files>
- `/home/jbl/projects/Spatial-Design-Studio/plans/no-llm-reference-asset-production-plan.md`
  - Source implementation plan. Stages 0-7 were implemented and merged.
- `/home/jbl/projects/Spatial-Design-Studio/apps/api/spatial_api/main.py`
  - Central API surface. Contains reference upload queueing, job lookup, candidate acceptance, scene object endpoints, and product candidate endpoints.
- `/home/jbl/projects/Spatial-Design-Studio/apps/api/spatial_api/ai_runner.py`
  - Determines worker behavior. Reference jobs route to deterministic local processing.
- `/home/jbl/projects/Spatial-Design-Studio/apps/api/spatial_api/reference/`
  - New deterministic processing package: quality normalization, OpenCV geometry, OCR, QR/URL extraction, calibration, proposals.
- `/home/jbl/projects/Spatial-Design-Studio/apps/api/tests/test_reference_workflow.py`
  - Primary backend regression suite for the implemented no-LLM workflow.
- `/home/jbl/projects/Spatial-Design-Studio/apps/web/app/studio-shell.tsx`
  - Main UI orchestration. Now wires product candidates and object transforms.
- `/home/jbl/projects/Spatial-Design-Studio/apps/web/app/components/inspector/ProductCandidatePanel.tsx`
  - New UI for OCR/QR/manual product candidates.
- `/home/jbl/projects/Spatial-Design-Studio/apps/web/app/components/inspector/ObjectTransformPanel.tsx`
  - New UI for object x/y/z/width/depth/height/rotation/lock/visibility controls.
- `/home/jbl/projects/Spatial-Design-Studio/apps/web/app/components/planner/Plan2D.tsx`
  - Renders product footprints and reference objects; supports dragging/selecting.
- `/home/jbl/projects/Spatial-Design-Studio/apps/web/app/components/three/Scene3D.tsx`
  - Renders products, fixed elements, and reference objects in 3D.
- `/home/jbl/projects/homelab/compose/compose.web.yml`
  - Homelab deploy definition. Contains Spatial API/web and new reference worker. Must include `PYTHONPATH=/app/apps/api` for worker.
- `/home/jbl/projects/homelab/.env`
  - Local runtime config; now includes `SPATIAL_REFERENCE_*` non-secret flags. Do not commit.
- `/home/jbl/projects/homelab/.env.example`
  - Tracked template with `SPATIAL_REFERENCE_*` vars.
- `/home/jbl/projects/homelab/scripts/ops/setup.sh`
  - Creates Spatial reference-jobs directory, but has unrelated Riven chown failure.
- `/home/jbl/projects/homelab/docs/05-service-guide.md`
  - Documents Spatial no-LLM worker and deployment guidance.
</important_files>

<next_steps>
Immediate next steps:
1. Validate post-hotfix deployed web stack:
   - `cd /home/jbl/projects/homelab`
   - `docker compose --env-file .env -f compose/compose.web.yml ps spatial-design-studio-api spatial-design-studio-reference-worker spatial-design-studio-web`
   - Confirm API/web healthy and worker `Up`, not restarting.
   - `docker logs --tail 80 spatial-design-studio-reference-worker`
   - Confirm no `ModuleNotFoundError`.
   - Confirm worker has no Caddy labels:
     `docker inspect spatial-design-studio-reference-worker --format '{{json .Config.Labels}}' | grep -vq caddy && echo 'worker has no caddy labels'`
2. Smoke-test ingress:
   - `curl -fsS -H "Host: spatial-api.${DOMAIN}" http://127.0.0.1/health`
   - `curl -fsS -H "Host: spatial.${DOMAIN}" http://127.0.0.1/ | head`
3. Ideally smoke-test a reference job against the deployed API. Requires an authenticated account/session cookie, so either use an existing browser/API session or create a safe test account only if signups are currently allowed.
4. Mark SQL todo `final-deploy` done after validation.
5. Record MemPalace diary and important durable finding. Suggested memory:
   - Spatial no-LLM plan implemented through PRs #3-#9, homelab PRs #10-#11, deployed web stack; worker requires `PYTHONPATH=/app/apps/api`.
   - Homelab `setup.sh` has unrelated Riven chown failure on FUSE media mount.
6. Optionally log a task-observer/open observation or future fix for `homelab-deploy`: setup scripts that chown FUSE mounts can block unrelated service setup; deployment should verify only required directories or make Riven chown non-fatal.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
