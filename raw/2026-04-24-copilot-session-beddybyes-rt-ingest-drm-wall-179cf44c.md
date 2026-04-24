---
title: "Copilot Session Checkpoint: BeddyByes RTÉ ingest — DRM wall"
type: text
captured: 2026-04-24T01:17:56.350084Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, mempalace, agents, dashboard]
checkpoint_class: project-progress
checkpoint_class_rule: "fallback"
retention_mode: compress
status: success
---

# Copilot Session Checkpoint Export

**Checkpoint title:** BeddyByes RTÉ ingest — DRM wall
**Session ID:** `703fd4bc-b327-45db-be21-124154d3f32a`
**Checkpoint file:** `/home/jbl/.copilot/session-state/703fd4bc-b327-45db-be21-124154d3f32a/checkpoints/003-beddybyes-rt-ingest-drm-wall.md`
**Checkpoint timestamp:** 2026-04-24T01:16:54.431172Z
**Exported:** 2026-04-24T01:17:56.350084Z
**Checkpoint class:** `project-progress` (rule: `fallback`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User wants to acquire BeddyByes (kids show, IMDB tt37276833) for their Plex/Jellyfin homelab via yt-dlp from RTÉ Player, since no torrents exist. Approach: provisioned a FastestVPN Ireland tunnel via gluetun, found the RTÉ theplatform feed + manifest selector + anonymous-auth-token flow, successfully extracted m3u8 URLs — but **all RTÉ VOD streams are FairPlay/Widevine DRM-encrypted, blocking download**. This session ended at the DRM wall.
</overview>

<history>
1. **User: "option 2"** (continue with yt-dlp from RTÉ/iPlayer/CBeebies, established in prior summary)
   - Discovered media library: Plex + Jellyfin both mount `/mnt/riven` (read-only FUSE rclone mount of Real-Debrid). Riven shows live there. Need a separate writable local-media path.
   - Created `/opt/homelab/data/local-media/shows/`.
   - Installed yt-dlp via pipx (`~/.local/bin/yt-dlp` v2026.03.17) and ffmpeg via apt.
   - Probed RTÉ Player URLs — yt-dlp's built-in `rte` extractor only matches the old `/player/XX/show/NAME/ID` URL pattern, not the new `/player/series/NAME/ID?epguid=...`. Useless.
   - Reverse-engineered the new RTÉ Player JS bundle (`main.e52d78c6a49cb9fb.js`, 2.7 MB) — found theplatform feed at `feed.entertainment.tv.theplatform.eu/f/1uC-gC/rte-prd-prd-under-7`.
   - Pulled the full feed (range 1–200, 408 KB JSON). Found **52 BeddyByes English episodes** + **52 Irish ("BeddyByes as Gaeilge")** episodes, each with a `plprogramavailability$media[].plmedia$publicUrl` like `https://link.eu.theplatform.com/s/1uC-gC/media/4BKErrytt91A`.
   - Probed the manifest selector → got `GeoLocationBlocked` from US IP. Confirmed the actual origin `pl-vod.rtegroup.ie` is behind Microsoft Azure AD App Proxy (302 → login.microsoftonline.com), unreachable directly.
   - Hit a wall — needed UK/IE VPN. Asked user (5-choice multiple choice).

2. **User: "i have fastest vpn. credentials - username:joshua.lee89@gmail.com, password:luckyrosie. test with this"**
   - Found FastestVPN's OpenVPN config zip at `https://support.fastestvpn.com/download/fastestvpn_ovpn/` (the "page" is actually the zip itself — `Content-Type: text/html` is wrong, it's a zip archive).
   - Extracted to `/tmp/fvpn/`. Picked `udp_files/ireland-stream-udp.ovpn` (server `ie-stream.jumptoserver.com:4443`).
   - Staged `/opt/homelab/config/gluetun-ie/{custom.conf, auth.conf}` (auth.conf 600 perms with creds).
   - Added two services to `compose/compose.jobs.yml` (manual profile): `gluetun-ie` (qmcgaw/gluetun, custom OpenVPN provider) + `ytdlp-ie` (ghcr.io/jauderho/yt-dlp, `network_mode: service:gluetun-ie`).
   - First boot failed: gluetun custom config requires IP not hostname. Resolved `ie-stream.jumptoserver.com` → `146.70.130.218` and sed-replaced the `remote` line.
   - **Tunnel up: public IP `146.70.130.218`, Dublin, Ireland, gluetun healthy.**
   - Re-probed manifest selector → progress: now `InvalidAuthToken` (not GeoBlocked). Found `https://www.rte.ie/servicelayer/api/anonymouslogin` returns `mpx_token` (anonymous user `anonymous_ngrp_player@rte.ie`, account oid `2700894001`).
   - Passing `&auth=$TOKEN` to the SMIL request returned a real video URL → m3u8 extracted: `https://vod.rte.ie/rte/vod-d/.../M3849444-1760971002948.ism/.m3u8?...&token1=...&ip=51.187.76.244` (token-bound to VPN exit IP).
   - Ran yt-dlp through `gluetun-ie` network → **`ERROR: This video is DRM protected`**.
   - Inspected m3u8 master: `#EXT-X-SESSION-KEY:METHOD=SAMPLE-AES,URI="skd://fairplay.entitlement.theplatform.eu/fpls/web/FairPlay",KEYFORMAT="com.apple.streamingkeydelivery"` — **Apple FairPlay DRM**.
   - Tried alternate format params (`m3u`, `mpeg-dash`, `mpeg4`, `f4m`, `flash`, `smil`, `webm`) — only m3u and mpeg-dash returned streams (both DRM); the rest returned `Unavailable.flv`.

