import argparse


def main():
    input_file, output_file = _parse_args()
    channels, params = _read_file(input_file)
    channels = _add_trigger(channels)
    _write_file(channels, params, output_file)


def _parse_args():
    parser = argparse.ArgumentParser(description="Patch .wav files")
    parser.add_argument("input_file", help="Path to input .wav file")
    parser.add_argument(
        "output_file", help="Path to output .wav file", required=False)
    data = parser.parse_args()
    output_file = data.output_file or data.input_file
    return data.input_file, output_file


if __name__ == "__main__":
    main()
