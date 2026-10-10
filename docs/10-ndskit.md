# What this port gave ndskit

ndskit is the game-agnostic DS toolkit born with pc-moon. This port is
its second game: where it learns whether it is game-agnostic. It is a
git submodule at `ndskit/` (URL `../ndskit`, its own repository beside
this one); pc-moon takes the same repository.

The flow of a change: committed in this port's `ndskit/` ("ndskit: ...",
the kit's files only), checked on pc-moon (its build from the
recompiler, the self-test's 81 555 vectors with no failure, its run of
466 VBlanks against melonDS's state at frame 464: 74 bytes of main RAM)
and by discovery on the user's two other cartridges (a 2010 one with a
compressed ARM9 and 366 overlays, a 2008 one with 3 overlays and mostly
Thumb code), then fast-forwarded into `D:\Homebrew6\ndskit` and taken by
both ports' submodules.

## Session 1

| Commit | What | Checked by |
|---|---|---|
| split | ndskit's eight commits out of pc-moon (`git subtree split --prefix ndskit`), its own repository; the README says how to clone a port with it | pc-moon on the submodule: build, self-test (81 555 vectors, 0 failures), 74 bytes at frame 464; a recursive clone |
| `sdat --waves` | the SWAR's waves (format, loop, rate) and the SBNK's programs (PCM, PSG, noise, drum sets, key splits) | four cartridges' five archives: Moon's 104 PCM waves and 115 instruments as its sound unit played them; this one's all ADPCM, with PSG and noise |
| `recomp.discover` | a trial descent that runs into a literal it loads itself is refused (a string's odd address had passed for Thumb code: this cartridge's only conflict) | the four cartridges' discovery, both CPUs: unchanged but for that false entry |
| `recomp.discover --overlay` | the program with one overlay loaded as its own segment; its sinit pointers as seeds; calls and jumps into an overlay from outside it taken only where they walk clean (another overlay may own the address); `{id}` in `--out` gives one list per overlay and the program's own with what only overlays reach | this cartridge's 14 overlays, 0 conflicts, every reachable function of Ghidra's; the 2008 cartridge's 3 overlays, 0 conflicts; the 2010 one's (compressed by the game itself, read as stored) without a crash; pc-moon's check unchanged |
| `melonds --overlays` | which overlay each load address holds in a savestate, by the share of its bytes found there | this cartridge's states: overlay 1 at the title (99.55%), overlay 0 in the field (99.95%) |

ndskit's commits this session: `933ee8d` (the split's README), `16e1e8a`
(`sdat --waves`), `5abc6c6` (overlays in discovery, `melonds
--overlays`). pc-moon's submodule is at `5abc6c6`.

What the kit still lacks for this game (`06-attack-plan.md`): overlays
in the recompiler and the runtime, the SDK's functions named by
signature (`FS_StartOverlay`), a fingerprint of the ARM7 components; the
sound unit's ADPCM, PSG and noise checked; display capture, edge marking,
toon in the renderer.

## Session 2

| Commit | What | Checked by |
|---|---|---|
| `ddc2f63` | discovery of C++'s tiny methods: pointers to member functions (a table neighbour 8 or 12 bytes away past small words), candidates with a boundary and a clean descent counting for each other, a function filling a gap, a return's literal pool as a function's end | the four cartridges, both CPUs: 0 conflicts; the functions added all getters, setters, empty callbacks (Moon's ARM9 6 580 to 6 613, its ARM7 943 to 944; a 2010 cartridge's protection-region setters); the three this game called |
| `31bf132` | overlays in the recompiler (a module per overlay, discovered with the program, calling its functions directly by name; the program's module with what only overlays reach) and the runtime (the resident overlay by its code's crc32, checked again after the cartridge's data and at each dispatched call; segments with a kind); `selftest --overlay` | Nostalgia from a new cartridge into its first dungeon, three changes of overlay; 100 994 vectors, no failure; pc-moon: build, 81 555 vectors, 74 bytes at frame 464, its route |
| `c814b02` | `ndsrun --save-size`: the backup memory's size for a new cartridge | Nostalgia's 512 Kbit EEPROM formatted as on melonDS (4 bytes apart); pc-moon unchanged |
| `3b94035` | the resident overlay checked by 64 sampled words, the full crc32 only when one differs; a call whose target is not the cached resident's entry checks the slot again | a run without the epoch follows the game's three changes; the route and the self-test unchanged; pc-moon unchanged |

pc-moon's submodule is at `3b94035`, recorded in its `10-ndskit.md`.

## Session 3

| Commit | What | Checked by |
|---|---|---|
| `1560296` | discovery across overlays: foreign targets (calls and data pointers from other overlays' runs, taken where they start as a function would and walk clean), the areas of overlays not loaded (a vtable neighbour, a veneer's target), any unconditional transfer ending a function, a pool of up to four loaded words after it as a boundary, a prologue after such a pool | the four cartridges, both CPUs: 0 conflicts, no function lost or split; this game through three battles and its prologue; pc-moon unchanged |
| `01da2cf` | display capture; shadow polygons through the stencil; the save written on a fatal stop | this game's pre-battle transition and dungeon shadows, played; pc-moon: build, 81 555 vectors, 74 bytes, its route and its pictures |

pc-moon's submodule is at `01da2cf`.

## From pc-lufiacots

Changes of the kit made for the third game, Lufia: Curse of the
Sinistrals, each checked here before it was taken (the build from the
recompiler, the self-test, the route into the first dungeon against
melonDS):

| Commit | What | Here |
|---|---|---|
| `b2c3fd6` | `lz`: the BIOS's Huffman (4- and 8-bit units) | - (this game's archives use LZ77 and LZ11) |
| `49a3de7` | discovery: CodeWarrior's Thumb switches, a newer ARM7's halfword tables, Thumb's `bl` as a long branch (walked as a `b`, emitted as a goto or a tail call), Thumb's return through a popped register, a conditional `movne lr, pc` call, a jump into code unrolled by two instructions, a guessed entry refused when its descent meets data | this game's discovery unchanged, program, ARM7 and every overlay (the lists identical); the build; the route from a new cartridge into the Tower of Babel with the same three changes of overlay, 2 047 bytes of main RAM apart from melonDS's state |
| `6eda9f5` | the self-test checks the overlay slots again after loading an image | the whole self-test in one command: 115 393 vectors, no failure (with the kit as published, the same command stopped overlay 1's file at its first function: 17 failures, overlay 0's code run in its place) |
| `08ba0d2` | an ARM interpreter in the runtime (code no module holds, functions the emitter cannot take; the self-test's `--interp`); overlays told apart function by function (each function's bytes checked against its module, stores marking the pages they write: the slots, the cartridge's epoch and the samples gone); a compressed program's stored image as a segment; the emitter's Thumb `add pc, rB` read unaligned; discovery's pushed-constant `pop {pc}` as a jump; `--auto` keeps only vectors that run discovered code; display capture from engine A's graphics; VRAM in the run's dump | discovery unchanged, program, ARM7 and every overlay; the whole self-test, 115 425 vectors, no failure, recompiled and interpreted; the route into the first dungeon, 2 047 bytes apart from melonDS's state as before |
| `720c636` | the overlay log tells each change of hands | the route's log: overlays 0, 1, and 0 again at frame 2 792 |

The submodule is at `720c636`, as pc-moon's.
