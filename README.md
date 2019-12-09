#osxaliases.py

### Create, manipulate and resolve Mac OS X aliases.


## About
Mac OSX aliases are not symbolic links. Trying to read one will probably crash your code.

#### public functions:

`is_alias(path)` Returns true if a file is an OSX alias, false otherwise.

`create_osx_alias(filename, aliasname)` creates an alias pointing to file.

`resolve_osx_alias(path)` Returns the full path of the file pointed to by the alias.

#### commandline:
When run from command line accept one argument, an alias, and resolve it.

Based on this blog post and code by : Scott H. Hawley:
https://drscotthawley.github.io/Resolving-OSX-Aliases/



## Installation
 * System requirement: Python 3.x


## Usage:

usage: osxaliases.py [-h] file

Resolve OSX alias

positional arguments:
  file        alias file to resolve

optional arguments:
  -h, --help  show this help message and exit

## License
See [UNLICENSE](UNLICENSE) file
