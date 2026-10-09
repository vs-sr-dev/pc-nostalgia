# Open questions

* **The frame loop**: where it waits for its two VBlanks (30 fps is
  measured, not read); whether a heavier place drops below 30; whether
  the game's steps follow a fixed time step (what 60 would take).
* **Which overlay is which**: overlay 1 is resident at the title,
  overlay 0 from the opening into the first dungeon; overlay 2 and
  overlays 4-13 (the second slot) are still to meet: battles, the
  airship, the world map, menus, shops? `melonds --overlays` at each.
* **The main program's 117 direct calls into the overlays' regions**:
  for each, which overlays have a function at that address (a call meant
  for one overlay must not be dispatched into another's code).
* **The ARM7's 109 different functions**: what changed against Moon's
  component (the sound driver, the wireless, the backup).
* **The 3D features**: does the field use display capture (for what),
  edge marking, toon shading, anti-aliasing, the clear image? Their
  registers' addresses are in the code; DISP3DCNT's value in melonDS's
  state at each place would answer.
* **The touch screen**: what it does in play (the map? menus?).
* **The formats inside the wrappers**: `.mmc` map cells, `.mgpf`,
  `.nsdp`, `.ntpk`, `.bad`, `.hich`, `.mai`, `.pak` (only needed if the
  port ever replaces assets; the recompiled game reads them itself).
* **The dead cluster** at 0x0201C518-0x0201D6EC: what library it came
  from (it is never called).
