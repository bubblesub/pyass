# pip install clang ctypeslib2
# clang2py -o libass.py -c -d -l libass.so ass.h

import ctypes
import os

from .get_library import get_library

lib = get_library(
    "ass",
    win_format="lib{}.dll",
    win64_format=["lib{}.dll"],
    win_class_name="WinDLL",
)

LIBASS_VERSION = 0x01400000
FUNCTYPE = ctypes.WINFUNCTYPE if os.name == "nt" else ctypes.CFUNCTYPE


""" Enum Definitions """

ASS_Hinting = ctypes.c_int  # enum

ASS_ShapingLevel = ctypes.c_int  # enum

ASS_OverrideBits = ctypes.c_int  # enum

ASS_DefaultFontProvider = ctypes.c_int  # enum

ASS_YCbCrMatrix = ctypes.c_int  # enum


""" Opaque objects """


class ASS_Renderer(ctypes.Structure):
    pass


class ASS_RenderPriv(ctypes.Structure):
    pass


class ASS_ParserPriv(ctypes.Structure):
    pass


class ASS_Library(ctypes.Structure):
    pass


""" Public Structs """


class ASS_Style(ctypes.Structure):
    pass


ASS_Style._fields_ = [
    ("Name", ctypes.c_char_p),
    ("FontName", ctypes.c_char_p),
    ("FontSize", ctypes.c_double),
    ("PrimaryColour", ctypes.c_uint32),
    ("SecondaryColour", ctypes.c_uint32),
    ("OutlineColour", ctypes.c_uint32),
    ("BackColour", ctypes.c_uint32),
    ("Bold", ctypes.c_int32),
    ("Italic", ctypes.c_int32),
    ("Underline", ctypes.c_int32),
    ("StrikeOut", ctypes.c_int32),
    ("ScaleX", ctypes.c_double),
    ("ScaleY", ctypes.c_double),
    ("Spacing", ctypes.c_double),
    ("Angle", ctypes.c_double),
    ("BorderStyle", ctypes.c_int32),
    ("Outline", ctypes.c_double),
    ("Shadow", ctypes.c_double),
    ("Alignment", ctypes.c_int32),
    ("MarginL", ctypes.c_int32),
    ("MarginR", ctypes.c_int32),
    ("MarginV", ctypes.c_int32),
    ("Encoding", ctypes.c_int32),
    ("treat_fontname_as_pattern", ctypes.c_int32),
    ("Blur", ctypes.c_double),
    ("Justify", ctypes.c_int32),
]


class ASS_Event(ctypes.Structure):
    pass


ASS_Event._fields_ = [
    ("Start", ctypes.c_int64),
    ("Duration", ctypes.c_int64),
    ("ReadOrder", ctypes.c_int32),
    ("Layer", ctypes.c_int32),
    ("Style", ctypes.c_int32),
    ("Name", ctypes.c_char_p),
    ("MarginL", ctypes.c_int32),
    ("MarginR", ctypes.c_int32),
    ("MarginV", ctypes.c_int32),
    ("Effect", ctypes.c_char_p),
    ("Text", ctypes.c_char_p),
    ("render_priv", ctypes.POINTER(ASS_RenderPriv)),
]


class ASS_Track(ctypes.Structure):
    pass


ASS_Track._fields_ = [
    ("n_styles", ctypes.c_int32),
    ("max_styles", ctypes.c_int32),
    ("n_events", ctypes.c_int32),
    ("max_events", ctypes.c_int32),
    ("styles", ctypes.POINTER(ASS_Style)),
    ("events", ctypes.POINTER(ASS_Event)),
    ("style_format", ctypes.c_char_p),
    ("event_format", ctypes.c_char_p),
    ("track_type", ctypes.c_int),
    ("PlayResX", ctypes.c_int32),
    ("PlayResY", ctypes.c_int32),
    ("Timer", ctypes.c_double),
    ("WrapStyle", ctypes.c_int32),
    ("ScaledBorderAndShadow", ctypes.c_int32),
    ("Kerning", ctypes.c_int32),
    ("Language", ctypes.c_char_p),
    ("YCbCrMatrix", ctypes.c_int),
    ("default_style", ctypes.c_int32),
    ("name", ctypes.c_char_p),
    ("library", ctypes.POINTER(ASS_Library)),
    ("parser_priv", ctypes.POINTER(ASS_ParserPriv)),
]


class ASS_Image(ctypes.Structure):
    pass


ASS_Image._fields_ = [
    ("w", ctypes.c_int32),
    ("h", ctypes.c_int32),
    ("stride", ctypes.c_int32),
    ("bitmap", ctypes.POINTER(ctypes.c_uint8)),
    ("color", ctypes.c_uint32),
    ("dst_x", ctypes.c_int32),
    ("dst_y", ctypes.c_int32),
    ("next", ctypes.POINTER(ASS_Image)),
    ("type", ctypes.c_int),
]

