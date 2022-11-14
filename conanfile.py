from conan import ConanFile
import conan.tools
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
class sockets_p(ConanFile):
    name="conan_p"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def source(self):
        self.exports_sources== "CMakeLists.txt", "source/*", "c_app/*" , "tests/*"
    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()
    def layout(self):
        cmake_layout(self,build_folder="conan_cmake")
        pass
    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()