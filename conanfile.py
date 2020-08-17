from conans import CMake, ConanFile, tools
import os


class ArmadilloConan(ConanFile):
    name = "Armadillo"
    version = "9.900.2"
    license = "Apache License 2.0"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "C++ linear algebra library"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "BLAS": [True, False],
        "OpenBLAS": [True, False],
        "MKL": [True, False],
        "ATLAS": [True, False],
        "ACML": [True, False],
        "ACMLMP": [True, False],
        "LAPACK": [True, False],
        "BUILD_SMOKE_TEST": [True, False]
    }
    default_options = "shared=True", "BLAS=False", "OpenBLAS=True", "MKL=False", "ACML=False", "ACMLMP=False", \
                      "LAPACK=False", "BUILD_SMOKE_TEST=True", "ATLAS=False", "openblas:TARGET=HASWELL"
    generators = "cmake", "cmake_paths"
    source_folder_name = ("armadillo-%s" % version)
    source_tarxz_file = ("%s.tar.xz" % source_folder_name)
    source_tar_file = ("%s.tar" % source_folder_name)
    requires = ()
    exports_sources = "CMakeLists.txt.patch"

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")

    def requirements(self):
        if self.options.OpenBLAS:
            self.requires("openblas/0.3.10@nrl/stable")

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
        tools.patch(base_path="sources", patch_file="CMakeLists.txt.patch")

    def build(self):
        cmake = CMake(self)
        for (key, value) in list(self.options.items()):
            if key not in ("shared", "BUILD_SMOKE_TESTS"):
                cmake.definitions["USE_{}".format(key)] = "ON" if value == "True" else "OFF"
        cmake.definitions["BUILD_SMOKE_TESTS"] = "ON" if self.options["BUILD_SMOKE_TESTS"] else "OFF"
        cmake.configure(source_dir="sources")
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()

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
