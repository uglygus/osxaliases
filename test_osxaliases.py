#!/usr/bin/env python3
"""
pytest osxaliases

run 'pytest' in the root of this module.

"""

import os
import shutil
import osxaliases

testfolder = './testfolder/'
realfile = testfolder + 'real-file.txt'
aliasfile = testfolder + 'alias-file.txt'
aliascreatedfile = testfolder + 'newly-created-alias-file.txt'

testfolder_deeper = testfolder+'./testfolder_deeper/'
alias_pointing_to_an_alias = testfolder + 'alias_pointing_to_an_alias'


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    if os.path.exists(testfolder):
        shutil.rmtree(testfolder)
    os.mkdir(testfolder)
    open(realfile, 'a').close()
    osxaliases.create_osx_alias(realfile, aliasfile)


def teardown_module(module):
    """ teardown the testfolder """
    shutil.rmtree(testfolder)


class Test_is_alias:
    '''test is_alias function'''

    def test_realfile(self):
        print('testing is_alias(realfile)')
        assert osxaliases.is_alias(realfile) == False

    def test_aliasfile(self):
        assert osxaliases.is_alias(aliasfile)


class Test_ResolveOSXAlias:
    '''test resolve_osx_alias function'''

    def test_resolve_alias_to_realfile(self):
        assert osxaliases.resolve_osx_alias(
            aliasfile) == os.path.abspath(realfile)

    def test_resolve_osx_alias_from_realfile(self):
        assert osxaliases.resolve_osx_alias(realfile) == False

    def test_resolve_osx_nested(self):

        osxaliases.create_osx_alias(aliascreatedfile, aliascreatedfile)

        assert osxaliases.resolve_osx_alias(realfile) == False


class Test_CreateAlias:
    '''test icreate_osx_alias function'''

    def test_create_osx_alias(self):
        assert osxaliases.create_osx_alias(
            realfile, aliascreatedfile) and os.path.exists(aliascreatedfile)
