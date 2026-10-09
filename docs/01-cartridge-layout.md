# The cartridge

Everything here was read from the cartridge with ndskit (`python -m
ndskit.rom ROM --info`, `--list`, `--extract build/extract --nested`) or
seen running in melonDS, unless marked *inferred*.

## Identity

| Field | Value |
|---|---|
| File | `Nostalgia (USA).nds`, 128 MiB image, 0x07031F7C bytes used |
| Title, code, maker | `NOSTALGIA`, `CJKE` (USA), `7U` (Ignition Entertainment) |
| Unit, region, version | 0 (DS), 0, 0 |
| Header CRC, logo CRC | 0x1769, 0xCF56: both correct |
| Secure area | decrypted (the 0xE7FFDEFF marker), its CRC 0x75E8 |
| SDK | NitroSDK 4.2 (ModuleParams' relstep 30001), the same as Moon's |
| Banner | version 1; every language: "Nostalgia / Ignition  Entertainment" |
| Internal name | "BoysLife": the sound archive `BoysLife_SE.sdat`, the `BL_` prefix of the message files, the banner file `bl.bnr` |

On screen (melonDS, the boot): the logos of Ignition Entertainment ("a UTV
enterprise"), "Licensed by Nintendo", Tecmo, RED Entertainment and Matrix
Software, each pair on the two screens; then an illustrated sequence and
the title, whose lower screen reads "© TECMO, LTD. / RED 2009 — Published
by Ignition Entertainment Ltd." (the year read pixel by pixel). The
Matrix Software logo also carries that line. No developer's name is in
the cartridge as text; the credits are pictures (`MASS/mass_ending.dat`,
unread).

## The two programs

| | ARM9 | ARM7 |
|---|---|---|
| Stored at | 0x4000, 0x9CDD8 bytes | 0x1C7000, 0x26F28 bytes |
| Runs at | 0x02000000, entry 0x02000800 | 0x02380000, entry 0x02380000 |
| Compressed | **no** (ModuleParams at 0x02000BA0: no compressed end) | no |
| crc32 | 0xED4537CE | **0x3DFBBAA1** (Moon's: 0x1B16DBE2) |
| Static BSS | 0x0209CA40-0x020BB360 | |
| Autoloads | ITCM 0x01FF8000 (0x320 bytes), DTCM 0x027E0000 (0x60, BSS 0x20) | shared WRAM 0x037F8000 (0xF4B0, BSS 0x3E64), main RAM 0x027E0000 (0x17878, BSS 0x1968) |

The ARM7 is the SDK's component, as Moon's, but not byte-identical to it:
discovery finds 943 functions in each, 818 identical at the same address,
16 identical elsewhere, 109 different (73 in main RAM, 36 in the shared
WRAM; `03-executables.md`).

## Overlays

14 ARM9 overlays, none for the ARM7, **none compressed** (the overlay
table's flag clear on all, and each file its RAM size). They share two
load addresses:

| Slot | Overlays | Sizes |
|---|---|---|
| 0x020BB360 (right after the static BSS) | 0, 1, 2, 3 | 0x3CC40, 0x48D20, 0x51F60; overlay 3 is 0x20 bytes of zeros |
| 0x0210DB40 | 4-13 | 0x36E0 to 0x10B80 |

Each slot's area ends at most at 0x0211E6C0 (overlay 8 with its BSS).
Overlay 3, all zeros with an empty initialiser table, is *inferred* to
be a placeholder that empties the first slot.

Which one is loaded, read from melonDS's savestates (`python -m
ndskit.melonds STATE --overlays ROM`, the share of each overlay's bytes
found in memory):

| Moment | First slot | Second slot |
|---|---|---|
| the title's menu (VBlank 2 680) | overlay 1 (99.55%) | none (the best, overlay 5, 19%) |
| the opening scene, the first dungeon (VBlanks 3 220-8 890) | overlay 0 (99.95%) | none |

So overlay 0 is the field; overlay 1 the title and, with overlay 4 in
the second slot, the battles (seen in play, session 3); overlay 2 and the
second slot's other nine wait for the airship, the menus, the towns.

## File system

104 files in 9 directories: 90 named files and the 14 overlays. Every FAT
entry is named; no NitroROM image is nested (`--nested` finds none).

| Directory | Files | Bytes | Share of the used image |
|---|---|---|---|
| `MASS/` | 44 | 99 713 933 | 84.8% |
| `SOUND/` | 2 | 14 410 656 | 12.2% |
| the root | 15 | 1 301 073 | 1.1% |
| `SAMPLE/` | 16 | 141 608 | 0.1% |
| `SHOP/`, `FONT/`, `ENDING_PARAM/`, `TITLE_CUTIN_PARAM/` | 13 | 29 408 | |
| the overlays | 14 | 1 200 416 | 1.0% |

* `MASS/`: the game's own archives ("SSAM", `02-data-formats.md`): the
  characters, the camera and motion of the events, the maps of the
  towns, the dungeons and the world, the effects, the menus, the faces,
  the navigation maps, the title, the ending.
* the root: twelve message files (`BL_msg_*.msd`, one an archive of 258
  event scripts' texts), the item parameters and the quest data
  (`.lz`), the banner `bl.bnr`.
* `SOUND/`: two sound archives, `sound_data.sdat` (the music) and
  `BoysLife_SE.sdat` (the effects).
* `SAMPLE/`: G2D files named like the SDK's samples (`WT_test1_256`,
  `op_window`): left over, *inferred* unused.
* `SHOP/`: the shops' tables (`.bbd`, the first named "Debug Shop !") and
  four weapon pictures' layouts (`.dsc`).
* `FONT/`: two NFTR fonts, 10x10 and 8x8.

## The save

**EEPROM, 512 Kbit (64 KiB)**: the game's save module (0x02081784) passes
0x1001 to the SDK's backup functions, which is
`CARD_BACKUP_TYPE_EEPROM_512KBITS` (device 1, size 2^16); melonDS made a
64 KiB save file for it. Not a flash chip: the same bus as Moon's EEPROM
(64 Kbit), larger. The menu's text mentions a quick save ("Quick save
completed. Please turn off the Nintendo DS Series System", then "Note
about quick save DATA: This DATA will be deleted the nex[t ...]").
