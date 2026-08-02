# SevenRooms / DoorDash Going Out API Full Mapping

Generated: `2026-06-08T19:34:48Z`

## Scope and evidence levels

This file maps the API surface discovered during the SevenRooms / DoorDash Going Out browser-to-api run. It separates **live-observed** endpoints from **static-observed** endpoint strings extracted from public SevenRooms widget JavaScript.

- **Live-observed**: present in `.o11y/sevenrooms-doordash-going-out/cdp/network/*` and in generated `openapi.json`.
- **Static-observed**: string literal or template endpoint found in public `dining.js`; method/contract may be inferred but was not exercised.
- **Not attempted**: booking holds, reservation creation/cancellation, payment setup, DoorDash marketplace mutation, auth bypass, anti-bot bypass, or credentialed partner API access.

## Source artifacts

| Artifact | Path / URL |
|---|---|
| browser-to-api OpenAPI | `/home/jbl/projects/labs-wiki/.o11y/sevenrooms-doordash-going-out/api-spec/openapi.json` |
| browser-to-api report | `/home/jbl/projects/labs-wiki/.o11y/sevenrooms-doordash-going-out/api-spec/report.md` |
| booking-flow notes | `/home/jbl/projects/labs-wiki/.o11y/sevenrooms-doordash-going-out/api-spec/booking-flow.md` |
| overlay OpenAPI | `/home/jbl/projects/labs-wiki/.o11y/sevenrooms-doordash-going-out/api-spec/booking-flow-overlay.openapi.yaml` |
| public widget JS | `https://www.sevenrooms.com/static/21bc93acc1900fc2ac156b2a7b1752af5b7844bf/cdn/app/widget/dining.js` |
| widget JS SHA-256 | `d431c93148d613dc1e7e9dfc464aec49332d60c376051a67a599a3cb7241bf53` |

## 1. Live-observed endpoints

### GET `/api-yoa/availability/widget/range`

- Evidence: live-observed (`samples=3`, statuses=[200], confidence=low)
- Role: Availability / discovery
- Query/body parameters: `venue`:string required, `time_slot`:string required, `party_size`:integer required, `halo_size_interval`:integer required, `start_date`:string required, `num_days`:integer required, `channel`:string required
- Response statuses in spec: `200`
- Discovery semantics: returns `data.availability` keyed by date. Each date contains shifts, each shift contains `times[]`.
- Important slot fields observed: `time_iso`, `utc_datetime`, `access_persistent_id`, `access_rule_id`, `shift_persistent_id`, `experience_id`, `is_held`, `require_credit_card`, `cc_payment_rule`, `cancellation_policy`, `pacing_covers_remaining`, `duration`, `reservation_tags`, `upsell_categories`.
- Booking implication: identifies candidate slots and downstream IDs; it does **not** by itself create a reservation.

### GET `/api-yoa/venue/reservation_widget_settings_v2`

- Evidence: live-observed (`samples=1`, statuses=[401], confidence=low)
- Role: Venue / widget configuration
- Query/body parameters: `venue_id`:string required
- Response statuses in spec: `401`
- Boundary semantics: unauthenticated/insufficient-context request returned `401`; likely requires browser/session/widget context.

### GET `/api-yoa/dining/venue_info`

- Evidence: live-observed (`samples=1`, statuses=[400], confidence=low)
- Role: Venue / widget configuration
- Query/body parameters: `venue`:string required
- Response statuses in spec: `400`
- Boundary semantics: direct request with only `venue` returned `400`; likely requires a different parameter set or context.

## 2. Reservation discovery-to-booking flow map

```text
Public/widget or marketplace discovery
  -> GET /api-yoa/availability/widget/range
       Inputs: venue, date range, party size, target time, channel
       Outputs: candidate shifts + times + access IDs + policy/payment hints
  -> POST /api-yoa/dining/hold/add              # static-observed; NOT called
       Likely purpose: hold a selected table/slot before checkout
  -> POST /api-yoa/dining/hold/upgrades         # static-observed; NOT called
       Likely purpose: apply optional upsells/upgrades to held slot
  -> POST /api-yoa/customer-payment-session/    # static-observed; NOT called
  -> POST /api-yoa/customer-adyen-session/      # static-observed; NOT called
       Likely purpose: payment/card setup where venue policy requires card/deposit
  -> final reservation submit/update/cancel paths
       Not observed in the safe trace; likely session/auth/CSRF/partner gated
```

