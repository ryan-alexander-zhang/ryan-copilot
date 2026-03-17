#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import struct
import sys
from pathlib import Path

DEFAULT_SIZES = (16, 20, 24, 32, 48, 128, 512)
MAX_STANDARD_ICO_SIZE = 256


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an image into one ICO file per requested size."
    )
    parser.add_argument("input_image", help="Path to the source image.")
    parser.add_argument(
        "--output-dir",
        help="Directory for generated .ico files. Defaults to the input image directory.",
    )
    parser.add_argument(
        "--sizes",
        default=",".join(str(size) for size in DEFAULT_SIZES),
        help="Comma-separated icon sizes. Default: 16,20,24,32,48,128,512.",
    )
    return parser.parse_args()


def load_pillow():
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:  # pragma: no cover - exercised in real environments
        raise SystemExit(
            "Pillow is required. Install it with `python3 -m pip install Pillow`."
        ) from exc
    return Image, ImageOps


def parse_sizes(raw_sizes: str) -> list[int]:
    sizes: list[int] = []
    for chunk in raw_sizes.split(","):
        value = chunk.strip()
        if not value:
            continue
        try:
            size = int(value)
        except ValueError as exc:
            raise SystemExit(f"Invalid size value: {value!r}") from exc
        if size <= 0 or size > 4096:
            raise SystemExit(f"Icon sizes must be between 1 and 4096: {size}")
        sizes.append(size)
    unique_sizes = sorted(set(sizes))
    if not unique_sizes:
        raise SystemExit("At least one icon size is required.")
    return unique_sizes


def resampling_filter(image_module):
    resampling = getattr(image_module, "Resampling", None)
    if resampling is not None:
        return resampling.LANCZOS
    return image_module.LANCZOS


def render_square_frame(source_image, size: int, image_module, image_ops_module):
    fitted = image_ops_module.contain(
        source_image,
        (size, size),
        method=resampling_filter(image_module),
    )
    canvas = image_module.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - fitted.width) // 2, (size - fitted.height) // 2)
    canvas.alpha_composite(fitted, offset)
    return canvas


def encode_png(frame) -> bytes:
    buffer = io.BytesIO()
    frame.save(buffer, format="PNG")
    return buffer.getvalue()


def write_ico(frames: list[tuple[int, bytes]], output_path: Path) -> None:
    header = struct.pack("<HHH", 0, 1, len(frames))
    offset = 6 + (16 * len(frames))
    entries: list[bytes] = []
    payloads: list[bytes] = []

    for size, image_data in frames:
        icon_dim = 0 if size >= 256 else size
        entries.append(
            struct.pack(
                "<BBBBHHII",
                icon_dim,
                icon_dim,
                0,
                0,
                1,
                32,
                len(image_data),
                offset,
            )
        )
        payloads.append(image_data)
        offset += len(image_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as file_obj:
        file_obj.write(header)
        for entry in entries:
            file_obj.write(entry)
        for payload in payloads:
            file_obj.write(payload)


def write_png(frame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.save(output_path, format="PNG")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input_image).expanduser().resolve()
    if not input_path.is_file():
        raise SystemExit(f"Input image does not exist: {input_path}")

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else input_path.parent
    )
    sizes = parse_sizes(args.sizes)
    image_module, image_ops_module = load_pillow()
    output_dir.mkdir(parents=True, exist_ok=True)

    with image_module.open(input_path) as source:
        normalized = image_ops_module.exif_transpose(source).convert("RGBA")
        output_paths: list[Path] = []
        for size in sizes:
            frame = render_square_frame(
                normalized,
                size,
                image_module,
                image_ops_module,
            )
            if size <= MAX_STANDARD_ICO_SIZE:
                output_path = output_dir / f"{input_path.stem}-{size}x{size}.ico"
                write_ico([(size, encode_png(frame))], output_path)
            else:
                output_path = output_dir / f"{input_path.stem}-{size}x{size}.png"
                write_png(frame, output_path)
            output_paths.append(output_path)

    print("Wrote:")
    for output_path in output_paths:
        print(f"- {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
