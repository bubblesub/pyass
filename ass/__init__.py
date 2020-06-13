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
from collections import namedtuple

import numpy

from .enums import *
from .libass import ASS_Event, ASS_Image, ASS_Style, ass_library_version
from .library import ASS_Library
from .renderer import ASS_Renderer
from .track import ASS_Track

__all__ = [
    "get_version_info",
    "get_version",
    "ASS_Library",
    "ASS_Renderer",
    "ASS_Track",
    "ASS_HINTING_NONE",
    "ASS_HINTING_LIGHT",
    "ASS_HINTING_NORMAL",
    "ASS_HINTING_NATIVE",
    "ASS_SHAPING_SIMPLE",
    "ASS_SHAPING_COMPLEX",
    "ASS_OVERRIDE_DEFAULT",
    "ASS_OVERRIDE_BIT_STYLE",
    "ASS_OVERRIDE_BIT_SELECTIVE_FONT_SCALE",
    "ASS_OVERRIDE_BIT_FONT_SIZE",
    "ASS_OVERRIDE_BIT_FONT_SIZE_FIELDS",
    "ASS_OVERRIDE_BIT_FONT_NAME",
    "ASS_OVERRIDE_BIT_COLORS",
    "ASS_OVERRIDE_BIT_ATTRIBUTES",
    "ASS_OVERRIDE_BIT_BORDER",
    "ASS_OVERRIDE_BIT_ALIGNMENT",
    "ASS_OVERRIDE_BIT_MARGINS",
    "ASS_OVERRIDE_FULL_STYLE",
    "ASS_OVERRIDE_BIT_JUSTIFY",
    "ASS_FONTPROVIDER_NONE",
    "ASS_FONTPROVIDER_AUTODETECT",
    "ASS_FONTPROVIDER_CORETEXT",
    "ASS_FONTPROVIDER_FONTCONFIG",
    "ASS_FONTPROVIDER_DIRECTWRITE",
    "YCBCR_DEFAULT",
    "YCBCR_UNKNOWN",
    "YCBCR_NONE",
    "YCBCR_BT601_TV",
    "YCBCR_BT601_PC",
    "YCBCR_BT709_TV",
    "YCBCR_BT709_PC",
    "YCBCR_SMPTE240M_TV",
    "YCBCR_SMPTE240M_PC",
    "YCBCR_FCC_TV",
    "YCBCR_FCC_PC",
]


def get_version_info():
    """Return the LIBASS_VERSION as a tuple.
    """

    def hex_prefix(n):
        return int(hex(n)[2:])

    VersionInfo = namedtuple("VersionInfo", ("major", "minor", "micro"))
    n = ass_library_version()
    major, r = divmod(n, 1 << 28)
    minor, r = divmod(r, 1 << 20)
    micro, bump = divmod(r, 1 << 12)
    return VersionInfo(hex_prefix(major), hex_prefix(minor), hex_prefix(micro))


def get_version():
    """Return the LIBASS_VERSION as a string.
    """
    version_info = get_version_info()
    return ".".join(str(e) for e in version_info)


def _get_name(struct):
    return ctypes.cast(struct.Name, ctypes.c_char_p).value


ASS_Style.name = property(_get_name)


def _get_effect(struct):
    return ctypes.cast(struct.Effect, ctypes.c_char_p).value


def _get_text(struct):
    return ctypes.cast(struct.Text, ctypes.c_char_p).value


ASS_Event.name = property(_get_name)
ASS_Event.effect = property(_get_effect)
ASS_Event.text = property(_get_text)


def _get_image(ass_image):
    return numpy.ctypeslib.as_array(
        ass_image.bitmap, shape=(ass_image.stride * ass_image.h,)
    )


def _get_next_image(ass_image):
    next_img = ass_image.next
    return None if not next_img else next_img[0]


ASS_Image.image = property(_get_image)
ASS_Image.next_image = property(_get_next_image)
