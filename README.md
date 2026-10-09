# pc-nostalgia

A native PC port, in the making, of **Nostalgia** (Nintendo DS; Red
Entertainment and Matrix Software, © Tecmo; the North American release
published by Ignition Entertainment, "© TECMO, LTD. / RED 2009" on its
title), a turn-based RPG with a 3D world and an airship: Eddie,
Gilbert Brown, London, the Tower of Babel. Both of the cartridge's
programs are to be recompiled statically to C++ and run on a runtime
that replaces the DS's hardware, the 3D drawn by the PC's GPU at the
window's resolution.

It is the second game of **ndskit**, the game-agnostic DS toolkit born
with [pc-moon](https://github.com/vs-sr-dev/pc-moon); ndskit is a git
submodule at `ndskit/`: clone with `--recursive` (or run `git submodule
update --init` after a clone).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data,
no executables, no assets. You need your own cartridge, dumped. The work
is done on the North American release, `Nostalgia (USA).nds` (game code
CJKE, version 0, NitroSDK 4.2), a 128 MiB image with its secure area
decrypted, placed in the repository's root or in `rom/`.

## Layout

    docs/            cartridge, format and code analysis, and the plan
    tools/           Nostalgia-specific tools: mass.py (the game's archives), oracle.py (melonDS)
    ndskit/          the game-agnostic DS toolkit (a submodule)
    rom/, build/     your cartridge and everything derived from it (ignored by git)

## Tools

Python 3, no dependencies (the oracle needs PIL for its pictures, and a
copy of melonDS for itself: `ORACLE_DIR`, `tools/oracle.py`). From the
repository's root:

```sh
ROM="rom/Nostalgia (USA).nds"

# the cartridge: header, programs, autoloads, overlays, SDK, banner; its files
python -m ndskit.rom "$ROM" --info
python -m ndskit.rom "$ROM" --list
python -m ndskit.rom "$ROM" --extract build/extract --nested

# the game's archives (MASS/*.dat, "SSAM"), the sound archives
python tools/mass.py --scan build/extract
python tools/mass.py build/extract/MASS/mass_title.dat --extract build/mass_title --lz
python -m ndskit.sdat build/extract/SOUND/sound_data.sdat --list
python -m ndskit.sdat build/extract/SOUND/BoysLife_SE.sdat --waves

# the code: every function of the ARM9, of each overlay with it, of the ARM7
python -m ndskit.recomp.discover "$ROM" --cpu 9 --overlay all --report --out "build/disc/ov{id}.tsv"
python -m ndskit.recomp.discover "$ROM" --cpu 7 --report --out build/disc/disc7.tsv
python -m ndskit.arm "$ROM" --offset 4000 --size 9CDD8 --base 02000000 --at 0200CBF0 --count 60

# the oracle: melonDS from a new cartridge into the first dungeon, and its states read
python tools/oracle.py --fresh --at 40:START,41:START,46:A,140:state
python -m ndskit.melonds build/oracle/t140.ml1 --overlays "$ROM"
```

## Status

Session 1: feasibility. ndskit split out of pc-moon into its own
repository and taken back by both ports as a submodule. The cartridge
read (a plain ARM9, 14 overlays in two slots, an ARM7 component near
Moon's but not it, a 512 Kbit EEPROM save), the formats at a glance (the
game's "SSAM" archives holding the SDK's own 2D and 3D formats, text in
UTF-16, every sound sample IMA-ADPCM, PSG and noise in the effects), the
code mapped with no conflict (ARM9 and its overlays 11 609 functions,
all of Ghidra's that can run), the frame rate measured (30), the oracle
driven into the first dungeon, and the plan: Moon's road, with overlays
as modules (`docs/06-attack-plan.md`).

## Documentation

* [00-sessions.md](docs/00-sessions.md) — what each session did
* [01-cartridge-layout.md](docs/01-cartridge-layout.md) — header, programs, overlays, the file system, the save
* [02-data-formats.md](docs/02-data-formats.md) — the game's archives, the 3D and 2D, text, sound
* [03-executables.md](docs/03-executables.md) — crt0, main, the overlays' loading, the frame, discovery against Ghidra, the ARM7
* [04-curiosities.md](docs/04-curiosities.md) — things found on the way
* [05-open-questions.md](docs/05-open-questions.md) — what is not known yet
* [06-attack-plan.md](docs/06-attack-plan.md) — what is new against Moon, a better Nostalgia on PC, the phases, the oracle's route
* [07-next-session.md](docs/07-next-session.md) — the next session's list
* [10-ndskit.md](docs/10-ndskit.md) — what this port gave ndskit

## Licence

MIT — see [LICENSE](LICENSE). Nostalgia is © Tecmo, Ltd. and Red
Entertainment; this project contains none of it.
