# The runtime: Nostalgia on ndskit's machine

ndskit's runtime (pc-moon's `docs/11-runtime.md`, `12-picture.md`,
`13-sound.md`) runs Nostalgia's recompiled programs. This session it
learnt overlays; everything else Nostalgia met, Moon had already asked
for.

```sh
ROM="rom/Nostalgia (USA).nds"
export PATH=/c/msys64/mingw64/bin:$PATH          # SDL3.dll at run time
build/recomp/b/ndsrun "$ROM" --out build/route --save-size 65536 --vblanks 8400 \
    --input "2382:START,2442:START,2742:A" --shots 2680,5499,8361
python -m ndskit.melonds build/oracle/dungeon.ml1 --compare build/route
build/recomp/b/ndsrun "$ROM" --window --save-size 65536 --out build/play   # to play
```

## Overlays at run time

An address in an overlay's load area (0x020BB360 for overlays 0-3,
0x0210DB40 for 4-13) that is not an entry of the program's module is
looked up in the module of the overlay resident there:

* **Recognised by its code**: the crc32 of the module's code ranges,
  read from memory. The overlay's data changes once it runs and is left
  out.
* **Checked again** when memory may have changed under it: the cartridge
  counts every word it delivers (an epoch); after that the resident
  overlay's 64 sampled words are compared, and the full crc32 only when
  one differs (and then every overlay of the slot is tried).
* **Checked at every dispatched call**: the target's first instruction
  must be the module's; and a target that is not the cached resident's
  entry makes the slot be checked again before the call fails. Either of
  these alone follows Nostalgia's overlays: a build without the epoch
  (a test, not kept) walks the same route with the same three changes.
* A change of hands is reported: `the overlay area 020BB360 holds
  ARM9_OV1`.

In a run from a new cartridge, the first slot holds overlay 0 at frame
5, overlay 1 at frame 6 (the title's, through the logos and the
illustrated sequence), and overlay 0 again at frame 2 792, after "New
Game" (the field, the opening and the dungeon). The second slot stays
empty along the route. melonDS's states agree: overlay 1 at the title,
overlay 0 in the opening and the dungeon.

## The save

The backup memory is a 512 Kbit EEPROM (`01-cartridge-layout.md`): a new
cartridge needs `--save-size 65536` (ndskit's default, 8 KiB, would wrap
its 2-byte addresses at 8 KiB). The game formats it at its first boot;
after 3 000 frames the runtime's save equals melonDS's but for 4 bytes at
0xFF0C (*inferred*: a date or a time).

## Against melonDS

The route of `06-attack-plan.md` pressed at the frames of the oracle's
presses (a press at wall-clock second t lands near frame 60 t - 18): START
at 2 382 and 2 442, A at 2 742.

| Frame (SDK's VBlank count) | State | Main RAM | ITCM | DTCM | Shared WRAM | ARM7's WRAM |
|---|---|---|---|---|---|---|
| 2 680, the title's menu, no press | `title.ml1` | 1 458 bytes in 104 ranges | 0 | 31 | 0 | 1 054 |
| 8 361, the first dungeon | `dungeon.ml1` | 2 112 bytes in 169 ranges | 0 | 49 | 0 | 1 068 |

Most of what differs is the sound: the sequencer's state, in main RAM
at 0x020AB000-0x020AD000 and in the ARM7's WRAM, a few frames apart, the
same kind of offset Moon's sound had (the cartridge answers at once,
melonDS takes time; pc-moon's `13-sound.md`). The rest is game state
that follows time (0x020A98DC, 0x020A9B80).

The pictures: the logos, the title, the opening's 3D (the man in armour,
the girl, a hooded figure, a man in a hat with a sword) and the first
dungeon, drawn as melonDS draws them, by eye: the title at frame 2 680
against melonDS's title, the dungeon at frame 8 361 against melonDS's
picture of the player standing there (a few seconds later; nothing
moves). The opening's frames were not taken at the same frames in
melonDS: the same scenes, not compared picture for picture.

## What the runtime said along the way

* `3D: shadow polygons (not drawn)` from frame 8 360: the dungeon uses
  the DS's shadow polygons (*inferred*: the characters' shadows); ndskit's
  renderer does not draw them yet.
* Writes to VRAM that no bank maps (0x06000000-0x0607FFFF), at the start
  of a new game: the game clears engine A's background area before
  mapping its banks; ignored, as on the DS.
* Sound from frame 856: IMA-ADPCM channels, a looped one and a one-shot.

## Speed

Headless, about 1.1 ms a frame: 2 682 frames in 2.9 s, 15 times the DS
(Moon runs at about 210). Not the overlays (fewer than 500 checks of a
slot along the title's 2 682 frames); where the time goes is still to
measure (`05-open-questions.md`). In a window a frame has 16.7 ms.
