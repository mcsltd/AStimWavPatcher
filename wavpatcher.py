def main():
    input_file, output_file = _parse_args()
    channels, params = _read_file(input_file)
    channels = _add_trigger(channels)
    _write_file(channels, params, output_file)


if __name__ == "__main__":
    main()
