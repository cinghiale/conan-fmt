from conans import ConanFile, CMake, tools
import os


class FmtConan(ConanFile):
    name = "fmt"
    version = "3.0.0"
    license = "BSD"
    url = "https://github.com/memsharded/conan-fmt"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    def source(self):
       self.run("git clone https://github.com/fmtlib/fmt")
       self.run("cd fmt && git checkout 3.0.0")

    def build(self):
       shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
       fpic = "-DCMAKE_POSITION_INDEPENDENT_CODE=TRUE" if self.options.fPIC else ""
       cmake = CMake(self.settings)
       self.run("cd fmt && cmake . %s %s %s" % (cmake.command_line, shared, fpic))
       self.run("cd fmt && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/fmt", src="fmt/fmt")
        self.copy("*.a", dst="lib", src="fmt/fmt", keep_path=False)
        self.copy("*.so*", dst="lib", src="fmt/fmt", keep_path=False)
        self.copy("*.lib", dst="lib", src="fmt/fmt", keep_path=False)
        self.copy("*.dll", dst="bin", src="fmt/fmt", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["fmt"]

