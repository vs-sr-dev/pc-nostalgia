# Next session

Nostalgia plays on ndskit: the user went from a new cartridge through the
first dungeon, three battles and the prologue's end to the first cutscene
with Edward without a stop (`00-sessions.md`, session 3). Next, in this
order:

1. **Keep playing**: Edward's chapter, the first town, the airship. Every
   new overlay (2, and the second slot's nine besides 4) prints `the
   overlay area ... holds`; every stop is a lesson for discovery (a call
   to a non-entry: look for the pointer and why its marks were missing,
   fix it in ndskit, check the four cartridges). A stop now keeps the
   save.
2. **The sound against melonDS**: IMA-ADPCM on all 16 channels, then the
   effects' PSG and noise (138 and 19 programs): the channels' registers
   at the same frames (`melonds --compare`), then the user's ears.
3. **The picture against melonDS**: the shadows (the DS's rule that a
   shadow skips its own polygon ID, not followed yet), the pre-battle
   capture, edge marking and toon if the field turns them on (DISP3DCNT
   in melonDS's states).
4. **Speed**: headless 15 times the DS where Moon runs 210; where does the
   time go.
5. **Publication**: the rule is a kit proven on two games, Nostalgia
   working "until proven otherwise". When the user judges it there, the
   three repositories (ndskit, pc-moon, pc-nostalgia) are swept (no
   cartridge content in any history, a clean recursive clone builds and
   runs) and created and pushed by the user, together.
6. Then phase 7 for both games: the PC versions (the screens' layout,
   the frame rate, the capture at the 3D's resolution, controls).

Before starting: MSYS2's tools on PATH (`/c/msys64/mingw64/bin`, also
SDL3.dll at run time); `git submodule update --init` after a clone; the
cartridge in `rom/`; the build as in the README (about four minutes from
nothing); `--save-size 65536` for a new cartridge.
