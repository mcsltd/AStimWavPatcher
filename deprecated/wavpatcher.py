import os
import argparse
from scipy.io import wavfile
import numpy as np
from enum import Enum, auto

_SILENCE = 15


class Ears(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTH = auto()


def main():
    input_file, output_file = _parse_args()
    samplerate, channels = _read_file(input_file)
    channels = _add_trigger(channels)
    wavfile.write(output_file, samplerate, channels)


def _parse_args():
    parser = argparse.ArgumentParser(description="Patch .wav files")
    parser.add_argument("input_file", help="Path to input .wav file")
    parser.add_argument("-o", "--output", help="Path to output .wav file")
    data = parser.parse_args()
    output_file = data.output or data.input_file
    return data.input_file, output_file


def _read_file(filepath):
    if not os.path.exists(filepath):
        print("File {0} not found!".format(filepath))
        os.sys.exit()
    filepath = os.path.abspath(filepath)
    return wavfile.read(filepath)


def _add_trigger(channels, ears=Ears.BOTH):
    if channels.ndim == 1:
        left = channels
    else:
        left = channels[:, 0]
    dtype = left.dtype
    left = np.append(np.zeros(_SILENCE, dtype), left)
    right = _get_right_channel(len(left), ears, dtype)
    return np.column_stack([left, right])


def _get_right_channel(size, ears, dtype):
    max_int16 = np.iinfo(np.int16).max
    min_int16 = np.iinfo(np.int16).min
    result = np.zeros(size, dtype)
    if ears == Ears.RIGHT:
        # 000 - disable left channel
        result[1] = min_int16
        result[2] = max_int16
        result[3] = min_int16
        result[4] = max_int16
        result[5] = min_int16
        result[6] = max_int16
        # [7] is zero value between commands
        # 011 - enable right channel
        result[8] = min_int16
        result[9] = max_int16
        result[10] = max_int16
        result[11] = min_int16
        result[12] = max_int16
        result[13] = min_int16
    elif ears == Ears.LEFT:
        # 001 - enable left channel
        result[1] = min_int16
        result[2] = max_int16
        result[3] = min_int16
        result[4] = max_int16
        result[5] = max_int16
        result[6] = min_int16
        # 010 - disable right channel
        result[8] = min_int16
        result[9] = max_int16
        result[10] = max_int16
        result[11] = min_int16
        result[12] = min_int16
        result[13] = max_int16
    else:
        # 001 - enable left channel
        result[1] = min_int16
        result[2] = max_int16
        result[3] = min_int16
        result[4] = max_int16
        result[5] = max_int16
        result[6] = min_int16
        # 011 - enable right channel
        result[8] = min_int16
        result[9] = max_int16
        result[10] = max_int16
        result[11] = min_int16
        result[12] = max_int16
        result[13] = min_int16

    # 100 - set trigger 6 LOW
    result[_SILENCE] = max_int16
    result[_SILENCE + 1] = min_int16
    result[_SILENCE + 2] = min_int16
    result[_SILENCE + 3] = max_int16
    result[_SILENCE + 4] = min_int16
    result[_SILENCE + 5] = max_int16

    # 101 - set trigger 6 HIGH (default)
    result[size - 6] = max_int16
    result[size - 5] = min_int16
    result[size - 4] = min_int16
    result[size - 3] = max_int16
    result[size - 2] = max_int16
    result[size - 1] = min_int16

    return result


if __name__ == "__main__":
    main()
