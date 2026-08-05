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

# Frequency Following Response Project
https://en.wikipedia.org/wiki/Frequency_following_response

Frequency Following Response (FFR) is a neurophysiological response to an auditory stimulus that reflects the neural processing of its acoustic parameters with high precision.

## Equipment, software, documentation

AStim Auditory stimulator for FFR paradigms https://mks.ru/en/products/ep-erp https://docs.mks.ru/ru/file/682f7130953d8#to-docs

NVX 36 EEG acquisition system https://mks.ru/en/products/nvx

NVX 136 EEG acquisition system https://mks.ru/en/products/nvx-136

MCScap EEG cap system https://mks.ru/en/products/mcscap

Electrodes MCScap-CS22 Dry/gel electrodes for stimulation and recording https://mcscap.ru/catalog/tes-elektrody-dlya-stimulyatsii/mcscap-cs22/

NeoRec 1.6 Data acquisition and control software https://docs.mks.ru/en/file/65dd0ac5d6895#to-docs

Frequency_Following_Response_Astim (v1) Custom Python suite for FFR stimulus generation and analysis https://github.com/asmyasikova83/Frequency_Following_Response_Astim.git

FFR Astim v1 Documentation https://docs.mks.ru/download/6a50e1d6de9d5

## Configuration with ASTIM + EEG NVX36 Suite

![](./img/nvx36_scheme.jpg)

## Configuration with ASTIM + EEG NVX36 Suite
![](./img/nvx_136_scheme.jpg)

## Stimuli with ASTIM triggers

A WAV file with audio stimuli was generated using ASTIM commands placed in the right channel of the WAV file.
To mitigate bone‑conduction artifacts, two trigger types are used: 

\- trigger 6: original stimulus polarity.

\- trigger 7: inverted stimulus polarity.

Trigger timing protocol:

\- At the onset of each stimulus, the corresponding trigger (6 or 7) is set to LOW.

\- At the end of the stimulus, the trigger is set to HIGH. 

> Attention!
1. AStim correctly transfers triggers only when they are encoded in the right channel with ASTIM commands and zeros elsewhere. 
No additional channel activation is required.
2. Including a RESET CYCLE command when generating the audio file helps reduce trigger loss.
3. Implementation details can be found in the add_triggers() and make_full_signal() functions in functions.py (Frequency_Following_Response_Astim v1).

WAV file https://docs.mks.ru/en/file/6a575b8d86e5e#to-docs

## Audio stimuli generation

The `create_wav.py` script (from Frequency_Following_Response_Astim v1) generates WAV files containing:

\- Syllable stimuli (e.g., “Da”), or

\- Sinusoidal tones within a predefined frequency range.

Example calls:
           
Multiple sinusoidal tones at specified frequencies

           python create_wav.py  --function multiple_sin --F 110 220 440 880 --TS 100 --TP 100 --N 2 --INV 0

Repeated “Da” syllable with inverted polarity

           python create_wav.py  --function repeated_da  --TS 100 --TP 100 --N 100 --INV 1 --wavfname '\\MCSSERVER\DB Temp\physionet.org\FFR\stim\DA+20.wav' 

--F frequency

--TS stimulus latency

--TP interstimulus interval (pause) latency

--N number of stimulus repetitions

--INV add polar (inverted) stimulus

--wavfname path to an example of syllable to be multiplied and wrapped into audio stimulation

For a full list of arguments, run:

            python create_wav.py -h

## Preprocessing and Visualization of FFR

The `command_line_ffr.py` script performs FFR preprocessing and generates a PDF report containing:

\- Waveform and spectrum of the stimulus.

\- Grand average of the FFR response and its spectral representation.

\- Correlation coefficient 𝑅 between the stimulus waveform and the FFR waveform (computed over averages).

\- Relative power of FFR spectral peaks across averages.

Data files (`.bfd/.fif`) and associated stimuli (`.wav`) are selected interactively.

Example call:
        
            python command_line_ffr.py --TS 250 --TP 200 --fmin 80 --fmax 1500 --tmin -100 --tmax 300 --N 500

--TS: stimulus latency

--TP: interstimulus interval (pause) latency

--fmin: lower cutoff frequency for filtering

--fmax: upper cutoff frequency for filtering

--tmin: lower boundary of the time window (ms)

--tmax: upper boundary of the time window (ms)

--N: number of stimulus repetitions


For a full list of arguments, run:

            python command_line_ffr.py -h

## Software Requirements (Frequency_Following_Response_Astim v1)

        matplotlib==3.8.4
        mne==1.12.1
        numpy==2.3.4
        pandas==2.3.3
        pypdf==6.13.1
        reportlab==4.5.1
        scipy==1.16.3

