"""Turns the textures you exported from Ready or Not into Skyrim SE DDS files.

    python tools/make_textures.py --base T_Ram_BC.png --normal T_Ram_N.png \
        --rough T_Ram_ORM.png --rough-channel G --out textures/RoNBreachingRam

Writes ram.dds (diffuse) and ram_n.dds (normal, with specular in alpha).
The specular mask is the roughness channel inverted, so shiny metal shows up white.
Needs Pillow (pip install pillow) and Microsoft's texconv.exe on PATH
(https://github.com/microsoft/DirectXTex/releases).

Packed maps differ between games. Open yours and check which channel is roughness
(often G in an ORM map, sometimes A). Pass it with --rough-channel.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps


def pow2_size(img, cap):
    side = 1
    while side * 2 <= min(max(img.size), cap):
        side *= 2
    return (side, side)


def texconv(src, out_dir, flip_green=False):
    cmd = ["texconv", "-f", "BC7_UNORM", "-m", "0", "-y", "-o", str(out_dir)]
    if flip_green:
        cmd.append("-inverty")
    cmd.append(str(src))
    subprocess.run(cmd, check=True)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--base", required=True, help="base color / albedo PNG")
    p.add_argument("--normal", required=True, help="normal map PNG")
    p.add_argument("--rough", help="map holding roughness (a plain roughness map or a packed ORM map)")
    p.add_argument("--rough-channel", default="G", choices="RGBA", help="channel of --rough that is roughness")
    p.add_argument("--out", default="textures/RoNBreachingRam")
    p.add_argument("--name", default="ram", help="file name stem: ram -> ram.dds, ram_n.dds")
    p.add_argument("--size", type=int, default=2048, help="largest side, rounded down to a power of two")
    p.add_argument("--flip-green", action="store_true", help="flip the normal map's green channel")
    args = p.parse_args()

    if not shutil.which("texconv"):
        sys.exit("texconv not found on PATH. Get it from https://github.com/microsoft/DirectXTex/releases")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    base = Image.open(args.base).convert("RGBA")
    size = pow2_size(base, args.size)
    base = base.resize(size, Image.LANCZOS)

    normal = Image.open(args.normal).convert("RGB").resize(size, Image.LANCZOS)
    if args.rough:
        rough = Image.open(args.rough).convert("RGBA").getchannel(args.rough_channel)
        spec = ImageOps.invert(rough.resize(size, Image.LANCZOS))
    else:
        spec = Image.new("L", size, 64)  # dull default if there's no roughness map
    normal_spec = Image.merge("RGBA", (*normal.split(), spec))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        diffuse_png = tmp / f"{args.name}.png"
        normal_png = tmp / f"{args.name}_n.png"
        base.save(diffuse_png)
        normal_spec.save(normal_png)
        texconv(diffuse_png, out)
        texconv(normal_png, out, flip_green=args.flip_green)

    print(f"Wrote {out / (args.name + '.dds')} and {out / (args.name + '_n.dds')} at {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
