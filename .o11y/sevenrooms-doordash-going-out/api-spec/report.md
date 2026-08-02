# Discovered API

**Base URL:** `https://www.sevenrooms.com`

## Quick start

```js
import { get_api_yoa_availability_widget_range, get_api_yoa_venue_reservation_widget_settings_v2, get_api_yoa_dining_venue_info } from './client.mjs';
```

**3 functions**, zero dependencies. See [`client.mjs`](./client.mjs) for full signatures.

## Endpoints

| Method | Path | Samples | Statuses | Confidence |
|---|---|---|---|---|
| GET | `/api-yoa/availability/widget/range` | 3 | 200 | low |
| GET | `/api-yoa/venue/reservation_widget_settings_v2` | 1 | 401 | low |
| GET | `/api-yoa/dining/venue_info` | 1 | 400 | low |

### `GET /api-yoa/availability/widget/range`

<details><summary>Example response</summary>

```json
{
  "status": 200,
  "data": {
    "availability": {
      "2026-06-08": [
        {
          "name": "Dinner",
          "shift_id": "ahNzfnNldmVucm9vbXMtc2VjdXJlcjgLEg9uaWdodGxvb3BfVmVudWUYgICoov3a2AsMCxIPc3JfU2hpZnREZWZhdWx0GICAsfqk5JULDA",
          "shift_persistent_id": "ahNzfnNldmVucm9vbXMtc2VjdXJlchwLEg9uaWdodGxvb3BfVmVudWUYgICoov3a2AsM-DINNER-1647967825.6",
          "shift_category": "DINNER",
          "is_closed": false,
          "is_previous_version": false,
          "is_forced_empty_availability": false,
          "duration_minutes_by_party_size": {
            "1": 105,
            "2": 120,
            "3": 150,
            "4": 165,
            "5": 180,
            "6": 180,
            "7": 180,
            "8": 180,
            "9": 210,
            "-1": 210
          },
          "upsell_categories": [],
          "times": [
            {
              "type": "book",
              "sort_order": 46,
              "time": "5:30 PM",
              "time_iso": "20
  ...
}
```
</details>

## Coverage

- **3** API endpoints discovered
- **2** observed only once
