#! /usr/bin/env python
# encoding: utf-8

import os
from waflib import Task, TaskGen

APPNAME = 'seasocks'
VERSION = '1.0.0'

def configure(conf):
    if conf.is_mkspec_platform('linux') and not conf.env['LIB_PTHREAD']:
        conf.check_cxx(lib='pthread')

def build(bld):
    bld.env.append_unique(
        'DEFINES_STEINWURF_VERSION',
        'STEINWURF_SEASOCKS_VERSION="{}"'.format(VERSION))

    use_flags = []
    if bld.is_mkspec_platform('linux'):
        use_flags += ['PTHREAD']

    # Path to the seasocks repo
    path = bld.dependency_path("seasocks-source")
    seasocks_path = bld.root.find_dir(path)
    sources = seasocks_path.ant_glob('src/main/c/**/*.cpp', excl=['**/ZlibContext.cpp'])
    sources += bld.path.ant_glob('src/Embedded.cpp')

    include_paths = [os.path.join(path, 'src', 'main', 'c'), './src']


    bld.stlib(
        features='cxx',
        source=sources,
        includes=include_paths,
        target='seasocks',
        use=use_flags,
        export_includes=include_paths
    )

    if bld.is_toplevel():
        # Only build tests when executed from the top-level wscript,
        # i.e. not when included as a dependency

        # Export thirdparty includes
        out = bld(name='thirdparty',
            includes='./thirdparty',
            export_includes='./thirdparty')

        bld.program(
            features='cxx test',
            source=seasocks_path.ant_glob('src/test/c/*.cpp', excl=['**/EmbeddedContentTests.cpp']),
            target='seasocks_tests',
            includes=include_paths,
            use=['thirdparty', 'seasocks'])
