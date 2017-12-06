from conans import CMake, ConanFile


class ArmadilloConan(ConanFile):
    name = 'armadillo'
    version = '8.3'
    license = 'Apache License 2.0'
    url = '<Package recipe repository url here, for issues about the package>'
    description = 'C++ linear algebra library'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    generators = 'cmake'

    def source(self):
        self.run(
            'curl -OL http://sourceforge.net/projects/arma/files/armadillo-8.300.0.tar.xz'
        )
        self.run('tar -xvf armadillo-8.300.0.tar.xz')

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
        self.cpp_info.libs = ['armadillo']
