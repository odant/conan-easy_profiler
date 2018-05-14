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
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Release", "Debug"],
        "arch": ["x86_64", "x86", "mips"]
    }
    options = {
        "stub": [False, True],
        "gui": [False, True]
    }
    default_options = "stub=False"
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "Findeasy_profiler.cmake", "disable_converter.patch", "core_install.patch", "gui_install.patch"
    no_copy_source = True
    build_policy = "missing"

    def configure(self):
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")
        # Auto stub-mode
        toolset = str(self.settings.compiler.get_safe("toolset"))
        if toolset.endswith("_xp"):
            self.options.stub = True
        if self.settings.arch == "mips":
            self.options.stub = True
        if self.options.stub:
            self.output.warn("Stub-mode, not real library!")
            if self.options.gui:
                raise Exception("GUI not supported in stub-mode!")

    def source(self):
        tools.patch(patch_file="disable_converter.patch")
        tools.patch(patch_file="core_install.patch")
        tools.patch(patch_file="gui_install.patch")

    def build(self):
        if self.options.stub:
            return
        cmake = CMake(self)
        if self.settings.compiler != "Visual Studio":
            cmake.verbose = True
        #
        if self.settings.compiler == "Visual Studio":
            cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder
        cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        cmake.definitions["EASY_OPTION_PRETTY_PRINT"] = "ON"
        cmake.definitions["EASY_PROFILER_NO_SAMPLES"] = "ON"
        if not self.options.gui:
            cmake.definitions["EASY_PROFILER_NO_GUI"] = "ON"
        else:
            cmake.definitions["EASY_PROFILER_NO_GUI"] = "OFF"
            cmake.definitions["CMAKE_PREFIX_PATH"] = self._get_qt_path()
        #
        cmake.configure()
        cmake.build()
        cmake.install()

    def _get_qt_path(self):
        qt_path = os.getenv("QT_PATH")
        if qt_path is None:
            raise Exception("Please set QT_PATH environment variable!")
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            toolkit = {
                "14": "msvc2015",
                "15": "msvc2017"
            }.get(str(self.settings.compiler.version))
            toolkit += {
                "x86_64": "_64"
            }.get(str(self.settings.arch))
            qt_path = os.path.join(qt_path, toolkit)
            qt_path.replace("\\", "/")
        else:
            raise Exception("Not released!")
        return qt_path

    def package(self):
        # CMake script
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        self.copy("Findeasy_profiler.cmake", dst=".", src=".", keep_path=False)
        # PDB
        self.copy("easy_profiler.pdb", dst="bin", src="lib", keep_path=False)
        self.copy("profiler_gui.pdb", dst="bin", src="bin", keep_path=False)
        # Manual packing headers in stub-mode
        if self.options.stub:
            self.copy("*.h", dst="include", src="src/easy_profiler_core/include", keep_path=True)
            tools.save(os.path.join(self.package_folder, "stub"), "")

    def deploy(self):
        if self.options.gui:
            self.copy("*", dst=".", src="bin", keep_path=True)

    def package_info(self):
        if not self.options.stub:
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
