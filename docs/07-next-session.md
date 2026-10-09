# Next session: playing it, the picture and the sound (phases 4-5)

Phases 2 and 3 are done as far as the route goes (`09-recompiler.md`,
`11-runtime.md`): the programs and the overlays recompiled, the
self-test clean, the game booting from a new cartridge into its first
dungeon with its memories close to melonDS's. Next:

1. **The user plays it**: `ndsrun --window --save-size 65536 --out
   build/play` (the README's "Playing it"), as far as it goes. Every
   stop is a lesson for the kit (a call to a non-entry: discovery; a
   wrong return; a register not done). In particular the overlays not
   met yet: overlay 2 and the second slot's ten (battles, the airship,
   menus?), each loading should print `the overlay area ... holds`.
2. **Shadow polygons** (ndskit's renderer): the dungeon's shadows, the
   DS's stencil rules (a mask pass with polygon ID 0, then the shadow
   polygons drawn where the mask is set and the ID differs). Then what
   else the field turns on: display capture (overlay 0 holds DISPCAPCNT's
   address), edge marking, toon; read DISP3DCNT in melonDS's states and
   in the runtime.
3. **The sound** against melonDS: IMA-ADPCM on all 16 channels in the
   dungeon, then the PSG and noise programs of the effects' banks (138
   and 19): the channels' registers at the same frames
   (`melonds --compare` lists both), then the user's ears.
4. **Speed**: headless 15 times the DS where Moon runs 210; find where
   the time goes (a thread busy-waiting where Moon's halt? the cost per
   safe point?) before the window's 60 Hz pacing hides it.
5. A longer route for the oracle and the runtime: the first battle, the
   airship (each with savestates and `melonds --overlays`), so the
   comparisons follow the game past the dungeon.

Each ndskit change checked on pc-moon (`10-ndskit.md`) and by discovery
on the other two cartridges.

Before starting: MSYS2's tools on PATH (`/c/msys64/mingw64/bin`, also
SDL3.dll at run time); `git submodule update --init` after a clone; the
cartridge in `rom/`; the build as in `09-recompiler.md` (about four
minutes from nothing); `--save-size 65536` for a new cartridge.
