# Capture Sources

> How to add sources to labs-wiki from any device.

All channels feed into the **Wiki Ingest API** (`wiki-ingest-api/`), which writes standardized markdown files to `raw/`. The `/wiki-ingest` skill then processes them into wiki pages.

---

## 1. Terminal — CLI Functions (`wa` / `waf`)

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Wiki Add — capture text, URL, or note
wa() {
  local type="${1:-text}"
  local content="$2"
  local title="${3:-}"

  if [[ "$type" == "url" && -z "$content" ]]; then
    echo "Usage: wa url <URL> [title]"; return 1
  fi

  if [[ "$type" == "text" && -z "$content" ]]; then
    content=$(cat)  # Read from stdin (pipe support)
  fi

  curl -s -X POST "${WIKI_API_URL:-http://localhost:8000}/api/ingest" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $WIKI_API_TOKEN" \
    -d "$(jq -n --arg t "$type" --arg c "$content" --arg ti "$title" \
      '{type:$t, content:$c, title:$ti, source:"cli"}')" \
    | jq -r '.path // .error'
}

# Wiki Add File — upload a file
waf() {
  local file="$1"
  local title="${2:-$(basename "$file")}"

  curl -s -X POST "${WIKI_API_URL:-http://localhost:8000}/api/ingest/file" \
    -H "Authorization: Bearer $WIKI_API_TOKEN" \
    -F "file=@$file" \
    -F "title=$title" \
    -F "source=cli" \
    | jq -r '.path // .error'
}
```

### Examples

```bash
# Add a URL
wa url https://arxiv.org/abs/2104.09864 "RoPE Paper"

# Add a text note
wa text "Key insight: attention is O(n²) in sequence length" "Attention Complexity"

# Pipe from clipboard
pbpaste | wa text "" "Clipboard Capture"

