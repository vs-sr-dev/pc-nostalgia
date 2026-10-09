# The code

Read with ndskit (`arm`, `recomp.discover`) and Ghidra 12.1.2, and seen
running in melonDS through its savestates. *Inferred* marks what is
read from the shape of the code without a run to confirm it.

```sh
ROM="rom/Nostalgia (USA).nds"
A9="--offset 4000 --size 9CDD8 --base 02000000"
python -m ndskit.arm "$ROM" $A9 --at 02000800 --count 80     # crt0
python -m ndskit.arm "$ROM" $A9 --at 02000BDC --count 6      # main
python -m ndskit.recomp.discover "$ROM" --cpu 9 --report --out build/disc/disc9.tsv
python -m ndskit.recomp.discover "$ROM" --cpu 9 --overlay all --report --out "build/disc/ov{id}.tsv"
python -m ndskit.recomp.discover "$ROM" --cpu 7 --report --out build/disc/disc7.tsv
```

## The ARM9

* **crt0** at 0x02000800: the SDK's, as Moon's (CP15, the TCMs, the
  stacks, the autoloads through ModuleParams at 0x02000BA0, the BSS),
  then `bx` to `main` at **0x02000BDC** with lr = 0xFFFF0000.
* **`main`** (0x02000BDC) is four calls: 0x0204AC5C (the set-up),
  0x0208AAA0 (the game), 0x0204BF7C, 0x02007E08 (*inferred*: the end,
  never reached).
* The ARM9 is stored plain, the overlays too: nothing to decompress
  before reading the code.

### The overlays' loading

The SDK's **`FS_StartOverlay`** is at **0x0200CBF0**, read: it checks the
boot type at 0x027FFC40 (a download-play child verifies the overlay's
digest), undoes the backward LZ when the entry's flag says so (bit 0 of
byte 0x1F, `MI_UncompressBackward` at 0x02000970; never set on this
cartridge), flushes the cache over the overlay, then calls each non-zero
pointer between the entry's sinit start (+0x10) and end (+0x14). The
loading before it goes through the cartridge's registers like every
other read. This is the one place where the runtime can know which
overlay has just become resident, and its id is the entry's first word.

The main program calls into the overlays' regions directly: **117 call
sites** (`bl` into 0x020BB360-0x0211E6C0) and 64 literal pointers. The
same address means different code in different overlays, so whatever
the recompiler does with these calls has to look at which overlay is
resident.

### The frame

**30 frames a second**, measured in melonDS from pairs of savestates two
seconds apart (`tools/oracle.py`, the method of pc-moon's session 2): the
game's counters at 0x0209CEC4, 0x0209CEE0, 0x0209CF20, 0x020AAFC8 and
0x020BAC18 advance by half the SDK's VBlank count, in three situations:

| Moment | VBlanks | Counters |
|---|---|---|
| the opening scene (3D, a dialogue box) | +104 | +52 |
| the first dungeon, standing | +120 | +60 |
| the first dungeon, walking (DOWN, then LEFT, held) | +119, +119 | +59/+60, +60 |

No counter of the game's advanced once per VBlank. 0x0209CEE0 is
incremented by 0x02009D80, which queues a frame's command buffer (0x1800
bytes at 0x0209D1A0) in a ring of nine (0x0209CEE4) and waits while
eight are queued: the frames produced. *Not read yet*: where the frame
loop waits for its two VBlanks, and whether a heavier place drops to 20.

### What it draws with

The code loads the addresses of DISP3DCNT, the edge colours, the toon
table, the fog's colour, offset and table, the clear colour and
POLYGON_ATTR in the main program (the SDK's G3X library, linked), and
**DISPCAPCNT, the display capture, in overlay 0** (the field), with
DISP3DCNT and the fog's colour. *Inferred*, to see in the runtime: the
field uses display capture (a transition or a blur), fog, and perhaps
edge marking and toon shading.

## Function discovery against Ghidra

The numbers below are session 1's. Session 2 taught discovery three
forms of C++'s tiny methods, met running the game: the program alone has
4 907 functions now, with what its overlays reach 5 270, overlay 0 1 824
(`09-recompiler.md`).

| Program | Functions | Thumb | Switches | Conflicts |
|---|---|---|---|---|
| ARM9 alone | 4 899 | 31 | 94 (1 143 targets) | 0 |
| ARM9 with what its overlays reach | 5 239 | | | 0 |
| overlay 0 (the field) | 1 714 | 36 | | 0 |
| overlay 1 (the title) | 2 221 | 2 | | 0 |
| overlay 2 | 1 102 | 0 | | 0 |
| overlay 3 | 0 (32 zero bytes) | | | 0 |
| overlays 4-13 | 216, 395, 106, 145, 251, 32, 79, 35, 37, 37 | 0 | | 0 |
| ARM7 | 943 | 9 | 40 (712 targets) | 0 |

11 609 functions in all for the ARM9's code (5 239 and the overlays' 6 370). Each overlay is discovered
with the program, loaded at its address (ndskit's `--overlay`, new this
session); main-program functions that only overlays call (340 of them)
are found that way, and must be in the main program's module.

**Against Ghidra** (12.1.2, auto-analysis of the ARM9 as a flat binary
with the entry as root, `ndskit/ghidra/ExportFuncs.java`): 4 101
functions in the main program. The program alone covers 3 980 as
entries; with what the overlays reach, **4 090**. The 11 left
(0x0201C518-0x0201D6EC and 0x0201DD90) are a cluster of dead code: no
call, branch or pointer reaches them from the program or any overlay,
only from each other, and the first is a leaf after a literal pool,
which no rule of discovery may take. They never run. 1 143 of ours are
not in Ghidra's (vtables' methods and thunks, as on Moon).

What discovery got wrong on the first run: a string's address with bit
0 set (`"%s.face.lz"` at 0x02099CB3, passed to the formatter) was taken
for a Thumb function and ran into a vtable: one conflict. Fixed in ndskit
(a trial descent may not run into a literal it loads itself); on Moon
and the two other cartridges nothing changed.

Not resolved: 1 140 calls or jumps through registers in the main program
(C++'s virtual calls, the SDK's callbacks; resolved at run time by the
recompiler's dispatch), 2 of them jumps.

## Thumb

Little: 31 functions in the main program, 36 in overlay 0, 2 in overlay
1, none in the others (Tales of Innocence, by contrast, is almost all
Thumb). No conflict and only two unresolved jumps: CodeWarrior's Thumb
switches, a known gap of discovery, do not seem to bite here.

## The ARM7

The SDK's component, crc32 0x3DFBBAA1 (Moon's 0x1B16DBE2), 0x26F28 bytes
(Moon's 0x27080). Discovery: 943 functions, 37 607 instructions, 40
switches, 0 conflicts. Function by function against Moon's: **818
byte-identical at the same address, 16 identical elsewhere, 109
different** (73 in its main-RAM part, 36 in the shared WRAM). The same
library in a near version; which of its parts differ (the sound driver,
the wireless, the backup) is still to read. Its 40 switches are ARM
ones: the newer SDK's halfword-offset tables (a known gap of discovery)
are not here.

The ARM7 serves what Moon's served (*inferred* from the same component:
the sound, the touch screen, the RTC, the power, the backup memory) and
plays all 16 sound channels in ADPCM in the first dungeon (seen in
melonDS's savestate).