## 3. Static endpoint inventory from public SevenRooms widget JavaScript

Total unique normalized `/api-yoa/` endpoint strings extracted: **287**. Counts are occurrence counts in the minified JS, not request counts. Methods are inferred only when the endpoint appeared as the first argument to a recognizable request helper (`Yr`, `$i`, `Fi`, `dc`, `Ad`).

### Admin / integration configuration (35)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET/POST (inferred) | `/api-yoa/admin/api-integration-partners` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| PUT/PATCH/DELETE (inferred) | `/api-yoa/admin/api-integration-partners/{L_integrationTypeId}` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/autotag/config_tiers` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/autotag/configs` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/autotag/configs/{L_id}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/autotag/configs/{L}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/DELETE/POST (inferred) | `/api-yoa/admin/clientapps` | 3 | Likely authenticated/admin/partner surface; static clue only. |
| GET/PUT/PATCH (inferred) | `/api-yoa/admin/clientapps/{U_clientAppId}` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/clientapps/{U_clientAppId}/form` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/clientapps/{U_clientAppId}/rotate-secret` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/custom_domains` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/PUT/PATCH/DELETE (inferred) | `/api-yoa/admin/custom_font/{v}` | 3 | Likely authenticated/admin/partner surface; static clue only. |
| GET/POST (inferred) | `/api-yoa/admin/custom_fonts` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/email_campaign_template/publish/{v}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/DELETE (inferred) | `/api-yoa/admin/email_campaign_template/{v}` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| GET/POST/PUT/PATCH (inferred) | `/api-yoa/admin/email_campaign_templates` | 3 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/email_campaign_test` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| UNKNOWN | `/api-yoa/admin/importutils/` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/integration-template-form` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/POST (inferred) | `/api-yoa/admin/integration-templates` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| GET/PUT/PATCH (inferred) | `/api-yoa/admin/integration-templates/{W_integrationTemplateId}` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/refresh_custom_domains` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/venue-group-history-tracking` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/venue-history-tracking` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST/GET (inferred) | `/api-yoa/admin/venue-images/{D_venueId}` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| DELETE (inferred) | `/api-yoa/admin/venue-images/{D_venueId}/{D_imageId}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/POST (inferred) | `/api-yoa/admin/venue-package-provisioning` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/venue-package-provisioning-diff` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/POST (inferred) | `/api-yoa/admin/venue-phone-numbers` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/venue-phone-numbers/migrate/{X}?venue_id={U}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| DELETE (inferred) | `/api-yoa/admin/venue-phone-numbers/{U}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/venue_group_merge` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/venuegroup/{U_venueGroupId}/venue-phone-numbers/twilio/toll-free/latest-verified` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/venuegroup/{W_venueGroupId}/package-wizard/reports` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/admin/venuegroup/{W_venueGroupId}/package-wizard/start` | 1 | Likely authenticated/admin/partner surface; static clue only. |

### Availability / discovery (18)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET (inferred) | `/api-yoa/availability/access_rules` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/availability/active_audiences` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/availability/booked_covers` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/availability/calendar` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/availability/dates?venue=` | 1 | Static/public discovery clue; read-oriented but not fully live-verified in this exact shape. |
| UNKNOWN | `/api-yoa/availability/dates?{dates_query}` | 1 | Static/public discovery clue; read-oriented but not fully live-verified in this exact shape. |
| GET (inferred) | `/api-yoa/availability/debugger` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/availability/experience/dates?venue=` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/availability/experience/dates?{experience_dates_query}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/availability/mode` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/availability/mode/{W_modeId}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/availability/mode/{W_modeId}/shifts` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/availability/mode/{W_modeId}?venue={W_venue}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/availability/mode?venue={W_venue}` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/availability/ng/widget/range?{availability_query}` | 1 | Static/public discovery clue; read-oriented but not fully live-verified in this exact shape. |
| GET (inferred) | `/api-yoa/availability/venuegroup/{T}/access_rules` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/availability/widget/experiences/range?{experience_query}` | 1 | Static/public discovery clue; read-oriented but not fully live-verified in this exact shape. |
| GET (live) | `/api-yoa/availability/widget/range` | 1 | LIVE observed: statuses [200] samples=3 confidence=low |

### Booking access rules / audiences (9)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET (inferred) | `/api-yoa/booking_access` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/booking_access/audience_hierarchy` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/booking_access/bulk_edit?venue_id={U}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/booking_access/create` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/booking_access/v2` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| PUT/PATCH (inferred) | `/api-yoa/booking_access/{U_args_id}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET/DELETE (inferred) | `/api-yoa/booking_access/{U_id}` | 2 | Likely authenticated/admin/partner surface; static clue only. |
| POST (inferred) | `/api-yoa/concierge_access_report/{T_conciergeId}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/booking_access_validation_criteria` | 1 | Likely authenticated/admin/partner surface; static clue only. |

### Client / guest data (9)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| POST (inferred) | `/api-yoa/client/marketing_opt_in/{v}?venue={E}` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| GET (inferred) | `/api-yoa/client/{v}/external-profile-notes` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| GET (inferred) | `/api-yoa/client/{v}/marketing_preferences` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| GET (inferred) | `/api-yoa/client/{v}/marketing_preferences/{E}` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| PUT/PATCH (inferred) | `/api-yoa/client/{v}/marketing_preferences?venue={E}` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| GET (inferred) | `/api-yoa/client/{v}/stats` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| GET (inferred) | `/api-yoa/client/{v}/tag-followers` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| GET (inferred) | `/api-yoa/client/{v}/tags` | 1 | Guest/client data surface; likely private or session-scoped; not called. |
| POST (inferred) | `/api-yoa/customer-email/` | 1 | Guest/client data surface; likely private or session-scoped; not called. |

### Custom assets/domains/audiences (9)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET/POST (inferred) | `/api-yoa/custom_audience/{W_venueId}` | 2 | Static JS endpoint clue; not live-verified. |
| GET/DELETE/PUT/PATCH (inferred) | `/api-yoa/custom_audience/{W_venueId}/{W_id}` | 3 | Static JS endpoint clue; not live-verified. |
| DELETE (inferred) | `/api-yoa/custom_domains` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/custom_domains/activate?venue_id={W}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/custom_domains/verify?venue_id={W}` | 1 | Static JS endpoint clue; not live-verified. |
| GET/POST (inferred) | `/api-yoa/custom_domains?venue_id={W}` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/custom_fonts?venue={T}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/custom_sms/{L}` | 2 | Static JS endpoint clue; not live-verified. |
| DELETE (inferred) | `/api-yoa/custom_sms/{L}/{W}` | 1 | Static JS endpoint clue; not live-verified. |

### Dining hold / checkout flow (2)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| UNKNOWN | `/api-yoa/dining/hold/add` | 2 | Probable write-sensitive table-hold step; not called. |
| UNKNOWN | `/api-yoa/dining/hold/upgrades` | 1 | Probable write-sensitive table-hold step; not called. |

### DoorDash marketplace/storefront (9)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET (inferred) | `/api-yoa/doordash_marketplace` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/cuisine_update?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/image_upload?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/photos_reorder?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/photos_update?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/toggle?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/venue_description_update?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_storefront/connect?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_storefront/disconnect?venue={venue}` | 1 | DoorDash integration/marketplace clue from SevenRooms JS; likely partner/admin/config surface, not confirmed consumer Going Out API. |

