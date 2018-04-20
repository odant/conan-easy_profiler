# Test for easy_profiler Conan package
# Dmitriy Vetutnev, Odant, 2018


from conans import ConanFile, CMake


class GoogletestTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.pdb", dst="bin", src="bin")

    def test(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.run("ctest --verbose --build-config %s" % self.settings.build_type)
        else:
            self.run("ctest --verbose")
