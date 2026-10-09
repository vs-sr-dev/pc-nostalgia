# The recompiler: the program, its overlays, the ARM7

ndskit's recompiler (pc-moon's `docs/09-recompiler.md` for what it does
with one program) learnt overlays this session. Built and checked here:

```sh
ROM="rom/Nostalgia (USA).nds"
export PATH=/c/msys64/mingw64/bin:$PATH
python -m ndskit.recomp "$ROM" --out build/recomp --optest          # about 3 minutes: 14 discoveries
cmake -S build/recomp -B build/recomp/b -G Ninja -DCMAKE_CXX_COMPILER=clang++
ninja -C build/recomp/b                                             # about a minute
```

## Modules

One module for the ARM9's program, one per overlay that has code (13:
overlay 3 is 32 zero bytes), one for the ARM7:

| Module | Functions | Instructions | Calls through registers left to run time | Static targets that are not its entries |
|---|---|---|---|---|
| ARM9 | 5 270 | 140 704 | 1 216 | 73 (its direct calls into the overlays' areas) |
| ARM9_OV0 (the field) | 1 824 | 56 315 | 1 256 | 1 |
| ARM9_OV1 (the title) | 2 259 | 67 213 | 733 | 6 |
| ARM9_OV2 | 1 118 | 73 054 | 210 | 10 |
| ARM9_OV4 ... OV13 | 232, 402, 110, 152, 251, 33, 80, 36, 38, 38 | 71 325 in all | | 14 to 163 each: calls into the first slot's overlays |
| ARM7 | 944 | 37 609 | 39 | 0 |

42 MB of C++ in 84 files (with ndskit's instruction test), compiled by
clang 22 without a warning.

How (`python -m ndskit.recomp`, `ndskit/recomp/__main__.py`):

* Each overlay is discovered with the program, loaded at its address
  (as `discover --overlay`). The program's module is discovered with
  every function of its own that one of these runs found (those only
  overlays call included: 5 270 against 4 907 for the program alone).
* An overlay's module emits only the functions inside the overlay and
  calls the program's directly, by their C++ names
  (`p_arm9::f_0201C1CC(c)`). A call or a jump to an address outside its
  module goes through the runtime's dispatch: the program's calls into
  the overlays' areas, and the second slot's overlays calling into the
  first slot's (overlay 0's, the field's; 14 to 163 targets each).
* An overlay's module carries what the runtime needs to know it is
  resident: the address ranges of its code (each function from its first
  to its last instruction, merged across literal pools; 10 to 16 ranges
  for the large ones, 93% of the overlay), their crc32, each entry's
  first instruction, and 64 sampled words. The overlay's data lies
  outside the ranges: in melonDS's states the bytes that changed after
  loading (133 in overlay 0, 1 339 in overlay 1) are all outside them.

The main program's direct calls into the overlays' areas, by target:
almost every target is a function of one overlay only; a few are
functions of two (0x020FDE70 of overlays 1 and 2, 0x02110D6C of 4 and 7,
0x02112B04 of 5 and 10), and 0x0210DB40, the second slot's first byte, is a
function in all ten of its overlays (the same entry of whichever is
loaded). The dispatch by the resident overlay is what makes these
right.

## Discovery, three more forms

Running the game met three functions discovery had missed, all tiny C++
methods reached only through data (each fixed in ndskit, `10-ndskit.md`):

* 0x0205F1D0, `bx lr`: an empty handler in a table of pointers to member
  functions, `{function, this adjustment}` pairs, 8 bytes apart: its
  table neighbour is two words away (called after "New Game").
* 0x020BF09C, `ldr r0, =0x403; bx lr` (a type's id), in overlay 0: in
  records of three words; the word before it is the literal pool of the
  method before, itself unknown.
* 0x020CAC80 and 0x020CAC8C: two such methods whose only neighbours are
  each other.

Then a rule for a method that exactly fills the gap between two known
functions. With them: Nostalgia's program 4 907 functions alone (was
4 899), overlay 0 1 824 (was 1 714); Moon's ARM9 6 613 (was 6 580), all
getters, setters and empty callbacks; 0 conflicts on the four
cartridges.

## The self-test

| Vectors | Functions | Vectors | Failures |
|---|---|---|---|
| ndskit's instruction test, ARM9 and ARM7 | 7 292 | 57 749 | 0 |
| the ARM9 program's functions that run alone (`selftest --auto`) | 2 017 | 31 735 | 0 |
| the ARM7's | 172 | 2 737 | 0 |
| overlay 0's (`selftest --overlay 0 --auto`), through the dispatch | 559 | 8 773 | 0 |
| **total** | **10 040** | **100 994** | **0** |

Overlay 0's vectors are replayed with the program's module active and
the overlay loaded: every call into the overlay goes through the
runtime's choice of the resident overlay, as in the game.

```sh
python -m ndskit.recomp.selftest "$ROM" --cpu 9 --auto --out build/vectors/arm9.txt
python -m ndskit.recomp.selftest "$ROM" --cpu 7 --auto --out build/vectors/arm7.txt
python -m ndskit.recomp.selftest "$ROM" --cpu 9 --overlay 0 --auto --out build/vectors/ov0.txt
build/recomp/b/selftest build/recomp/selftest/optest9.txt build/recomp/selftest/optest7.txt \
    build/vectors/arm9.txt build/vectors/arm7.txt build/vectors/ov0.txt
```
