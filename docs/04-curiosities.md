# Curiosities

* **"BoysLife"**: the project's internal name, in the effects' sound
  archive (`BoysLife_SE.sdat`), the `BL_` prefix of every message file
  and the banner file `bl.bnr`.
* **A debug shop**: the inn's and the shop's tables (`SHOP/bl_inn.bbd`,
  `SHOP/bl_shop.bbd`) both open with an entry named "Debug Shop !"; in
  the inn's, "London Inn" follows.
* **Debugging leftovers**: `MASS/mass_debuglobby.dat` (one texture pack)
  and `MASS/effect_viewer.def` (a text list of 391 effect files,
  `e001.efp.lz` ... with CRLF line ends: a tool's input).
* **The SDK's samples** shipped: `SAMPLE/2D/` holds G2D files named like
  NitroSDK's demos (`WT_test1_256`, `op_window`).
* **Empty map cells** are 4-byte files of their own: 3 251 "DMMC"
  placeholders among the 4 732 cells, each with a name and an entry in
  its archive.
* **An empty archive**: `MASS/mass_monster.dat` holds no member (512
  bytes, a count of 0).
* **A placeholder overlay**: overlay 3 is 32 bytes of zeros at the first
  slot's address.
* **Dead code**: eleven functions (0x0201C518-0x0201D6EC, 0x0201DD90)
  that only call each other, linked but never reached.
* **The Japanese banner** (and every other language's) reads "Nostalgia /
  Ignition Entertainment": the US release's banner, in all six slots.
