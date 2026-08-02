# Static SevenRooms dining widget endpoint clues

Source JS: `https://www.sevenrooms.com/static/21bc93acc1900fc2ac156b2a7b1752af5b7844bf/cdn/app/widget/dining.js`
SHA-256: `9da003562adbcb03751414ea015d80b693666463d66887d6f277b071f1574abe`

These strings were extracted from public widget JavaScript. Only `/api-yoa/availability/widget/range` was exercised as a successful public API call in this run. The other paths are booking-flow clues and may require browser state, CSRF, authenticated user state, venue/partner permissions, or payment setup. No mutation endpoint was called.

| Endpoint string | Live-observed in trace? | Notes |
|---|---:|---|
| `/api-yoa/availability/widget/range` | yes | public availability discovery |
| `/api-yoa/availability/ng/widget/range?${lt.toString()}` | no | auth/boundary or booking-flow clue from static JS |
| `/api-yoa/customer-payment-session/` | no | payment-session clue; not called |
| `/api-yoa/customer-payment-session/?customer_payment_session_id=${V}` | no | payment-session clue; not called |
| `/api-yoa/customer-adyen-session/` | no | payment-session clue; not called |
| `/api-yoa/doordash_marketplace` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_marketplace/cuisine_update?venue=${encodeURIComponent(U.venue)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_marketplace/venue_description_update?venue=${encodeURIComponent(U.venue)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_marketplace/photos_update?venue=${encodeURIComponent(U.venue)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_marketplace/photos_reorder?venue=${encodeURIComponent(U.venue)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_marketplace/toggle?venue=${encodeURIComponent(X)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_marketplace/image_upload?venue=${encodeURIComponent(X)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_storefront/connect?venue=${encodeURIComponent(D)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/doordash_storefront/disconnect?venue=${encodeURIComponent(I.venue)}` | no | DoorDash marketplace/storefront configuration clue from static JS; likely partner/admin surface, not consumer booking contract |
| `/api-yoa/availability/widget/experiences/range?${Be}` | no | auth/boundary or booking-flow clue from static JS |
| `/api-yoa/dining/hold/upgrades` | no | probable table-hold/checkout step; not called to avoid live reservation side effects |
| `/api-yoa/dining/hold/add` | no | probable table-hold/checkout step; not called to avoid live reservation side effects |
| `/api-yoa/venue/reservation_widget_settings_v2` | yes | auth/boundary or booking-flow clue from static JS |
| `/api-yoa/venue/reservation_widget_settings_v2?venue_id=${W}` | yes | auth/boundary or booking-flow clue from static JS |
