project(
    'libblake3',
    'c',
    default_options: ['c_std=c23', 'buildtype=release'],
    version: '1.8.7',
)
include = include_directories('include')
add_project_arguments(
    '-DBLAKE3_NO_SSE2',
    '-DBLAKE3_NO_SSE41',
    '-DBLAKE3_NO_AVX2',
    '-DBLAKE3_NO_AVX512',
    language: ['c'],
)
libblake3 = static_library(
    'blake3',
    ['src/blake3.c', 'src/blake3_portable.c', 'src/blake3_dispatch.c'],
    include_directories: include,
    install: true,
)

libblake3_dep = declare_dependency(include_directories: include, link_with: libblake3)
