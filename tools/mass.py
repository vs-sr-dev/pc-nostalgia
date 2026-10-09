"""Nostalgia's MASS archives ("SSAM" files): list, check, extract.

Layout, read from the cartridge's files (docs/02-data-formats.md):

    0x00  "SSAM"
    0x04  u32 count
    0x08  count entries of 0x28 bytes:
              u32 offset   from the end of the entry table
              u32 size
              char name[32], NUL-padded
    then the members' data

Members named *.lz are in the BIOS's LZ77 (type 0x10).

    python tools/mass.py FILE.dat [--list] [--extract DIR [--lz]]
    python tools/mass.py --scan DIR        # every SSAM file under DIR, a summary
"""
import argparse
import collections
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from ndskit import lz  # noqa: E402


def parse(data):
    if data[:4] != b"SSAM":
        raise ValueError("not an SSAM archive")
    count, = struct.unpack_from("<I", data, 4)
    base = 8 + count * 0x28
    out = []
    for i in range(count):
        off, size = struct.unpack_from("<2I", data, 8 + i * 0x28)
        name = data[16 + i * 0x28:48 + i * 0x28].split(b"\0")[0].decode("ascii")
        if base + off + size > len(data):
            raise ValueError("entry %d (%s) past the end" % (i, name))
        out.append((name, base + off, size))
    return out


def magic(blob, name):
    if name.endswith(".lz"):
        try:
            blob = lz.decompress(blob)
        except ValueError:
            pass                    # stored plain despite its name (4-byte "DMMC" placeholders)
    m = blob[:4]
    return m.decode("latin-1") if all(32 <= c < 127 for c in m) else m.hex()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--extract")
    ap.add_argument("--lz", action="store_true", help="decompress .lz members on extraction")
    ap.add_argument("--scan")
    a = ap.parse_args()

    if a.scan:
        exts = collections.Counter()
        magics = collections.defaultdict(collections.Counter)
        for root, _, files in os.walk(a.scan):
            for f in sorted(files):
                p = os.path.join(root, f)
                data = open(p, "rb").read()
                if data[:4] != b"SSAM":
                    continue
                ents = parse(data)
                end = max((o + s for _, o, s in ents), default=8)
                kinds = collections.Counter(n.split(".", 1)[1] if "." in n else "-" for n, _, _ in ents)
                exts.update(kinds)
                print("%-40s %5d members  tail %5d  %s" % (os.path.relpath(p, a.scan), len(ents), len(data) - end,
                      " ".join("%s:%d" % kv for kv in kinds.most_common(6))))
                for n, o, s in ents:
                    k = n.split(".", 1)[1].lower() if "." in n else "-"
                    k = k[:-3] if k.endswith(".lz") else k
                    if len(magics[k]) < 4 or sum(magics[k].values()) < 8:
                        magics[k][magic(data[o:o + s], n)] += 1
        print("all:", " ".join("%s:%d" % kv for kv in exts.most_common()))
        print("magics (a sample of each kind, after LZ):")
        for k, c in sorted(magics.items()):
            print("  %-8s %s" % (k, " ".join("%s:%d" % kv for kv in c.most_common())))
        return

    data = open(a.file, "rb").read()
    ents = parse(data)
    if a.list or not a.extract:
        for i, (n, o, s) in enumerate(ents):
            print("%4d  %08X %9d  %-32s %s" % (i, o, s, n, magic(data[o:o + s], n)))
    if a.extract:
        os.makedirs(a.extract, exist_ok=True)
        for n, o, s in ents:
            blob = data[o:o + s]
            if a.lz and n.endswith(".lz"):
                blob, n = lz.decompress(blob), n[:-3]
            open(os.path.join(a.extract, n), "wb").write(blob)


if __name__ == "__main__":
    main()
