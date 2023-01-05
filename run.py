# -================GOD ENDS HERE===============================

#region TODO
# --TODO ENABLE EAST CROSS SCRIPTING
# - TODO TRY EMSCRIPTIN

# - TODO create CONAN PACKAGE NAME and version for conan_create and conan_test
#endregion
# region imports
import os
import subprocess
import sys
import argparse
import shutil
import time
from io import StringIO
from os.path import join
from os.path import isdir
from os.path import isfile
import inspect
from inspect import currentframe, getframeinfo
# endregion

conan = True
TargetApp = True
EnableTest = True

godot = False
RecordTime = False
ShowTime = False
#region CONSTANTS
# ---------DEFS DONT ALTER-------------
cwd = os.getcwd()
cfd = os.path.dirname(os.path.realpath(__file__))
Fatal = True
# --------------END DEFS----------------------
#endregion

# region -------------------CONAN DATA---------------------------
if conan:
    conan_data_path = join(cfd, "conan")
    conan_dir_path = join(cfd, "")
    conan_build_dir_path = join(cfd, "conan_cmake")

    # 'clang' | ''/'default'
    conan_profile_host = "android"
    conan_profile_host = "default"
    conan_profile_host = "clang_pr"

    conan_profile_build = "default"
    conan_profile_build = "clang_pr"

    conan_profile_host_path = join(conan_data_path, conan_profile_host)
    conan_profile_build_path = join(conan_data_path, conan_profile_build)

    if conan_profile_host == "default" or conan_profile_host == "":
        conan_profile_host_path = "default"
    if conan_profile_build == "default" or conan_profile_build == "":
        conan_profile_build_path = "default"

    #! need to pulll this from conanfile
    #! not currently used, modify the function directly
    conan_package_name = f"sockets_p"
    conan_version = f"0.1"
    conan_user = f"xzijoq"
    conan_channel = f"testing"

# -------------------CONAN DATA ENDS----------------------
# endregion

#region ---------------CMAKE DATA--------------------
# -- Required vaiables-- set to "" if not in use
if Fatal == True:

    build_dir_path = join(cfd, "build")
    
    # cmake_c_compiler = ""
    cmake_c_compiler = "clang"

    # cmake_cxx_compiler = "gcc"
    # cmake_cxx_compiler = "Visual Studio"
    # cmake_cxx_compiler = ""
    cmake_cxx_compiler = "clang++"
    
    #! debug type not working (no effect) fix

    # cmake_build_type = "Debug" ##wont work not
    cmake_build_type = "Release"

    # cmake_generator = "\"Ninja Multi-Config\""  # notWorking
    # cmake_generator = "vs...fix"
    cmake_generator = ""
    cmake_generator = "Ninja"
    # leave empty if using conan
    cmake_toolchain_path = ""


# endregion

# region ---------------------------TARGET DATA----

if TargetApp:
    # target_name="c_app"
    #! need to pull this and full path from cmake

    target_src_dir = "c_app"
    target = "c_app"

# endregion

# region --------Test DATA---

if EnableTest == True:
    TestSourceDir = "tests/"
    Tests = ['g_tst']
if RecordTime:
    rTime = []
    pass


# endregion



# region ---------------MAIN STARTS HERE----------------------


def MainFunc():

    global rTime
    fTime = time.time()
    fun.p("executing")
    goRun_check()
    if 'clean' in args.goRun:
        clean()
        return
    if 'c' in args.goRun:
        conan_run()
    if 'r' in args.goRun:
        cmake_run()
    if 'b' in args.goRun:
        cmake_build()
    if 'x' in args.goRun:
        run_target()
    if 't' in args.goRun:
        run_test()
    if 'cr' in args.goRun:
        conan_create()
    if 'ct' in args.goRun:
        conan_test()
    if 'gc' in args.goRun:
        godot_copy()
    if 'gx' in args.goRun:
        godot_run()
    goRun_check()

    if RecordTime:
        for i in rTime:
            p_time(i)

    pr_time(str(time.time()-fTime))
    msg.p("Script END")
    return 0
# endregion

# region conan_func