""" API """

Callback = FUNCTYPE(
    ctypes.c_void_p,
    ctypes.c_int32,
    ctypes.c_char_p,
    ctypes.c_int32,
    ctypes.c_void_p,
)

# Return the version of library. This returns the value LIBASS_VERSION was set
# to when the library was compiled.
ass_library_version = lib.ass_library_version
ass_library_version.restype = ctypes.c_int32
ass_library_version.argtypes = []

# Initialize the library.
ass_library_init = lib.ass_library_init
ass_library_init.restype = ctypes.POINTER(ASS_Library)
ass_library_init.argtypes = []

# Finalize the library
ass_library_done = lib.ass_library_done
ass_library_done.restype = None
ass_library_done.argtypes = [ctypes.POINTER(ASS_Library)]

# Set additional fonts directory. Optional directory that will be scanned for
# fonts recursively. The fonts found are used for font lookup. NOTE: A valid
# font directory is not needed to support embedded fonts.
ass_set_fonts_dir = lib.ass_set_fonts_dir
ass_set_fonts_dir.restype = None
ass_set_fonts_dir.argtypes = [
    ctypes.POINTER(ASS_Library),
    ctypes.c_char_p,
]

# Whether fonts should be extracted from track data.
ass_set_extract_fonts = lib.ass_set_extract_fonts
ass_set_extract_fonts.restype = None
ass_set_extract_fonts.argtypes = [ctypes.POINTER(ASS_Library), ctypes.c_int32]

# Register style overrides with a library instance. The overrides should have
# the form [Style.]Param=Value, e.g. SomeStyle.Font=Arial
# ScaledBorderAndShadow=yes
ass_set_style_overrides = lib.ass_set_style_overrides
ass_set_style_overrides.restype = None
ass_set_style_overrides.argtypes = [
    ctypes.POINTER(ASS_Library),
    ctypes.POINTER(ctypes.c_char_p),
]

# Explicitly process style overrides for a track.
ass_process_force_style = lib.ass_process_force_style
ass_process_force_style.restype = None
ass_process_force_style.argtypes = [ctypes.POINTER(ASS_Track)]

# Register a callback for debug/info messages. If a callback is registered, it
# is called for every message emitted by libass. The callback receives a format
# string and a list of arguments, to be used for the printf family of functions.
# Additionally, a log level from 0 (FATAL errors) to 7 (verbose DEBUG) is
# passed. Usually, level 5 should be used by applications. If no callback is
# set, all messages level < 5 are printed to stderr, prefixed with [ass].
ass_set_message_cb = lib.ass_set_message_cb
ass_set_message_cb.restype = None
ass_set_message_cb.argtypes = [
    ctypes.POINTER(ASS_Library),
    Callback,
    ctypes.c_void_p,
]

# Initialize the renderer.
ass_renderer_init = lib.ass_renderer_init
ass_renderer_init.restype = ctypes.POINTER(ASS_Renderer)
ass_renderer_init.argtypes = [ctypes.POINTER(ASS_Library)]

# Finalize the renderer.
ass_renderer_done = lib.ass_renderer_done
ass_renderer_done.restype = None
ass_renderer_done.argtypes = [ctypes.POINTER(ASS_Renderer)]

# Set the frame size in pixels, including margins. The renderer will never
# return images that are outside of the frame area. The value set with this
# function can influence the pixel aspect ratio used for rendering. If the frame
# size doesn't equal to the video size, you may have to use
# ass_set_pixel_aspect().
ass_set_frame_size = lib.ass_set_frame_size
ass_set_frame_size.restype = None
ass_set_frame_size.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_int32,
    ctypes.c_int32,
]

# Set the source image size in pixels. This is used to calculate the source
# aspect ratio and the blur scale. The source image size can be reset to default
# by setting w and h to 0. The value set with this function can influence the
# pixel aspect ratio used for rendering.
ass_set_storage_size = lib.ass_set_storage_size
ass_set_storage_size.restype = None
ass_set_storage_size.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_int32,
    ctypes.c_int32,
]

# Set shaping level. This is merely a hint, the renderer will use whatever is
# available if the request cannot be fulfilled.
ass_set_shaper = lib.ass_set_shaper
ass_set_shaper.restype = None
ass_set_shaper.argtypes = [ctypes.POINTER(ASS_Renderer), ctypes.c_int]

# Set frame margins. These values may be negative if pan-and-scan is used. The
# margins are in pixels. Each value specifies the distance from the video
# rectangle to the renderer frame. If a given margin value is positive, there
# will be free space between renderer frame and video area. If a given margin
# value is negative, the frame is inside the video, i.e. the video has been
# cropped.
ass_set_margins = lib.ass_set_margins
ass_set_margins.restype = None
ass_set_margins.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_int32,
    ctypes.c_int32,
]

