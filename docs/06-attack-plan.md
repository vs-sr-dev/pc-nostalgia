# The porting route

## Verdict: feasible, by static recompilation, as Moon

The same road as pc-moon (its `06-attack-plan.md` weighs the others):
both programs recompiled to C++ by ndskit, the DS's hardware replaced at
its registers by ndskit's runtime, melonDS as the oracle. Moon took six
sessions from nothing to playing with picture and sound; most of that
work is ndskit's now and is reused here as it is. This port is where
ndskit learns whether it is really game-agnostic.

What is the same as Moon (and so already done):

* NitroSDK 4.2, CodeWarrior's ARM code (Thumb is rare: 69 functions of
  11 609), the SDK's crt0, threads, interrupts and IPC.
* An ARM7 that is the SDK's component, 834 of its 943 functions
  byte-identical to Moon's.
* The 3D is the SDK's G3D (NSBMD, NSBTX, NSBCA, NSBTA in thin wrappers),
  the 2D the SDK's G2D, the music sequenced by the ARM7's sequencer.
* The save is an EEPROM on AUXSPI (512 Kbit instead of 64 Kbit).
* Discovery finds every function of the program that can run (all of
  Ghidra's but a dead cluster), with no conflict.

What is new, and what it asks of ndskit (each of these goes into the
kit, not into the port):

| New here | Why it matters | In ndskit |
|---|---|---|
| **14 overlays in two slots** | the same addresses hold different code; the main program calls into them directly (117 sites) | discovery: done this session (`--overlay`). The recompiler: one module per overlay, each emitted with the program's functions as known entries; a call into an overlay's region dispatched to the resident overlay's module. The runtime: which overlay each slot holds, learned where the SDK's `FS_StartOverlay` (0x0200CBF0 here) runs the initialisers (its entry's id), or recognised by a crc32 of the slot when code is first called there, as saturnkit does for programs swapped at one address. Moon never loaded one |
| **another ARM7 component** (crc32 0x3DFBBAA1) | the recompiled ARM7 module of Moon is not this one | none: recompiled as Moon's was. A `fingerprint` of the SDK's components by crc32 (layer 1) to name it |
| **IMA-ADPCM everywhere, PSG and noise** | written from GBATEK in session 6 of pc-moon, never heard | the sound unit's ADPCM, PSG and noise checked against melonDS's savestates and by ear |
| **30 frames a second** | the game paces itself to every other VBlank | nothing in the kit; a better frame rate is phase 7's |
| **display capture, fog, perhaps edge marking and toon** (the code loads their registers; overlay 0 the capture) | Moon drew none but fog | the renderer: display capture (into a VRAM bank, read back as a bitmap: at the 3D's own resolution if the port keeps the copy on the GPU), edge marking, toon/highlight, and the anti-aliasing, the clear image, shadow polygons if a room asks |
| **a 512 Kbit EEPROM** | larger than Moon's | the runtime's EEPROM by the save file's size: to check (Moon's default is 64 Kbit) |

What is not here: no compressed ARM9, no compressed overlay, no movies,
no streams, no Thumb switches met, no newer SDK's ARM7 tables, no flash
save, no nested archives.

## Where to cut

Unchanged from pc-moon's plan: everything at the hardware registers,
the BIOS's SWIs in HLE, the ARM7 recompiled and run as a coroutine, the
3D's geometry engine in software in the DS's fixed point and its
rendering on OpenGL at the window's resolution. The one new cut is the
overlays': at the recompiled code's dispatch (an address in an overlay's
region goes to the module of the overlay resident there), with the slot's
owner set when `FS_StartOverlay` runs its initialisers.

## A better Nostalgia on PC

### Resolution

The 3D (towns, dungeons, the world from the airship, battles) drawn at
the window's resolution, as Moon's; the 2D (menus, the map, the text)
at 256x192 and scaled without blurring. The display capture, if it is
what the field uses for transitions, should then capture at the 3D's
resolution too, or the transitions will drop to 256x192 for their
length.

### The frame rate

The game runs at 30. In order:

1. **A steady 30**, the DS's drops in heavy places gone.
2. **The camera and the 3D at 60** where the game's logic allows it:
   the port's geometry engine sees every matrix and vertex, so a frame
   in between can be drawn by interpolating two of the game's (one frame
   of latency), or the game's two VBlanks per frame cut to one where its
   steps follow a time step. Only after the rest works; to read in the
   frame loop first (where it waits for its two VBlanks, `05-open-questions.md`).

### The two screens

An RPG's lower screen is its map and menus. On PC: the upper screen as
the main view, the lower one beside it or under it at the player's
choice, or on demand (a key) with the mouse as the stylus over it.

### Controls

The keyboard and a gamepad as the DS's buttons; the mouse as the stylus
on the lower screen. What the game does with the touch screen (menus,
the map) is to see in play.

## The phases

| Phase | What | Done when |
|---|---|---|
| 1. Recognise (session 1) | the cartridge, the formats, the code, the oracle, this plan; ndskit split out, with overlays in discovery | this document |
| 2. Recompile | the program and each overlay as modules, the overlay dispatch; the ARM7 recompiled; the self-test with vectors of this game's functions | everything compiles and links; the self-test has no difference |
| 3. Runtime | the machine boots Nostalgia headless: the overlays loaded and dispatched, the save (512 Kbit EEPROM), the route from boot to the first dungeon by a script of presses | its memories at the title and in the dungeon against melonDS's states at the same VBlank count |
| 4. Picture | the title, the opening and the dungeon drawn; display capture, fog, edge marking and toon as the game uses them | the pictures against melonDS's at the same frames; the user's eyes |
| 5. Sound | ADPCM, PSG and noise against melonDS | the channels' registers equal at the same frames; the user's ears |
| 6. Publication | ndskit proven on two games: the three repositories created and pushed together (by the user) | Nostalgia works "until proven otherwise" |
| 7. PC | the screens' layout, the frame rate, the controls, the resolution of the capture | played by the user |

## Oracle

melonDS (`D:\Tools\melonDS-oracle`), driven by `tools/oracle.py` (pc-moon's,
with `down:`/`up:` to hold a button across savestates). The route from a
new cartridge into the first controllable moment:

    python tools/oracle.py --fresh --at 40:START,41:START,46:A,140:state

START twice at the title (the first press may come before it takes
input), A on "New Game"; the opening plays by itself, with no press,
into the Tower of Babel, 5F, where the player moves (UP walks up the
stairs' landing) between 120 and 130 seconds. States kept in
`build/oracle/`: `title.ml1` (the menu, VBlank 2 680), `opening.ml1`
(5 499), `dungeon.ml1` and `dungeon2.ml1` (8 361 and 8 481, standing).
