# drunken-hipster
Frequncy analysis tool for interactive decoding of a monosubstitution cipertext

# Bugs
It is only possible to use --load-string with a single word of text, whitespace gets eaten
and trying to escape by quoting or backticks are ignored by argparse
### Example
     $ --load-string QVJDB MEDGB QJJSG WQGZS NSZBN
     Mono Subsitution Helper: error: unrecognized arguments: MEDGB QJJSG WQGZS NSZBN

Instead use underscores, which are ignored by the actual parsing and decoding
	 $ --load-string QVJDB_MEDGB_QJJSG_WQGZS_NSZBN
This is not great behavior, so please fix this and make a pull request
