# drunken-hipster
Frequncy analysis tool for interactive decoding of a monosubstitution cipertext

# Purpose

# Install

# Useage
Run from the command line with python 2 to launch an interacive session
    [user@host]$ python freq_analysis.py
    $ 

There is help text for each command availble using `-h` or `--help` flags.

You can load any type of file for ananlysis. This program only treats capital ASCII as 
ciphertext, all other characters are ignored

Currently there is no way to write decoded files, if you need that feature let me know using the **Issue** button

# Bugs
It is only possible to use --load-string with a single word of text, whitespace gets eaten
and trying to escape by quoting or backticks are ignored by argparse
### Example
     $ --load-string QVJDB MEDGB QJJSG WQGZS NSZBN
     Mono Subsitution Helper: error: unrecognized arguments: MEDGB QJJSG WQGZS NSZBN

Instead use underscores, which are ignored by the actual parsing and decoding

	 $ --load-string QVJDB_MEDGB_QJJSG_WQGZS_NSZBN

This is not great behavior, so please fix this and make a pull request
