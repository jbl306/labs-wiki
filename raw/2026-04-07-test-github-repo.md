---
title: htmx - HTML Over The Wire
type: url
captured: 2026-04-07 19:50:00+00:00
source: test
url: https://github.com/bigskysoftware/htmx
tags: []
status: ingested
content_hash: sha256:e722d6e5ab18e3f788f2521907100918c28120d1280c11cfe636a84324954c32
last_refreshed: '2026-04-22T02:44:11+00:00'
---

https://github.com/bigskysoftware/htmx

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:44:11+00:00
- source_url: https://github.com/bigskysoftware/htmx
- resolved_url: https://github.com/bigskysoftware/htmx
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: bigskysoftware/htmx
Description: </> htmx - high power tools for HTML
Stars: 47867
Language: JavaScript
Topics: hateoas, html, htmx, hyperscript, javascript, rest

## README

[![</> htmx](https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/static/img/htmx_logo.1.png "high power tools for HTML")](https://htmx.org)

*high power tools for HTML*

[![Discord](https://img.shields.io/discord/725789699527933952)](https://htmx.org/discord)
[![Netlify](https://img.shields.io/netlify/dba3fc85-d9c9-476a-a35a-e52a632cef78)](https://app.netlify.com/sites/htmx/deploys)
[![Bundlephobia](https://badgen.net/bundlephobia/dependency-count/htmx.org)](https://bundlephobia.com/result?p=htmx.org)
[![Bundlephobia](https://badgen.net/bundlephobia/minzip/htmx.org)](https://bundlephobia.com/result?p=htmx.org)

## introduction

htmx allows you to access  [AJAX](https://htmx.org/docs#ajax), [CSS Transitions](https://htmx.org/docs#css_transitions),
[WebSockets](https://htmx.org/extensions/ws/) and [Server Sent Events](https://htmx.org/extensions/sse/)
directly in HTML, using [attributes](https://htmx.org/reference#attributes), so you can build
[modern user interfaces](https://htmx.org/examples) with the [simplicity](https://en.wikipedia.org/wiki/HATEOAS) and
[power](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm) of hypertext

htmx is small ([~14k min.gz'd](https://cdn.jsdelivr.net/npm/htmx.org/dist/)),
[dependency-free](https://github.com/bigskysoftware/htmx/blob/master/package.json) &
[extendable](https://htmx.org/extensions)

## motivation

* Why should only `<a>` and `<form>` be able to make HTTP requests?
* Why should only `click` & `submit` events trigger them?
* Why should only GET & POST be available?
* Why should you only be able to replace the *entire* screen?

By removing these arbitrary constraints htmx completes HTML as a
[hypertext](https://en.wikipedia.org/wiki/Hypertext)

## quick start

```html
  <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js"    
          integrity="sha384-H5SrcfygHmAuTDZphMHqBJLc3FhssKjG7w/CeCpFReSfwBWDTKpkzPP8c+cLsK+V" 
          crossorigin="anonymous"></script>
  <!-- have a button POST a click via AJAX -->
  <button hx-post="/clicked" hx-swap="outerHTML">
    Click Me
  </button>
```

The [`hx-post`](https://htmx.org/attributes/hx-post) and [`hx-swap`](https://htmx.org/attributes/hx-swap) attributes tell htmx:

> "When a user clicks on this button, issue an AJAX request to /clicked, and replace the entire button with the response"

htmx is the successor to [intercooler.js](http://intercoolerjs.org)

### installing as a node package

To install using npm:

```
npm install htmx.org --save
```

Note there is an old broken package called `htmx`.  This is `htmx.org`.

## website & docs

* <https://htmx.org>
* <https://htmx.org/docs>

## contributing
Want to contribute? Check out our [contribution guidelines](CONTRIBUTING.md)

No time? Then [become a sponsor](https://github.com/sponsors/bigskysoftware#sponsors)

### hacking guide

To develop htmx locally, you will need to install the development dependencies.

Run:

```
npm install
```

Then, run a web server in the root.

This is easiest with:

```
npx serve
```

You can then run the test suite by navigating to:

<http://0.0.0.0:3000/test/>

At this point you can modify `/src/htmx.js` to add features, and then add tests in the appropriate area under `/test`.

* `/test/index.html` - the root test page from which all other tests are included
* `/test/attributes` - attribute specific tests
* `/test/core` - core functionality tests
* `/test/core/regressions.js` - regression tests
* `/test/ext` - extension tests
* `/test/manual` - manual tests that cannot be automated

htmx uses the [mocha](https://mochajs.org/) testing framework, the [chai](https://www.chaijs.com/) assertion framework
and [sinon](https://sinonjs.org/releases/v9/fake-xhr-and-server/) to mock out AJAX requests.  They are all OK.

## haiku

*javascript fatigue:<br/>
longing for a hypertext<br/>
already in hand*

Languages: JavaScript 92.1%, HTML 7.1%, CSS 0.4%, TypeScript 0.2%, Ruby 0.1%, Shell 0.1%

## Recent Releases

### v2.0.9 (2026-04-20)

See CHANGELOG.md for details

### v2.0.7 (2025-09-11)

## What's Changed
* Remove extra "2" from unminified v2.0.6 SRI hash by @danieljsummers in https://github.com/bigskysoftware/htmx/pull/3362
* Bugfix: swap="outerHTML" on <div> with style attribute leaves htmx-swapping class behind by @matthews314 in https://github.com/bigskysoftware/htmx/pull/3341
* Fix variable names by @szepeviktor in https://github.com/bigskysoftware/htmx/pull/3344
* update indicator style to have visibility:hidden for screen readers by @MichaelWest22 in https://github.com/bigskysoftware/htmx/pull/3361
* Cancel button with inner content form submit properly by @MichaelWest2…

### v2.0.6 (2025-06-27)

## What's Changed
* Adding Lua Server Pages server example by @surfskidude in https://github.com/bigskysoftware/htmx/pull/3347
* fix click events on elements wrapped by link don't cancel link navigation by @MichaelWest22 in https://github.com/bigskysoftware/htmx/pull/3357

## New Contributors
* @surfskidude made their first contribution in https://github.com/bigskysoftware/htmx/pull/3347

**Full Changelog**: https://github.com/bigskysoftware/htmx/compare/v2.0.5...v2.0.6

### v2.0.5 (2025-06-20)

## What's Changed
* Add http4k server example by @mikaelstaldal in https://github.com/bigskysoftware/htmx/pull/3012
* Update hx-trigger.md by @zachczx in https://github.com/bigskysoftware/htmx/pull/3076
* Update preload extension documentation: form preloading and preload="always" by @marisst in https://github.com/bigskysoftware/htmx/pull/3001
* Improve active-search example by not using chrome-only event "search" by @MikeMoolenaar in https://github.com/bigskysoftware/htmx/pull/2229
* Add reference to hx-preserve to the example at "Preserving File Inputs after Form Errors" by @Matt544 in https…

### v2.0.4 (2024-12-13)

## What's Changed
* Clarify event filter uses in hx-trigger by @brackendawson in https://github.com/bigskysoftware/htmx/pull/2914
* Fix typos in docs by @szepeviktor in https://github.com/bigskysoftware/htmx/pull/2943
* Add htmx4s to scala server-examples by @eikek in https://github.com/bigskysoftware/htmx/pull/2722
* improve hx-preserve documentation by @MichaelWest22 in https://github.com/bigskysoftware/htmx/pull/2949
* Correct lint command in contribution guidelines by @scrhartley in https://github.com/bigskysoftware/htmx/pull/2950
* docs: Fix typo in URL to prevent broken link redirect by …

## Recent Commits

- 2026-04-21 dbf77dd Carson Gross: add --skipLibCheck to fix build... again
- 2026-04-21 2fdfe05 Carson Gross: add --skipLibCheck to fix build
- 2026-04-21 c87e29d Carson Gross: fix merge
- 2026-04-21 1b3fb3e Carson Gross: Merge remote-tracking branch 'origin/master'
- 2026-04-21 bdc7d7d Carson Gross: 2.10 release prep
- 2026-04-21 20951cc Carson Gross: update libs
- 2026-04-21 1b4f793 dependabot[bot]: Bump playwright from 1.55.0 to 1.56.1 (#3479)
- 2026-04-21 17d349d Carson Gross: Merge remote-tracking branch 'origin/dev' into dev
- 2026-04-21 d53932d MichaelWest22: improve escaping of tag and id in settle lookup (#3752)
- 2026-04-21 013f335 Carson Gross: restore ts file
- 2026-04-20 6ff7c48 Carson Gross: typo
- 2026-04-15 2fe8cc2 Carson Gross: fix URL
- 2026-04-15 b2e8866 Carson Gross: update shas
- 2026-04-15 e14f887 Carson Gross: update dist
- 2026-04-15 ebeca09 Carson Gross: update www
- 2026-04-15 61784fe Carson Gross: update dist
- 2026-04-15 b1ddcce Carson Gross: bump version
- 2026-04-15 294c7ad Carson Gross: 2.0.9 changelog
- 2026-04-15 a67a6a6 Carson Gross: Merge remote-tracking branch 'origin/dev' into dev
- 2026-04-15 8183f07 StabbarN: Preserves pre-disabled elements with hx-disabled-elt on other element (#3443)

## Open Issues (top 10)

- #3765 No GitHub Release for version 2.0.10 (by adamchainz)
- #1911 Support for chunked transfer encoding (by carlos-verdes)
- #3757 Missing types for typescript (by cuboci)
- #3743 Nested OOB swap is performed even though it is off (by AlexLup06)
- #2131 [1.9.10] WebSockets: handling events with `hx-on` seems broken (by haja)
- #2825 Exposing saveCurrentPageToHistory via js API (by Wulfheart)
- #3726 `title` tag not at the top of the response does not update the existing tab title (by metametadata)

## Recently Merged PRs (top 10)

- #3479 Bump playwright from 1.55.0 to 1.56.1 (merged 2026-04-21)
- #3752 improve escaping of tag and id in settle lookup (merged 2026-04-21)
- #3759 update header documentation for retarget-reswap-reselect (merged 2026-04-21)
- #3711 restore hx-on:: shorthand from htmx 2 (merged 2026-03-19)
- #3717 Align WS and SSE extension APIs (merged 2026-03-30)
- #3744 Add support for multiple prefix (merged 2026-04-19)
- #3756 Add auto detection and header based triggering to hx-download extension (merged 2026-04-19)
- #3443 Preserves pre-disabled elements with hx-disabled-elt on other element (merged 2026-04-15)
- #3477 fix history normalizePath relative path normalization (merged 2026-04-15)
- #3715 fix: remove empty class attribute left behind after settle/swap/request (merged 2026-04-15)


## File: .gitignore

```
.idea
*.iml
/node_modules
_site
test/scratch/scratch.html
.DS_Store
.vscode
/coverage

```


## File: dist/ext/README.md

```
# Why Are These Files Here?

These are legacy extensions for htmx 1.x and are **NOT** actively maintained or guaranteed to work with htmx 2.x.
They are here because we unfortunately linked to unversioned unpkg URLs in the installation guides for them
in 1.x, so we need to keep them here to preserve those URLs and not break existing users functionality.

If you are looking for extensions for htmx 2.x, please see the [htmx 2.0 extensions site](https://htmx.org/extensions), 
which has links to the new extensions repos (They have all been moved to their own NPM projects and URLs, like
they should have been from the start!)

```


## File: LICENSE

```
Zero-Clause BSD
=============

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE
FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

```


## File: package-lock.json

```
{
  "name": "htmx.org",
  "version": "2.0.10",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "htmx.org",
      "version": "2.0.10",
      "license": "0BSD",
      "devDependencies": {
        "@types/node": "^22.18.8",
        "@types/parse5": "^7.0.0",
        "@web/test-runner": "^0.20.2",
        "@web/test-runner-playwright": "^0.11.0",
        "chai": "^4.5.0",
        "chai-dom": "^1.12.1",
        "eslint": "^8.57.1",
        "eslint-config-standard": "^17.1.0",
        "eslint-plugin-import": "^2.29.1",
        "eslint-plugin-mocha": "^10.5.0",
        "fs-extra": "^9.1.0",
        "mocha": "^11.7.4",
        "mock-socket": "^9.3.1",
        "sinon": "^10.0.1",
        "typescript": "^5.9.3",
        "uglify-js": "^3.19.3",
        "ws": "^8.18.1"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.29.0",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.29.0.tgz",
      "integrity": "sha512-9NhCeYjq9+3uxgdtp20LSiJXJvN0FeCtNGpJxuMFZ1Kv3cWUNb6DOhJwUvcVCzKGR66cw4njwM6hrJLqgOwbcw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.28.5",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.28.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.28.5.tgz",
      "integrity": "sha512-qSs4ifwzKJSV39ucNjsvc6WVHs6b7S03sOh2OcHF9UHfVPqWWALUsNUVzhSBiItjRZoLHx7nIarVjqKVusUZ1Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.1.tgz",
      "integrity": "sha512-phrYmNiYppR7znFEdqgfWHXR6NCkZEK7hwWDHZUjit/2/U0r6XvkDl0SYnoM51Hq7FhCGdLDT6zxCCOY1hexsQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.2",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.2.tgz",
      "integrity": "sha512-EriSTlt5OC9/7SXkRSCAhfSxxoSUgBm33OH+IkwbdpgoqsSsUg7y3uh+IICI/Qg4BBWr3U2i39RpmycbxMq4ew==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/eslintrc": {
      "version": "2.1.4",
      "resolved": "https://registry.npmjs.org/@eslint/eslintrc/-/eslintrc-2.1.4.tgz",
      "integrity": "sha512-269Z39MS6wVJtsoUl10L60WdkhJVdPG24Q4eZTH3nnF6lpvSShEK3wQjDX9JRWAUPvPh7COouPpU9IrqaZFvtQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ajv": "^6.12.4",
        "debug": "^4.3.2",
        "espree": "^9.6.0",
        "globals": "^13.19.0",
        "ignore": "^5.2.0",
        "import-fresh": "^3.2.1",
        "js-yaml": "^4.1.0",
        "minimatch": "^3.1.2",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint/js": {
      "version": "8.57.1",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-8.57.1.tgz",
      "integrity": "sha512-d9zaMRSTIKDLhctzH12MtXvJKSSUhaHcjV+2Z+GK+EEY7XKpP5yR4x+N3TAcHTcu963nIr+TMcCb4DBCYX1z6Q==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      }
    },
    "node_modules/@hapi/bourne": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/@hapi/bourne/-/bourne-3.0.0.tgz",
      "integrity": "sha512-Waj1cwPXJDucOib4a3bAISsKJVb15MKi9IvmTI/7ssVEm6sywXGjVJDhl6/umt1pK1ZS7PacXU3A1PmFKHEZ2w==",
      "dev": true,
      "license": "BSD-3-Clause"
    },
    "node_modules/@humanwhocodes/config-array": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/config-array/-/config-array-0.13.0.tgz",
      "integrity": "sha512-DZLEEqFWQFiyK6h5YIeynKx7JlvCYWL0cImfSRXZ9l4Sg2efkFGTuFf6vzXjK1cq6IYkU+Eg/JizXw+TD2vRNw==",
      "deprecated": "Use @eslint/config-array instead",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@humanwhocodes/object-schema": "^2.0.3",
        "debug": "^4.3.1",
        "minimatch": "^3.0.5"
      },
      "engines": {
        "node": ">=10.10.0"
      }
    },
    "node_modules/@humanwhocodes/module-importer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/module-importer/-/module-importer-1.0.1.tgz",
      "integrity": "sha512-bxveV4V8v5Yb4ncFTT3rPSgZBOpCkjfK0y4oVVVJwIuDVBRMDXrPyXRL988i5ap9m9bnyEEjWfm5WkBmtffLfA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=12.22"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@humanwhocodes/object-schema": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/object-schema/-/object-schema-2.0.3.tgz",
      "integrity": "sha512-93zYdMES/c1D69yZiKDBj0V24vqNzB/koF26KPaagAfd3P/4gUlh3Dys5ogAK+Exi9QyzlD8x/08Zt7wIKcDcA==",
      "deprecated": "Use @eslint/object-schema instead",
      "dev": true,
      "license": "BSD-3-Clause"
    },
    "node_modules/@isaacs/cliui": {
      "version": "8.0.2",
      "resolved": "https://registry.npmjs.org/@isaacs/cliui/-/cliui-8.0.2.tgz",
      "integrity": "sha512-O8jcjabXaleOG9DQ0+ARXWZBTfnP4WNAqzuiJK7ll44AmxGKv/J2M4TPjxjY3znBCfvBXFzucm1twdyFybFqEA==",
      "dev": true,
      "license": "ISC",
      "dependencies": {
        "string-width": "^5.1.2",
        "string-width-cjs": "npm:string-width@^4.2.0",
        "strip-ansi": "^7.0.1",
        "strip-ansi-cjs": "npm:strip-ansi@^6.0.1",
        "wrap-ansi": "^8.1.0",
        "wrap-ansi-cjs": "npm:wrap-ansi@^7.0.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/ansi-regex": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-6.2.2.tgz",
      "integrity": "sha512-Bq3SmSpyFHaWjPk8If9yc6svM8c56dB5BAtW4Qbw5jHTwwXXcTLoRMkpDJp6VL0XzlWaCHTXrkFURMYmD0sLqg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-regex?sponsor=1"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/ansi-styles": {
      "version": "6.2.3",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-6.2.3.tgz",
      "integrity": "sha512-4Dj6M28JB+oAH8kFkTLUo+a2jwOFkuqb3yucU0CANcRRUbxS0cP0nZYCGjcc3BNXwRIsUVmDGgzawme7zvJHvg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/strip-ansi": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-7.2.0.tgz",
      "integrity": "sha512-yDPMNjp4WyfYBkHnjIRLfca1i6KMyGCtsVgoKe/z1+6vukgaENdgGBZt+ZmKPc4gavvEZ5OgHfHdrazhgNyG7w==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^6.2.2"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/strip-ansi?sponsor=1"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/wrap-ansi": {
      "version": "8.1.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-8.1.0.tgz",
      "integrity": "sha512-si7QWI6zUMq56bESFvagtmzMdGOtoxfR+Sez11Mobfc7tm+VkUckk9bW2UeffTGVUbOksxmSw0AA2gs8g71NCQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^6.1.0",
        "string-width": "^5.0.1",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@nodelib/fs.scandir": {
      "version": "2.1.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.scandir/-/fs.scandir-2.1.5.tgz",
      "integrity": "sha512-vq24Bq3ym5HEQm2NKCr3yXDwjc7vTsEThRDnkp2DK9p1uqLR+DHurm/NOTo0KG7HYHU7eppKZj3MyqYuMBf62g==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "2.0.5",
        "run-parallel": "^1.1.9"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.stat": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.stat/-/fs.stat-2.0.5.tgz",
      "integrity": "sha512-RkhPPp2zrqDAQA/2jNhnztcPAlv64XdhIp7a7454A5ovI7Bukxgt7MX7udwAu3zg1DcpPU0rz3VV1SeaqvY4+A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.walk": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.walk/-/fs.walk-1.2.8.tgz",
      "integrity": "sha512-oGB+UxlgWcgQkgwo8GcEGwemoTFt3FIO9ababBmaGwXIoBKZ+GTy0pP185beGg7Llih/NSHSV2XAs1lnznocSg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.scandir": "2.1.5",
        "fastq": "^1.6.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@pkgjs/parseargs": {
      "version": "0.11.0",
      "resolved": "https://registry.npmjs.org/@pkgjs/parseargs/-/parseargs-0.11.0.tgz",
      "integrity": "sha512-+1VkjdD0QBLPodGrJUeqarH8VAIvQODIbwh9XpP5Syisf7YoQgsJKPNFoqqLQlu+VQ/tVSshMR6loPMn8U+dPg==",
      "dev": true,
      "license": "MIT",
      "optional": true,
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/@puppeteer/browsers": {
      "version": "2.13.0",
      "resolved": "https://registry.npmjs.org/@puppeteer/browsers/-/browsers-2.13.0.tgz",
      "integrity": "sha512-46BZJYJjc/WwmKjsvDFykHtXrtomsCIrwYQPOP7VfMJoZY2bsDF9oROBABR3paDjDcmkUye1Pb1BqdcdiipaWA==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "debug": "^4.4.3",
        "extract-zip": "^2.0.1",
        "progress": "^2.0.3",
        "proxy-agent": "^6.5.0",
        "semver": "^7.7.4",
        "tar-fs": "^3.1.1",
        "yargs": "^17.7.2"
      },
      "bin": {
        "browsers": "lib/cjs/main-cli.js"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@puppeteer/browsers/node_modules/semver": {
      "version": "7.7.4",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.4.tgz",
      "integrity": "sha512-vFKC2IEtQnVhpT78h1Yp8wzwrf8CM+MzKMHGJZfBtzhZNycRFnXsHk6E5TxIkkMsgNS7mdX3AGB7x2QM2di4lA==",
      "dev": true,
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@rollup/plugin-node-resolve": {
      "version": "15.3.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-node-resolve/-/plugin-node-resolve-15.3.1.tgz",
      "integrity": "sha512-tgg6b91pAybXHJQMAAwW9VuWBO6Thi+q7BCNARLwSqlmsHz0XYURtGvh/AuwSADXSI4h/2uHbs7s4FzlZDGSGA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^5.0.1",
        "@types/resolve": "1.20.2",
        "deepmerge": "^4.2.2",
        "is-module": "^1.0.0",
        "resolve": "^1.22.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "rollup": "^2.78.0||^3.0.0||^4.0.0"
      },
      "peerDependenciesMeta": {
        "rollup": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/pluginutils": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/@rollup/pluginutils/-/pluginutils-5.3.0.tgz",
      "integrity": "sha512-5EdhGZtnu3V88ces7s53hhfK5KSASnJZv8Lulpc04cWO3REESroJXg73DFsOmgbU2BhwV0E20bu2IDZb3VKW4Q==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@types/estree": "^1.0.0",
        "estree-walker": "^2.0.2",
        "picomatch": "^4.0.2"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0||^3.0.0||^4.0.0"
      },
      "peerDependenciesMeta": {
        "rollup": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/pluginutils/node_modules/picomatch": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-4.0.4.tgz",
      "integrity": "sha512-QP88BAKvMam/3NxH6vj2o21R6MjxZUAd6nlwAS/pnGvN9IVLocLHxGYIzFhg6fUQ+5th6P4dv4eW9jX3DSIj7A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.60.2",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.60.2.tgz",
      "integrity": "sha512-dnlp69efPPg6Uaw2dVqzWRfAWRnYVb1XJ8CyyhIbZeaq4CA5/mLeZ1IEt9QqQxmbdvagjLIm2ZL8BxXv5lH4Yw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.60.2",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.60.2.tgz",
      "integrity": "sha512-OqZTwDRDchGRHHm/hwLOL7uVPB9aUvI0am/eQuWMNyFHf5PSEQmyEeYYheA0EPPKUO/l0uigCp+iaTjoLjVoHg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-darwin-arm64": {
      "version": "4.60.2",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-arm64/-/rollup-darwin-arm64-4.60.2.tgz",
      "integrity": "sha512-UwRE7CGpvSVEQS8gUMBe1uADWjNnVgP3Iusyda1nSRwNDCsRjnGc7w6El6WLQsXmZTbLZx9cecegumcitNfpmA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "dar
```


## File: package.json

```
{
  "name": "htmx.org",
  "description": "high power tools for html",
  "keywords": [
    "AJAX",
    "HTML"
  ],
  "version": "2.0.10",
  "homepage": "https://htmx.org/",
  "bugs": {
    "url": "https://github.com/bigskysoftware/htmx/issues"
  },
  "license": "0BSD",
  "files": [
    "LICENSE",
    "README.md",
    "dist/htmx.esm.d.ts",
    "dist/*.js",
    "dist/ext/*.js",
    "dist/*.js.gz",
    "editors/jetbrains/htmx.web-types.json"
  ],
  "main": "dist/htmx.esm.js",
  "types": "dist/htmx.esm.d.ts",
  "jsdelivr": "dist/htmx.min.js",
  "unpkg": "dist/htmx.min.js",
  "web-types": "editors/jetbrains/htmx.web-types.json",
  "scripts": {
    "dist": "./scripts/dist.sh && npm run types-generate && npm run web-types-generate",
    "lint": "eslint src/htmx.js test/attributes/ test/core/ test/util/ scripts/*.mjs",
    "format": "eslint --fix src/htmx.js test/attributes/ test/core/ test/util/ scripts/*.mjs",
    "types-check": "tsc src/htmx.js --noEmit --checkJs --target es6 --lib dom,dom.iterable --moduleResolution node --skipLibCheck",
    "types-generate": "tsc dist/htmx.esm.js --declaration --emitDeclarationOnly --allowJs --skipLibCheck --outDir dist",
    "test": "npm run lint && npm run types-check && npm run test:chrome",
    "test:debug": "web-test-runner --manual --open",
    "test:chrome": "playwright install chromium && web-test-runner --browsers chromium --playwright",
    "test:firefox": "playwright install firefox && web-test-runner --concurrency 1 --browsers firefox --playwright",
    "test:webkit": "playwright install webkit && web-test-runner --browsers webkit --playwright",
    "test:all": "playwright install chromium firefox webkit && web-test-runner --concurrency 1 --browsers chromium firefox webkit --playwright",
    "test:ci": "npm run lint && npm run types-check && npm run test:all",
    "ws-tests": "cd ./test/ws-sse && node ./server.js",
    "web-types-generate": "node ./scripts/generate-web-types.mjs",
    "www": "bash ./scripts/www.sh",
    "sha": "bash ./scripts/sha.sh",
    "update-sha": "bash ./scripts/update-sha.sh"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/bigskysoftware/htmx.git"
  },
  "eslintConfig": {
    "extends": ["standard", "plugin:mocha/recommended"],
    "rules": {
      "mocha/consistent-spacing-between-blocks": 0,
      "mocha/no-setup-in-describe": 0,
      "mocha/no-skipped-tests": 0,
      "camelcase": 0,
      "no-var": 0,
      "no-undef": 0,
      "eqeqeq": 0,
      "no-multi-str": 0,
      "no-prototype-builtins": 0,
      "no-cond-assign": 0,
      "no-empty": 0,
      "no-eval": 0,
      "no-new-func": 0,
      "no-redeclare": 0,
      "no-return-assign": 0,
      "no-unused-vars": 0,
      "no-useless-call": 0,
      "no-useless-escape": 0,
      "no-unused-expressions": 0,
      "no-restricted-properties": ["error", {
          "property": "substr",
          "message": "Use .slice or .substring instead of .substr"
      }],
      "space-before-function-paren": [
        "error",
        "never"
      ]
    }
  },
  "devDependencies": {
    "@types/node": "^22.18.8",
    "@types/parse5": "^7.0.0",
    "@web/test-runner": "^0.20.2",
    "@web/test-runner-playwright": "^0.11.0",
    "chai": "^4.5.0",
    "chai-dom": "^1.12.1",
    "eslint": "^8.57.1",
    "eslint-config-standard": "^17.1.0",
    "eslint-plugin-import": "^2.29.1",
    "eslint-plugin-mocha": "^10.5.0",
    "fs-extra": "^9.1.0",
    "mocha": "^11.7.4",
    "mock-socket": "^9.3.1",
    "sinon": "^10.0.1",
    "typescript": "^5.9.3",
    "uglify-js": "^3.19.3",
    "ws": "^8.18.1"
  }
}

```


## File: www/.gitignore

```
public/**

```


## File: www/README.md

```
## Running The Website Locally

The htmx.org website is built with [Zola](https://www.getzola.org/).
To run the site, [install Zola](https://www.getzola.org/documentation/getting-started/installation/); then, from the root of the repository:

```
cd www
zola serve
```

The site should then be available at <http://localhost:1111>

```


## File: www/content/examples/_index.md

```
+++
title = "Examples"
insert_anchor_links = "heading"
+++

## Server-side Integration Examples

A list of [GitHub repositories showing examples of integration](@/server-examples.md) with a wide variety of
server-side languages and platforms, including JavaScript, Python, Java, and many others.

## UI Examples

Below are a set of UX patterns implemented in htmx with minimal HTML and styling.

You can copy and paste them and then adjust them for your needs.

| Pattern                                                                     | Description                                                                                                                                        |
|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| [Click To Edit](@/examples/click-to-edit.md)                                | Demonstrates inline editing of a data object                                                                                                       |
| [Bulk Update](@/examples/bulk-update.md)                                    | Demonstrates bulk updating of multiple rows of data                                                                                                |
| [Click To Load](@/examples/click-to-load.md)                                | Demonstrates clicking to load more rows in a table                                                                                                 |
| [Delete Row](@/examples/delete-row.md)                                      | Demonstrates row deletion in a table                                                                                                               |
| [Edit Row](@/examples/edit-row.md)                                          | Demonstrates how to edit rows in a table                                                                                                           |
| [Lazy Loading](@/examples/lazy-load.md)                                     | Demonstrates how to lazy load content                                                                                                              |
| [Inline Validation](@/examples/inline-validation.md)                        | Demonstrates how to do inline field validation                                                                                                     |
| [Infinite Scroll](@/examples/infinite-scroll.md)                            | Demonstrates infinite scrolling of a page                                                                                                          |
| [Active Search](@/examples/active-search.md)                                | Demonstrates the active search box pattern                                                                                                         |
| [Progress Bar](@/examples/progress-bar.md)                                  | Demonstrates a job-runner like progress bar                                                                                                        |
| [Value Select](@/examples/value-select.md)                                  | Demonstrates making the values of a select dependent on another select                                                                             |
| [Animations](@/examples/animations.md)                                      | Demonstrates various animation techniques                                                                                                          |
| [File Upload](@/examples/file-upload.md)                                    | Demonstrates how to upload a file via ajax with a progress bar                                                                                     |
| [Preserving File Inputs after Form Errors](@/examples/file-upload-input.md) | Demonstrates how to preserve file inputs after form errors                                                                                         |
| [Reset User Input](@/examples/reset-user-input.md)                          | Demonstrates how to reset form inputs after submission                                                                                             |
| [Dialogs - Browser](@/examples/dialogs.md)                                  | Demonstrates the prompt and confirm dialogs                                                                                                        |
| [Dialogs - UIKit](@/examples/modal-uikit.md)                                | Demonstrates modal dialogs using UIKit                                                                                                             |
| [Dialogs - Bootstrap](@/examples/modal-bootstrap.md)                        | Demonstrates modal dialogs using Bootstrap                                                                                                         |
| [Dialogs - Custom](@/examples/modal-custom.md)                              | Demonstrates modal dialogs from scratch                                                                                                            |
| [Tabs (Using HATEOAS)](@/examples/tabs-hateoas.md)                          | Demonstrates how to display and select tabs using HATEOAS principles                                                                               |
| [Tabs (Using JavaScript)](@/examples/tabs-javascript.md)                    | Demonstrates how to display and select tabs using JavaScript                                                                                       |
| [Keyboard Shortcuts](@/examples/keyboard-shortcuts.md)                      | Demonstrates how to create keyboard shortcuts for htmx enabled elements                                                                            |
| [Drag & Drop / Sortable](@/examples/sortable.md)                            | Demonstrates how to use htmx with the Sortable.js plugin to implement drag-and-drop reordering                                                     |
| [Updating Other Content](@/examples/update-other-content.md)                | Demonstrates how to update content beyond just the target elements                                                                                 |
| [Confirm](@/examples/confirm.md)                                            | Demonstrates how to implement a custom confirmation dialog with htmx                                                                               |
| [Async Authentication](@/examples/async-auth.md)                            | Demonstrates how to handle async authentication tokens in htmx                                                                                     |
| [Web Components](@/examples/web-components.md)                              | Demonstrates how to integrate htmx with web components and shadow DOM                                                                              |
| [(Experimental) moveBefore()-powered hx-preserve](/examples/move-before)    | htmx will use the experimental [`moveBefore()`](https://cr-status.appspot.com/feature/5135990159835136) API for moving elements, if it is present. |

## Migrating from Hotwire / Turbo ?

For common practices see the [Hotwire / Turbo to htmx Migration Guide](@/migration-guide-hotwire-turbo.md).

```


## File: www/content/examples/active-search.md

```
+++
title = "Active Search"
template = "demo.html"
+++

This example actively searches a contacts database as the user enters text.

We start with a search input and an empty table:

```html
<h3>
  Search Contacts
  <span class="htmx-indicator">
    <img src="/img/bars.svg" alt=""/> Searching...
   </span>
</h3>
<input class="form-control" type="search"
       name="search" placeholder="Begin Typing To Search Users..."
       hx-post="/search"
       hx-trigger="input changed delay:500ms, keyup[key=='Enter'], load"
       hx-target="#search-results"
       hx-indicator=".htmx-indicator">

<table class="table">
    <thead>
    <tr>
      <th>First Name</th>
      <th>Last Name</th>
      <th>Email</th>
    </tr>
    </thead>
    <tbody id="search-results">
    </tbody>
</table>
```

The input issues a `POST` to `/search` on the [`input`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/input_event) event and sets the body of the table to be the resulting content.

We add the `delay:500ms` modifier to the trigger to delay sending the query until the user stops typing.  Additionally,
we add the `changed` modifier to the trigger to ensure we don't send new queries when the user doesn't change the
value of the input (e.g. they hit an arrow key, or pasted the same value).

We can use multiple triggers by separating them with a comma, this way we add 2 more triggers:
- `keyup[key=='Enter']` triggers once enter is pressed. We use [event filters](/attributes/hx-trigger#standard-event-filters) here to check for [the key property in the KeyboardEvent object](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/key).
- `load` in order to show all results initially on load.

Finally, we show an indicator when the search is in flight with the `hx-indicator` attribute.

{{ demoenv() }}

<script>
    
    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    // routes
    init("/init", function(request, params){
      return searchUI();
    });
    
    onPost(/\/search.*/, function(request, params){
        var search = params['search'];
        var contacts = dataStore.findContactsMatching(search);
        return resultsUI(contacts);
      });
      
    // templates
    function searchUI() {
      return `  <h3>
Search Contacts
<span class="htmx-indicator">
<img src="/img/bars.svg" alt=""/> Searching...
</span>
</h3>

<input class="form-control" type="search"
       name="search" placeholder="Begin Typing To Search Users..."
       hx-post="/search"
       hx-trigger="input changed delay:500ms, keyup[key=='Enter'], load"
       hx-target="#search-results"
       hx-indicator=".htmx-indicator">

<table class="table">
<thead>
<tr>
  <th>First Name</th>
  <th>Last Name</th>
  <th>Email</th>
</tr>
</thead>
<tbody id="search-results">
</tbody>
</table>`;
    }
    
    function resultsUI(contacts){
        var txt = "";
        for (var i = 0; i < contacts.length; i++) {
          var c = contacts[i];
          txt += "<tr><td>" + c.FirstName + "</td><td>" + c.LastName + "</td><td>" + c.Email + "</td></tr>\n";
        }
        return txt;  
    }
    
    //datastore
    
     var dataStore = function(){
          var data = [
            { "FirstName": "Venus", "LastName": "Grimes", "Email": "lectus.rutrum@Duisa.edu", "City": "Ankara" },
            { "FirstName": "Fletcher", "LastName": "Owen", "Email": "metus@Aenean.org", "City": "Niort" },
            { "FirstName": "William", "LastName": "Hale", "Email": "eu.dolor@risusodio.edu", "City": "Te Awamutu" },
            { "FirstName": "TaShya", "LastName": "Cash", "Email": "tincidunt.orci.quis@nuncnullavulputate.co.uk", "City": "Titagarh" },
            { "FirstName": "Kevyn", "LastName": "Hoover", "Email": "tristique.pellentesque.tellus@Cumsociis.co.uk", "City": "Cuenca" },
            { "FirstName": "Jakeem", "LastName": "Walker", "Email": "Morbi.vehicula.Pellentesque@faucibusorci.org", "City": "St. Andrä" },
            { "FirstName": "Malcolm", "LastName": "Trujillo", "Email": "sagittis@velit.edu", "City": "Fort Resolution" },
            { "FirstName": "Wynne", "LastName": "Rice", "Email": "augue.id@felisorciadipiscing.edu", "City": "Kinross" },
            { "FirstName": "Evangeline", "LastName": "Klein", "Email": "adipiscing.lobortis@sem.org", "City": "San Giovanni in Galdo" },
            { "FirstName": "Jennifer", "LastName": "Russell", "Email": "sapien.Aenean.massa@risus.com", "City": "Laives/Leifers" },
            { "FirstName": "Rama", "LastName": "Freeman", "Email": "Proin@quamPellentesquehabitant.net", "City": "Flin Flon" },
            { "FirstName": "Jena", "LastName": "Mathis", "Email": "non.cursus.non@Phaselluselit.com", "City": "Fort Simpson" },
            { "FirstName": "Alexandra", "LastName": "Maynard", "Email": "porta.elit.a@anequeNullam.ca", "City": "Nazilli" },
            { "FirstName": "Tallulah", "LastName": "Haley", "Email": "ligula@id.net", "City": "Bay Roberts" },
            { "FirstName": "Timon", "LastName": "Small", "Email": "velit.Quisque.varius@gravidaPraesent.org", "City": "Girona" },
            { "FirstName": "Randall", "LastName": "Pena", "Email": "facilisis@Donecconsectetuer.edu", "City": "Edam" },
            { "FirstName": "Conan", "LastName": "Vaughan", "Email": "luctus.sit@Classaptenttaciti.edu", "City": "Nadiad" },
            { "FirstName": "Dora", "LastName": "Allen", "Email": "est.arcu.ac@Vestibulumante.co.uk", "City": "Renfrew" },
            { "FirstName": "Aiko", "LastName": "Little", "Email": "quam.dignissim@convallisest.net", "City": "Delitzsch" },
            { "FirstName": "Jessamine", "LastName": "Bauer", "Email": "taciti.sociosqu@nibhvulputatemauris.co.uk", "City": "Offida" },
            { "FirstName": "Gillian", "LastName": "Livingston", "Email": "justo@atiaculisquis.com", "City": "Saskatoon" },
            { "FirstName": "Laith", "LastName": "Nicholson", "Email": "elit.pellentesque.a@diam.org", "City": "Tallahassee" },
            { "FirstName": "Paloma", "LastName": "Alston", "Email": "cursus@metus.org", "City": "Cache Creek" },
            { "FirstName": "Freya", "LastName": "Dunn", "Email": "Vestibulum.accumsan@metus.co.uk", "City": "Heist-aan-Zee" },
            { "FirstName": "Griffin", "LastName": "Rice", "Email": "justo@tortordictumeu.net", "City": "Montpelier" },
            { "FirstName": "Catherine", "LastName": "West", "Email": "malesuada.augue@elementum.com", "City": "Tarnów" },
            { "FirstName": "Jena", "LastName": "Chambers", "Email": "erat.Etiam.vestibulum@quamelementumat.net", "City": "Konya" },
            { "FirstName": "Neil", "LastName": "Rodriguez", "Email": "enim@facilisis.com", "City": "Kraków" },
            { "FirstName": "Freya", "LastName": "Charles", "Email": "metus@nec.net", "City": "Arzano" },
            { "FirstName": "Anastasia", "LastName": "Strong", "Email": "sit@vitae.edu", "City": "Polpenazze del Garda" },
            { "FirstName": "Bell", "LastName": "Simon", "Email": "mollis.nec.cursus@disparturientmontes.ca", "City": "Caxias do Sul" },
            { "FirstName": "Minerva", "LastName": "Allison", "Email": "Donec@nequeIn.edu", "City": "Rio de Janeiro" },
            { "FirstName": "Yoko", "LastName": "Dawson", "Email": "neque.sed@semper.net", "City": "Saint-Remy-Geest" },
            { "FirstName": "Nadine", "LastName": "Justice", "Email": "netus@et.edu", "City": "Calgary" },
            { "FirstName": "Hoyt", "LastName": "Rosa", "Email": "Nullam.ut.nisi@Aliquam.co.uk", "City": "Mold" },
            { "FirstName": "Shafira", "LastName": "Noel", "Email": "tincidunt.nunc@non.edu", "City": "Kitzbühel" },
            { "FirstName": "Jin", "LastName": "Nunez", "Email": "porttitor.tellus.non@venenatisamagna.net", "City": "Dreieich" },
            { "FirstName": "Barbara", "LastName": "Gay", "Email": "est.congue.a@elit.com", "City": "Overland Park" },
            { "FirstName": "Riley", "LastName": "Hammond", "Email": "tempor.diam@sodalesnisi.net", "City": "Smoky Lake" },
            { "FirstName": "Molly", "LastName": "Fulton", "Email": "semper@Naminterdumenim.net", "City": "Montese" },
            { "FirstName": "Dexter", "LastName": "Owen", "Email": "non.ante@odiosagittissemper.ca", "City": "Bousval" },
            { "FirstName": "Kuame", "LastName": "Merritt", "Email": "ornare.placerat.orci@nisinibh.ca", "City": "Solingen" },
            { "FirstName": "Maggie", "LastName": "Delgado", "Email": "Nam.ligula.elit@Cum.org", "City": "Tredegar" },
            { "FirstName": "Hanae", "LastName": "Washington", "Email": "nec.euismod@adipiscingelit.org", "City": "Amersfoort" },
            { "FirstName": "Jonah", "LastName": "Cherry", "Email": "ridiculus.mus.Proin@quispede.edu", "City": "Acciano" },
            { "FirstName": "Cheyenne", "LastName": "Munoz", "Email": "at@molestiesodalesMauris.edu", "City": "Saint-L?onard" },
            { "FirstName": "India", "LastName": "Mack", "Email": "sem.mollis@Inmi.co.uk", "City": "Maryborough" },
            { "FirstName": "Lael", "LastName": "Mcneil", "Email": "porttitor@risusDonecegestas.com", "City": "Livorno" },
            { "FirstName": "Jillian", "LastName": "Mckay", "Email": "vulputate.eu.odio@amagnaLorem.co.uk", "City": "Salvador" },
            { "FirstName": "Shaine", "LastName": "Wright", "Email": "malesuada@pharetraQuisqueac.org", "City": "Newton Abbot" },
            { "FirstName": "Keane", "LastName": "Richmond", "Email": "nostra.per.inceptos@euismodurna.org", "City": "Canterano" },
            { "FirstName": "Samuel", "LastName": "Davis", "Email": "felis@euenim.com", "City": "Peterhead" },
            { "FirstName": "Zelenia", "LastName": "Sheppard", "Email": "Quisque.nonummy@antelectusconvallis.org", "City": "Motta Visconti" },
            { "FirstName": "Giacomo", "LastName": "Cole", "Email": "aliquet.libero@urnaUttincidunt.ca", "City": "Donnas" },
            { "FirstName": "Mason", "LastName": "Hinton", "Email": "est@Nunc.co.uk", "City": "St. Asaph" },
            { "FirstName": "Katelyn", "LastName": "Koch", "Email": "velit.Aliquam@Suspendisse.edu", "City": "Cleveland" },
            { "FirstName": "Olga", "LastName": "Spencer", "Email": "faucibus@Praesenteudui.net", "City": "Karapınar" },
            { "FirstName": "Erasmus", "LastName": "Strong", "Email": "dignissim.lacus@euarcu.net", "City": "Passau" },
            { "FirstName": "Regan", "LastName": "Cline", "Email": "vitae.erat.vel@lacusEtiambibendum.co.uk", "City": "Pergola" },
            { "FirstName": "Stone", "LastName": "Holt", "Email": "eget.mollis.lectus@Aeneanegestas.ca", "City": "Houston" },
            { "FirstName": "Deanna", "LastName": "Branch", "Email": "turpis@estMauris.net", "City": "Olcenengo" },
            { "FirstName": "Rana", "LastName": "Green", "Email": "metus@conguea.edu", "City": "Onze-Lieve-Vrouw-Lombeek" },
            { "FirstName": "Caryn", "LastName": "Henson", "Email": "Donec.sollicitudin.adipiscing@sed.net", "City": "Kington" },
            { "FirstName": "Clarke", "LastName": "Stein", "Email": "nec@mollis.co.uk", "City": "Tenali" },
            { "FirstName": "Kelsie", "LastName": "Porter", "Email": "Cum@gravidaAliquam.com", "City": "İskenderun" },
            { "FirstName": "Cooper", "LastName": "Pugh", "Email": "Quisque.ornare.tortor@dictum.co.uk", "City": "Delhi" },
            { "FirstName": "Paul", "LastName": "Spencer", "Email": "ac@InfaucibusMorbi.com", "City": "Biez" },
            { "FirstName": "Cassady", "LastName": "Farrell", "Email": "Suspendisse.non@venenatisa.net", "City": "New Maryland" },
            { "FirstName": "Sydnee", "LastName": "Velazquez", "Email": "mollis@loremfringillaornare.com", "City": "Strée" },
            { "FirstName": "Felix", "LastName": "Boyle", "Email": "id.libero.Donec@aauctor.org", "City": "Edinburgh" },
            { "FirstName": "Ryder", "LastName": "House", "Email": "molestie@natoquepenatibus.org", "City": "Copertino" },
            { "FirstName": "Hadley", "LastName": "Holcomb", "Email": "penatibus@nisi.ca", "City": "Avadi" },
            { "FirstName": "Marsden", "LastName": "Nunez", "Email": "Nulla.eget.metus@facilisisvitaeorci.org", "City": "New Galloway" },
            { "FirstName": "Alana", "LastName": "Powell", "Email": "non.lobortis.quis@interdumfeugiatSed.net", "City": "Pitt Meadows" },
            { "FirstName": "Dennis", "LastName": "Wyatt", "Email": "Morbi.non@nibhQuisquenonummy.ca", "City": "Wrexham" },
            { "FirstName": "Karleigh", "LastName": "Walton", "Email": "nascetur.ridiculus@quamdignissimpharetra.com", "City": "Diksmuide" },
            { "FirstName": "Brielle", "LastName": "Donovan", "Email": "placerat@at.edu", "City": "Kolmont" },
            { "FirstName": "Donna", "LastName": "Dickerson", "Email": "lacus.pede.sagittis@lacusvestibulum.com", "City": "Vallepietra" },
            { "FirstName": "Eagan", "LastName": "Pate", "Email": "est.Nunc@cursusNunc.ca", "City": "Durness" },
            { "FirstName": "Carlos", "LastName": "Ramsey", "Email": "est.ac.facilisis@duinec.co.uk", "City": "Tiruvottiyur" },
            { "FirstName": "Regan", "LastName": "Murphy", "Email": "lectus.Cum@aptent.com", "City": "Candidoni" },
            { "FirstName": "Claudia", "LastName": "Spence", "Email": "Nunc.lectus.pede@aceleifend.co.uk", "City": "Augusta" },
            { "FirstName": "Genevieve", "LastName": "Parker", "Email": "ultrices@inaliquetlobortis.net", "City": "Forbach" },
            { "FirstName": "Marshall", "LastName": "Allison", "Email": "erat.semper.rutrum@odio.org", "City": "Landau" },
            { "FirstName": "Reuben", "LastName": "Davis", "Email": "Donec@auctorodio.edu", "City": "Schönebeck" },
            { "FirstName": "Ralph", "LastName": "Doyle", "Email": "pede.Suspendisse.dui@Curabitur.org", "City": "Linkebeek" },
            { "FirstName": "Constance", "LastName": "Gilliam", "Email": "mollis@Nulla.edu", "City": "Enterprise" },
            { "FirstName": "Serina", "LastName": "Jacobson", "Email": "dictum.augue@ipsum.net", "City": "Hérouville-Saint-Clair" },
            { "FirstName": "Charity", "LastName": "Byrd", "Email": "convallis.ante.lectus@scelerisquemollisPhasellus.co.uk", "City": "Brussegem" },
            { "FirstName": "Hyatt", "LastName": "Bird", "Email": "enim.Nunc.ut@nonmagnaNam.com", "City": "Gdynia" },
            { "FirstName": "Brent", "LastName": "Dunn", "Email": "ac.sem@nuncid.com", "City": "Hay-on-Wye" },
            { "FirstName": "Casey", "LastName": "Bonner", "Email": "id@ornareelitelit.edu", "City": "Kearny" },
            { "FirstName": "Hakeem", "LastName": "Gill", "Email": "dis@nonummyipsumnon.org", "City": "Portico e San Benedetto" },
            { "FirstName": "Stewart", "LastName": "Meadows", "Email": "Nunc.pulvinar.arcu@convallisdolorQuisque.net", "City": "Dignano" },
            { "FirstName": "Nomlanga", "LastName": "Wooten", "Email": "inceptos@turpisegestas.ca", "City": "Troon" },
            { "FirstName": "Sebastian", "LastName": "Watts", "Email": "Sed.diam.lorem@lorem.co.uk", "City": "Palermo" },
            { "FirstName": "Chelsea", "LastName": "Larsen", "Email": "ligula@Nam.net", "City": "Poole" },
            { "FirstName": "Cameron", "LastName": "Humphrey", "Email": "placerat@id.org", "City": "Manfredonia" },
            { "FirstName": "Juliet", "LastName": "Bush", "Email": "consectetuer.euismod@vitaeeratVivamus.co.uk", "City": "Lavacherie" },
            { "FirstName": "Caryn", "LastName": "Hooper", "Email": "eu.enim.Etiam@ridiculus.org", "City": "Amelia" }
          ];
          return {
            findContactsMatching : function(str) {
              var result = [];
              var s = str.toLowerCase();
              for (var i = 0; i < data.length; i++) {
                var c = data[i];
                if(c['FirstName'].toLowerCase().indexOf(s) >= 0 || c['LastName'].toLowerCase().indexOf(s) >= 0 || c['Email'].toLowerCase().in
```


## File: www/content/examples/animations.md

```
+++
title = "Animations"
template = "demo.html"
+++

htmx is designed to allow you to use [CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions)
to add smooth animations and transitions to your web page using only CSS and HTML.  Below are a few examples of
various animation techniques.

htmx also allows you to use the new [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
for creating animations.

### Basic CSS Animations {#basic}

### Color Throb

The simplest animation technique in htmx is to keep the `id` of an element stable across a content swap.  If the
`id` of an element is kept stable, htmx will swap it in such a way that CSS transitions can be written between
the old version of the element and the new one.

Consider this div:

```html
<style>
.smooth {
  transition: all 1s ease-in;
}
</style>
<div id="color-demo" class="smooth" style="color:red"
      hx-get="/colors" hx-swap="outerHTML" hx-trigger="every 1s">
  Color Swap Demo
</div>

```

This div will poll every second and will get replaced with new content which changes the `color` style to a new value
(e.g. `blue`):

```html
<div id="color-demo" class="smooth" style="color:blue"
      hx-get="/colors" hx-swap="outerHTML" hx-trigger="every 1s">
  Color Swap Demo
</div>
```

Because the div has a stable id, `color-demo`, htmx will structure the swap such that a CSS transition, defined on the
`.smooth` class, applies to the style update from `red` to `blue`, and smoothly transitions between them.

#### Demo {#throb-demo}

<style>
.smooth {
  transition: all 1s ease-in;
}
</style>
<div id="color-demo" class="smooth" style="color:red"
      hx-get="/colors" hx-swap="outerHTML" hx-trigger="every 1s">
  Color Swap Demo
</div>

<script>
    var colors = ['blue', 'green', 'orange', 'red'];
    onGet("/colors", function () {
      var color = colors.shift();
      colors.push(color);
      return '<div id="color-demo" hx-get="/colors" hx-swap="outerHTML" class="smooth" hx-trigger="every 1s" style="color:' + color + '">\n'+
             '  Color Swap Demo\n'+
             '</div>\n'
    });
</script>

### Smooth Progress Bar

The [Progress Bar](@/examples/progress-bar.md) demo uses this basic CSS animation technique as well, by updating the `length`
property of a progress bar element, allowing for a smooth animation.

## Swap Transitions {#swapping}

### Fade Out On Swap

If you want to fade out an element that is going to be removed when the request ends, you want to take advantage
of the `htmx-swapping` class with some CSS and extend the swap phase to be long enough for your animation to
complete.  This can be done like so:

```html
<style>
.fade-me-out.htmx-swapping {
  opacity: 0;
  transition: opacity 1s ease-out;
}
</style>
<button class="fade-me-out"
        hx-delete="/fade_out_demo"
        hx-swap="outerHTML swap:1s">
        Fade Me Out
</button>
```

#### Demo {#fade-swap-demo}

<style>
.fade-me-out.htmx-swapping {
  opacity: 0;
  transition: opacity 1s ease-out;
}
</style>

<button class="fade-me-out"
        hx-delete="/fade_out_demo"
        hx-swap="outerHTML swap:1s">
        Delete Me
</button>

<script>
    onDelete("/fade_out_demo", function () {return ""});
</script>

## Settling Transitions {#settling}

### Fade In On Addition

Building on the last example, we can fade in the new content by using the `htmx-added` class during the settle
phase.  You can also write CSS transitions against the target, rather than the new content, by using the `htmx-settling`
class.

```html
<style>
#fade-me-in.htmx-added {
  opacity: 0;
}
#fade-me-in {
  opacity: 1;
  transition: opacity 1s ease-out;
}
</style>
<button id="fade-me-in"
        class="btn primary"
        hx-post="/fade_in_demo"
        hx-swap="outerHTML settle:1s">
        Fade Me In
</button>
```

#### Demo {#fade-settle-demo}

<style>
#fade-me-in.htmx-added {
  opacity: 0;
}
#fade-me-in {
  opacity: 1;
  transition: opacity 1s ease-out;
}
</style>

<button id="fade-me-in"
        class="btn primary"
        hx-post="/fade_me_in"
        hx-swap="outerHTML settle:1s">
        Fade Me In
</button>

<script>
    onPost("/fade_me_in", function () {return "<button id=\"fade-me-in\"\n"+
                                               "        class=\"btn primary\"\n"+
                                               "        hx-post=\"/fade_me_in\"\n"+
                                               "        hx-swap=\"outerHTML settle:1s\">\n"+
                                               "        Fade Me In\n"+
                                               "</button>"});
</script>

## Request In Flight Animation {#request}

You can also take advantage of the `htmx-request` class, which is applied to the element that triggers a request.  Below
is a form that on submit will change its look to indicate that a request is being processed:

```html
<style>
  form.htmx-request {
    opacity: .5;
    transition: opacity 300ms linear;
  }
</style>
<form hx-post="/name" hx-swap="outerHTML">
<label>Name:</label><input name="name"><br/>
<button class="btn primary">Submit</button>
</form>
```

#### Demo {#request-demo}

<style>
  form.htmx-request {
    opacity: .5;
    transition: opacity 300ms linear;
  }
</style>

<div aria-live="polite">
<form hx-post="/name" hx-swap="outerHTML">
<label>Name:</label><input name="name"><br/>
<button class="btn primary">Submit</button>
</form>
</div>

<script>
  onPost("/name", function(){ return "Submitted!"; });
</script>

## Using the htmx `class-tools` Extension

Many interesting animations can be created by using the [`class-tools`](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/class-tools/README.md) extension.

Here is an example that toggles the opacity of a div.  Note that we set the toggle time to be a bit longer than
the transition time.  This avoids flickering that can happen if the transition is interrupted by a class change.

```html
<style>
.demo.faded {
  opacity:.3;
}
.demo {
  opacity:1;
  transition: opacity ease-in 900ms;
}
</style>
<div class="demo" classes="toggle faded:1s">Toggle Demo</div>
```

#### Demo {#class-tools-demo}

<style>
.demo.faded {
  opacity:.3;
}
.demo {
  opacity:1;
  transition: opacity ease-in 900ms;
}
</style>
<div class="demo" classes="toggle faded:1s">Toggle Demo</div>

### Using the View Transition API {#view-transitions}

htmx provides access to the new  [View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
via the `transition` option of the [`hx-swap`](/attributes/hx-swap) attribute.

Below is an example of a swap that uses a view transition.  The transition is tied to the outer div via a
`view-transition-name` property in CSS, and that transition is defined in terms of `::view-transition-old`
and `::view-transition-new`, using `@keyframes` to define the animation.  (Fuller details on the View Transition
API can be found on the [Chrome Developer Page](https://developer.chrome.com/docs/web-platform/view-transitions/) on them.)

The old content of this transition should slide out to the left and the new content should slide in from the right.

Note that, as of this writing, the visual transition will only occur on Chrome 111+, but more browsers are expected to
implement this feature in the near future.

```html
<style>
   @keyframes fade-in {
     from { opacity: 0; }
   }

   @keyframes fade-out {
     to { opacity: 0; }
   }

   @keyframes slide-from-right {
     from { transform: translateX(90px); }
   }

   @keyframes slide-to-left {
     to { transform: translateX(-90px); }
   }

   .slide-it {
     view-transition-name: slide-it;
   }

   ::view-transition-old(slide-it) {
     animation: 180ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
     600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-left;
   }
   ::view-transition-new(slide-it) {
     animation: 420ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
     600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
   }
</style>


<div class="slide-it">
   <h1>Initial Content</h1>
   <button class="btn primary" hx-get="/new-content" hx-swap="innerHTML transition:true" hx-target="closest div">
     Swap It!
   </button>
</div>
```

#### Demo

<style>
   @keyframes fade-in {
     from { opacity: 0; }
   }

   @keyframes fade-out {
     to { opacity: 0; }
   }

   @keyframes slide-from-right {
     from { transform: translateX(90px); }
   }

   @keyframes slide-to-left {
     to { transform: translateX(-90px); }
   }

   .slide-it {
     view-transition-name: slide-it;
   }

   ::view-transition-old(slide-it) {
     animation: 180ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
     600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-left;
   }
   ::view-transition-new(slide-it) {
     animation: 420ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
     600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
   }
</style>

<div class="slide-it">
   <h1>Initial Content</h1>
   <button class="btn primary" hx-get="/new-content" hx-swap="innerHTML transition:true" hx-target="closest div">
     Swap It!
   </button>
</div>

<script>
    var originalContent = htmx.find(".slide-it").innerHTML;

    this.server.respondWith("GET", "/new-content", function(xhr){
        xhr.respond(200,  {}, "<h1>New Content</h1> <button class='btn danger' hx-get='/original-content' hx-swap='innerHTML transition:true' hx-target='closest div'>Restore It! </button>")
    });

    this.server.respondWith("GET", "/original-content", function(xhr){
        xhr.respond(200,  {}, originalContent)
    });
</script>

## Conclusion

You can use the techniques above to create quite a few interesting and pleasing effects with plain old HTML while using htmx.

```


## File: www/content/examples/async-auth.md

```
+++
title = "Async Authentication"
template = "demo.html"
+++

This example shows how to implement an an async auth token flow for htmx.

The technique we will use here will take advantage of the fact that you can delay requests
using the [`htmx:confirm`](@/events.md#htmx:confirm) event.

We first have a button that should not issue a request until an auth token has been retrieved:

```html
  <button hx-post="/example" hx-target="next output">
    An htmx-Powered button
  </button>
  <output>
    --
  </output>
```

Next we will add some scripting to work with an `auth` promise (returned by a library):

```html
<script>
  // auth is a promise returned by our authentication system

  // await the auth token and store it somewhere
  let authToken = null;
  auth.then((token) => {
    authToken = token
  })
  
  // gate htmx requests on the auth token
  htmx.on("htmx:confirm", (e)=> {
    // if there is no auth token
    if(authToken == null) {
      // stop the regular request from being issued
      e.preventDefault() 
      // only issue it once the auth promise has resolved
      auth.then(() => e.detail.issueRequest()) 
    }
  })

  // add the auth token to the request as a header
  htmx.on("htmx:configRequest", (e)=> {
    e.detail.headers["AUTH"] = authToken
  })
</script>
```

Here we use a global variable, but you could use `localStorage` or whatever preferred mechanism
you want to communicate the authentication token to the `htmx:configRequest` event.

With this code in place, htmx will not issue requests until the `auth` promise has been resolved.

```


## File: www/content/examples/bulk-update.md

```
+++
title = "Bulk Update"
template = "demo.html"
+++

This demo shows how to implement a common pattern where rows are selected and then bulk updated.  This is
accomplished by putting a form around a table, with checkboxes in the table, and then including the checked
values in the form submission (`POST` request):

```html
<form id="checked-contacts"
      hx-post="/users"
      hx-swap="innerHTML settle:3s"
      hx-target="#toast">
    <table>
      <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Active</th>
      </tr>
      </thead>
      <tbody id="tbody">
        <tr>
          <td>Joe Smith</td>
          <td>joe@smith.org</td>
          <td><input type="checkbox" name="active:joe@smith.org"></td>
        </tr>
        ...
      </tbody>
    </table>
    <input type="submit" value="Bulk Update" class="btn primary">
    <output id="toast"></output>
</form>
```

The server will bulk-update the statuses based on the values of the checkboxes.
We respond with a small toast message about the update to inform the user, and
use an `<output>` element to politely announce the update for accessibility. Note
that the `<output>` element is appropriate for announcing the result of an action
in a specific form, but if you need to announce general-purpose messages that are
not connected to a form it would make sense to use an ARIA live region, eg
`<p id="toast" aria-live="polite"></p>`.

```css
#toast.htmx-settling {
  opacity: 100;
}

#toast {
  background: #E1F0DA;
  opacity: 0;
  transition: opacity 3s ease-out;
}
```

The cool thing is that, because HTML form inputs already manage their own state,
we don't need to re-render any part of the users table. The active users are
already checked and the inactive ones unchecked!

You can see a working example of this code below.

<style scoped="">
#toast.htmx-settling {
  opacity: 100;
}

#toast {
  background: #E1F0DA;
  opacity: 0;
  transition: opacity 3s ease-out;
}
</style>

{{ demoenv() }}

<script>
    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    const dataStore = (() => {
      const data = {
        "joe@smith.org": {name: 'Joe Smith', status: 'Active'},
        "angie@macdowell.org": {name: 'Angie MacDowell', status: 'Active'},
        "fuqua@tarkenton.org": {name: 'Fuqua Tarkenton', status: 'Active'},
        "kim@yee.org": {name: 'Kim Yee', status: 'Inactive'},
      };

      return {
        all() {
          return data;
        },

        activate(email) {
          if (data[email].status === 'Active') {
            return 0;
          } else {
            data[email].status = 'Active';
            return 1;
          }
        },

        deactivate(email) {
          if (data[email].status === 'Inactive') {
            return 0;
          } else {
            data[email].status = 'Inactive';
            return 1;
          }
        },
      };
    })();

    // routes
    init("/demo", function(request){
        return displayUI(dataStore.all());
    });

    /*
    Params look like:
    {"active:joe@smith.org":"on","active:angie@macdowell.org":"on","active:fuqua@tarkenton.org":"on"}
    */
    onPost("/users", function (req, params) {
      const actives = {};
      let activated = 0;
      let deactivated = 0;

      // Build a set of active users for efficient lookup
      for (const param of Object.keys(params)) {
        const nameEmail = param.split(':');
        if (nameEmail[0] === 'active') {
          actives[nameEmail[1]] = true;
        }
      }

      // Activate or deactivate users based on the lookup
      for (const email of Object.keys(dataStore.all())) {
        if (actives[email]) {
          activated += dataStore.activate(email);
        } else {
          deactivated += dataStore.deactivate(email);
        }
      }

      return `Activated ${activated} and deactivated ${deactivated} users`;
    });

    // templates
    function displayUI(contacts) {
      return `<h3>Select Rows And Activate Or Deactivate Below</h3>
               <form
                id="checked-contacts"
                hx-post="/users"
                hx-swap="innerHTML settle:3s"
                hx-target="#toast"
              >
                <table>
                  <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Active</th>
                  </tr>
                  </thead>
                  <tbody id="tbody">
                    ${displayTable(contacts)}
                  </tbody>
                </table>
                <input type="submit" value="Bulk Update" class="btn primary">
                <output id="toast"></output>
              </form>
              <br>`;
    }

    function displayTable(contacts) {
      var txt = "";

      for (email of Object.keys(contacts)) {
        txt += `
<tr>
  <td>${contacts[email].name}</td>
  <td>${email}</td>
  <td>
    <input
      type="checkbox"
      name="active:${email}"
      ${contacts[email].status === 'Active' ? 'checked' : ''}>
  </td>
</tr>
`;
      }

      return txt;
    }
</script>

```


## File: www/content/examples/click-to-edit.md

```
+++
title = "Click to Edit"
template = "demo.html"
+++

The click to edit pattern provides a way to offer inline editing of all or part of a record without a page refresh.

* This pattern starts with a UI that shows the details of a contact.  The div has a button that will get the editing UI for the contact from `/contact/1/edit`

```html
<div hx-target="this" hx-swap="outerHTML">
    <div><label>First Name</label>: Joe</div>
    <div><label>Last Name</label>: Blow</div>
    <div><label>Email</label>: joe@blow.com</div>
    <button hx-get="/contact/1/edit" class="btn primary">
    Click To Edit
    </button>
</div>
```

* This returns a form that can be used to edit the contact

```html
<form hx-put="/contact/1" hx-target="this" hx-swap="outerHTML">
  <div>
    <label>First Name</label>
    <input type="text" name="firstName" value="Joe">
  </div>
  <div class="form-group">
    <label>Last Name</label>
    <input type="text" name="lastName" value="Blow">
  </div>
  <div class="form-group">
    <label>Email Address</label>
    <input type="email" name="email" value="joe@blow.com">
  </div>
  <button class="btn" type="submit">Submit</button>
  <button class="btn" hx-get="/contact/1">Cancel</button>
</form>
```

* The form issues a `PUT` back to `/contact/1`, following the usual REST-ful pattern.

{{ demoenv() }}

<script>
    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    // data
    var contact = {
        "firstName" : "Joe",
        "lastName" : "Blow",
        "email" : "joe@blow.com"
    };

    // routes
    init("/contact/1", function(request){
        return displayTemplate(contact);
    });

    onGet("/contact/1/edit", function(request){
        return formTemplate(contact);
    });

    onPut("/contact/1", function (req, params) {
        contact.firstName = params['firstName'];
        contact.lastName = params['lastName'];
        contact.email = params['email'];
        return displayTemplate(contact);
    });

    // templates
    function formTemplate(contact) {
return `<form hx-put="/contact/1" hx-target="this" hx-swap="outerHTML">
  <div>
    <label for="firstName">First Name</label>
    <input autofocus type="text" id="firstName" name="firstName" value="${contact.firstName}">
  </div>
  <div class="form-group">
    <label for="lastName">Last Name</label>
    <input type="text" id="lastName" name="lastName" value="${contact.lastName}">
  </div>
  <div class="form-group">
    <label for="email">Email Address</label>
    <input type="email" id="email" name="email" value="${contact.email}">
  </div>
  <button class="btn primary" type="submit">Submit</button>
  <button class="btn danger" hx-get="/contact/1">Cancel</button>
</form>`
    }

    function displayTemplate(contact) {
        return `<div hx-target="this" hx-swap="outerHTML">
    <div><label>First Name</label>: ${contact.firstName}</div>
    <div><label>Last Name</label>: ${contact.lastName}</div>
    <div><label>Email Address</label>: ${contact.email}</div>
    <button hx-get="/contact/1/edit" class="btn primary">
    Click To Edit
    </button>
</div>`;
    }
</script>

```


## File: www/content/examples/click-to-load.md

```
+++
title = "Click to Load"
template = "demo.html"
+++

This example shows how to implement click-to-load the next page in a table of data.  The crux of the demo is
the final row:

```html
<tr id="replaceMe">
  <td colspan="3">
    <button class='btn primary' hx-get="/contacts/?page=2"
                        hx-target="#replaceMe"
                        hx-swap="outerHTML">
         Load More Agents... <img class="htmx-indicator" src="/img/bars.svg" alt="">
    </button>
  </td>
</tr>
```

This row contains a button that will replace the entire row with the next page of
results (which will contain a button to load the *next* page of results).  And so on.

{{ demoenv() }}

<script>
    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    // data
    var dataStore = function(){
      var contactId = 9;
      function generateContact() {
        contactId++;
        var idHash = "";
        var possible = "ABCDEFG0123456789";
        for( var i=0; i < 15; i++ ) idHash += possible.charAt(Math.floor(Math.random() * possible.length));
        return { name: "Agent Smith", email: "void" + contactId + "@null.org", id: idHash }
      }
      return {
        contactsForPage : function(page) {
          var vals = [];
          for( var i=0; i < 10; i++ ){
            vals.push(generateContact());
          }
          return vals;
        }
      }
    }()

    // routes
    init("/demo", function(request, params){
        var contacts = dataStore.contactsForPage(1)
        return tableTemplate(contacts)
    });

    onGet(/\/contacts.*/, function(request, params){
        var page = parseInt(params['page']);
        var contacts = dataStore.contactsForPage(page)
        return rowsTemplate(page, contacts);
    });

    // templates
    function tableTemplate(contacts) {
        return `<table><thead><tr><th>Name</th><th>Email</th><th>ID</th></tr></thead><tbody>
                ${rowsTemplate(1, contacts)}
                </tbody></table>`
    }

    function rowsTemplate(page, contacts) {
      var txt = "";
      for (var i = 0; i < contacts.length; i++) {
        var c = contacts[i];
        txt += `<tr><td>${c.name}</td><td>${c.email}</td><td>${c.id}</td></tr>\n`;
      }
      txt += loadMoreRow(page);
      return txt;
    }

    function loadMoreRow(page) {
      return `<tr id="replaceMe">
  <td colspan="3">
    <center>
      <button class='btn primary' hx-get="/contacts/?page=${page + 1}"
                       hx-target="#replaceMe"
                       hx-swap="outerHTML">
         Load More Agents... <img class="htmx-indicator" src="/img/bars.svg" alt="">
       </button>
    </center>
  </td>
</tr>`;
    }
</script>

```


## File: www/content/examples/confirm.md

```
+++
title = "A Customized Confirmation UI"
template = "demo.html"
+++

htmx supports the [`hx-confirm`](@/attributes/hx-confirm.md) attribute to provide a simple mechanism for confirming a user
action.  This uses the default `confirm()` function in javascript which, while trusty, may not be consistent with your 
applications UX.

In this example we will see how to use [sweetalert2](https://sweetalert2.github.io)  to implement a custom confirmation dialog. Below are two 
examples, one using a click+custom event method, and one using the built-in `hx-confirm` attribute and
the [`htmx:confirm`](@/events.md#htmx:confirm) event.

## Using on click+custom event

```html
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<button hx-get="/confirmed" 
        hx-trigger='confirmed'
        onClick="Swal.fire({title: 'Confirm', text:'Do you want to continue?'}).then((result)=>{
            if(result.isConfirmed){
              htmx.trigger(this, 'confirmed');  
            } 
        })">
  Click Me
</button>
```

Here we use javascript to show a Sweet Alert 2 on a click, asking for confirmation.  If the user confirms
the dialog, we then trigger the request by triggering the custom "confirmed" event
which is then picked up by `hx-trigger`.

## Vanilla JS, hx-confirm

```html
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<script>
  document.addEventListener("htmx:confirm", function(e) {
    // The event is triggered on every trigger for a request, so we need to check if the element
    // that triggered the request has a confirm question set via the hx-confirm attribute,
    // if not we can return early and let the default behavior happen
    if (!e.detail.question) return

    // This will prevent the request from being issued to later manually issue it
    e.preventDefault()

    Swal.fire({
      title: "Proceed?",
      text: `I ask you... ${e.detail.question}`
    }).then(function(result) {
      if (result.isConfirmed) {
        // If the user confirms, we manually issue the request
        e.detail.issueRequest(true); // true to skip the built-in window.confirm()
      }
    })
  })
</script>
  
<button hx-get="/confirmed" hx-confirm="Some confirm text here">
  Click Me
</button>
```

We add some javascript to invoke Sweet Alert 2 on a click, asking for confirmation.  If the user confirms
the dialog, we trigger the request by calling the `issueRequest` method. We pass `skipConfirmation=true` as argument to skip `window.confirm`.

This allows to use `hx-confirm`'s value in the prompt which is convenient
when the question depends on the element e.g. a django list:

```html
{% for client in clients %}
<button hx-post="/delete/{{client.pk}}" hx-confirm="Delete {{client.name}}??">Delete</button>
{% endfor %}
```

Learn more about the [`htmx:confirm`](@/events.md#htmx:confirm) event [here](@/events.md#htmx:confirm).

```


## File: www/content/examples/delete-row.md

```
+++
title = "Delete Row"
template = "demo.html"
+++

This example shows how to implement a delete button that removes a table row upon completion.  First let's look at the
table body:

```html
<table class="table delete-row-example">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
      <th></th>
    </tr>
  </thead>
  <tbody hx-confirm="Are you sure?" hx-target="closest tr" hx-swap="outerHTML swap:1s">
    ...
  </tbody>
</table>
```

The table body has a [`hx-confirm`](@/attributes/hx-confirm.md) attribute to confirm the delete action.  It also
set the target to be the `closest tr` that is, the closest table row, for all the buttons ([`hx-target`](@/attributes/hx-target.md)
is inherited from parents in the DOM.)  The swap specification in [`hx-swap`](@/attributes/hx-swap.md) says to swap the
entire target out and to wait 1 second after receiving a response.  This last bit is so that we can use the following
CSS:

```css
tr.htmx-swapping td {
  opacity: 0;
  transition: opacity 1s ease-out;
}
```

To fade the row out before it is swapped/removed.

Each row has a button with a [`hx-delete`](@/attributes/hx-delete.md) attribute containing the url on which to issue a `DELETE`
request to delete the row from the server. This request responds with a `200` status code and empty content, indicating that the
row should be replaced with nothing.

```html
<tr>
  <td>Angie MacDowell</td>
  <td>angie@macdowell.org</td>
  <td>Active</td>
  <td>
    <button class="btn danger" hx-delete="/contact/1">
      Delete
    </button>
  </td>
</tr>
```

<style>
tr.htmx-swapping td {
  opacity: 0;
  transition: opacity 1s ease-out;
}
</style>

{{ demoenv() }}

<script>
    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    // data
    var contacts = [
      {
        name: "Joe Smith",
        email: "joe@smith.org",
        status: "Active",
      },
      {
        name: "Angie MacDowell",
        email: "angie@macdowell.org",
        status: "Active",
      },
      {
        name: "Fuqua Tarkenton",
        email: "fuqua@tarkenton.org",
        status: "Active",
      },
      {
        name: "Kim Yee",
        email: "kim@yee.org",
        status: "Inactive",
      },
    ];

    // routes
    init("/demo", function(request, params){
      return tableTemplate(contacts);
    });

    onDelete(/\/contact\/\d+/, function(request, params){
      return "";
    });

    // templates
    function rowTemplate(contact, i) {
      return `<tr>
      <td>${contact["name"]}</td>
      <td>${contact["email"]}</td>
      <td>${contact["status"]}</td>
      <td>
        <button class="btn danger" hx-delete="/contact/${i}">
          Delete
        </button>
      </td>
    </tr>`;
    }

    function tableTemplate(contacts) {
      var rows = "";

      for (var i = 0; i < contacts.length; i++) {
        rows += rowTemplate(contacts[i], i, "");
      }

      return `
<table class="table delete-row-example">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
      <th></th>
    </tr>
  </thead>
  <tbody hx-confirm="Are you sure?" hx-target="closest tr" hx-swap="outerHTML swap:1s">
    ${rows}
  </tbody>
</table>`;
    }

</script>

```


## File: www/content/examples/dialogs.md

```
+++
title = "Dialogs"
template = "demo.html"
+++

Dialogs can be triggered with the [`hx-prompt`](@/attributes/hx-prompt.md) and [`hx-confirm`](@/attributes/hx-confirm.md)attributes.  These are triggered by the user interaction that would trigger the AJAX request, but the request is only sent if the dialog is accepted.

```html
<div>
  <button class="btn primary"
          hx-post="/submit"
          hx-prompt="Enter a string"
          hx-confirm="Are you sure?"
          hx-target="#response">
    Prompt Submission
  </button>
  <div id="response"></div>
</div>
```

The value provided by the user to the prompt dialog is sent to the server in a `HX-Prompt` header.  In this case, the server simply echos the user input back.

```html
User entered <i>${response}</i>
```

{{ demoenv() }}

<script>

    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    // routes
    init("/demo", function(request, params){
      return submitButton();
    });

    onPost("/submit", function(request, params){
        var response = request.requestHeaders['HX-Prompt'];
        return promptSubmit(response);
    });

    // templates
    function submitButton() {
      return `<div>
  <button class="btn primary"
          hx-post="/submit"
          hx-prompt="Enter a string"
          hx-confirm="Are you sure?"
          hx-target="#response">
    Prompt Submission
  </button>
  <div id="response"></div>
</div>`;
    }

    function promptSubmit(response) {
        return `User entered <i>${response}</i>`;
    }
</script>

```


## File: www/content/examples/edit-row.md

```
+++
title = "Edit Row"
template = "demo.html"
+++

This example shows how to implement editable rows.  First let's look at the table body:

```html
<table class="table delete-row-example">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th></th>
    </tr>
  </thead>
  <tbody hx-target="closest tr" hx-swap="outerHTML">
    ...
  </tbody>
</table>
```

This will tell the requests from within the table to target the closest enclosing row that the request is triggered
on and to replace the entire row.

Here is the HTML for a row:

```html
<tr>
      <td>${contact.name}</td>
      <td>${contact.email}</td>
      <td>
        <button class="btn danger"
                hx-get="/contact/${contact.id}/edit"
                hx-trigger="edit"
                onClick="let editing = document.querySelector('.editing')
                         if(editing) {
                           Swal.fire({title: 'Already Editing',
                                      showCancelButton: true,
                                      confirmButtonText: 'Yep, Edit This Row!',
                                      text:'Hey!  You are already editing a row!  Do you want to cancel that edit and continue?'})
                           .then((result) => {
                                if(result.isConfirmed) {
                                   htmx.trigger(editing, 'cancel')
                                   htmx.trigger(this, 'edit')
                                }
                            })
                         } else {
                            htmx.trigger(this, 'edit')
                         }">
          Edit
        </button>
      </td>
    </tr>
```

Here we are getting a bit fancy and only allowing one row at a time to be edited, using some JavaScript.
We check to see if there is a row with the `.editing` class on it and confirm that the user wants to edit this row
and dismiss the other one.  If so, we send a cancel event to the other row so it will issue a request to go back to
its initial state.

We then trigger the `edit` event on the current element, which triggers the htmx request to get the editable version
of the row.

Note that if you didn't care if a user was editing multiple rows, you could omit the hyperscript and custom `hx-trigger`,
and just let the normal click handling work with htmx.  You could also implement mutual exclusivity by simply targeting the
entire table when the Edit button was clicked.  Here we wanted to show how to integrate htmx and JavaScript to solve
the problem and narrow down the server interactions a bit, plus we get to use a nice SweetAlert confirm dialog.

Finally, here is what the row looks like when the data is being edited:

```html
<tr hx-trigger='cancel' class='editing' hx-get="/contact/${contact.id}">
  <td><input autofocus name='name' value='${contact.name}'></td>
  <td><input name='email' value='${contact.email}'></td>
  <td>
    <button class="btn danger" hx-get="/contact/${contact.id}">
      Cancel
    </button>
    <button class="btn danger" hx-put="/contact/${contact.id}" hx-include="closest tr">
      Save
    </button>
  </td>
</tr>
```

Here we have a few things going on:  First off the row itself can respond to the `cancel` event, which will bring
back the read-only version of the row.  There is a cancel button that allows
cancelling the current edit.  Finally, there is a save button that issues a `PUT` to update the contact.  Note that
there is an [`hx-include`](@/attributes/hx-include.md) that includes all the inputs in the closest row.  Tables rows are
notoriously difficult to use with forms due to HTML constraints (you can't put a `form` directly inside a `tr`) so
this makes things a bit nicer to deal with.

{{ demoenv() }}

<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
<script>
    //=========================================================================
    // Fake Server Side Code
    //=========================================================================

    // data
    var contacts = [
      {
        name: "Joe Smith",
        email: "joe@smith.org",
        status: "Active",
        id: 0
      },
      {
        name: "Angie MacDowell",
        email: "angie@macdowell.org",
        status: "Active",
        id: 1
      },
      {
        name: "Fuqua Tarkenton",
        email: "fuqua@tarkenton.org",
        status: "Active",
        id: 2
      },
      {
        name: "Kim Yee",
        email: "kim@yee.org",
        status: "Inactive",
        id: 3
      },
    ];

    // routes
    init("/demo", function(request, params){
      return tableTemplate(contacts);
    });

    onGet(/\/contact\/\d+/, function(request, params){
      var id = parseInt(request.url.split("/")[2]); // get the contact
      var contact = contacts[id];
      console.log(request, id, contact)
      if(request.url.endsWith("/edit")) {
        return editTemplate(contacts[id])
      } else {
        return rowTemplate(contacts[id])
      }
    });

    onPut(/\/contact\/\d+/, function(request, params){
      var id = parseInt(request.url.split("/")[2]); // get the contact
      contact = contacts[id]
      contact.name = params['name'];
      contact.email = params['email'];
      return rowTemplate(contact);
    });

    // templates
    function rowTemplate(contact) {
      return `<tr>
      <td>${contact.name}</td>
      <td>${contact.email}</td>
      <td>
        <button class="btn danger"
                hx-get="/contact/${contact.id}/edit"
                hx-trigger="edit"
                onClick="let editing = document.querySelector('.editing')
                         if(editing) {
                           Swal.fire({title: 'Already Editing',
                                      showCancelButton: true,
                                      confirmButtonText: 'Yep, Edit This Row!',
                                      text:'Hey!  You are already editing a row!  Do you want to cancel that edit and continue?'})
                           .then((result) => {
                                if(result.isConfirmed) {
                                   htmx.trigger(editing, 'cancel')
                                   htmx.trigger(this, 'edit')
                                }
                            })
                         } else {
                            htmx.trigger(this, 'edit')
                         }">
          Edit
        </button>
      </td>
    </tr>`;
    }

    function editTemplate(contact) {
      return `<tr hx-trigger='cancel' class='editing' hx-get="/contact/${contact.id}">
      <td><input autofocus name='name' value='${contact.name}'</td>
      <td><input name='email' value='${contact.email}'</td>
      <td>
        <button class="btn danger" hx-get="/contact/${contact.id}">
          Cancel
        </button>
        <button class="btn danger" hx-put="/contact/${contact.id}" hx-include="closest tr">
          Save
        </button>
      </td>
    </tr>`;
    }

    function tableTemplate(contacts) {
      var rows = "";

      for (var i = 0; i < contacts.length; i++) {
        rows += rowTemplate(contacts[i], i, "");
      }

      return `
<table class="table delete-row-example">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th></th>
    </tr>
  </thead>
  <tbody hx-target="closest tr" hx-swap="outerHTML">
    ${rows}
  </tbody>
</table>`;
    }
</script>

```


(… 337 more files omitted due to size limit)
<!-- fetched-content:end -->
