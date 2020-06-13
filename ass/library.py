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
from .track import ASS_Track
from .utils import LibassError, encode_str, get_encoded_path


class ASS_Library:
    """ ASS_Library.
    """

    def __init__(self):
        """Initialize the library.
        """
        self.library = libass.ass_library_init()
        if not self.library:
            raise LibassError("Cannot initialize the library")
        self._msg_cb = None

    def ass_set_message_callback(self, msg_cb, data=None):
        """Register a callback for debug/info messages.

        :param msg_cb: callback function
        :param data: additional data, will be passed to callback
        """
        self._msg_cb = (
            libass.Callback(msg_cb)
            if msg_cb
            else ctypes.cast(msg_cb, libass.Callback)
        )
        libass.ass_set_message_cb(
            self.library, self._msg_cb, ctypes.cast(data, ctypes.c_void_p)
        )

    def ass_set_fonts_dir(self, fonts_dir):
        """Set additional fonts directory.

        :param fonts_dir: directory with additional fonts
        """
        libass.ass_set_fonts_dir(self.library, get_encoded_path(fonts_dir))

    def ass_set_extract_fonts(self, extract):
        """Whether fonts should be extracted from track data.

        :param extract: whether to extract fonts
        """
        libass.ass_set_extract_fonts(self.library, int(extract))

    def ass_set_style_overrides(self, string_list):
        """Register style overrides with a library instance.

        :param string_list: list of strings
        """
        string_list = [encode_str(s) for s in string_list]
        libass.ass_set_style_overrides(
            self.library, ctypes.cast(string_list, ctypes.c_char_p)
        )

    def ass_add_font(self, name, data):
        """Add a memory font.

        :param name: attachment name
        :param data: binary font data
        """
        libass.ass_add_font(
            self.library,
            encode_str(name),
            ctypes.cast(data, ctypes.c_char_p),
            len(data) * ctypes.sizeof(ctypes.c_char),
        )

    def ass_clear_fonts(self):
        """Remove all fonts stored in an ass_library object.
        """
        libass.ass_clear_fonts(self.library)

    def ass_get_available_font_providers(self):
        """Get the list of available font providers.

        :return: list of available font providers
        """
        font_provider_labels = {
            enums.ASS_FONTPROVIDER_NONE: "None",
            enums.ASS_FONTPROVIDER_AUTODETECT: "Autodetect",
            enums.ASS_FONTPROVIDER_CORETEXT: "CoreText",
            enums.ASS_FONTPROVIDER_FONTCONFIG: "Fontconfig",
            enums.ASS_FONTPROVIDER_DIRECTWRITE: "DirectWrite",
        }

        providers = ctypes.POINTER(libass.ASS_DefaultFontProvider)()
        providers_size = ctypes.c_int(0)
        libass.ass_get_available_font_providers(
            self.library, ctypes.byref(providers), ctypes.byref(providers_size)
        )
        providers_array = [
            font_provider_labels[providers[i]]
            for i in range(providers_size.value)
        ]
        del providers
        return providers_array

    def ass_read_file(self, fname, codepage):
        """Read subtitles from file.

        :param fname: file name
        :param codepage: encoding (iconv format)
        :return: a new ASS_Track object
        """
        track = libass.ass_read_file(
            self.library, encode_str(fname), encode_str(codepage)
        )

        if not track:
            raise LibassError("Cannot allocate a new empty track object")

        track_obj = ASS_Track(self)
        libass.ass_free_track(track_obj.track)
        track_obj.track = track
        return track_obj

    def ass_read_memory(self, buf, codepage):
        """Read subtitles from memory.

        :param buf: subtitles text data
        :param codepage: encoding (iconv format)
        :return: a new ASS_Track object
        """
        track = libass.ass_read_memory(
            self.library,
            ctypes.cast((ctypes.c_char * len(buf))(*buf), ctypes.c_char_p),
            encode_str(codepage),
        )

        if not track:
            raise LibassError("Cannot allocate a new empty track object")

        track_obj = ASS_Track(self)
        libass.ass_free_track(track_obj.track)
        track_obj.track = track
        return track_obj

    def __del__(self):
        """Finalize the library.
        """
        if self.library:
            libass.ass_library_done(self.library)
