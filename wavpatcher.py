import os
import argparse
import traceback
from scipy.io import wavfile
import numpy as np
from enum import Enum, auto

_SILENCE = 15


class Ears(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()


class Error(Exception):
    def __init__(self, message):
        super(Error, self).__init__(message)


def main():
    try:
        input_file, output_file = _parse_args()
        samplerate, channels = _read_file(input_file)
        channels = _add_trigger(channels, Ears.BOTH)
        wavfile.write(output_file, samplerate, channels)
    except Error as exc:
        print("Error: {0}\n".format(exc))
    except Exception as exc:
        if _is_debug():
            raise
        log_filename = "errors-log.txt"
        message = "Fatal error! {0}: {1}. See details in file '{2}'."
        print(message.format(type(exc).__name__, exc, log_filename))
        with open(log_filename, "wt") as log:
            log.write(traceback.format_exc())


def _is_debug():
    return getattr(os.sys, 'gettrace', None) is not None


def _parse_args():
    parser = argparse.ArgumentParser(description="Patch .wav files")
    parser.add_argument("input_file", help="Path to input .wav file")
    parser.add_argument(
        "output_file", help="Path to output .wav file", required=False)
    data = parser.parse_args()
    output_file = data.output_file or data.input_file
    return data.input_file, output_file


def _read_file(filepath):
    if not os.path.exists(filepath):
        raise Error("File {0} not found!".format(filepath))
    filepath = os.path.abspath(filepath)
    return wavfile.read(filepath)


def _add_trigger(channels, ears):
    left = np.zeros(_SILENCE).append(channels[:, 0])
    right = _get_right_channel(len(left), ears)
    return [left, right]


def _get_right_channel(size, ears):
    max_int16 = np.iinfo(np.int16).max
    min_int16 = np.iinfo(np.int16).min
    result = np.zeros(size)
    if ears == Ears.RIGHT:
        result[1] = min_int16
        result[2] = max_int16
        result[3] = min_int16
        result[4] = max_int16
        result[5] = min_int16
        result[6] = max_int16

        result[8] = min_int16
        result[9] = max_int16
        result[10] = max_int16
        result[11] = min_int16
        result[12] = max_int16
        result[13] = min_int16
    elif ears == Ears.LEFT:
        result[1] = min_int16
        result[2] = max_int16
        result[3] = min_int16
        result[4] = max_int16
        result[5] = max_int16
        result[6] = min_int16

        result[8] = min_int16
        result[9] = max_int16
        result[10] = max_int16
        result[11] = min_int16
        result[12] = min_int16
        result[13] = max_int16
    else:
        result[1] = min_int16
        result[2] = max_int16
        result[3] = min_int16
        result[4] = max_int16
        result[5] = max_int16
        result[6] = min_int16

        result[8] = min_int16
        result[9] = max_int16
        result[10] = max_int16
        result[11] = min_int16
        result[12] = max_int16
        result[13] = min_int16

    result[_SILENCE] = max_int16
    result[_SILENCE + 1] = min_int16
    result[_SILENCE + 2] = min_int16
    result[_SILENCE + 3] = max_int16
    result[_SILENCE + 4] = min_int16
    result[_SILENCE + 5] = max_int16

    result[size - 6] = max_int16
    result[size - 5] = min_int16
    result[size - 4] = min_int16
    result[size - 3] = max_int16
    result[size - 2] = max_int16
    result[size - 1] = min_int16

    return result


if __name__ == "__main__":
    main()
