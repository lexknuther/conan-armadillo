from conans import CMake, ConanFile, tools
import os


class ArmadilloConan(ConanFile):
    name = "Armadillo"
    version = "8.300.0"
    license = "Apache License 2.0"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "C++ linear algebra library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "ARMA_USE_LAPACK": [True, False], "ARMA_USE_BLAS":[True, False]}
    default_options = "shared=False", "ARMA_USE_LAPACK=False", "ARMA_USE_BLAS=False"
    generators = "cmake"
    requires = "7z_installer/1.0@conan/stable"
    source_folder_name = ("armadillo-%s" % version)
    source_tarxz_file = ("%s.tar.xz" % source_folder_name)
    source_tar_file = ("%s.tar" % source_folder_name)

    def source(self):
        tools.download(
            ("http://sourceforge.net/projects/arma/files/%s" % self.source_tarxz_file), self.source_tarxz_file)
        self.run("7z x %s" % self.source_tarxz_file)
        self.run("7z x %s" % self.source_tar_file)
        os.unlink(self.source_tarxz_file)
        os.unlink(self.source_tar_file)
        os.rename(self.source_folder_name, "sources")

    def build(self):
        cmake = CMake(self)
        self.run('cmake %s/armadillo-8.300.0 %s' % (self.conanfile_directory,
                                                    cmake.command_line))
        self.run('cmake --build .')

    def package(self):
        self.copy('armadillo', dst='include', src='armadillo-8.300.0/include')
        self.copy(
            '*.hpp',
            dst='include/armadillo_bits',
            src='armadillo-8.300.0/include/armadillo_bits')
        self.copy('*.so', dst='lib', keep_path=False)
        self.copy('*.so.*', dst='lib', keep_path=False)
        self.copy('*.a', dst='lib', keep_path=False)
        self.copy('*.dylib', dst='lib', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]
