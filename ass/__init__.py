"""Bindings for Libass
"""
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

from .enums import *
from .libass import *

__all__ = [
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