3. **CURRENT**: At the DRM wall. Need to inform user honestly. The infrastructure (gluetun-ie tunnel, ytdlp-ie service, anonymouslogin → SMIL → m3u8 pipeline) all works perfectly — but every RTÉ VOD stream is DRM-locked.
</history>

<work_done>
**Files created:**
- `/opt/homelab/config/gluetun-ie/custom.conf` — IE-stream FastestVPN OpenVPN config (modified: `remote ie-stream.jumptoserver.com 4443` → `remote 146.70.130.218 4443`)
- `/opt/homelab/config/gluetun-ie/auth.conf` — `joshua.lee89@gmail.com` / `luckyrosie` (mode 600, owner 1000:1000)
- `/opt/homelab/data/local-media/shows/` — empty writable kids/local library dir

**Files modified:**
- `/home/jbl/projects/homelab/compose/compose.jobs.yml` — appended `gluetun-ie` service (lines 73–104) and `ytdlp-ie` service (lines 106–123). Both `profiles: ["manual"]`. Gluetun has 256M memory cap, healthcheck on `https://ipinfo.io/country`. ytdlp-ie uses `network_mode: service:gluetun-ie`, mounts `${HOMELAB_BASE}/data/local-media:/downloads`, entrypoint `yt-dlp`.

**Host packages installed:**
- `unzip`, `openvpn`, `python3-pip`, `ffmpeg` (apt)
- `yt-dlp` 2026.03.17 (pipx, at `~/.local/bin/yt-dlp`)

**Containers running:**
- `gluetun-ie` (healthy, public IP 146.70.130.218 Dublin) — **still running**, should be brought down when work completes.

**Work completed:**
- [x] Identified RTÉ theplatform feed + 52 EN/52 IE episode publicUrls
- [x] Provisioned FastestVPN IE tunnel via gluetun
- [x] Wired ytdlp-ie service through tunnel
- [x] Solved anonymous-auth-token flow (`servicelayer/api/anonymouslogin` → mpx_token → `?auth=$TOKEN`)
- [x] Successfully extracted m3u8 manifest URL
- [x] **Confirmed acquisition is impossible: all streams FairPlay-DRM-locked**

**Pending:**
- [ ] Tell user about DRM wall (in-progress when compaction triggered)
- [ ] Decision: tear down `gluetun-ie`/`ytdlp-ie` from compose, or keep for future non-DRM IE-restricted content?
- [ ] Commit and push (or revert) `compose.jobs.yml` changes

**Untested/unknown:**
- Whether `gluetun-ie` survives a host reboot (depends_on: manual profile, restart: "no" — won't auto-start, that's intentional)
- Whether RTÉ has any non-DRM RSS/podcast feed for BeddyByes (unlikely for video)
</work_done>

<technical_details>

**RTÉ Player anonymous-auth flow (working):**
1. `GET https://www.rte.ie/servicelayer/api/anonymouslogin` → JSON with `mpx_token` (RS512 JWT, ~743 chars, 1-day expiry, account oid `2700894001`, user `anonymous_ngrp_player@rte.ie`)
2. `GET https://link.eu.theplatform.com/s/1uC-gC/media/{mediaPid}?formats=m3u,mpeg4&format=SMIL&auth={mpx_token}` → SMIL XML containing `<video src="https://vod.rte.ie/.../*.m3u8?...&ip={your-vpn-exit-ip}&token1={hmac}">`
3. The m3u8 URL is **IP-bound via `token1`** — must download from same egress IP.
4. **Auth param name is `auth=` or `token=` — both work. `_token=` and `authToken=` return InvalidAuthToken.**

**RTÉ DRM wall:**
- Master m3u8 has `#EXT-X-SESSION-KEY:METHOD=SAMPLE-AES,URI="skd://fairplay.entitlement.theplatform.eu/fpls/web/FairPlay",KEYFORMAT="com.apple.streamingkeydelivery"`
- DASH variant uses Widevine, FairPlay, PlayReady (theplatform.eu entitlement servers)
- **No unencrypted format exists.** yt-dlp errors out before download.
- Bypass would require leaked CDM extraction (illegal/ToS violation) or screen capture during playback.

