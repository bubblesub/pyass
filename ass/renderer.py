#   © 2019 Luni-4 <luni-4@hotmail.it>
#   https://github.com/bubblesub/pyass
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#   See the GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.

import ctypes

from . import enums, libass
from .utils import LibassError, encode_str, get_encoded_path


class ASS_Renderer:
    """ ASS_Renderer.
    """

    def __init__(self, ass_library):
        """Initialize the renderer.

        :param ass_library: ASS_Library handle
        """
        self._renderer = libass.ass_renderer_init(ass_library.library)
        if not self._renderer:
            raise LibassError("Cannot initialize the renderer")

    def ass_set_frame_size(self, w, h):
        """Set the frame size in pixels, including margins.

        :param w: width
        :param h: height
        """
        if w < 0 or h < 0:
            raise LibassError("Width or height cannot be less than 0")

        libass.ass_set_frame_size(self._renderer, int(w), int(h))

    def ass_set_storage_size(self, w, h):
        """Set the source image size in pixels.

        :param w: width
        :param h: height
        """
        if w < 0 or h < 0:
            raise LibassError("Width or height cannot be less than 0")

        libass.ass_set_storage_size(self._renderer, int(w), int(h))

    def ass_set_sharper(self, level):
        """Set shaping level.

        :param level: shaping level
        """
        libass.ass_set_sharper(self._renderer, int(level))

    def ass_set_margins(self, t, b, l, r):
        """Set frame margins.

        :param t: top margin
        :param b: bottom margin
        :param l: left margin
        :param r: right margin
        """
        libass.ass_set_margins(self._renderer, int(t), int(b), int(l), int(r))

    def ass_set_use_margins(self, use):
        """Whether margins should be used for placing regular events.

        :param use: whether to use the margins
        """
        libass.ass_set_use_margins(self._renderer, int(use))

    def ass_set_pixel_aspect(self, par):
        """Set pixel aspect ratio correction.

        :param par: pixel aspect ratio (1.0 means square pixels, 0 means default)
        """
        libass.ass_set_pixel_aspect(self._renderer, float(par))

    def ass_set_aspect_ratio(self, dar, sar):
        """Set aspect ratio parameters.

        :param dar: display aspect ratio (DAR), prescaled for output PAR
        :param sar: storage aspect ratio (SAR)
        """
        libass.ass_set_aspect_ratio(self._renderer, float(dar), float(sar))

    def ass_set_font_scale(self, font_scale):
        """Set a fixed font scaling factor.

        :param font_scale: scaling factor, default is 1.0
        """
        libass.ass_set_font_scale(self._renderer, float(font_scale))

    def ass_set_hinting(self, ht):
        """Set font hinting method.

        :param ht: hinting method
        """
        libass.ass_set_hinting(self._renderer, int(ht))

    def ass_set_line_spacing(self, line_spacing):
        """Set line spacing. Will not be scaled with frame size.

        :param line_spacing: line spacing in pixels
        """
        libass.ass_set_line_spacing(self._renderer, float(line_spacing))

    def ass_set_line_position(self, line_position):
        """Set vertical line position.

        :param line_position: vertical line position of subtitles in percent
        """
        libass.ass_set_line_position(self._renderer, float(line_position))

    def ass_set_fonts(self, default_font, default_family, dfp, config, update):
        """Set font lookup defaults.

        :param default_font: path to default font to use.
        :param default_family: fallback font family for fontconfig
        :param dfp: which font provider to use (one of ASS_DefaultFontProvider)
        :param config: path to fontconfig configuration file
        :param update: whether fontconfig cache should be built/updated now.
        """
        libass.ass_set_fonts(
            self._renderer,
            get_encoded_path(default_font),
            encode_str(default_family),
            int(dfp),
            get_encoded_path(config),
            int(update),
        )

    def ass_set_selective_style_override_enabled(self, bits):
        """Set selective style override mode.

        :param bits: bit mask comprised of ASS_OverrideBits values.
        """
        libass.ass_set_selective_style_override_enabled(
            self_renderer, int(bits)
        )

    def ass_set_selective_style_override(self, style):
        if not isinstance(style, libass.ASS_Style):
            raise LibassError("Pass an ASS_Style class")

        libass.ass_set_selective_style_override(
            self._renderer,
            ctypes.cast(style, ctypes.POINTER(libass.ASS_Style)),
        )

    def ass_set_cache_limits(self, glyph_max, bitmap_max_size):
        """Set hard cache limits.

        :param glyph_max: maximum number of cached glyphs.
        :param bitmap_max_size: maximum bitmap cache size (in MB)
        """
        libass.ass_set_cache_limits(
            self._renderer, int(glyph_max), int(bitmap_max_size)
        )

    def ass_render_frame(self, track, now):
        """Render a frame, producing a list of ASS_Image.

        :param track: ASS_Track
        :param now: video timestamp in milliseconds
        :return: ASS_Image object and a value that is set to 1 if positions, or
                 set to 2 if the content changed compared to the previous call
        """
        detect_change = ctypes.c_int(0)
        image = libass.ass_render_frame(
            self._renderer, track.track, int(now), ctypes.byref(detect_change),
        )

        if not image:
            raise LibassError("Cannot render the frame")

        return [image[0], detect_change.value]

    def __del__(self):
        """Finalize the renderer.
        """
        if self._renderer:
            libass.ass_renderer_done(self._renderer)
