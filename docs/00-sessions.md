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

## Session 2 (2026-10-09) — overlays recompiled and dispatched; into the first dungeon

* **The recompiler and overlays** (`09-recompiler.md`): one module for
  the ARM9's program, one per overlay (13 with code), one for the ARM7;
  each overlay discovered with the program loaded and calling its
  functions directly; the program's module with every function only
  overlays reach (5 270). 42 MB of C++, built by clang without a warning.
* **The runtime and overlays** (`11-runtime.md`): an address in an
  overlay's area looked up in the resident overlay's module, recognised
  by its code's crc32, checked again by sampled words when the cartridge
  has delivered data, and by the first instruction of every dispatched
  call; either check alone follows the game.
* **Nostalgia runs**: from a new cartridge, through the logos and the
  title, "New Game", the opening in 3D, into the Tower of Babel's 5F,
  the first slot changing hands three times (overlay 0, 1, then 0).
  Against melonDS: at the title 1 458 bytes of 4 MiB of main RAM differ,
  in the dungeon (frame 8 361) 2 112, most of them the sound sequencer's
  state; the ITCM and the shared WRAM not at all. The pictures as
  melonDS's.
* **Three more forms in discovery**, met running the game: C++'s
  pointers to member functions (records of two or three words), tables
  of tiny methods none of them known, a method filling a gap between two
  functions; and a return's literal pool as a function's end.
* **The self-test**: 100 994 vectors, no failure: the instruction test,
  2 017 of the program's functions, 172 of the ARM7's, 559 of overlay
  0's through the overlay dispatch.
* **The save**: a 512 Kbit EEPROM needs `ndsrun --save-size 65536` for a
  new cartridge (new in ndskit); the game formats it as on melonDS (4
  bytes apart).
* **Met, not done**: shadow polygons in the dungeon (not drawn yet);
  headless speed 15 times the DS (Moon's 210), its cause not measured.
* ndskit's commits checked on pc-moon each time (its build, 81 555
  vectors with no failure, 74 bytes at frame 464, its route into the
  first room) and by discovery on the other two cartridges.
