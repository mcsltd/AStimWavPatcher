import os
import argparse
import traceback
from scipy.io import wavfile


class Error(Exception):
    def __init__(self, message):
        super(Error, self).__init__(message)


def main():
    try:
        input_file, output_file = _parse_args()
        samplerate, channels = _read_file(input_file)
        channels = _add_trigger(channels)
        _write_file(channels, samplerate, output_file)
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


if __name__ == "__main__":
    main()