def conan_run():
    fTime = time.time()
    fun.p("executing")

    if not conan:
        wrn.p("Conan is DEFINED FALSE")
        return False
    if not isdir(conan_dir_path):
        err.p(f"Conan Directory Not Found: {conan_dir_path}", Fatal)
    if conan_profile_host_path != "default" and not isfile(conan_profile_host_path):
        err.p(f"NOT FOUND {conan_profile_host_path}", Fatal)

    if conan_profile_build_path != "default" and not isfile(conan_profile_build_path):
        err.p(f"NOT FOUND {conan_profile_build_path}", Fatal)

    msg.p(
        f"Deleting ConanBuildDir: {conan_build_dir_path}"+c_del(conan_build_dir_path))
    c_del(join(cfd, "conan.lock"))
    c_del(join(cfd, "conanbuildinfo.txt"))
    c_del(join(cfd, "conaninfo.txt"))
    c_del(join(cfd, "graph_info.json"))
    c_del(join(cfd, "CMakeUserPresets.json"))

    #            -of={conan_build_dir_path} \
    # $ REAL DEAL
    conan_r = f"conan install {conan_dir_path}\
             --build=missing \
             --profile:build={conan_profile_build_path} \
             --profile:host={conan_profile_host_path} "
    # $ ENd
    if (not {args.coa} == ""):
        conan_r += f" {args.coa}"

    c_run(conan_r, True)

    pr_time(str(time.time()-fTime))
    # conan test test_package sockets_p/0.1

def conan_create():
    fTime = time.time()
    fun.p("Executing")
    # conan create . --user=xzijoq --channel=testing

    co_crt = f"conan create {conan_dir_path} --user=xzijoq --channel=testing"
    c_run(co_crt)
    pr_time(str(time.time()-fTime))
    pass

def conan_test():
    fTime = time.time()
    fun.p("Executing")

    # conan test test_package sockets_p/0.1@xzijoq/testing
    tf_path = join(cfd, "test_package")
    co_tst = f"conan test {tf_path} sockets_p/0.1@xzijoq/testing"
    c_run(co_tst)
    pr_time(str(time.time()-fTime))
    pass

# endregion

# region cmake_func

def cmake_run():
    fTime = time.time()

    fun.p("Executing")
    global cmake_toolchain_path
    if not isfile(join(cfd, "CMakeLists.txt")):
        err.p("CMakeLists.txt not found", Fatal)
    if (build_dir_path == ""):
        err.p("CmakeBuildDir cant be null specified", Fatal)

    msg.p(f"Deleting:  {build_dir_path}"+c_del(build_dir_path))

    # @ todo: currently specifying source directory is not supported
    cmake_command = f"cmake -S./ -B {build_dir_path}"

    if (not cmake_build_type == ""):
        cmake_command += f" -D CMAKE_BUILD_TYPE={cmake_build_type}"

    if (not cmake_c_compiler == ""):
        cmake_command += f" -D CMAKE_C_COMPILER={cmake_c_compiler}"

    if (not cmake_cxx_compiler == ""):
        cmake_command += f" -D CMAKE_CXX_COMPILER={cmake_cxx_compiler}"

    if (not cmake_generator == ""):
        cmake_command += f" -G {cmake_generator}"

    if conan and cmake_toolchain_path == "":
        cmake_toolchain_path = join(
            conan_build_dir_path, "generators", "conan_toolchain.cmake")

    if (not cmake_toolchain_path == ""):
        # cmake_command += f" -D CMAKE_TOOLCHAIN_FILE={cmake_toolchain_path}"
        cmake_command += f" {cfd} --preset release "

    if (TargetApp == True):
        cmake_command += f" -D TargetApp=True "
    if (godot == True):
        cmake_command += f" -D Godot=True "
    if (EnableTest == True):
        cmake_command += f" -D EnableTest=True "

    if (not {args.cma} == ""):
        cmake_command += f" {args.cma}"

    cmake_command += f" -DCMAKE_POLICY_DEFAULT_CMP0091=NEW "
    cmake_command += f" --warn-uninitialized "

    c_run(cmake_command, Fatal)

    pr_time(str(time.time()-fTime))
    pass



  
