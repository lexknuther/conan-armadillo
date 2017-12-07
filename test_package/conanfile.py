from conans import ConanFile, CMake
import os

class ArmadilloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*armadillo.dll", dst="bin", src="bin")
        self.copy("*blas.dll", dst="bin", src="bin")
        self.copy("*armadillo.dylib*", dst="bin", src="lib")
        self.copy("*blas.dylib*", dst="bin", src="lib")
        self.copy("*armadillo.so*", dst="bin", src="lib")
        self.copy("*blas.so*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
