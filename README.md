# drunken-hipster
Frequncy analysis tool for interactive decoding of a monosubstitution cipertext

# Install
##### Windows
You need the colorama package to allow the pretty printing using ANSI escape codes. 

	pip install colorama
	
Unix based terminals should work right out of the box.

Then clone this repo and run!

	$ git clone git@github.com:YetAnotherMinion/drunken-hipster.git
	$ cd drunken-hipster

# Usage
Run from the command line with Python 2 to launch an interacive session giving you a prompt.

   	[shivaebola@localhost drunken-hipster]$ python freq_analysis.py 
   	$ --help
   	usage: Mono Subsitution Helper [-h] [-decode <char> <char>] [-q]
	                               [--load-file <filename>]
	                               [--load-string <string>] [--sub] [--to-upper]
	                               [--show-mapping] [-c] [-f [1,2,3]]
	
	assists in decoding a mono substitution cipher
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -decode <char> <char>
	                        <A> <B> where A in ciphertext maps to B in plaintext
	  -q, --quit            Exit the program, discarding all data
	  --load-file <filename>
	                        Loads a file and treats it as cipher text
	  --load-string <string>
	                        Loads a string of cipher text from command line
	  --sub                 Substitute the characters in the ciphetext with their
	                        assigned mappings
	  --to-upper            Changes lowercase ASCII characters in input format to
	                        upper case
	  --show-mapping        show the individual character level mapping of the
	                        cipher
	  -c, --ciphertext      print the cipher text to the screen
	  -f [1,2,3], --frequency [1,2,3]
	                        compute a frequency analysis on ciphertext, default
	                        behaviour is to print counts for the 1-grams 2-grams
	                        and 3-grams in the ciphertext sorted from most
	                        frequent to least frequent shown alongside sorted
	                        frequency of n-grams for english language Use optional
	                        argument of [1,2,3] to only show a specific n-gram
	                        frequency analysis, any other values will be ignored
	$ 

================
When you launch the program there is an empty mapping between characters in the ciphertext and the plaintext alphabets.

	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
	
You add mapping by using `-decode` which takes a character string of ciphertext which is an injective map to the
plaintext string. These two strings must be the same length.

	$ -decode JDS THE
	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ H _ _ _ _ _ T _ _ _ _ _ _ _ _ E _ _ _ _ _ _ _
	$   

If the mapping strings are not the same length, nothing will happen, although no error message is currently emmited

	$ -decode FAT BB
	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ H _ _ _ _ _ T _ _ _ _ _ _ _ _ E _ _ _ _ _ _ _
	$ 

You can use mix lower and upper case letters with no effect, to mappings, some might consider this a bug.

	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ E _ _ _ _ _ _ _
	$ -decode jd th
	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ H _ _ _ _ _ T _ _ _ _ _ _ _ _ E _ _ _ _ _ _ _
	$ 
You can remove mapping using an underscore character in the plaintext mapping string

	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ H _ _ _ _ _ T _ _ _ _ _ _ _ _ E _ _ _ _ _ _ _
	$ -decode JD __
	$ --show-mapping
	Mappings:
	C: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
	P: _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ E _ _ _ _ _ _ _

You can load textfiles with ascii text. It is unlikely that unicode will work, same goes for binary files. 
This program only treats capital ASCII as  ciphertext, all other characters are ignored. 
Filenames and paths with **spaces are not supported**.
All filenames are relative to the excution location of the script, so relative paths to 
files in other directories are supported **as long as there are no spaces** If the you want to convert the lower 
case letters from the input file to upper case, specify the `--to-upper` flag



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