def cmake_build():
    fTime = time.time()
    fun.p("executing")
    if not os.path.isdir(build_dir_path):
        nfy.p("Try calling the script with f/r or full/run")
        err.p("Build Directory not found", Fatal)
    config_r = f" --config {cmake_build_type}"
    cmake_build_command = f"cmake --build {build_dir_path} {config_r} -j8 "

    if not (args.cba == ""):
        cmake_build_command += f"{args.cba}"

    c_run(cmake_build_command, Fatal)

    nfy.p("NOT! Copyting compile_commands.json")
    # & CopyCopileCommands
    # if isfile(join(build_dir_path, "compile_commands.json")):
    #    if isfile(join(cfd, "compile_commands.json")):
    #        os.remove(join(cfd, "compile_commands.json"))
    #    else:
    #        wrn.p(
    #            f"can'nt find compile_commands.json in cfd trying new copy: {cfd}")
    #    wrn.p(" Copyting compile_commands.json")
    #    shutil.copy(
    #        join(build_dir_path, "compile_commands.json"),
    #        join(cfd, "compile_commands.json"),
    #    )
    # else:
    #    wrn.p(
    #        f"ERR: can'nt find compile_commands.json in build dir: {build_dir_path}")
    pr_time(str(time.time()-fTime))
 
# endregion


# region def run_target():
def run_target():
    fTime = time.time()
    fun.p("Executing")
    if TargetApp == False:
        wrn.p("TargetApp is DEFINED FALSE")
        return
    global target

    if args.target != "":
        target = args.target

    if target == "":
        wrn.p("NO TARGET TO RUN")
        return False

    target_path = join(build_dir_path, target_src_dir, target)
    if (cmake_generator == "\"Ninja Multi-Config\""):
        target_path = join(build_dir_path, target_src_dir,
                           cmake_build_type, target)

    if not isfile(target_path):
        err.p(f"NotFound {target_path}")
        return

    c_run(f"{target_path} {args.exa}")

    pr_time(str(time.time()-fTime))
# endregion


# region def run_test():
def run_test():
    fTime = time.time()
    fun.p("executing")
    if EnableTest == False:
        wrn.p("EnableTest is FALSE")
        return
    # $CAN USE CTEST FOR ITS FEATURES
    # test=f"ctest  --output-on-failure --verbose --gtest_color=yes"
    test_dir = join(build_dir_path, TestSourceDir)

    if (cmake_generator == "\"Ninja Multi-Config\""):
        test_dir = join(build_dir_path, TestSourceDir,
                        cmake_build_type)

    for i in Tests:
        test_path = join(test_dir, i)
        test_command = test_path
        if args.tea != "":
            test_command += args.tea
        c_run(test_command)
    pr_time(str(time.time()-fTime))
# endregion


# region def clean():
def clean():
    fTime = time.time()
    fun.p("Executing")

    wrn.p(c_del(join(cfd, "conan.lock")))
    wrn.p(c_del(join(cfd, "conanbuildinfo.txt")))
    wrn.p(c_del(join(cfd, "conaninfo.txt")))
    wrn.p(c_del(join(cfd, "graph_info.json")))
    wrn.p(c_del(join(cfd, "CMakeUserPresets.json")))

    wrn.p(c_del(join(cfd, ".vscode")))
    wrn.p(c_del(join(cfd, ".cache")))
    wrn.p(c_del(build_dir_path))
    wrn.p(c_del(conan_build_dir_path))

    wrn.p(c_del(join(cfd, "test_package","build")))

    if godot:
        for i in godot_lib:
            target_lib = join(godot_dir, i)
            if isfile(target_lib):
                os.remove(target_lib)
    pr_time(str(time.time()-fTime))
# endregion


# region c_run


def c_run(command, isFatal=False, is_silent=False):
    fTime = time.time()
    # err.p(command)
    result = subprocess.run(f"{command}", shell=True)
    nfy.p(f"----------\n{result}\n")
    nfy.p(f"done")
    short_command = (
        command[:15] + '..                     ') if len(command) > 15 else command
    pr_time(f"{short_command} "+str(time.time()-fTime))

    if not result.returncode == 0:
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        err.p(f"Failed : {result.returncode}", Fatal, frame)
    pass
