from conan import ConanFile
import conan.tools
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
class sockets_p(ConanFile):
    name="sockets_p"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    #requires="asio/1.24.0"
    exports_sources = "CMakeLists.txt", "source/*", "c_app/*" , "tests/*"


    def requirements(self):
        self.requires("asio/[>=1.24.0]")#,headers=True, libs=True,transitive_headers=True,transitive_libs=True,run=True,visible=True,package_id_mode="full_mode")
        pass

    def source(self):
        pass
        #follloing is officialy depricated
        #self.exports_sources== "CMakeLists.txt", "source/*", "c_app/*" , "tests/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()
    def layout(self):
        cmake_layout(self,build_folder="conan_cmake")

    def build(self):
        cmake = CMake(self)        
        cmake.configure()
        cmake.build()
    def package(self):
        cmake = CMake(self)
        cmake.install()
    def package_info(self):
        self.cpp_info.libs = ["client","server"]