# Upload a PDF
waf ~/Downloads/paper.pdf "Research Paper"
```

### Required Environment Variables

```bash
export WIKI_API_URL="https://wiki-api.internal"  # or http://localhost:8000
export WIKI_API_TOKEN="your-token-here"
```

---

## 2. Browser — Bookmarklet

Create a bookmark with this URL (replace `YOUR_API_URL` and `TOKEN`):

```javascript
javascript:void(fetch('YOUR_API_URL/api/ingest',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer TOKEN'},body:JSON.stringify({type:'url',content:location.href,title:document.title,source:'bookmarklet'})}).then(r=>r.json()).then(d=>alert('✅ '+d.path)).catch(e=>alert('❌ '+e)))
```

### Setup

1. Right-click your bookmarks bar → "Add page" / "Add bookmark"
2. Name it "📥 Wiki Add"
3. Paste the JavaScript above as the URL
4. Replace `YOUR_API_URL` and `TOKEN` with your values
5. Click the bookmarklet on any page to capture it

---

## 3. Phone — iOS Shortcut

### Setup Steps

1. Open the **Shortcuts** app on iOS
2. Tap **+** to create a new shortcut
3. Name it "Add to Wiki"
4. Add these actions:

| Step | Action | Setting |
|------|--------|---------|
| 1 | Receive **Any** input from **Share Sheet** | — |
| 2 | Get **URLs** from input | — |
| 3 | **Get Contents of URL** | Method: POST |
| | | URL: `https://wiki-api.internal/api/ingest` |
| | | Headers: `Authorization: Bearer <token>` |
| | | Headers: `Content-Type: application/json` |
| | | Body (JSON): `{"type":"url","content":"<URL from step 2>","source":"ios-share"}` |
| 4 | **Show Notification**: "✅ Captured to wiki" | — |

5. In Shortcut settings, enable **Show in Share Sheet**
6. Select the content types: URLs, Text, Images

### Usage

See an article → Share → "Add to Wiki" → done in 3 taps.

### Android — HTTP Shortcuts

[HTTP Shortcuts](https://http-shortcuts.rmy.ch/) is a free, open-source Android app for creating custom HTTP request shortcuts. Install from [Google Play](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts) or [F-Droid](https://f-droid.org/packages/ch.rmy.android.http_shortcuts/).

#### Step 1: Create Global Variables

Shared content from Android's share sheet is received via **global variables** with the "Allow Receiving Value from Share Dialog" option enabled. You must create these **before** building the shortcut.

1. Open HTTP Shortcuts → tap the **⋮ menu** (top-right) → **Global Variables**
2. Tap **+** to create a new variable:

   | Field | Value |
   |-------|-------|
   | **Name** | `shared_text` |
   | **Type** | Static Variable |
   | **Value** | _(leave empty)_ |

3. Scroll down to **Advanced Settings** and enable:
   - ✅ **Allow Receiving Value from Share Dialog**
   - Set **Use shared value as:** → **Text**

4. Create a second variable:

   | Field | Value |
   |-------|-------|
   | **Name** | `shared_title` |
   | **Type** | Static Variable |
   | **Value** | _(leave empty)_ |

5. Same as above — enable **Allow Receiving Value from Share Dialog**, set to **Title / Subject**

#### Step 2: Create a New Shortcut

1. Go back to the main screen → tap **+** → **Regular Shortcut**
2. Name it **"Add to Wiki"**
3. Set icon to 📥 (or any icon you like)

#### Step 3: Configure the Request

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `https://YOUR_API_URL/api/ingest` |

#### Step 4: Add Headers

Tap **Request Headers** → add two entries:

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Authorization` | `Bearer YOUR_TOKEN` |

#### Step 5: Build the Request Body via Scripting

Shared content often contains characters (quotes, `&`, query params) that break JSON when inserted as raw placeholders. Build the body in a **scripting block** instead, where `JSON.stringify` handles escaping.

1. Create one more global variable for the body:

   | Field | Value |
   |-------|-------|
   | **Name** | `request_body` |
   | **Type** | Static Variable |
   | **Value** | `{}` |

2. In the shortcut editor → **Scripting** → **Run before execution** → add:

   ```javascript
   const shared = getVariable("shared_text");
   const title = getVariable("shared_title");

   // Detect if shared content is a URL or plain text
   const urlMatch = shared.match(/https?:\/\/[^\s]+/);
   const type = urlMatch ? "url" : "text";
   const content = urlMatch ? urlMatch[0] : shared;

   const body = JSON.stringify({
     type: type,
     content: content,
     title: title || content.substring(0, 80),
     source: "android-share"
   });

   setVariable("request_body", body);
   ```

3. Set **Request Body** → **Custom Text** → content type `application/json`
4. For the body text, insert just the variable placeholder:

   ```
   {request_body}
   ```

   Use the **{ }** button to insert `request_body`, or type it manually. The entire JSON is built by the script — the body field just passes it through.

#### Step 6: Enable Share Sheet Integration

1. Go to the shortcut's **Trigger & Execution Settings**
2. Enable **Accept shared text from other apps**
3. Optionally enable **Direct Share** (Android 11+) for the shortcut to appear in the Direct Share row

#### Step 7: Configure Response Display

1. In shortcut settings → **Response Handling**
2. Set to **Show as dialog** (for testing) or **Show as toast** (for production use)

#### Step 8: Test It

1. Open Chrome, find an article
2. Tap **Share** → select **"Add to Wiki"**
3. You should see a success response with the `raw/` file path

#### Optional: Home Screen Widget

HTTP Shortcuts supports home screen widgets for one-tap access:
1. Long-press your home screen → **Widgets**
2. Find **HTTP Shortcuts** → drag a 1×1 widget
3. Select your "Add to Wiki" shortcut
4. Tap the widget to trigger a quick-capture dialog

#### Troubleshooting

| Problem | Solution |
|---------|----------|
| "No suitable shortcuts found" | Global variables must have **Allow Receiving Value from Share Dialog** enabled |
| Share sheet doesn't show "Add to Wiki" | Enable **Accept shared text from other apps** in Trigger & Execution Settings |
| 400 Bad Request / invalid type | Shared content has special chars breaking JSON — use the scripting approach in Step 5 |
| `{shared_text}` sent as literal text | Use the **{ }** button to insert placeholders — don't type braces manually |
| 401 error | Double-check the `Authorization` header value |
| Empty content captured | Set **Use shared value as → Text** in the variable's Advanced Settings |
| Want to debug the request | **Response Handling** → **Show as dialog** to see the full API response |

---

## 4. GitHub Issues

Create an issue in the labs-wiki repo with the label `ingest`:

1. Go to https://github.com/jbl306/labs-wiki/issues/new
2. **Title:** The source title
3. **Body:** The content (URL, text, notes)
4. **Label:** Add the `ingest` label

A GitHub Action will automatically:
- Create a `raw/` file from the issue
- Commit it to the repo
- Close the issue with a confirmation comment

---

## 5. ntfy Messages

Send a message to the ntfy topic and the watcher script forwards it to the API:

```bash
# From any device with curl
curl -d "https://interesting-article.com" ntfy.sh/your-wiki-topic

# From a phone using the ntfy app
# Just send a message to your topic
```

### Setup

The ntfy watcher script (`scripts/ntfy-wiki-watcher.sh`) subscribes to the topic and forwards messages. Run it as a background process:

```bash
WIKI_API_URL=http://localhost:8000 \
WIKI_API_TOKEN=your-token \
NTFY_TOPIC=your-wiki-topic \
./scripts/ntfy-wiki-watcher.sh
```

---

## 6. Ingest API Direct

For custom integrations, POST directly to the API:

### JSON (text/URL/note)

```bash
curl -X POST https://wiki-api.internal/api/ingest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"type":"url","content":"https://example.com","title":"Example","tags":["test"]}'
```

### File Upload

```bash
curl -X POST https://wiki-api.internal/api/ingest/file \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@paper.pdf" \
  -F "title=Research Paper" \
  -F "tags=ml,research"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Check `WIKI_API_TOKEN` matches between client and server |
| 413 File Too Large | Files are limited to 15MB |
| Connection refused | Ensure API is running: `curl http://localhost:8000/health` |
| File not appearing in raw/ | Check API logs: `docker logs wiki-ingest-api` |
| ntfy watcher stops | Restart the script; it auto-reconnects |
