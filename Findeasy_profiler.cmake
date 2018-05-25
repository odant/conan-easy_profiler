# easy_profiler Conan package
# Dmitriy Vetutnev, Odant, 2018


option(EASY_PROFILER_STUB_MODE "Stub mode" OFF)

find_path(EASY_PROFILER_INCLUDE_DIR
    NAMES easy/profiler.h
    PATHS ${CONAN_INCLUDE_DIRS_EASY_PROFILER}
    NO_DEFAULT_PATH
)

find_library(EASY_PROFILER_LIBRARY
    NAMES easy_profiler
    PATHS ${CONAN_LIB_DIRS_EASY_PROFILER}
    NO_DEFAULT_PATH
)
if(EXISTS ${CONAN_EASY_PROFILER_ROOT}/stub)
    message(STATUS "ESAY_PROFILER in stub-mode")
    set(EASY_PROFILER_STUB_MODE ON)
    unset(EASY_PROFILER_LIBRARY)
endif()

if(EASY_PROFILER_INCLUDE_DIR)

    set(EASY_PROFILER_VERSION_MAJOR 2)
    set(EASY_PROFILER_VERSION_MINOR 0)
    set(EASY_PROFILER_VERSION_TWEAK 0)
    set(EASY_PROFILER_VERSION_STRING "${EASY_PROFILER_VERSION_MAJOR}.${EASY_PROFILER_VERSION_MINOR}.${EASY_PROFILER_VERSION_TWEAK}")

endif()

include(FindPackageHandleStandardArgs)
if(NOT EASY_PROFILER_STUB_MODE)
    find_package_handle_standard_args(easy_profiler
        REQUIRED_VARS EASY_PROFILER_INCLUDE_DIR EASY_PROFILER_LIBRARY
        VERSION_VAR EASY_PROFILER_VERSION_STRING
    )
else()
    find_package_handle_standard_args(easy_profiler
        REQUIRED_VARS EASY_PROFILER_INCLUDE_DIR
        VERSION_VAR EASY_PROFILER_VERSION_STRING
    )
endif()

if(EASY_PROFILER_FOUND AND NOT TARGET easy_profiler)

    if(NOT EASY_PROFILER_STUB_MODE)

        include(CMakeFindDependencyMacro)
        find_dependency(Threads)

        add_library(easy_profiler UNKNOWN IMPORTED)

        set_target_properties(easy_profiler PROPERTIES
            IMPORTED_LOCATION "${EASY_PROFILER_LIBRARY}"
            INTERFACE_INCLUDE_DIRECTORIES "${EASY_PROFILER_INCLUDE_DIR}"
            INTERFACE_COMPILE_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_EASY_PROFILER}"
            INTERFACE_LINK_LIBRARIES Threads::Threads
        )

        if(WIN32)
            set_property(TARGET easy_profiler APPEND PROPERTY INTERFACE_LINK_LIBRARIES "ws2_32" "psapi")
        endif()

    else()

        add_library(easy_profiler INTERFACE IMPORTED)

        set_target_properties(easy_profiler PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${EASY_PROFILER_INCLUDE_DIR}"
            INTERFACE_COMPILE_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_EASY_PROFILER}"
        )

    endif()

    mark_as_advanced(EASY_PROFILER_INCLUDE_DIR EASY_PROFILER_LIBRARY EASY_PROFILER_STUB_MODE)

    set(EASY_PROFILER_INCLUDE_DIRS ${EASY_PROFILER_INCLUDE_DIR})
    set(EASY_PROFILER_LIBRARIES ${EASY_PROFILER_LIBRARY})
    set(EASY_PROFILER_DEFINITIONS ${CONAN_COMPILE_DEFINITIONS_EASY_PROFILER})

endif()

