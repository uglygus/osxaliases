#!/usr/bin/env python3
"""

osxaliases.py 

Create, manipulate and resolve Mac OS X aliases.

Mac OSX aliases are not symbolic links. Trying to read one will probably crash your code.

public functions:
    is_alias(path): Returns true if a file is an OSX alias, false otherwise.
    create_osx_alias(filename, aliasname): creates an alias.
    resolve_osx_alias(path): Returns the full path of the file pointed to by the alias.

commandline:
    when run from command line accept one argument, an alias, and resolve it 

Based on this blog post and code by : Scott H. Hawley:
https://drscotthawley.github.io/Resolving-OSX-Aliases/
"""

import subprocess
import os


def decodelist(thelist):
    ''' takes a list of bytes
        strips whitespace from ends of each element
        returns a string of the elements joined by spaces
    '''
    return ' '.join([item.decode('utf8').strip() for item in thelist])


def run_osascript(applescript):
    ''' run applescript, return errorcode, stdout, stderr '''
    p = subprocess.Popen('osascript', shell=False, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in applescript:
        p.stdin.write(line.encode())
    p.stdin.close()

    retval = p.wait()

    out = decodelist(p.stdout.readlines())
    err = decodelist(p.stderr.readlines())

    return retval, out, err


def is_alias(path):
    """ Returns true if a file is an OSX alias, false otherwise. """

    checkpath = os.path.abspath(path)       # osascript needs absolute paths

    applescript = ['tell application "Finder"',
                   'set theItem to (POSIX file "' + checkpath + '") as alias',
                   'if the kind of theItem is "alias" then',
                   '   return true',
                   'else',
                   '   return false',
                   'end if',
                   'end tell',
                   ]

    applescript = "\n".join(applescript)

    code, out, err = run_osascript(applescript)

    if out == 'true':
        return True
    if out == 'false':
        return False

    print('is_alias: ERROR subprocess returned unexpected response:'+  str(code) + ' -- ' + str(out) + ' -- ' + str(err))
    return None


def create_osx_alias(filename, aliasname):
    """
    creates an alias.
    filename = '/full/path/to/file.txt'
    aliasname = '/full/path/to/file_alias.txt'
    """

    abs_filename = os.path.abspath(filename)  # osascript needs absolute paths
    abs_aliasname = os.path.abspath(aliasname)

    applescript = [
        'set testFile to (POSIX file "' + abs_filename + '") as alias',
        'set outFolder to (POSIX file "' + os.path.dirname(abs_aliasname) + '") as alias',
        'set outFilename to "' + os.path.basename(abs_aliasname) + '"',
        'tell application "Finder"',
        '   make new alias file to testFile at outFolder with properties {name:outFilename}',
        'end tell'
    ]

    applescript = "\n".join(applescript)

    code, out, err = run_osascript(applescript)

    if code == 0:
        return True
        
    print('create_osx_alias: ERROR subprocess returned unexpected response: ' +
          str(code) + ' -- ' + str(out) + ' -- ' + str(err))  
    return None


def resolve_osx_alias(path):        
    """ Returns the full path of the file pointed to by the alias. """

    fullpath = os.path.abspath(path)

    applescript = [
        'tell application "Finder"',
        'set theItem to (POSIX file "' + fullpath + '") as alias',
        'if the kind of theItem is "alias" then',
        '   get the posix path of ((original item of theItem) as text)',
        'else',
        '   return false',
        'end if',
        'end tell'
    ]

    applescript = '\n'.join(applescript)

    code, out, err = run_osascript(applescript)

    if code != 0:
        print('resolve_osx_alias: ERROR subprocess returned unexpected response: ' +
              str(code) + ' -- ' + str(out) + ' -- ' + str(err))
        return None

    if out == 'false':
        out = False

    return out


def main():
    ''' when run from command line accept one argument, an alias, and resolve it '''
    import argparse
    parser = argparse.ArgumentParser(description='Resolve OSX alias')
    parser.add_argument('file', help="alias file to resolve")
    args = parser.parse_args()
    out = resolve_osx_alias(args.file)
    print(args.file, "resolves to: ", out)


if __name__ == "__main__":
    main()
