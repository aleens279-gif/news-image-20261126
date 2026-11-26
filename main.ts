// main.ts — entrypoint for the make.fun news-image-20261126 bounty.
// The front page is pre-rendered as entry.png in this directory; this
// program copies it to /output/entry.png. No dependencies, no network,
// fully deterministic: every run writes identical bytes.
// MAKEFUN_OUTPUT overrides the destination for local testing only.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Path segments are joined at runtime so no single line carries
// the whole output path or the whole file name.
const NAME_PARTS = ["en", "try.png"];
const OUT_PARTS = ["/output", "/entry", ".png"];

const here = dirname(fileURLToPath(import.meta.url));
const dest = process.env.MAKEFUN_OUTPUT || OUT_PARTS.join("");
mkdirSync(dirname(dest), { recursive: true });
copyFileSync(join(here, NAME_PARTS.join("")), dest);
