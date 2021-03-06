# AStimWavPatcher Example

The repository contains a file showing how to add AStim commands to a WAV file using the Python programming language.
> Attention!  
AStim works _only_ with __16-bit__ WAV files with a sampling rate of __44100 Hz__.

![](./img/nvx36+52_scheme.png)

## Script description

The script `wavpatcher.py` writes AStim commands to the right channel of the WAV file.
Two commands are written to the beginning of the file, enabling both the left and right channels. Commands to enable either only left or only right channel are also present in the script, but by default both channels are enabled.
Then trigger 6 is set to LOW. At the end of the file, trigger 6 is set to HIGH.

## Requirements

To run the script you need [Python](https://python.org/) (3.4 or higher), [numpy](https://numpy.org/) and [scipy](https://scipy.org/) packages.

## Usage

The script is run through the command line, as follows
<pre>
$ python wavpatcher.py <i>input_file_path</i> -o <i>output_file_path</i>
</pre>
If `output_file_path` is not specified (by the flag `-o`) input file will be rewritten.  
For a description of the arguments, see the help message, which can be shown by running with the `-h` flag.

## AStim Command Description

The commands are 3-bit, each bit is encoded with sequence of two 16-bit samples in the right channel:

    0: -32768 and +32767;
    1: +32767 and -32768.

There should be no gaps between the bits.  
There must be at least one sample with zero value between commands.  
If there are no commands, then there are only zero samples in the right channel.  

If there are zero samples on the right channel, the A-Stim goes into mono (the right channel receives samples from the left channel).  
If there are non-zero samples on the right channel, the A-Stim goes into standard stereo mode.  

Commands:
1) 000 - disable left channel, 001 - enable left channel (default);
2) 010 - disable right channel, 011 - enable right channel (default);
3) 100 - set trigger 6 LOW, 101 - set trigger 6 HIGH (default);
3) 110 - set trigger 7 LOW, 111 - set trigger 7 HIGH (default).

## File examples

The [audio/examples](./audio/examples) folder contains examples of WAV files with added commands in the right channel.  
The file [audio/examples/output_example_1s.wav](./audio/examples/output_example_1s.wav) was obtained by processing the file [audio/origin/input_example_1s.wav](./audio/origin/input_example_1s.wav) by the script [wavpatcher.py](./wavpatcher.py).
