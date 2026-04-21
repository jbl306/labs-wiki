---
title: "htmx - HTML Over The Wire"
type: url
captured: 2026-04-07T19:50:00Z
source: test
url: "https://github.com/bigskysoftware/htmx"
tags: []
status: ingested
---

https://github.com/bigskysoftware/htmx

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T13:28:50+00:00
- source_url: https://github.com/bigskysoftware/htmx
- resolved_url: https://github.com/bigskysoftware/htmx
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: bigskysoftware/htmx
Description: </> htmx - high power tools for HTML
Stars: 47862
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
  <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.9/dist/htmx.min.js"></script>
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


## File: CHANGELOG.md

```
# Changelog

## [2.0.9] - 2026-04-15

* [Fixed](https://github.com/bigskysoftware/htmx/commit/a706897e84ed271528658c84a0b73eb5e3f2fe57) `HX-Location` to correctly honor `replace` when `push` is `false` (thanks @MichaelWest22)
* [Fixed](https://github.com/bigskysoftware/htmx/commit/7c0732352df80770d893c9e8806bffe4a9d55686) history `normalizePath` to resolve relative paths against the current page location rather than a dummy base URL (thanks @MichaelWest22)
* [Fixed](https://github.com/bigskysoftware/htmx/commit/bd442b56396da2fffcf756613329b01c16035e67) empty `class=""` attribute being left on elements after htmx utility classes (`htmx-swapping`, `htmx-settling`, `htmx-request`) are removed (thanks @manwithacat)
* [Fixed](https://github.com/bigskysoftware/htmx/commit/8183f074a669b26a26f6af4ad5e24303b9a26bed) `hx-disabled-elt` to preserve elements that were already `disabled` in the source HTML (thanks @StabbarN)
* [Added](https://github.com/bigskysoftware/htmx/commit/31430d995fff37b858188a85f704cfd32b07608a) the failing selector to the `htmx:oobErrorNoTarget` event detail and error log for easier debugging (thanks @RensDimmendaal)

## [2.0.8] - 2025-10-24

* [Updated](https://github.com/bigskysoftware/htmx/commit/b9336a96fbdcf28550699971dc2218a90c7a4e01) `parseHTML` to use the (unfortunately named) [`Document.parseHTMLUnsafe()`](https://developer.mozilla.org/en-US/docs/Web/API/Document/parseHTMLUnsafe_static) 
  method for better Web Components support
* [Added](https://github.com/bigskysoftware/htmx/commit/83a1449a89b1fcd1c1655039ede02d74d61e4800) `pushURL` option to the `htmx.ajax()` API
* [Fixed](https://github.com/bigskysoftware/htmx/commit/cd045c3e0eb31776a80e3a4b4c74e37d0631c1f1) `hx-sync` and `htmx:abort` within the Shadow Dom [Issue 3419](https://github.com/bigskysoftware/htmx/issues/3419)
* [Fixed](https://github.com/bigskysoftware/htmx/commit/04d6c7249b7fd7b8518ddca92e7a70fdcc651b34) a long-standing bug in history support with respect to relative paths [Issue 3449](https://github.com/bigskysoftware/htmx/issues/3449)
* Once again, this is a release mainly done by @MichaelWest22's heroic work, thank you!

## [2.0.7] - 2025-09-08

* Fix not preventing link when inside htmx enabled element (fixes https://github.com/bigskysoftware/htmx/issues/3395)
* Implement `reportValidity()` for reporting proper form validation errors behind config flag (fixes https://github.com/bigskysoftware/htmx/issues/2372)
* Update indicator style to have `visibility:hidden` for screen readers (fixes https://github.com/bigskysoftware/htmx/issues/3354)
* Bugfix: swap="outerHTML" on <div> with style attribute leaves htmx-swapping class behind (see https://github.com/bigskysoftware/htmx/pull/3341)

## [2.0.6] - 2025-06-27

* [Fix](https://github.com/bigskysoftware/htmx/pull/3357) a [regression](https://github.com/bigskysoftware/htmx/issues/3356) 
  with htmx-powered links that contain other elements in them issuing full page refreshes

## [2.0.5] - 2025-06-20

* 100% test coverage! (Thank you @MichaelWest22!)
* The default recommended CDN is now jsDelivr
* The `inherit` keyword is now supported by `hx-include`, `hx-indicator` and `hx-disabled-elt` to allow you to inherit
  the value from a parent and extend it.
* `hx-on` listeners are now added before processing nodes so events during processing can be captured
* Using `<button hx-verb="/endpoint" type="reset">` will now reset the associated form (after submitting to `/endpoint`)
* Using `<button formmethod="dialog">` will no longer submit its associated form
* Local history cache now uses `sessionStorage` rather than `localStorage` so cross-tab contamination doesn't occur
* History restoration now follows the standard swapping code paths 
* Many other smaller bug and documentation fixes

## [2.0.4] - 2024-12-13

* Calling `htmx.ajax` with no target or source now defaults to body (previously did nothing)
* Nested [shadow root](https://github.com/bigskysoftware/htmx/commit/5ab508f6523a37890932176f7dc54be9f7a281ff) fix
* The `htmx:trigger` event now properly fires on the synthetic `load` event
* The synthetic `load` event will not be re-called when an element is reinitialized via `htmx.process()`
* Boosted `<form>` tags that issue a `GET` with no or empty `action` attributes will properly replace all existing query 
  parameters
* Events that are triggered on htmx-powered elements located outside a form, but that refer to a form via the`form` 
  attribute, now properly cancel the submission of the referred-to form
* Extension Updates
  * `preload` extension was 
    [completely reworked](https://github.com/bigskysoftware/htmx-extensions/commit/fb68dfb48063505d2d7420d717c24ac9a8dae244) 
    by @marisst to be compatible with `hx-boost`, not cause side effect, etc. Thank you!
  * `response-targets` was updated to not use deprecated methods
  * A [small fix](https://github.com/bigskysoftware/htmx-extensions/commit/e87e1c3d0bf728b4e43861c7459f3f937883eb99) to
    `ws` to avoid an error when closing in some cases
  * The `head-support` extension was updated to work with the `sse` extension

## [2.0.3] - 2024-10-03
* Added support for the experimental `moveBefore()` functionality in [Chrome Canary](https://www.google.com/chrome/canary/), 
  see the [demo page](/examples/move-before) for more information.
* Fixed `revealed` event when a resize reveals an element
* Enabled `hx-preserve` in oob-swaps
* Better degredation of `hx-boost` on forms with query parameters in their `action`
* Improved shadowRoot support
* Many smaller bug fixes
* Moved the core extension documentation back to <https://htmx.org/extensions>

## [2.0.2] - 2024-08-12
* no longer boost forms of type `dialog`
* properly trigger the `htmx:trigger` event when an event is delayed or throttled
* file upload is now fixed
* empty templates that are not used for oob swaps are no longer removed from the DOM
* request indicators are not removed when a full page redirect or refresh occurs
* elements that have been disabled for a request are properly re-enabled before snapshotting for history
* you can now trigger events on other elements using the `HX-Trigger` response header
* The `.d.ts` file should now work properly

## [2.0.1] - 2024-07-12

* Make the `/dist/htmx.esm.js` file the `main` file in `package.json` to make installing htmx smoother
* Update `htmx.d.ts` & include it in the distribution
* A fix to avoid removing text-only templates on htmx cleanup
* A fix for outerHTML swapping of the `body` tag
* Many docs fixes

## [2.0.0] - 2024-06-17

* Removed extensions and moved to their own repos linked off of <https://extensions.htmx.org>
* The website now supports dark mode! (Thanks [@pokonski](https://github.com/pokonski)!)
* The older, deprecated [SSE & WS](https://v1.htmx.org/docs/#websockets-and-sse) attributes were removed
* Better support for [Web Components & Shadow DOM](https://htmx.org/examples/web-components/)
* HTTP `DELETE` requests now use parameters, rather than form encoded bodies, for their payload (This is in accordance w/ the spec.)
* Module support was split into different files:
* We now provide specific files in `/dist` for the various JavaScript module styles:
  * ESM Modules: `/dist/htmx.esm.js`
  * AMD Modules: `/dist/htmx.amd.js`
  * CJS Modules: `/dist/htmx.cjs.js`
  * The `/dist/htmx.js` file continues to be browser-loadable
* The `hx-on` attribute, with its special syntax, has been removed in favor of the less-hacky `hx-on:` syntax.
* See the [Upgrade Guide](https://htmx.org/migration-guide-htmx-1/) for more details on upgrade steps
* The `selectAndSwap()` internal API method was replaced with the public (and much better) [`swap()`](/api/#swap) method

## [1.9.12] - 2024-04-17

* [IE Fixes](https://github.com/bigskysoftware/htmx/commit/e64238dba3113c2eabe26b1e9e9ba7fe29ba3010)

## [1.9.11] - 2024-03-15

* Fix for new issue w/ web sockets & SSE on iOS 17.4 (thanks apple!)
* Fix for double script execution issue when using template parsing
* F
```