### Email / campaign tooling (7)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET (inferred) | `/api-yoa/email_campaign_activity` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/email_campaign_templates` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/email_campaign_test` | 1 | Static JS endpoint clue; not live-verified. |
| GET/PUT/PATCH/POST (inferred) | `/api-yoa/email_campaigns` | 3 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/email_campaigns/fetch_template_fields/{E}` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/email_campaigns/resolve_parent_template_updates/{E}` | 2 | Static JS endpoint clue; not live-verified. |
| GET/DELETE (inferred) | `/api-yoa/email_campaigns/{E}` | 2 | Static JS endpoint clue; not live-verified. |

### Manager / activity or ops (1)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| POST (inferred) | `/api-yoa/manager/{v}/activitylog/json` | 1 | Likely authenticated/admin/partner surface; static clue only. |

### Other / miscellaneous (134)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| POST (inferred) | `/api-yoa/actuals/manage/cancel?token={D}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/actuals/manage/preferences?token={L}` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/actuals/manage?token={D}&lang={L}` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/adyen/` | 2 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/adyen/{v}/get_initial_data` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/adyen/{v}/post_payment_details` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/autotag/audience_size` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/backwriter/{D}/conversations${L?` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/backwriter/{D}/reviews/summary` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/backwriter/{D}/reviews/{L}` | 1 | Static JS endpoint clue; not live-verified. |
| POST/PUT/PATCH (inferred) | `/api-yoa/client-import-ma/{D}/` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/clients/marketing_opt_in/count` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/cybersource/` | 4 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/cybersource/auth/` | 2 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/cybersource/auth/{v}/get_initial_data` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/cybersource/{v}/generate_token` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/cybersource/{v}/get_capture_context` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/default_policy_data/{I}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/deliveroo_marketplace` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/deliveroo_marketplace/cuisine?venue={venue}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/deliveroo_marketplace/image_uploader?venue={venue}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/deliveroo_marketplace/photos/reorder?venue={venue}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/deliveroo_marketplace/photos?venue={venue}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/deliveroo_marketplace/toggle?venue={venue}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/deliveroo_marketplace/venue_description?venue={venue}` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/dining/pre_arrival_upgrades/` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/dining/pre_arrival_upgrades/{L}/{W}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/dining/widget_info` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH/GET (inferred) | `/api-yoa/experiences` | 2 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/experiences/` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/experiences/{T}` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/experiences/{v}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/experiences?venue_id={E}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/floorplan_layouts` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/insights/{L}` | 1 | Static JS endpoint clue; not live-verified. |
| GET/PUT/PATCH (inferred) | `/api-yoa/insights/{L}/{W}` | 2 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/insights/{L}/{W}/comment` | 1 | Static JS endpoint clue; not live-verified. |
| GET/POST (inferred) | `/api-yoa/ivvy/{I}` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/languages/{L}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/languagestrings/{T}/all` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/languagestrings/{v_venueId}/sms-description-keys` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/loyalty/{T}/signup` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH/POST (inferred) | `/api-yoa/marketing_assistant?venue_id={E}` | 2 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/mfa/auth/step_up` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/mfa/provisioning/app/initiate` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/mfa/provisioning/sms/initiate` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/mfa/provisioning/{W_mfaMethod}/disable` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/mfa/provisioning/{W_mfaMethod}/verify` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/ordering/notification_settings` | 2 | Static JS endpoint clue; not live-verified. |
| GET/POST/PUT/PATCH/DELETE (inferred) | `/api-yoa/ordering/room_numbers/{v}` | 4 | Static JS endpoint clue; not live-verified. |
| DELETE (inferred) | `/api-yoa/ordering/room_numbers/{v}/{E}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/orders` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/orders/{L}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/orders/{L}/status` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/policies/{I_venueId}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/posi/{D}/internal_menu/clear` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{D}/internal_menu/items` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/posi/{D}/internal_menu/upload_csv` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/base_urls` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/check_creation_mappings_data` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/config` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/course_status_mapping_data` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/deposit_data` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/posi/{Fe}/internal_menu/save_config` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/landing` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/locations` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/seating_areas` | 1 | Static JS endpoint clue; not live-verified. |
| GET/PUT/PATCH (inferred) | `/api-yoa/posi/{Fe}/table_mapping_data` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{Fe}/tender_items` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/posi/{Fe}/validate_mapping_sync` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/posi/{Fe}/{Ve_toLowerCase}/save_config` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{I}/agilysys_infogenesis/automatic_check_creation_data` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/posi/{I}/agilysys_infogenesis/default_profit_center` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/posi/{experience_query}/{Fe_toLowerCase}/authenticate` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/posi/{experience_query}/{Fe_toLowerCase}/disconnect` | 1 | Static JS endpoint clue; not live-verified. |
| GET/POST (inferred) | `/api-yoa/promo_codes/{V}` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/promo_codes/{V}/resources` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/promo_codes/{V}/{U_key}` | 1 | Static JS endpoint clue; not live-verified. |
| GET/DELETE (inferred) | `/api-yoa/promo_codes/{V}/{U}` | 2 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/redemption_hub/` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/redemption_hub/{T}/check_balance` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/referrals_program` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/referrals_program?venue_id={D_venueId}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/reporting/revenue_dashboard/{T}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/requests/{D}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/requests/{D}/cancel` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/reviews` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/reviews/{D}` | 1 | Static JS endpoint clue; not live-verified. |
| DELETE (inferred) | `/api-yoa/reviews/{D}/reply` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/reviews/{D}/reply?venue_id={L}` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/saferpay/` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/saferpay/{v}/get_initial_data` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/shift_4/` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/shift_4/{v}/get_initial_data` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/shifts/schedule` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/shifts/summary` | 1 | Static JS endpoint clue; not live-verified. |
| GET/DELETE (inferred) | `/api-yoa/smart_boost` | 2 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/smart_boost?venue={v}` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/smart_boost?venue_id={v}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/smart_boost_preview?venue={v}` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/smart_boost_status?venue={v}` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/smart_boost_time_slots?venue={v}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/smart_boost_time_slots_range` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/sms_campaign_activity` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/sms_campaign_templates` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/sms_campaign_templates/fetch_template_fields/{E}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/sms_campaign_test?venue={v}` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/sms_campaigns` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/step_up/initiate` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/step_up/mfa/verify` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/stripe/{U_venueId}/disconnect` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/stripe/{U_venueId}/generate_connect_link` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/subscription/{T}/signup` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/tags/translated/{T}/{I}/` | 1 | Static JS endpoint clue; not live-verified. |
| POST/DELETE (inferred) | `/api-yoa/users/{I}/suspend` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue_events/list` | 1 | Static JS endpoint clue; not live-verified. |
| GET/POST (inferred) | `/api-yoa/venue_profile` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue_static_data` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue_users` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venuegroup/accessible_pods` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venuegroup/get_group_venues` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venuegroup/{I}/activity_log` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/waitlist` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/waitlist/` | 2 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/waitlist/quote_times?venue_id=` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/whatsapp/phone-numbers/acquire?venue_id={v}` | 1 | Static JS endpoint clue; not live-verified. |
| DELETE (inferred) | `/api-yoa/whatsapp/phone-numbers/{E}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/whatsapp/phone-numbers?venue_id={v}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/widget/experiences/{I}` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/{D}/fee_list` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/{I_venueId}/fees` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/{T_venueId}/tables` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/{T_venueId}/taxes` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/{v}/topol_token` | 1 | Static JS endpoint clue; not live-verified. |

