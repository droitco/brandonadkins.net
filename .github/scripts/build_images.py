"""Rebuild the site images byte-for-byte from the original Clear Space drone photo.

Source: Brandon's own store site (clearspaceselfstoragewi.com, StorEdge upload).
Requires Pillow==12.3.0 (manylinux wheel) for byte-identical output; the
workflow checks every file against images.sha256 and fails on any mismatch.
"""
import hashlib, os, sys, urllib.request
from PIL import Image

SRC = ("https://uploads.website.storedge.com/a7266e7c-3943-4c45-84eb-fb6e877a31b3/"
       "dji_0113-1_08152022123117693_12062023110714309.jpg")
SRC_SHA256 = "6004d13c71db870dab612ba492759eb4ec659a852e910a2dec82259b54bae812"
CROPS = {
    "clear-space-hero-1600x700.jpg": ((0, 250, 3500, 1781), (1600, 700), 85),
    "clear-space-og-1200x630.jpg": ((0, 200, 3400, 1985), (1200, 630), 85),
    "clear-space-linkedin-banner-1584x396.jpg": ((0, 560, 3600, 1460), (1584, 396), 85),
    "clear-space-square-400.jpg": ((300, 250, 1600, 1550), (400, 400), 88),
}

def main(src_path, out_dir):
    if not os.path.exists(src_path):
        urllib.request.urlretrieve(SRC, src_path)
    if hashlib.sha256(open(src_path, "rb").read()).hexdigest() != SRC_SHA256:
        sys.exit("source photo hash mismatch")
    img = Image.open(src_path).convert("RGB")
    os.makedirs(out_dir, exist_ok=True)
    for name, (box, size, q) in CROPS.items():
        img.crop(box).resize(size, Image.LANCZOS).save(
            os.path.join(out_dir, name), "JPEG", quality=q, progressive=True, optimize=True)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/source.jpg",
         sys.argv[2] if len(sys.argv) > 2 else "images")
