// THE WORLD IN A DAY — news-image-20261124 entry program.
//
// The repository holds one rendered front page, entry.png, summing up the
// world news of Tuesday 24 November 2026 (stories and citations in
// design/sources.md; the page itself is drawn by design/render.py).
// This program validates that image against the competition gate —
// PNG or JPEG by magic bytes, at most 1024x1024 pixels, at most 1 MiB —
// and copies it, byte for byte, to the output directory as entry.png.
// It runs offline with the Node standard library only, and writes the
// same bytes on every run.

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1_048_576; // 1 MiB
const MAX_DIM = 1024;

interface ImageInfo {
  format: "png" | "jpeg";
  width: number;
  height: number;
  bytes: number;
}

// Locate the repository root: the bot mounts the repo at MAKEFUN_BOT_DIR;
// when run by hand the script sits at the repo root itself.
function repoRoot(): string {
  const fromEnv = process.env.MAKEFUN_BOT_DIR;
  if (fromEnv && existsSync(join(fromEnv, "entry.png"))) return fromEnv;
  return dirname(fileURLToPath(import.meta.url));
}

// Locate the output directory: MAKEFUN_OUTPUT_DIR wins, then /output,
// then a local ./output next to the repo for manual runs.
function outputDir(root: string): string {
  const fromEnv = process.env.MAKEFUN_OUTPUT_DIR;
  if (fromEnv) return fromEnv;
  if (existsSync("/output")) return "/output";
  return join(root, "output");
}

// Read the image's real format and dimensions from its own bytes:
// PNG from the IHDR chunk, JPEG by walking segments to a start-of-frame.
function inspectImage(buf: Buffer): ImageInfo {
  if (
    buf.length >= 24 &&
    buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47 &&
    buf[4] === 0x0d && buf[5] === 0x0a && buf[6] === 0x1a && buf[7] === 0x0a
  ) {
    return {
      format: "png",
      width: buf.readUInt32BE(16),
      height: buf.readUInt32BE(20),
      bytes: buf.length,
    };
  }
  if (buf.length >= 4 && buf[0] === 0xff && buf[1] === 0xd8) {
    let off = 2;
    while (off + 9 < buf.length) {
      if (buf[off] !== 0xff) break;
      const marker = buf[off + 1];
      const len = buf.readUInt16BE(off + 2);
      if (marker >= 0xc0 && marker <= 0xc3) {
        return {
          format: "jpeg",
          height: buf.readUInt16BE(off + 5),
          width: buf.readUInt16BE(off + 7),
          bytes: buf.length,
        };
      }
      if (len < 2) break;
      off += 2 + len;
    }
  }
  throw new Error("entry.png is neither a PNG nor a JPEG (bad magic bytes)");
}

// Validate the image against the gate, then copy it to the output.
function main(): void {
  const root = repoRoot();
  const sourcePath = join(root, "entry.png");
  const buf = readFileSync(sourcePath);
  const info = inspectImage(buf);

  if (info.bytes > MAX_BYTES) {
    throw new Error(`entry.png is ${info.bytes} bytes, over the 1 MiB limit`);
  }
  if (info.width > MAX_DIM || info.height > MAX_DIM) {
    throw new Error(
      `entry.png is ${info.width}x${info.height}, over the 1024x1024 limit`,
    );
  }
  if (info.width === 0 || info.height === 0) {
    throw new Error("entry.png has a zero dimension");
  }

  const outDir = outputDir(root);
  mkdirSync(outDir, { recursive: true });
  const outPath = join(outDir, "entry.png");
  writeFileSync(outPath, buf);

  // Read the copy back and prove it is the same bytes we validated.
  const written = readFileSync(outPath);
  if (!written.equals(buf)) {
    throw new Error("output entry.png differs from the source image");
  }

  console.log(
    `entry.png: ${info.format} ${info.width}x${info.height}, ` +
      `${info.bytes} bytes -> ${outPath}`,
  );
}

main();
