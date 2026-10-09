# Sessions

## Session 1 (2026-10-09) — ndskit split out, the cartridge, the code, the oracle, the plan

* **ndskit is its own repository** (`10-ndskit.md`): split out of
  pc-moon with its history (`git subtree split`), into
  `D:\Homebrew6\ndskit`, and taken back as a git submodule at `ndskit/`
  by both ports (a relative URL). pc-moon checked on the submodule: its
  build, the self-test (81 555 vectors, no failure), its run against
  melonDS (74 bytes of main RAM at frame 464), unchanged; a clean
  recursive clone works.
* **The cartridge** (`01-cartridge-layout.md`): the US release, CJKE,
  Ignition (7U), NitroSDK 4.2 as Moon; the ARM9 stored plain; **14 ARM9
  overlays** in two slots, none compressed, overlay 3 a placeholder of
  zeros; an ARM7 component that is not Moon's (crc32 0x3DFBBAA1), 834 of
  its 943 functions identical to Moon's; 104 files, 85% of them the
  game's own "SSAM" archives; the save an **EEPROM of 512 Kbit**, read
  in the code (not a flash chip). On screen: Ignition, Tecmo, RED
  Entertainment and Matrix Software, "© TECMO, LTD. / RED 2009"; the
  user confirmed Matrix Software's logo as the last before the
  illustrated sequence, then photographed.
* **The formats** (`02-data-formats.md`): `tools/mass.py` reads the SSAM
  archives (all 44); the 3D is the SDK's G3D (BMD0, BTX0, BCA0, BTA0) in
  thin wrappers, the 2D its G2D; text in UTF-16LE; two sound archives,
  all sequenced, **every sample IMA-ADPCM**, the effects' banks with 138
  PSG and 19 noise instruments; no movies, no streams.
* **The code** (`03-executables.md`): crt0, `main` at 0x02000BDC, the
  SDK's `FS_StartOverlay` at 0x0200CBF0; 117 direct calls from the
  program into the overlays' regions. Discovery: the ARM9 with its
  overlays 5 239 functions, the overlays 6 370, the ARM7 943, **0
  conflicts**; every function of Ghidra's that can run is found (4 090
  of 4 101, the rest dead code). **30 frames a second**, measured three
  ways (the opening, the dungeon standing and walking). The code loads
  the display capture's register in overlay 0, and the edge, toon and
  fog registers.
* **The oracle**: `tools/oracle.py` (pc-moon's, with `down:`/`up:`);
  from a new cartridge into the first dungeon (Tower of Babel, 5F) with
  three presses, controllable at about two minutes; states at the title,
  the opening and the dungeon. Overlay 1 is the title's, overlay 0 the
  field's.
* **ndskit gained** (`10-ndskit.md`): discovery with an overlay loaded
  (`--overlay`), a false Thumb entry refused (a string's odd address),
  `sdat --waves`, `melonds --overlays`; each checked on pc-moon and the
  user's other two cartridges.
* **The plan** (`06-attack-plan.md`): Moon's road; new here the
  overlays as modules with a dispatch by the resident overlay, the other
  ARM7, ADPCM, PSG and noise, display capture and the 3D's extra
  features; on PC the 3D at the screen's resolution (the capture too),
  30 steady then 60 by interpolation, the screens' layout.