# endregion


# region c_Del
def c_del(what, isFatal=False):
    if os.path.isfile(what):
        os.remove(what)
        return ""
    elif os.path.isdir(what):
        shutil.rmtree(what)
        return ""
    else:
        if (isFatal):
            callerframerecord = inspect.stack()[1]
            frame = callerframerecord[0]
            err.p(f"Can't Delete {what} not found", Fatal, frame)
            # err.p(f"Can't Delete {what} not found", Fatal)
        return f"Can't Delete {what} not found"
    pass
# endregion


# ---------------HELPER---------------------------
# region parser
# -------------------PARSER STARTS HERE----------------------
parser = argparse.ArgumentParser()
parser.add_argument("goRun", help="Get Some Help", nargs='+', default="b")
parser.add_argument("-t", "--target", help="target to run", default="")
parser.add_argument("-exa", help="executable args ", default="")
parser.add_argument("-cma", help="cmake args ENTER IN QUOTES", default="")
parser.add_argument(
    "-cba", help="cmake build args ENTER IN QUOTES", default="")
parser.add_argument("-coa", help="conan args ENTER IN QUOTES", default="")
parser.add_argument("-tea", help="TEST args ENTER IN QUOTES", default="")
parser.add_argument("-sc", "--scene", help="GodotScene", default="")
args = parser.parse_args()


# -------------------PARSER ENDS HERE----------------------
# -------------------PARSER_Helper starts----------------------
def goRun_check():
    fTime = time.time()
    fun.p("executing")
    validLis = ['c', 'r', 'b', 'x', 't', 'ct', 'cr', 'gc', 'gx', 'clean']
    isValid = False
    # isValid = goRun_has('clean') or goRun_has('c') or goRun_has(
    #    'r') or goRun_has('b') or goRun_has('x') or goRun_has('gc') or goRun_has('gx')
    for i in args.goRun:
        if i in validLis:
            isValid = True
        else:
            wrn.p(f"Unused argument: {i}")
        pass
    if not isValid:
        msg.p(f"Valid Arguments to Run:\n\
            c:     conan_run()\n\
            r:     cmake_run()\n\
            b:     cmake_build()\n\
            x:     run_target()\n\
            t:     run_tests()\n\
            ct:    conan_test()\n\
            cr:    conan_create()\n\
            gc:    godot_copy()\n\
            gx:    godot_run()\n\
            clean: clean() and return\n\
            --help: for help\n\
        ")
        err.p("Please Enter a Valid Command", Fatal)

    if (('c' in args.goRun) and conan == False):
        wrn.p(f"Coan is set to false, yet coanan_run() was requested via arg 'c'\n")

    if (('gc' in args.goRun) and godot == False):
        wrn.p("Godot is set to false, yet godot_copy() was requested via arg 'gc' \n")
    if (('gx' in args.goRun) and godot == False):
        wrn.p("Godot is set to false, yet  godot_run() was requested via arg 'gx'\n")

    if (('gx' in args.goRun) and not 'gc' in args.goRun):
        err.p("Will Try To Run Godot Scene Without Copying THe LIBRARY !!!! \n")

    if (('x' in args.goRun) and TargetApp == False):
        wrn.p("TargetApp is set to false, yet run_target() was requested via arg 'x'\n")
    if (('t' in args.goRun) and EnableTest == False):
        wrn.p("EnableTest is set to false, yet run_test) was requested via arg 't'\n")
    pr_time(str(time.time()-fTime))

# ------------------HELPER END------------
# endregion

# region ---------------- PRINT FUNCS ---------------
class p_hpr:
    style = f"\033[30;101;3;4mErr:"
    label = f"default"
    layout = "word"
    end_word = f"\033[00m"
    end_line = f"\033[00m"

    def __init__(self, layout="word", style=f"\033[30;101m", label=f"default"):
        self.style = style
        self.label = label
        self.layout = layout
        if self.layout == "word":
            self.end_line = ""
        else:
            self.end_word = ""

    def p(self, what: str, isFatal: bool = False, frame1: str = 0):
        if frame1 != 0:
            frame = frame1
        else:
            callerframerecord = inspect.stack()[1]
            frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        print(f"{self.style}{self.label}{self.end_word} {what}\
        func:{info.function}\
        line:{info.lineno}\
        {self.end_line}")

        if isFatal:
            quit()