### Payment setup (13)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| GET (inferred) | `/api-yoa/admin/payments-debug` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/payments-debug/load-more-http-logs` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| POST/PUT/PATCH (inferred) | `/api-yoa/customer-adyen-session/` | 2 | Payment-sensitive setup step; not called. |
| POST/PUT/PATCH (inferred) | `/api-yoa/customer-payment-session/` | 2 | Payment-sensitive setup step; not called. |
| GET (inferred) | `/api-yoa/customer-payment-session/?customer_payment_session_id={V}` | 1 | Payment-sensitive setup step; not called. |
| UNKNOWN | `/api-yoa/payments/` | 4 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/payments/{I_venueUrlKey}/refund` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/payments/{U_gateway}/{U_venueKey}/setup` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/payments/{U_venueId}/recommended_integrations` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/payments/{U_venueId}/setup` | 1 | Static JS endpoint clue; not live-verified. |
| POST/GET (inferred) | `/api-yoa/payments/{U_venueId}/setup/test` | 2 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/payments/{v}/authorize` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/payments/{v}/begin_payment` | 1 | Static JS endpoint clue; not live-verified. |

### Upsells / upgrades (2)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| UNKNOWN | `/api-yoa/upgrades/widget/status` | 1 | Static JS endpoint clue; not live-verified. |
| UNKNOWN | `/api-yoa/upgrades/widget?venue_id={D}` | 1 | Static JS endpoint clue; not live-verified. |

