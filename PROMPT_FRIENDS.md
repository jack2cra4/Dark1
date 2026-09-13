# AGENT PROMPT — FRIENDS.PY ULTIMATE POWER UPGRADE
## Target: `/storage/emulated/0/1AfrozPAKS2/Dark/friends.py` (MAKE IT MAX POWERFUL)

You are a senior reverse-engineering Python engineer. Rewrite/upgrade the file
`friends.py` given below's description so EVERY feature becomes bulletproof and
readable-first. The user owns this tool personally; it is the only deliverable.

---

## HARD RULES (DO NOT BREAK)

1. **NO APP/APK BUILD.** Do NOT create an Android project, no Gradle, no
   `assembleDebug`, no GitHub Actions build. This is a pure Python tool only.
2. **KEEP THE ENTIRE MENU IDENTICAL.** Options `0..9` and every sub-menu must
   stay exactly as they are now, with the SAME labels and flow:
   - 1 UNPACK ALL TYPES PAKS
   - 2 REPACK ALL TYPES PAKS
   - 3 REPACK ANY SIZE (EXISTING FILES)
   - 4 REPACK TO PATH (NEW FILES)
   - 5 DELETE CACHE / FOLDERS
   - 6 OBB UNPACK / REPACK
   - 7 LUA UNPACK / REPACK
   - 8 UNIVERSAL DUMP (Select by Number)
   - 9 REPACK FROM DUMP
   - 0 EXIT
   No option is removed, renamed or re-ordered. You may ONLY add power INSIDE
   the existing options. Do not change branding/console styling.
3. **Single-file Python**, Python 3.8+ compatible, runs on Termux/phone (no GUI,
   no server). Runtime dependencies stay: `pycryptodome`, `zstandard`, `rich`,
   `gmalg`(optional, auto-fallback). Standard library only otherwise.
4. **NO fake success.** Every operation must report the TRUE result. If
   something cannot be decrypted/decompiled, print exactly why + save raw data
   for manual salvage. Never print "Success" for garbage output.
5. **No runtime internet** — all cipher/key tables must be embedded in the file.

---

## WHAT THE USER REPORTED (why this upgrade is needed)

1. Dump: extracts GARBAGE / useless code instead of the ORIGINAL file. There is
   usually encryption on the pack, and the tool dumps the wrong raw bytes
   without checking. It must break the encryption and output the TRUE original
   file, byte-exact.
2. Lua: unpack runs but output is NOT readable code; some Lua files are not
   unpacked/dumped AT ALL; repack fails too.
3. PAK: many packs cannot be unpacked at all ("readable nahi ban raha"),
   hence repack also fails. ANY type of pack must unpack → readable → repackable.
4. OBB: unpacks but output is NOT readable/usable; needs readable content and
   working repack.
5. "Kisi bhi tarah ka encryption laga ho — pack ho, lua ho, koi bhi app ho —
   use TODO ke readable banana aur repack karna." (If ANY kind of encryption is
   applied — packs, Lua, any app asset — break it, make it readable, and let it
   be repacked.)

---

## TECHNICAL WORK ORDER (implement ALL)

### A. UNIVERSAL DUMP → ORIGINAL FILES, NOT GARBAGE
- Containers to fingerprint automatically: Tencent **PAK** (footer layout
  versions 1..12+), **Zip/APK/JAR**, **OBB** (Zip and Android Blob), **Lua**
  bytecode (`\x1bLua` 5.1/5.2/5.3/5.4) and **LuaJIT** (`\x1bLJ` 2.0/2.1),
  plain-text Lua, SQLite (`SQLite format 3`), PNG/other COCO-assets.
- **Verify before writing**: every dumped file must be checked. For PAK entries
  compare against `TencentPakEntry.content_hash` (SHA-1). For Lua/others check
  magic + readability + entropy. If a file fails verification, automatically
  **retry with alternate decryption keys/variants/methods** from the master key
  table (below) until it passes. Only write verified, real content to disk.
- **Recursive nested processing**: after a container is dumped, scan the
  extracted bytes for embedded containers (pak-inside-pak, lua-inside-pak,
  pak-inside-obb, sqlite-inside-obb…). Auto-extract them too, so the user always
  reaches the REAL editable assets.

### B. PAK UNPACK — "ANY PAK WILL UNPACK"
- Build a **master embedded key/variant table**: multiple ZUC `KEY/IV` pairs,
  the existing `RSA_MOD_1`/`RSA_MOD_2` plus more known Tencent RSA moduli, the
  SM4 secret tables (keep `SM4_SECRET_2/4/NEW`), SIMPLE1/SIMPLE2, plus common
  RC4/XOR key candidates.
