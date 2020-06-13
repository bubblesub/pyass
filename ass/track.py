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


from ctypes import c_char_p, cast

from . import enums, libass
from .utils import LibassError, encode_str, get_encoded_path


class ASS_Track:
    """ ASS_Track.
    """

    def __init__(self, ass_library):
        """Allocate a new empty track object.

        :param ass_library: ASS_Library handle
        """
        self.track = libass.ass_new_track(ass_library.library)
        if not self.track:
            raise LibassError("Cannot allocate a new empty track object")

    def ass_alloc_style(self):
        """Register a callback for debug/info messages.

        :return: newly allocated style id
        """
        return libass.ass_alloc_style(self.track)

    def ass_alloc_event(self):
        """Register a callback for debug/info messages.

        :return: newly allocated event id
        """
        return libass.ass_alloc_event(self.track)

    def ass_free_style(self, sid):
        """Delete a style.

        :param sid: style id
        """
        return libass.ass_free_style(self.track, int(sid))

    def ass_free_event(self, eid):
        """Delete an event.

        :param eid: event id
        """
        return libass.ass_free_event(self.track, int(eid))

    def ass_process_data(self, data):
        """Parse a chunk of subtitle stream data.

        :param data: string to parse
        """
        libass.ass_process_data(self.track, encode_str(data), len(data))

    def ass_process_codec_private(self, data):
        """Parse Codec Private section of the subtitle stream, in Matroska
           format.

        :param data: string to parse
        """
        libass.ass_process_codec_private(
            self.track, encode_str(data), len(data)
        )

    def ass_process_chunk(self, data, timecode, duration):
        """Parse a chunk of subtitle stream data.

        :param data: string to parse
        :param timecode: starting time of the event (milliseconds)
        :param duration: duration of the event (milliseconds)
        """
        libass.ass_process_chunk(
            self.track,
            encode_str(data),
            len(data),
            int(timecode),
            int(duration),
        )

    def ass_set_check_readorder(self, check_readorder):
        """Set whether the ReadOrder field when processing a packet with
           ass_process_chunk() should be used for eliminating duplicates.

        :param check_readorder: 0 means do not try to eliminate duplicates; 1 means
         use the ReadOrder field embedded in the packet as unique identifier, and
         discard the packet if there was already a packet with the same ReadOrder.
         Other values are undefined.
        """
        libass.ass_set_check_readorder(self.track, int(check_readorder))

    def ass_flush_events(self):
        """Flush buffered events.
        """
        libass.ass_flush_events(self.track)

    def ass_read_styles(self, fname, codepage):
        """Read styles from file into already initialized track.

        :param fname: file name
        :param codepage: encoding (iconv format)
        """
        if libass.ass_read_styles(
            self.track, get_encoded_path(fname), encode_str(codepage)
        ):
            raise LibassError("Can't read styles from {}".format(fname))

    def ass_step_sub(self, now, movement):
        """Calculates timeshift from now to the start of some other subtitle
           event, depending on movement parameter.

        :param now: current time in milliseconds
        :param movement: how many events to skip from the one currently displayed
        """
        return libass.ass_step_sub(self.track, int(now), int(movement))

    def __getattr__(self, name):
        track = self.track[0]

        class EmptyDict:
            pass

        return_value = {
            "name": cast(track.name, c_char_p).value,
            "styles": track.styles[0],
            "events": track.events[0],
            "style_format": cast(track.style_format, c_char_p).value,
            "event_format": cast(track.event_format, c_char_p).value,
            "Language": cast(track.Language, c_char_p).value,
        }.get(name, EmptyDict())

        if isinstance(return_value, EmptyDict):
            return getattr(track, name)

        return return_value

    def __del__(self):
        """Deallocate track and all its child objects (styles and events).
        """
        if self.track:
            libass.ass_free_track(self.track)
