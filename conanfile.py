from conans import CMake, ConanFile, tools
import os


class ArmadilloConan(ConanFile):
    name = "Armadillo"
    version = "8.300.0"
    license = "Apache License 2.0"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "C++ linear algebra library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "ARMA_USE_LAPACK": [True, False],
               "ARMA_USE_BLAS": [True, False]}
    default_options = "shared=True", "ARMA_USE_LAPACK=True", "ARMA_USE_BLAS=True"
    generators = "cmake"
    source_folder_name = ("armadillo-%s" % version)
    source_tarxz_file = ("%s.tar.xz" % source_folder_name)
    source_tar_file = ("%s.tar" % source_folder_name)
    requires = (
        "openblas/0.3.5@nrl/stable"
    )

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")

    def source(self):
        tools.download(("http://sourceforge.net/projects/arma/files/%s" % self.source_tarxz_file),
                       self.source_tarxz_file)

        if self.settings.os == "Windows":
            self.run("7z x %s" % self.source_tarxz_file)
            self.run("7z x %s" % self.source_tar_file)
            os.unlink(self.source_tar_file)
        else:
            self.run("tar -xvf %s" % self.source_tarxz_file)

        os.unlink(self.source_tarxz_file)
        os.rename(self.source_folder_name, "sources")

    def build(self):
        if not self.options.ARMA_USE_LAPACK:
            tools.replace_in_file(file_path="sources/include/armadillo_bits/config.hpp",
                                  search="#define ARMA_USE_LAPACK",
                                  replace="//#define ARMA_USE_LAPACK")

        if not self.options.ARMA_USE_BLAS:
            tools.replace_in_file(file_path="sources/include/armadillo_bits/config.hpp",
                                  search="#define ARMA_USE_BLAS",
                                  replace="//#define ARMA_USE_BLAS")

        cmake = CMake(self)
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        self.copy("armadillo", dst="include", src="sources/include")
        self.copy("*.hpp", dst="include/armadillo_bits",
                  src="sources/include/armadillo_bits")
        self.copy("*armadillo.dll", dst="bin", keep_path=False)
        self.copy("*armadillo.lib", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]