- **Auto-detect & decrypted index**: parse the 45-byte(+extensions) footer for
  versions 1..12+, read keystream, retry index decryption across ALL candidate
  keys until the recovered `index_hash` matches SHA-1 of the parsed index
  (version≥6). Guarantee the ORIGINAL index is recovered, not a wrong one.
- Robust entry parser: `TencentPakEntry` fields per version, block lists,
  `compression_block_size`, encrypted flags, `encryption_method`, dict-zstd
  (`zstddic`) dictionaries. Salvage fallback: if index truly cannot be decoded,
  do a signature/heuristic scan and still extract the recoverable file blobs +
  explain the fails.
- Output a clean file tree + `meta.json` + a `STATUS.txt` per-file (HASH_OK /
  DECRYPT_OK / RAW_SALVAGED) with CAUSES. No misleading success.

### C. PAK REPACK — CORRECT IN-PLACE REBUILD (fix current bugs)
- **Preserve the ORIGINAL compression method of every file** (zlib/zstd/
  zstd-dict/none) exactly as the entry says — today the code force-compresses
  edited files with zstd which breaks many games.
- Correctly rebuild: index bytes + same encryption as the original index
  (AES/SIMPLE1), footer with new `index_offset`/`index_size`/`index_hash` XORed
  by the same keystream, and update version-gated fields
  (`content_org_hash`, `index_new_sep`, `encryption_method`, `unk*`) so the
  rebuilt pack is structurally identical.
- Unedited entries must be **bit-exact remapped** (offsets moved, bytes copied
  verbatim); edited entries produce the exact new bytes.
- **Self-test built-in**: after a repack, run an automatic verify that the tool
  can re-unpack its own output and that unedited files hash-equal the originals.
  Report PASS/FAIL to the user.

### D. LUA — REAL DECODER + READABLE + REPACK (replace weak string-dump only)
- Replace `_process_lua_file` (currently only regex string dumps) with an
  internal **Lua decompiler**:
  - Parse full chunk: header (magic/version/format/endian/int-size/size-t/
    instr-size/lua-number-size/integral-flag), constants, prototypes, debug info.
  - Handle Lua **5.1, 5.2, 5.3, 5.4** instructions and **LuaJIT 2.0/2.1**
    (including LuaJIT cross-builds) — different opcode maps.
  - Emit **READABLE, EDITABLE Lua source** (functions, params, locals,
    constants, upvalues, safe expressions), not raw hex.
- **Encrypted Lua**: detect and break common XOR custom headers / obfuscation
  (footer-keystore, prefix-keys, AES/SM4/XOR) using embedded key tables + brute
  fallback, then decompile the real bytecode.
- **Repack Lua**: compile edited source BACK to bytecode for the SAME target
  Lua/LuaJIT version and format (helper mini-compiler), or re-apply any
  encryption transform the original used, so the game loads it.
- Always also emit a sidecar hex dump + `strings_readable.txt` for audit.

### E. OBB — READABLE UNPACK + WORKING REPACK
- Support Zip OBB **and** Android Blob OBB (main/expansion blob header magic,
  `OBB\0`, CRC, signed footer). Auto-detect which one you have.
- Recursively dump nested PAK/LUA/BIN/DATA inside so the user edits the REAL
  content, not raw blobs.
- Repack must preserve structure/compression and remain readable by the tool.

### F. CLEAN & STRUCTURED CODE
- Keep the file organized; keep the existing vendored ZUC fallback, `SM4`
  class, `Reader`, `PakInfo`/`TencentPakEntry`, `PakCompression` — extend them,
  don't delete them. Add the new engines as well-factored functions/classes.
- All `except:` that silently swallow errors must print the cause in DEBUG mode.

---

## SUBMIT BEFORE FINISHING (agent self-verification)

Run and get GREEN:
1. `python3 -m py_compile friends.py`
2. Menu sanity via scripted input (print each menu once).
3. If a sample `.pak` / `.lua` / `.obb` is available offline, run a full cycle:
   dump → SHA-1 verify vs original (unedited) → repack → re-dump → equality.
4. Fix until PASS. If you cannot fully implement a decompiler, at minimum the
   engine must break encryption and dump REAL bytecode + complete instructions,
   and clearly report the limitation.

## OUTPUT FORMAT
Deliver: the upgraded single-file `friends.py` (written in-place at the target
path) + a short per-section change log (A–F). No other files unless needed.
Then follow the standing repo protocol: `git add .` → commit
`Auto-deploy: friends.py MAX power upgrade` → push to origin main (force) →
confirm with `gh run list --limit 1`.