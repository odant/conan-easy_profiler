# easy_profiler Conan package
# Dmitriy Vetutnev, Odant, 2018


from conan import ConanFile, tools
import os


class easy_profiler_Conan(ConanFile):
    name = "easy_profiler"
    version = "2.1.0-beta1+2"
    license = "MIT https://opensource.org/licenses/MIT"
    description = "Lightweight cross-platform profiler library for C++"
    url = "https://github.com/odant/conan-easy_profiler"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "ninja": [True, False],
        "stub": [False, True]
    }
    default_options = {
        "ninja": True,
        "stub": False
    }
    exports_sources = "src/*", "disable_converter.patch", "core_install.patch", "fix_cmake_version.patch", "fix_atomic_init.patch"
    no_copy_source = True
    build_policy = "missing"
    
    def layout(self):
        tools.cmake.cmake_layout(self, src_folder="src")

    def build_requirements(self):
        if self.options.ninja:
            self.build_requires("ninja/[>=1.12.1]")
            
    def configure(self):
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")
        # Auto stub-mode
        toolset = str(self.settings.compiler.get_safe("toolset"))
        if toolset.endswith("_xp"):
            self.options.stub = True
        if self.settings.arch == "mips" or self.settings.arch == "armv7":
            self.options.stub = True
        if self.options.stub:
            self.output.warn("Stub-mode, not real library!")

    def source(self):
        tools.files.patch(self, patch_file="disable_converter.patch")
        tools.files.patch(self, patch_file="core_install.patch")
        tools.files.patch(self, patch_file="fix_cmake_version.patch")
        tools.files.patch(self, patch_file="fix_atomic_init.patch")

    def generate(self):
        if self.options.stub:
            return
        benv = tools.env.VirtualBuildEnv(self)
        benv.generate()
        renv = tools.env.VirtualRunEnv(self)
        renv.generate()
        if tools.microsoft.is_msvc(self):
            vc = tools.microsoft.VCVars(self)
            vc.generate()
        deps = tools.cmake.CMakeDeps(self)    
        deps.generate()
        cmakeGenerator = "Ninja" if self.options.ninja else None
        tc = tools.cmake.CMakeToolchain(self, generator=cmakeGenerator)
        tc.variables["BUILD_SHARED_LIBS"] = "ON"
        tc.variables["EASY_OPTION_PRETTY_PRINT"] = "ON"
        tc.variables["EASY_PROFILER_NO_GUI"] = "ON"
        tc.variables["EASY_PROFILER_NO_SAMPLES"] = "ON"
        tc.generate()

    def build(self):
        if self.options.stub:
            return
        cmake = tools.cmake.CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        if not self.options.stub:
            cmake = tools.cmake.CMake(self)
            cmake.install()
            # CMake script
            tools.files.rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
            # PDB
            tools.files.copy(self, "easy_profiler.pdb", dst=os.path.join(self.package_folder, "bin"), src=os.path.join(self.build_folder, "lib"), keep_path=False)
        # Manual packing headers in stub-mode
        else:
            tools.files.copy(self, "*.h", dst=os.path.join(self.package_folder, "include"), src=os.path.join(self.source_folder, "easy_profiler_core/include"), keep_path=True)
            tools.files.save(os.path.join(self.package_folder, "stub"), "")

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        if not self.options.stub:
            # Libraries
            self.cpp_info.libs = ["easy_profiler"]
            if self.settings.os == "Windows":
                self.cpp_info.system_libs.extend(["ws2_32", "psapi"])
            else:
                self.cpp_info.system_libs.append("pthread")
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
                    "EASY_OPTION_LOW_PRIORITY_EVENT_TRACING=1"
                ])
