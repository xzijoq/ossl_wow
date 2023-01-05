if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  add_compile_options(-fdiagnostics-color=always)
elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  add_compile_options(-fcolor-diagnostics)
endif()

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  add_compile_options(
    # -gfull
    -O0
    -Wall
    -fdiagnostics-fixit-info
    -finline-hint-functions
    -fno-exceptions
    -fmodules
    -fdebug-info-for-profiling
    -fdiagnostics-show-template-tree
    # -fsanitize=cfi -flto -fsanitize-stats -fvisibility=hidden
    -fsanitize=address
    -fno-omit-frame-pointer
    -fsanitize=undefined
    #
  )

  add_link_options(
    # -fuse-ld=gold -fsanitize=cfi -flto -fsanitize-stats -fvisibility=hidden
    -fsanitize=address -fno-omit-frame-pointer -fsanitize=undefined
    #
  )
endif()
