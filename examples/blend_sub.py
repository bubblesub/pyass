"""Blend a subtitle onto a png image
"""

import argparse
import os
import sys

import numpy as np
from PIL import Image

import ass

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FRAME_STRIDE = FRAME_WIDTH * 3


def ic(level, fmt, *args, data=None):
    if level > 6:
        return

    print(fmt, *args)


def print_font_providers(ass_library):
    font_providers = ass_library.ass_get_available_font_providers()
    print("Available font providers:\n")
    for (i, provider) in enumerate(font_providers):
        print("{}. {}".format(i + 1, provider))
    print()


def blend_single(img, frame):
    opacity = 255 - (img.color & 0xFF)
    r = img.color >> 24
    g = (img.color >> 16) & 0xFF
    b = (img.color >> 8) & 0xFF

    dst = frame[img.dst_y * FRAME_STRIDE + img.dst_x * 3 :]
    for y in range(0, img.h):
        src_step = y * img.stride
        frame_step = y * FRAME_STRIDE
        for x in range(0, img.w):
            k = int(img.image[src_step + x]) * opacity / 255
            frame_row_step = frame_step + x * 3
            dst[frame_row_step] = (
                k * b + (255 - k) * dst[frame_row_step]
            ) / 255
            dst[frame_row_step + 1] = (
                k * g + (255 - k) * dst[frame_row_step + 1]
            ) / 255
            dst[frame_row_step + 2] = (
                k * r + (255 - k) * dst[frame_row_step + 2]
            ) / 255


def blend(img, frame):
    count_blended = 0
    while img is not None:
        blend_single(img, frame)
        count_blended += 1
        img = img.next_image

    print("{} images blended".format(count_blended))


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__.strip(),
        prog="{} -m {}".format(os.path.basename(sys.executable), "blend"),
    )
    parser.add_argument(
        "image_file", type=str, help="Filename of the output blended image",
    )
    parser.add_argument(
        "subtitle_file",
        type=str,
        help="Subtitle file containing the desidered subtitles",
    )
    parser.add_argument(
        "subtitle_time",
        type=float,
        default=0.0,
        help="Time in seconds of the desidered subtitle",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    ass_library = ass.ASS_Library()
    ass_renderer = ass.ASS_Renderer(ass_library)

    # Set callback
    ass_library.ass_set_message_callback(ic)

    # Print font providers
    print_font_providers(ass_library)

    # Set render configurations
    ass_renderer.ass_set_frame_size(FRAME_WIDTH, FRAME_HEIGHT)
    ass_renderer.ass_set_fonts(
        None, "sans-serif", ass.ASS_FONTPROVIDER_AUTODETECT, None, 1
    )

    # Get track
    track = ass_library.ass_read_file(args.subtitle_file, None)

    # Get subtitles as images
    ass_image, _ = ass_renderer.ass_render_frame(
        track, args.subtitle_time * 1000
    )

    # Generate a new frame
    frame = np.full((FRAME_HEIGHT * FRAME_STRIDE,), 63, dtype=np.uint8)

    # Blend image
    blend(ass_image, frame)

    # Save image as png
    im = Image.fromarray(
        frame[::3].reshape(FRAME_HEIGHT, FRAME_WIDTH), mode="P"
    )
    im.save(args.image_file)


if __name__ == "__main__":
    sys.exit(main())
