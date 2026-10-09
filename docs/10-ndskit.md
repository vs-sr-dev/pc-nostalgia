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
