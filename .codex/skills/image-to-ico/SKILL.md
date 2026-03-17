---
name: image-to-ico
description: Convert a source image into per-size icon assets through a deterministic Python script. Generate `.ico` files for standard icon sizes such as 16x16, 20x20, 24x24, 32x32, 48x48, and 128x128, and generate `.png` files for larger sizes such as 512x512 when standard ICO limits would be exceeded. Use when asked to turn PNG, JPG, WebP, BMP, or similar images into browser, app, favicon, or PWA icon assets programmatically instead of relying on model-based image editing.
---

# Image To Ico

## Inputs

Collect these inputs when available:

- source image path
- optional output directory
- optional size list when the default `16,20,24,32,48,128,512` should change

Default the output directory to the source image directory. Generated
files are named `<input-stem>-<size>x<size>.<ext>`.

## Workflow

Run the workflow in this order.

### 1. Confirm Python and Pillow

Check whether Pillow is available:

```bash
python3 -c 'import PIL'
```

If it is missing, install it before running the converter:

```bash
python3 -m pip install Pillow
```

### 2. Run the converter

Use the bundled script:

```bash
python3 .codex/skills/image-to-ico/scripts/image_to_ico.py <input-image>
```

To write the generated icon files into a specific directory:

```bash
python3 .codex/skills/image-to-ico/scripts/image_to_ico.py <input-image> --output-dir <dir>
```

To override the embedded icon sizes:

```bash
python3 .codex/skills/image-to-ico/scripts/image_to_ico.py <input-image> --sizes 16,20,24,32,48,128,512
```

### 3. Verify the result

Confirm that the output files exist and have the expected suffix:

```bash
ls -l <output-dir>
```

If you need a quick structural check, inspect the icon with Pillow or any
local icon viewer after generation.

## Script Behavior

`scripts/image_to_ico.py` does the following:

- reads a source image with Pillow
- fixes EXIF orientation before resizing
- preserves aspect ratio
- fits non-square images into a square canvas with transparent padding
- writes one `.ico` file per requested size up to `256x256`
- writes one `.png` file for requested sizes above `256x256`, such as `512x512`

Default sizes are `16,20,24,32,48,128,512`. Keep them unless the user explicitly
asks for a different set.

## Constraints

Follow these rules:

- use the bundled script instead of attempting manual or model-based image editing
- do not stretch the image out of aspect ratio
- prefer transparent padding over cropping unless the user explicitly asks for a crop-first result
- do not try to force sizes above `256x256` into `.ico`; use `.png` instead
- fail clearly when Pillow is unavailable or the input path is invalid

## Examples

User asks: "把这张 PNG 转成浏览器图标，带上 16、20、24、32、48、128、512 这几个尺寸。"

Run:

```bash
python3 .codex/skills/image-to-ico/scripts/image_to_ico.py ./logo.png
```

User asks: "输出到 `build/icons/`，其他逻辑保持默认。"

Run:

```bash
python3 .codex/skills/image-to-ico/scripts/image_to_ico.py ./logo.png --output-dir ./build/icons
```