## File: CONTRIBUTING.md

```
# Contributing
Thank you for your interest in contributing! Because we're a small team, we have a couple contribution guidelines that make it easier for us to triage all the incoming suggestions.

## Issues
1. Issues are the best place to propose a new feature. Keep in mind that htmx is a small library, so there are lots of great ideas that don't fit in the core; it's always best to check in about an idea before doing a bunch of work on it.
1. When proposing a new feature, we will often suggest that you implement it as an [extension](https://github.com/bigskysoftware/htmx-extensions), so try that first. Even if we don't end up supporting it officially, you can publish it yourself and we can link to it.
1. Search the issues before proposing a feature to see if it is already under discussion. Referencing existing issues is a good way to increase the priority of your own.
1. We don't have an issue template yet, but the more detailed your description of the issue, the more quickly we'll be able to evaluate it.
1. See an issue that you also have? Give it a reaction (and comment, if you have something to add). We note that!
1. If you haven't gotten any traction on an issue, feel free to bump it in the #issues-and-pull-requests channel on our Discord.
1. Want to contribute but don't know where to start? Look for issues with the "help wanted" tag.

## Creating a Development Environment
### Pre-requisites
To create a development environment for htmx, you'll need the following tools on your system:

- Node.js 20.x or later
- Chrome or Chromium

Additionally, the environment variable `CHROME_PATH` must contain the full path to the Chrome or Chromium binary on your system.

### Installing Packages
To install htmx's required packages, run the following command:

```bash
npm install
```

### Running Automated Tests
To verify that your htmx environment is working correctly, you can run htmx's automated tests with the following command:

```bash
npm test
```

## Pull Requests
### Technical Requirements
1. Please lint all proposed changes with the `npm run format` command
1. All PRs must be made against the `dev` branch, except documentation PRs (that only modify the `www/` directory) which can be made against `master`.
1. Please avoid sending the `dist` files along your PR, only include the `src` ones.
1. Please include test cases in [`/test`](https://github.com/bigskysoftware/htmx/tree/dev/test) and docs in [`/www`](https://github.com/bigskysoftware/htmx/tree/dev/www).
1. We squash all PRs, so you're welcome to submit with as many commits as you like; they will be evaluated as a single, standalone change.

### Review Guidelines
1. Open PRs represent issues that we're actively thinking working on merging (at a pace we can manage). If we think a proposal needs more discussion, or that the existing code would require a lot of back-and-forth to merge, we might close it and suggest you make an issue.
1. Smaller PRs are easier and quicker to review. If we feel that the scope of your changes is too large, we will close the PR and try to suggest ways that the change could be broken down.
1. Please do not PR new features unless you have already made an issue proposing the feature, and had it accepted by a core maintainer. This helps us triage the features we can support before you put a lot of work into them.
1. Correspondingly, it is fine to directly PR bugfixes for behavior that htmx already guarantees, but please check if there's an issue first, and if you're not sure whether this *is* a bug, make an issue where we can hash it out..
1. Refactors that do not make functional changes will be automatically closed, unless explicitly solicited. Imagine someone came into your house unannounced, rearranged a bunch of furniture, and left.
1. Typo fixes in the documentation (not the code comments) are welcome, but formatting or debatable grammar changes will be automatically closed.

## Misc
1. If you think we closed something incorrectly, feel free to (politely) tell us why! We're human and make mistakes.
1. There are lots of ways to improve htmx besides code changes. Sometimes a problem can be solved with better docs, usage patterns, extensions, or community support. Talk to us and we can almost always help you get to a solution.

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


## File: netlify.toml

```
[build]
base    = "www"
publish = "public"
command = "zola build"

