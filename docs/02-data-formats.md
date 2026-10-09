# The data formats, at a glance

Read from the extracted files (`build/extract`) with `tools/mass.py`
and ndskit; what is only a guess is marked *inferred*.

## MASS archives ("SSAM")

44 of the 90 files (85% of the data) are the game's own archive, named
`MASS/mass_*.dat` and read back to front "SSAM". `tools/mass.py` reads
them (`--list`, `--extract`, `--scan`); every one of the 44 parses, every
member inside its file.

    0x00  "SSAM"
    0x04  u32 count
    0x08  count entries of 0x28 bytes: u32 offset (from the end of the
          table), u32 size, char name[32] (NUL-padded; a name of 32
          characters has no NUL and is cut: "x.NCGR.", "x.dsc.l")
    then the members, aligned

Members named `.lz` are in the BIOS's LZ77 (type 0x10; a few members whose
names were cut start with an LZ11 header, 0x11). 3 251 of the 4 732 map cells (`.mmc.lz`) are 4-byte
placeholders, "DMMC", stored plain despite their name (*inferred*: empty
cells of the maps' grids). `BL_msg_cast_event_msd.dat` in the root is an
SSAM archive too (258 compressed message files, one per event).

What the members are, by name and by the magic after decompression (a
sample of each kind; `--scan`):

| Kind | Count | Magic | What |
|---|---|---|---|
| `.nmdp` | 614 | "NMDP" + a NitroSDK **BMD0** at +0x30 | models (NSBMD in a wrapper) |
| `.ntxp` | 869 | "NMDP" + **BTX0** at +0x30 | textures (NSBTX) |
| `.ncap` | 1 164 | "NCAP" + **BCA0** at +0x40 | skeletal animations (NSBCA) |
| `.namp` | 22 | "NAMP" + **BTA0** at +0x40 | texture SRT animations (NSBTA) |
| `.nsdp`, `.ntpk` | 6, 3 | "NSDP", "NTPK" | *inferred*: other G3D packs |
| `.mmc` | 4 732 | 0x00000006 or "DMMC" | map cells (towns, dungeons, the world in 18 archives) |
| `.mgpf` | 18 | 0x00000003 | *inferred*: a world map's grid |
| NCGR/NCBR, NCLR, NSCR, NCER, NANR | 2 880 | RGCN, RLCN, RCSN, RECN, RNAN | the SDK's G2D: characters, palettes, screens, cells, cell animations |
| `.face` | 48 | "NRTP" | portraits (*inferred*) |
| `.efp` | 339 | "EFCT" | effects |
| `.dsc` | 171 | "CMS2" | the events' cameras and layouts |
| `.hich`, `.script` | 351, 349 | -, "MHCS" | event data and scripts (`mass_hich.dat`) |
| `.mai` | 259 | - | monster AI (`mass_monster_ai.dat`) |
| `.pak` | 1 162 | - | the maps' parameters (`mass_MAPPARAM.dat`) |
| `.bad` | 374 | "bad " | *inferred*: battle animation data |
| `.msd` | 258 | "MSDA" | messages |

The 3D is the SDK's G3D in thin wrappers: a renderer that implements the
DS's geometry and rendering engines draws it without knowing the
wrappers, as with Moon. `mass_monster.dat` is an empty archive (no
members).

## Text ("MSDA")

The twelve `BL_msg_*.msd` files and the events' messages: "MSDA",
0x00010000, a count, then 12-byte entries (u32 id, u16 1, 0xCCCC, u32
offset) and **UTF-16LE** strings ("Eddie", "Pad", "Melody", "Fiona",
"Gilbert", ...). Two fonts, NFTR, 10x10 and 8x8.

## Other files

* `item_parameter.pak.lz`, `quest_data.lz`: LZ77.
* `SHOP/*.bbd`: shop tables (the inn's and the shop's first entry is
  "Debug Shop !", then "London Inn", ...); `SHOP/*.dsc`: "CMS2" layouts.
* `ENDING_PARAM/*.dat`, `TITLE_CUTIN_PARAM/title_cutin.dat`: small tables
  of words.
* `MASS/effect_viewer.def`: a text list of effect files, *inferred* a
  debugging tool's (as `mass_debuglobby.dat`).

## Sound

Two SDATs (`python -m ndskit.sdat FILE --list`, `--waves`):

| Archive | Records | Waves | Instruments |
|---|---|---|---|
| `sound_data.sdat` (7.3 MB, the music) | 66 sequences (`SEQ_m01`...), 25 sequence archives, 91 banks, 25 wave archives, 91 groups, 4 players | **350, all IMA-ADPCM**; rates 22 050, 44 100, 32 000, 24 000 Hz... | 494 PCM programs, 86 key splits, 59 drum sets: 2 164 sampled instruments, no PSG or noise |
| `BoysLife_SE.sdat` (7.1 MB, the effects) | 150 sequence archives (one per place or kind: `SE01_MENU`, `SE06_SKYSHIP`, `SE13_RAIN`, `SE22_LONDON`, `SE33_BABEL`...), 150 banks, 150 wave archives, 150 groups, 12 players | **621, all IMA-ADPCM** | 622 PCM, **138 PSG, 19 noise** |

No streams (no STRM records): the music is all sequenced, played by the
ARM7's sequencer, as Moon's. But where Moon's samples were PCM8 and its
banks only sampled, here **every sample is IMA-ADPCM** and the effects
use the **PSG and noise channels**. In the first dungeon, melonDS's
savestate has all 16 channels playing, every one of them ADPCM.

## Movies

None: no Mobiclip or other video file. The illustrated sequence before
the title and the opening are drawn by the game (G2D pictures and the 3D
engine).