# Whether margins should be used for placing regular events.
ass_set_use_margins = lib.ass_set_use_margins
ass_set_use_margins.restype = None
ass_set_use_margins.argtypes = [ctypes.POINTER(ASS_Renderer), ctypes.c_int32]

# Set pixel aspect ratio correction. This is the ratio of pixel width to pixel
# height.
ass_set_pixel_aspect = lib.ass_set_pixel_aspect
ass_set_pixel_aspect.restype = None
ass_set_pixel_aspect.argtypes = [ctypes.POINTER(ASS_Renderer), ctypes.c_double]

# Set aspect ratio parameters. This calls ass_set_pixel_aspect(priv, dar / sar).
ass_set_aspect_ratio = lib.ass_set_aspect_ratio
ass_set_aspect_ratio.restype = None
ass_set_aspect_ratio.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_double,
    ctypes.c_double,
]

# Set a fixed font scaling factor.
ass_set_font_scale = lib.ass_set_font_scale
ass_set_font_scale.restype = None
ass_set_font_scale.argtypes = [ctypes.POINTER(ASS_Renderer), ctypes.c_double]

# Set font hinting method.
ass_set_hinting = lib.ass_set_hinting
ass_set_hinting.restype = None
ass_set_hinting.argtypes = [ctypes.POINTER(ASS_Renderer), ctypes.c_int]

# Set line spacing. Will not be scaled with frame size.
ass_set_line_spacing = lib.ass_set_line_spacing
ass_set_line_spacing.restype = None
ass_set_line_spacing.argtypes = [ctypes.POINTER(ASS_Renderer), ctypes.c_double]

# Set vertical line position.
# Set vertical line position.
ass_set_line_position = lib.ass_set_line_position
ass_set_line_position.restype = None
ass_set_line_position.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_double,
]

# Get the list of available font providers. The output array is allocated with
# malloc and can be released with free(). If an allocation error occurs, size is
# set to (size_t)-1.
ass_get_available_font_providers = lib.ass_get_available_font_providers
ass_get_available_font_providers.restype = None
ass_get_available_font_providers.argtypes = [
    ctypes.POINTER(ASS_Library),
    ctypes.POINTER(ctypes.POINTER(ASS_DefaultFontProvider)),
    ctypes.POINTER(ctypes.c_int32),
]

# Set font lookup defaults.
ass_set_fonts = lib.ass_set_fonts
ass_set_fonts.restype = None
ass_set_fonts.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int32,
    ctypes.c_char_p,
    ctypes.c_int32,
]

# Set selective style override mode. If enabled, the renderer attempts to
# override the ASS script's styling of normal subtitles, without affecting
# explicitly positioned text. If an event looks like a normal subtitle, parts of
# the font style are copied from the user style set with
# ass_set_selective_style_override(). Warning: the heuristic used for deciding
# when to override the style is rather rough, and enabling this option can lead
# to incorrectly rendered subtitles. Since the ASS format doesn't have any
# support for allowing end-users to customize subtitle styling, this feature can
# only be implemented on "best effort" basis, and has to rely on heuristics that
# can easily break.
ass_set_selective_style_override_enabled = (
    lib.ass_set_selective_style_override_enabled
)
ass_set_selective_style_override_enabled.restype = None
ass_set_selective_style_override_enabled.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_int32,
]

# Set style for selective style override. See
# ass_set_selective_style_override_enabled().
ass_set_selective_style_override = lib.ass_set_selective_style_override
ass_set_selective_style_override.restype = None
ass_set_selective_style_override.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.POINTER(ASS_Style),
]

# This is a stub and does nothing. Old documentation: Update/build font cache.
# This needs to be called if it was disabled when ass_set_fonts was set.
ass_fonts_update = lib.ass_fonts_update
ass_fonts_update.restype = ctypes.c_int32
ass_fonts_update.argtypes = [ctypes.POINTER(ASS_Renderer)]

# Set hard cache limits. Do not set, or set to zero, for reasonable defaults.
ass_set_cache_limits = lib.ass_set_cache_limits
ass_set_cache_limits.restype = None
ass_set_cache_limits.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.c_int32,
    ctypes.c_int32,
]

# Render a frame, producing a list of ASS_Image.
ass_render_frame = lib.ass_render_frame
ass_render_frame.restype = ctypes.POINTER(ASS_Image)
ass_render_frame.argtypes = [
    ctypes.POINTER(ASS_Renderer),
    ctypes.POINTER(ASS_Track),
    ctypes.c_int64,
    ctypes.POINTER(ctypes.c_int32),
]

