# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles/Oscuola_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/Oscuola_autogen.dir/ParseCache.txt"
  "Oscuola_autogen"
  )
endif()