[build.environment]
ZOLA_VERSION = "0.19.1"

[context.deploy-preview]
command = "zola build --base-url $DEPLOY_PRIME_URL"

```


## File: package-lock.json

```
{
  "name": "htmx.org",
  "version": "2.0.9",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "htmx.org",
      "version": "2.0.9",
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
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.27.1.tgz",
      "integrity": "sha512-cjQ7ZlQ0Mv3b47hABuTevyTuYN4i+loJKGeV9flcCgIK37cCXRh+L1bd3iBHlynerhQ7BhCkn2BPbQUL+rGqFg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.27.1",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.27.1.tgz",
      "integrity": "sha512-D2hP9eA+Sqx1kBZgzxZh0y1trbuU+JoDkiEwqhQ36nodYqJwyEIhPSdMNd7lOm/4io72luTPWH20Yda0xOuUow==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.0",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.0.tgz",
      "integrity": "sha512-ayVFHdtZ+hsq1t2Dy24wCmGXGe4q9Gu3smhLYALJrr473ZH27MsnSL+LKUlimp4BWJqMDMLmPpx/Q9R3OAlL4g==",
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
      "version": "4.12.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.1.tgz",
      "integrity": "sha512-CCZCDJuduB9OUkFkY2IgppNZMi2lBQgD2qzwXkEia16cge2pijY/aXi96CJMquDMn3nJdlPV1A5KrJEXwfLNzQ==",
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
      "version": "7.1.2",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-7.1.2.tgz",
      "integrity": "sha512-gmBGslpoQJtgnMAvOVqGZpEz9dyoKTCzy2nfz/n8aIFhN/jCE/rCmcxabB6jOOHV+0WNnylOxaxBQPSvcWklhA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^6.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/strip-ansi?sponsor=
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
  "version": "2.0.9",
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
    "types-check": "tsc src/htmx.js --noEmit --checkJs --target es6 --lib dom,dom.iterable --moduleResolution node",
    "types-generate": "tsc dist/htmx.esm.js --declaration --emitDeclarationOnly --allowJs --outDir dist",
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


## File: SECURITY.md

```
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| 1.9.x   | :white_check_mark: |
| < 1.9   | :x:                |

## Reporting a Vulnerability

If you think you've found a vulnerability, please use the _Report a vulnerability_ button found in the [security tab](https://github.com/bigskysoftware/htmx/security) of the project on Github.

This process is documented in GitHub's _Secure Coding_ guide: [Privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability#privately-reporting-a-security-vulnerability). 

```


## File: TESTING.md

```
# HTMX Testing Guide

This guide outlines how to test htmx, focusing on running tests headlessly or in a browser environment, running individual tests, and other testing concerns.

## Prerequisites

1. Ensure you have a currently supported Node.js and npm installed.
2. Install dependencies by running:
   ```bash
   npm install
   npm run test
   ```
During test runs it will auto install playwright

## Running All Tests

To run all tests in headless mode, execute:
```bash
npm test
```
This will run all the tests using headless Chrome.

To run all tests against all browsers in headless mode, execute:
```bash
npm run test:all
```
This will run the tests using Playwright’s headless browser setup across Chrome, Firefox, and WebKit (Safari-adjacent).

To run all tests against a specific browser, execute:
```bash
npm run test:chrome
npm run test:firefox
npm run test:webkit
```

## Running Individual Tests

### Headless Mode
To run a specific test file headlessly, for example `test/core/ajax.js`, use the following command:
```bash
npm test test/core/ajax.js
```
If you want to run only one specific test, you can temporarily change `it("...` to `it.only("...` in the test file, and then specify the test file as above. Don't forget to undo this before you commit! You will get eslint warnings now to let you know when you have temporary `.only` in place to help avoid commiting these.

### Browser Mode
To run tests directly in the browser, simply `open test/index.html` in a browser.
On Ubuntu you can run:

```bash
xdg-open test/index.html
```
This runs all the tests in the browser using Mocha instead of web-test-runner for easier and faster debugging.

From the Mocha browser view you can rerun a just a single test file by clicking the header name or you can click on the play icon to re-play a single test. This makes it easy to update this test/code and refresh to re-run this single test. The browser console also now logs the names of the running tests so you can check here to find any errors or logs produced during each test execution. Adding debugger statements in your code or breakpoints in the browser lets you step though the test execution.

If you really want to open web-test-runner in headed mode, you can run:
```bash
npm run test:debug
```
This will start the server, and open the test runner in a browser. From there you can choose a test file to run. Note that all test logs will show up only in dev tools console unlike Mocha.

## Code Coverage Report
Lines of code coverage reporting will only work when running the default chrome headless testing

After a test run completes, you can open `coverage/lcov-report/index.html` to view the code coverage report. On Ubuntu you can run:
```bash
xdg-open coverage/lcov-report/index.html
```

## Test Locations
- All tests are located in the `test/attribues` and `test/core` directories. Only .js files in these directory will be discovered by the test runner.
- The `web-test-runner.config.mjs` file in the root directory contains the boilerplate HTML for the test runs, including `<script>` tags for the test dependencies.

### Local CI prediction
You can run `npm run test:ci` to locally simulate the result of the CI run. This is useful to run before pushing to GitHub to avoid fixup commits and CI reruns.

```


## File: .github/FUNDING.yml

```
# These are supported funding model platforms

github: [1cg]

```


## File: .github/PULL_REQUEST_TEMPLATE.md

```
## Description
*Please describe what changes you made, and why you feel they are necessary. Make sure to include
code examples, where applicable.*

Corresponding issue:

## Testing
*Please explain how you tested this change manually, and, if applicable, what new tests you added. If
you're making a change to just the website, you can omit this section.*

## Checklist

* [ ] I have read the contribution guidelines
* [ ] I have targeted this PR against the correct branch (`master` for website changes, `dev` for
  source changes)
* [ ] This is either a bugfix, a documentation update, or a new feature that has been explicitly
  approved via an issue
* [ ] I ran the test suite locally (`npm run test`) and verified that it succeeded

```


## File: .github/workflows/ci.yml

```
name: Node CI

on:
  push:
    branches: [ master, dev, htmx-2.0, v2.0v2.0 ]
  pull_request:
    branches: [ master, dev, htmx-2.0, v2.0v2.0 ]

jobs:
  test_suite:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'
      - run: npm ci
      - run: npm test

```


(… 341 more files omitted due to size limit)
<!-- fetched-content:end -->