# Allocate a new empty track object.
ass_new_track = lib.ass_new_track
ass_new_track.restype = ctypes.POINTER(ASS_Track)
ass_new_track.argtypes = [ctypes.POINTER(ASS_Library)]

# Deallocate track and all its child objects (styles and events).
ass_free_track = lib.ass_free_track
ass_free_track.restype = None
ass_free_track.argtypes = [ctypes.POINTER(ASS_Track)]

# Allocate new style.
ass_alloc_style = lib.ass_alloc_style
ass_alloc_style.restype = ctypes.c_int32
ass_alloc_style.argtypes = [ctypes.POINTER(ASS_Track)]

# Allocate new event.
ass_alloc_event = lib.ass_alloc_event
ass_alloc_event.restype = ctypes.c_int32
ass_alloc_event.argtypes = [ctypes.POINTER(ASS_Track)]

# Delete a style.
ass_free_style = lib.ass_free_style
ass_free_style.restype = None
ass_free_style.argtypes = [ctypes.POINTER(ASS_Track), ctypes.c_int32]

# Delete an event.
ass_free_event = lib.ass_free_event
ass_free_event.restype = None
ass_free_event.argtypes = [ctypes.POINTER(ASS_Track), ctypes.c_int32]

# Parse a chunk of subtitle stream data.
ass_process_data = lib.ass_process_data
ass_process_data.restype = None
ass_process_data.argtypes = [
    ctypes.POINTER(ASS_Track),
    ctypes.c_char_p,
    ctypes.c_int32,
]

# Parse Codec Private section of the subtitle stream, in Matroska format. See
# the Matroska specification for details.
ass_process_codec_private = lib.ass_process_codec_private
ass_process_codec_private.restype = None
ass_process_codec_private.argtypes = [
    ctypes.POINTER(ASS_Track),
    ctypes.c_char_p,
    ctypes.c_int32,
]

# Parse a chunk of subtitle stream data. A chunk contains exactly one event in
# Matroska format. See the Matroska specification for details. In later libass
# versions (since LIBASS_VERSION==0x01300001), using this function means you
# agree not to modify events manually, or using other functions manipulating the
# event list like ass_process_data(). If you do anyway, the internal duplicate
# checking might break. Calling ass_flush_events() is still allowed.
ass_process_chunk = lib.ass_process_chunk
ass_process_chunk.restype = None
ass_process_chunk.argtypes = [
    ctypes.POINTER(ASS_Track),
    ctypes.c_char_p,
    ctypes.c_int32,
    ctypes.c_int64,
    ctypes.c_int64,
]

# Set whether the ReadOrder field when processing a packet with
# ass_process_chunk() should be used for eliminating duplicates.
ass_set_check_readorder = lib.ass_set_check_readorder
ass_set_check_readorder.restype = None
ass_set_check_readorder.argtypes = [ctypes.POINTER(ASS_Track), ctypes.c_int32]

# Flush buffered events.
ass_flush_events = lib.ass_flush_events
ass_flush_events.restype = None
ass_flush_events.argtypes = [ctypes.POINTER(ASS_Track)]

# Read subtitles from file.
ass_read_file = lib.ass_read_file
ass_read_file.restype = ctypes.POINTER(ASS_Track)
ass_read_file.argtypes = [
    ctypes.POINTER(ASS_Library),
    ctypes.c_char_p,
    ctypes.c_char_p,
]

# Read subtitles from memory.
ass_read_memory = lib.ass_read_memory
ass_read_memory.restype = ctypes.POINTER(ASS_Track)
ass_read_memory.argtypes = [
    ctypes.POINTER(ASS_Library),
    ctypes.c_char_p,
    ctypes.c_int32,
    ctypes.c_char_p,
]

# Read styles from file into already initialized track.
ass_read_styles = lib.ass_read_styles
ass_read_styles.restype = ctypes.c_int32
ass_read_styles.argtypes = [
    ctypes.POINTER(ASS_Track),
    ctypes.c_char_p,
    ctypes.c_char_p,
]

# Add a memory font.
ass_add_font = lib.ass_add_font
ass_add_font.restype = None
ass_add_font.argtypes = [
    ctypes.POINTER(ASS_Library),
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_int32,
]

# Remove all fonts stored in an ass_library object.
ass_clear_fonts = lib.ass_clear_fonts
ass_clear_fonts.restype = None
ass_clear_fonts.argtypes = [ctypes.POINTER(ASS_Library)]

# Calculates timeshift from now to the start of some other subtitle event,
# depending on movement parameter.
ass_step_sub = lib.ass_step_sub
ass_step_sub.restype = ctypes.c_int64
ass_step_sub.argtypes = [
    ctypes.POINTER(ASS_Track),
    ctypes.c_int64,
    ctypes.c_int32,
]
