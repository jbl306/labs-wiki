import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";

const dockerfile = fs.readFileSync(
  path.resolve(import.meta.dirname, "../../Dockerfile.graph-ui"),
  "utf8",
);

test("graph UI image copies all top-level JS modules", () => {
  assert.match(dockerfile, /wiki-graph-ui\/\*\.js/);
});