### Venue / widget configuration (39)

| Method | Endpoint template | JS refs | Evidence / notes |
|---|---|---:|---|
| POST (inferred) | `/api-yoa/admin/venue/business-contact/resync` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/admin/venue/business-contact?venue={U_venueId}` | 1 | Likely authenticated/admin/partner surface; static clue only. |
| GET (inferred) | `/api-yoa/dining/venue_info` | 1 | LIVE observed: statuses [400] samples=1 confidence=low |
| UNKNOWN | `/api-yoa/dining/venue_info?venue_url_key=` | 1 | Static JS endpoint clue; not live-verified. |
| GET/POST (inferred) | `/api-yoa/venue/dining_widget_settings` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/marketing-status` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/perk_concierges` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/perks` | 1 | Static JS endpoint clue; not live-verified. |
| GET/DELETE (inferred) | `/api-yoa/venue/perks/{E}` | 2 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/venue/perks/{E}?venue_id={v}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/perks?venue_id={v}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/phone-numbers` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/reservation_widget_settings_v2` | 1 | LIVE observed: statuses [401] samples=1 confidence=low |
| POST (inferred) | `/api-yoa/venue/reservation_widget_settings_v2?venue_id={W}` | 3 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/settings` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/settings?venue_id={D_venueId}` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/settings?venue_id={L}` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/side_navigation` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/subscription_widget_settings` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/subscription_widget_settings?venue_id={I}` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/tax_rates` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/upsells/list` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/user_single_venue_user` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{D}/venue_users` | 1 | Static JS endpoint clue; not live-verified. |
| GET/PUT/PATCH (inferred) | `/api-yoa/venue/{D}/venue_users/{L}` | 2 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/{E}/whatsapp/connect` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/{E}/whatsapp/reconnect` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/{I}/go_live` | 1 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/{I}/go_live_extension` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{L}/app_context` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{L}/looker_folders` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{T}/default_availability_settings` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{T}/seating_areas_tables` | 2 | Static JS endpoint clue; not live-verified. |
| POST (inferred) | `/api-yoa/venue/{W}/block` | 1 | Static JS endpoint clue; not live-verified. |
| PUT/PATCH (inferred) | `/api-yoa/venue/{W}/block/{U}` | 1 | Static JS endpoint clue; not live-verified. |
| GET/DELETE (inferred) | `/api-yoa/venue/{W}/block/{V}` | 2 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{W}/blocks` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{v_venueId}/whatsapp/connect` | 1 | Static JS endpoint clue; not live-verified. |
| GET (inferred) | `/api-yoa/venue/{v}/activity_logs/{E}` | 1 | Static JS endpoint clue; not live-verified. |

