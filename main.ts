// "The World in One Day" -- entry for make.fun news-image-20261126.
// Node 22, standard library only. The image was drawn by draw.py (same
// repository) and is held here as entry.png; this program copies those
// exact bytes to the grader's output file, so the run is deterministic.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The directory this file lives in is the repository root, where entry.png
// sits beside it. __dirname is not defined in ESM, so derive it from the
// module URL instead.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

// The grader sets /output as the destination; outside it,
// MAKEFUN_OUTPUT_DIR stands in for /output.
const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(destDir, { recursive: true });

const bytes = readFileSync(source);
const dest = join(destDir, "entry.png");
writeFileSync(dest, bytes);

// Fail loudly instead of silently shipping a truncated copy.
if (readFileSync(dest).length !== bytes.length) {
  throw new Error("entry.png was not copied whole");
}
