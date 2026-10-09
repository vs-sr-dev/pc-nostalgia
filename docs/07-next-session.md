# Next session: the recompiler with overlays (phase 2)

Session 1 read the cartridge and the code and wrote the plan
(`06-attack-plan.md`). ndskit is its own repository now, a submodule
here and in pc-moon; discovery reads overlays. Next, phase 2: everything
compiled and linked, and checked by the self-test.

1. **The recompiler and overlays** (ndskit, `recomp.emit` and
   `python -m ndskit.recomp`): one module per overlay, emitted with the
   program's functions as known entries (calls out of an overlay are
   ordinary calls); the program's module with the functions only
   overlays reach (`--overlay all`'s `main` list). Calls from the
   program into an overlay's region go through the runtime's dispatch,
   which picks the resident overlay's module. The modules' names carry
   the overlay's id and crc32.
2. **The resident overlay** (ndskit's runtime): a slot's owner set when
   the SDK's `FS_StartOverlay` runs (found by signature, 0x0200CBF0 here;
   its entry's first word is the id), with a check of the slot's crc32
   against the module's on the first call, so a wrong guess is loud.
   Before that: read the 117 direct calls (which overlays have a
   function at each target).
3. **The ARM7**: recompiled as Moon's; its crc32 named in a
   `fingerprint` table of the SDK's components (layer 1).
4. **The self-test**: the instruction test of both CPUs, and vectors
   from this game's functions that run alone (`recomp.selftest --auto`;
   with overlays, from each overlay's module too).
5. Then phase 3 can start: `ndsrun` booting Nostalgia, the title against
   `build/oracle/title.ml1` (VBlank 2 680), overlay 1 resident.

Each ndskit change checked on pc-moon (its check: build, 81 555 vectors,
74 bytes at frame 464) and discovery on the other two cartridges, as
`10-ndskit.md` says.

Before starting: MSYS2's tools on PATH (`/c/msys64/mingw64/bin`);
`git submodule update --init` after a clone; the cartridge in `rom/`.
The oracle's route is in `06-attack-plan.md`.
