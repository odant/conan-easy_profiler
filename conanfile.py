# easy_profiler Conan package
# Dmitriy Vetutnev, Odant, 2018


from conans import ConanFile, CMake, tools
import os


class easy_profiler_Conan(ConanFile):
    name = "easy_profiler"
    version = "2.0.0"
    license = "MIT https://opensource.org/licenses/MIT"
    description = "Lightweight cross-platform profiler library for C++"
    url = "https://github.com/odant/conan-easy_profiler"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "Findeasy_profiler.cmake", "library_install_path.patch"
    no_copy_source = True
    build_policy = "missing"
    
    def configure(self):
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")

    def source(self):
        tools.patch(patch_file="library_install_path.patch")

    def build(self):
        cmake = CMake(self)
        if self.settings.compiler != "Visual Studio":
            cmake.verbose = True
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        cmake.definitions["EASY_OPTION_PRETTY_PRINT"] = "ON"
        cmake.definitions["EASY_PROFILER_NO_GUI"] = "ON"
        cmake.definitions["EASY_PROFILER_NO_SAMPLES"] = "ON"
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        # CMake script
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        self.copy("Findeasy_profiler.cmake", dst=".", src=".", keep_path=False)
        # PDB
        #self.copy("easy_profiler.pdb", dst="bin", src="lib", keep_path=False)
        #self.copy("profiler_converter.pdb", dst="bin", src="bin", keep_path=False)
        # Convertor to JSON
        #self.copy("profiler_converter.exe", dst="bin", src="bin", keep_path=False)
        #self.copy("profiler_converter", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        # Libraries
        self.cpp_info.libs = ["easy_profiler"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["ws2_32", "psapi"])
        else:
            self.cpp_info.libs.append("pthread")
        # Defines
        self.cpp_info.defines = [
            "BUILD_WITH_EASY_PROFILER=1",
            "EASY_PROFILER_STATIC=1",
            "EASY_OPTION_PRETTY_PRINT_FUNCTIONS=1",
            "EASY_OPTION_STORAGE_EXPAND_BLOCKS_ON=0",
            "EASY_OPTION_IMPLICIT_THREAD_REGISTRATION=1",
            "EASY_OPTION_BUILTIN_COLORS=1"
        ]
        if self.settings.os == "Windows":
            self.cpp_info.defines.extend([
                "EASY_OPTION_EVENT_TRACING_ENABLED=1",
                "DEASY_OPTION_LOW_PRIORITY_EVENT_TRACING=1"
            ])