## 4. DoorDash-specific mapping

| Method | Endpoint template | Interpretation |
|---|---|---|
| GET (inferred) | `/api-yoa/doordash_marketplace` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/cuisine_update?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/image_upload?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/photos_reorder?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/photos_update?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/toggle?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_marketplace/venue_description_update?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_storefront/connect?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |
| POST (inferred) | `/api-yoa/doordash_storefront/disconnect?venue={venue}` | SevenRooms-side DoorDash marketplace/storefront integration clue. Static-only; not confirmed consumer Going Out API. |

## 5. Safety/access classification

| Class | Endpoints | Treatment |
|---|---|---|
| Public read discovery | `/api-yoa/availability/widget/range` | OK for low-frequency read-only discovery; contract still unofficial. |
| Auth/session/config boundary | `/api-yoa/venue/reservation_widget_settings_v2`, `/api-yoa/dining/venue_info` | Live probes showed 401/400 without proper context. |
| Write-sensitive booking | `/api-yoa/dining/hold/add`, `/api-yoa/dining/hold/upgrades` | Do not call without explicit authorization and stop-before-submit guardrails. |
| Payment-sensitive | `/api-yoa/customer-payment-session/`, `/api-yoa/customer-adyen-session/` | Do not call in unauthenticated/public exploration. |
| Partner/admin/private | `/api-yoa/admin/*`, `/api-yoa/manager/*`, `/api-yoa/doordash_*`, booking access/admin paths | Treat as gated; static mapping only. |

## 6. Open questions / missing from safe trace

- Exact payload for `dining/hold/add` and whether it creates a reversible hold or has side effects.
- Exact final reservation creation endpoint and payload.
- DoorDash Going Out consumer-side BFF/GraphQL/mobile operation names.
- Required CSRF/session fields for first-party widget checkout.
- Whether DoorDash normalizes SevenRooms inventory or proxies widget/partner inventory behind a private service.

## 7. Recommended next safe capture

Use an authorized owned browser session, capture request/response bodies, click only through discovery and non-final checkout screens, and stop before final reservation/payment submission. Redact cookies, CSRF tokens, names, emails, phone numbers, card/payment fields, and guest IDs before re-running browser-to-api.