err = p_hpr("line", f"\033[30;101m", "error: ")
wrn = p_hpr("word", f"\033[30;103m", "warn : ")
nfy = p_hpr("word", f"\033[35;40m",  "notice: ")
fun = p_hpr("word", f"\033[93;34m",  "func-> ")
msg = p_hpr("word", f"\033[30;102m", "msg: ")





def pr_time(what):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    if RecordTime:
        global rTime
        rTime.append("   "+what+f"  {info.function}")
    if not ShowTime:
        return
    print(f"\033[30;10;1m       Time: {what}\
        func:{info.function}\
        line:{info.lineno}\
        \033[00m")


def p_time(what):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[1;10;1m {what}\
        \033[00m")

# ---------------- PRINT FUNCS END---------------
# endregion


# region -------------------GODOT DATA STARTS----------------------

if godot:
    godot_scene = "Display.tscn"
    godot_executable = f"/home/babayaga/godot/godotb"
    godot_project_path = join(cfd, "godot/tanks")
    godot_relative_src_path = f"godot/src_godot"
    godot_lib = ["libgui.so"]
    godot_dir = join(godot_project_path, "bin")
    godot_scene_dir = join(godot_project_path, "scenes")
# -------------------Godot DATA ENDS----------------------
# endregion

# region godot_func

def godot_copy():
    fTime = time.time()
    fun.p("executing")
    if godot == False:
       # wrn.p("Godot is set to False")
        return False

    if not isdir(godot_project_path):
        err.p("Godot ProjectDir NOT FOUND:\n{godot_project_path} ", Fatal)

    if not isfile(join(godot_project_path, "project.godot")):
        err.p(
            "MostLikely Invalid godot project Directoey:\n{godot_project_path}")
    if not isdir(godot_dir):
        err.p("Godot Library folder  not found:\n{godot_dir}", Fatal)

    if not isdir(godot_dir):
        err.p(f"{godot_dir} Not FOund", Fatal)

    for i in godot_lib:
        target_lib = join(godot_dir, i)
        src_lib = join(build_dir_path, godot_relative_src_path, i)

        if not isfile(src_lib):
            err.p(f"Godot Built Library Not FOund:\n{src_lib} ", Fatal)
        if isfile(target_lib):
            msg.p(f"removing {target_lib}:")
            os.remove(target_lib)
        else:
            wrn.p(f"{target_lib} not fouind")
        msg.p(f"copying {src_lib} --> {target_lib}")
        ts = shutil.copy(src_lib, target_lib)
    pr_time(str(time.time()-fTime))
  
def godot_run():
    fTime = time.time()
    fun.p("executing")
    if godot == False:
        # wrn.p("Godot is set to False")
        return False

    global godot_scene
    if not args.scene == "":
        godot_scene = args.scene
    if not str(godot_scene).endswith(".tscn"):
        godot_scene = godot_scene + ".tscn"

    os.chdir(godot_project_path)
    scene_path = join(godot_scene_dir, godot_scene)
    if not isfile(godot_executable):
        err.p("Godot Executable not found at {godot_executable}")
        return False
    if not isdir(godot_scene_dir):
        err.p(f"Does Not Exist {godot_scene_dir}  ")
        return False
    if not isfile(scene_path):
        err.p(f"Does Not Exist:--- {godot_scene} --AT \n {scene_path} ")
        return False

    runs = f"{godot_executable} -d {scene_path}"
    result = subprocess.run(f"{runs}", shell=True)
    nfy.p(f"{result}")

    pr_time(str(time.time()-fTime))
   

# endregion


MainFunc()
# scons platform=android android_arch=arm64v8 generate_bindings=yes -j8

# todo change functions to colorama and make a class out of em
