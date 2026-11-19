project(
    'tree-sinker',
    'cpp',
    default_options: ['cpp_std=c++23'],
    license: 'GPL-2.0-or-later',
    version: '0.5',
)
dep_curl = dependency('libcurl')
sinker_sources = 'src/tree-sinker.cpp'
executable('tree-sinker', sinker_sources, dependencies: [dep_curl])
