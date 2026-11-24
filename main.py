#!/usr/bin/env python3
"""news-23 b182 heroes-scene: entrypoint. Stdlib only (no PIL).

Verifies entry.png next to this file, then writes a byte-identical copy to
$MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png). Never writes
next to this file and never writes inside the repo.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SIZE = 146704  # filled after first run; see revision note below
EXPECTED_SHA256 = "fe013b4474745f5cc4e067f4ee20195938d0487ffe911e1fe49b71f244767657"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main(argv):
    here = os.path.dirname(os.path.realpath(__file__))
    src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return fail("cannot read entry.png: %s" % exc)
    if len(data) < 10000:
        return fail("entry.png too small (%d bytes)" % len(data))
    if len(data) > 1024 * 1024:
        return fail("entry.png over 1 MiB (%d bytes)" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG (bad signature)")
    # Parse the PNG header manually: first chunk must be a 13-byte IHDR
    # declaring 1024x1024, 8-bit, colour type 2 or 6, no compression/filter/
    # interlace tricks. Then walk every chunk, checking CRCs, requiring a
    # non-empty IDAT payload and a final empty IEND with no trailing bytes.
    if len(data) < 33:
        return fail("entry.png truncated before IHDR")
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        return fail("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != struct.unpack(">I", data[29:33])[0]:
        return fail("IHDR CRC mismatch")
    width, height, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (width, height) != (1024, 1024):
        return fail("expected 1024x1024, got %dx%d" % (width, height))
    if depth != 8 or ctype not in (2, 6):
        return fail("expected 8-bit RGB/RGBA, got depth %d type %d" % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        return fail("unexpected compression/filter/interlace flags")
    pos = 33
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return fail("truncated chunk header")
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype_b = data[pos + 4:pos + 8]
        end = pos + 8 + clen + 4
        if end > len(data):
            return fail("truncated chunk %r" % ctype_b)
        if zlib.crc32(ctype_b + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF != \
                struct.unpack(">I", data[pos + 8 + clen:end])[0]:
            return fail("CRC mismatch in chunk %r" % ctype_b)
        if ctype_b == b"IDAT":
            if clen == 0:
                return fail("empty IDAT chunk")
            idat_total += clen
        if ctype_b == b"IEND":
            if clen != 0:
                return fail("IEND must be empty")
            if end != len(data):
                return fail("trailing data after IEND")
            saw_iend = True
            break
        pos = end
    if not saw_iend:
        return fail("no IEND chunk")
    if idat_total < 1000:
        return fail("IDAT payload too small (%d bytes)" % idat_total)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_real = os.path.realpath(outdir)
    here_real = os.path.realpath(here)
    if outdir_real == here_real or outdir_real.startswith(here_real + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.isfile(outdir_real):
        return fail("MAKEFUN_OUTPUT_DIR is a file")
    out = os.path.join(outdir, "entry.png")
    if os.path.realpath(out) == os.path.realpath(src):
        return fail("refusing to overwrite the source image")
    os.makedirs(outdir, exist_ok=True)
    with open(out, "wb") as fh:
        fh.write(data)
    with open(out, "rb") as fh:
        written = fh.read()
    if written != data:
        return fail("written output differs from source")
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and digest != EXPECTED_SHA256:
        return fail("sha256 mismatch: got %s" % digest)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        return fail("size mismatch: got %d" % len(data))
    print("ok: wrote %s (%d bytes, sha256 %s)" % (out, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