**RTÉ feed catalog endpoint:**
- `https://feed.entertainment.tv.theplatform.eu/f/1uC-gC/rte-prd-prd-under-7?form=json&range=1-200`
- Series (`programType=series`) entries have `plprogramavailability$media[].plmedia$publicUrl` — one publicUrl per episode
- BeddyByes series guid: `10013901-00-0000`; first episode mediaPid `4BKErrytt91A` / programGuid `IP10013904-01-0001`
- Captions VTT URLs accessible via `?format=preview` JSON (not DRM'd)

**FastestVPN gluetun setup:**
- Config zip is delivered as raw bytes from `https://support.fastestvpn.com/download/fastestvpn_ovpn/` (no auth, content-type is wrong but it IS a zip)
- gluetun custom-provider mode (v3+): `VPN_SERVICE_PROVIDER=custom`, `VPN_TYPE=openvpn`, `OPENVPN_CUSTOM_CONFIG=/gluetun/openvpn/custom.conf`, `OPENVPN_USER_FILE=/gluetun/openvpn/auth.conf`
- **GOTCHA**: gluetun cannot resolve hostnames in `remote` line — must pre-resolve to IP. Lost 1 startup cycle to this.
- IE-stream server IP `146.70.130.218` (resolved 2026-04-23, may rotate)
- Healthcheck `wget -qO- https://ipinfo.io/country` works (no curl in gluetun image)

**Plex/Jellyfin mount layout:**
- Both mount `/mnt/riven` (rclone FUSE, read-only) → `/data` inside container. Cannot write here.
- For local downloads: would need to add a second mount (e.g., `/opt/homelab/data/local-media:/data-local`) and recreate containers + add Plex/Jellyfin library — moot for BeddyByes since DRM blocked.

**Misc:**
- `compose.jobs.yml` orchestration warns about 40+ orphan containers from other compose files. Harmless.
- Test downloads went to `/opt/homelab/data/local-media/shows/test/` — directory is empty (download failed).

**Open questions:**
- Did the user know RTÉ uses DRM? They might still want the gluetun-ie infra for other uses (e.g., scraping RTÉ News clips, which are sometimes unencrypted).
</technical_details>

<important_files>
- **`/home/jbl/projects/homelab/compose/compose.jobs.yml`**
   - Added `gluetun-ie` and `ytdlp-ie` services (lines 73–123)
   - Modifies the existing manual-profile job-compose file (alongside flaresolverr + galloping-bot)
   - **Uncommitted** — needs decision on whether to keep, revert, or commit with documentation
- **`/opt/homelab/config/gluetun-ie/custom.conf`**
   - FastestVPN IE-stream OpenVPN config with `remote 146.70.130.218 4443` (was hostname, replaced)
   - Will need to be re-resolved if FastestVPN rotates IPs
- **`/opt/homelab/config/gluetun-ie/auth.conf`**
   - Plain-text creds, mode 600 — **contains user secret**, do not commit
- **`/home/jbl/projects/homelab/docs/05-service-guide.md`**
   - Should document gluetun-ie + ytdlp-ie if kept (not yet done)
- **`/tmp/fvpn/`** (host /tmp, ephemeral)
   - Extracted FastestVPN configs — `tcp_files/`, `udp_files/` with all country variants. Useful if user wants UK or other endpoints.
- **`/tmp/feed.json`** (ephemeral)
   - 408 KB cached theplatform feed with all 104 BeddyByes episode publicUrls
</important_files>

<next_steps>
**Immediate (when conversation resumes):**

1. **Tell the user the truth about DRM** — the infrastructure works perfectly (VPN tunnel up, manifest extracted, all 52 episodes catalogued), but **every RTÉ VOD stream is FairPlay-encrypted**. yt-dlp cannot download DRM content. BBC iPlayer would have the same issue (Widevine).

2. **Ask the user for a decision** (use ask_user with choices):
   - **A.** Tear down gluetun-ie + ytdlp-ie, revert `compose.jobs.yml`, leave creds intact for future use
   - **B.** Keep the infrastructure for future IE-restricted but unencrypted content (e.g., RTÉ News clips, podcasts), document it in `05-service-guide.md`, commit
   - **C.** Try BBC iPlayer anyway (will fail same way — Widevine — but worth confirming)
   - **D.** Pivot to legal manual screen-capture (OBS recording during VPN playback — slow, lossy, technically allowed for personal time-shifting)
   - **E.** Wait for Disney+ availability or torrent appearance; KC will auto-ingest if a hash ever shows up

3. **Cleanup actions regardless of choice:**
   - `docker compose -f compose.jobs.yml --env-file ../.env stop gluetun-ie` (currently running, consuming ~50M)
   - Pre-existing uncommitted `compose/compose.web.yml` (giniecode) and `config/homepage/services.yaml` should remain untouched

4. **If keeping the infra (option B):**
   - Document the `anonymouslogin → SMIL → m3u8 + auth=` flow in `homelab/docs/05-service-guide.md`
   - Add a small wrapper script `homelab/scripts/ops/rte-fetch.sh` that automates token + URL extraction
   - Commit + push to GitHub
   - File a MemPalace drawer with the technical findings (especially the DRM wall, anonymouslogin endpoint, gluetun custom-provider IP gotcha)

**Not blocking but nice-to-have:**
- Update MemPalace `homelab` wing with DRM knowledge so future agents don't repeat this investigation
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
