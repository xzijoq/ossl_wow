# -================GOD ENDS HERE===============================
# --TODO ENABLE EAST CROSS SCRIPTING
# - TODO TRY EMSCRIPTIN

#- TODO create CONAN PACKAGE NAME and version for conan_create and conan_test
import os
import subprocess
import sys
import argparse
import shutil
import time

from os.path import join
from os.path import isdir
from os.path import isfile
import inspect
from inspect import currentframe, getframeinfo

conan = True
TargetApp = True
EnableTest = True
godot = False
RecordTime = False
ShowTime = False
# ---------DEFS DONT ALTER-------------
cwd = os.getcwd()
cfd = os.path.dirname(os.path.realpath(__file__))
Fatal = True
# --------------END DEFS----------------------


# -------------------CONAN DATA---------------------------

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
    conan_package_name=f"sockets_p"
    conan_version=f"0.1"
    conan_user=f"xzijoq"
    conan_channel=f"testing"
    
# -------------------CONAN DATA ENDS----------------------

# ---------------- CMAKE DATA START ---------------
# -- Required vaiables-- set to "" if not in use
if Fatal == True:

    build_dir_path = join(cfd, "build")

    # not required!! not currently used
    cmake_compiler = "clang++"
    cmake_c_compiler = "clang"
    #cmake_compiler = "Visual Studio"

    #! debug type not working fix
    cmake_build_type = "Debug"
    cmake_build_type = "Release"

    cmake_generator = "vs...fix"
    cmake_generator = "\"Ninja Multi-Config\""  # notWorking
    cmake_generator = "Ninja"

    # leave empty if using conan
    cmake_toolchain_path = ""

# ----------------CMAKE DATA ENDS HERE-------------------

# ---------------------------TARGET

if TargetApp:
    # target_name="c_app"
    #! need to pull this and full path from cmake
    target = "c_app"
    target_src_dir = "c_app"


# -- ------------------------END TARGET

# --------Test---

if EnableTest == True:
    TestSourceDir = "tests/"
    Tests = ['g_tst']

# ----EndTest------

# -------------------GODOT DATA STARTS----------------------

if godot:
    godot_scene = "Display.tscn"
    godot_executable = f"/home/babayaga/godot/godotb"
    godot_project_path = join(cfd, "godot/tanks")
    godot_relative_src_path = f"godot/src_godot"
    godot_lib = ["libgui.so"]
    godot_dir = join(godot_project_path, "bin")
    godot_scene_dir = join(godot_project_path, "scenes")
# -------------------Godot DATA ENDS----------------------


if RecordTime:
    rTime = []
    pass


# ---------------MAIN STARTS HERE----------------------


def MainFunc():

    global rTime
    fTime = time.time()
    p_fnc("executing")
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
    p_mwg("Script END")
    return 0


def conan_run():
    fTime = time.time()
    p_fnc("executing")
    if not conan:
        p_wrn("Conan is DEFINED FALSE")
        return False
    if not isdir(conan_dir_path):
        p_err(f"Conan Directory Not Found: {conan_dir_path}", Fatal)
    if conan_profile_host_path != "default" and not isfile(conan_profile_host_path):
        p_err(f"NOT FOUND {conan_profile_host_path}", Fatal)

    if conan_profile_build_path != "default" and not isfile(conan_profile_build_path):
        p_err(f"NOT FOUND {conan_profile_build_path}", Fatal)

    p_msg(
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
             --profile:host={conan_profile_host_path}"
    # $ ENd
    if (not {args.coa} == ""):
        conan_r += f" {args.coa}"

    c_run(conan_r, True)

    pr_time(str(time.time()-fTime))
    # conan test test_package sockets_p/0.1


def cmake_run():
    fTime = time.time()
    p_fnc("Executing")
    global cmake_toolchain_path
    if not isfile(join(cfd, "CMakeLists.txt")):
        p_err("CMakeLists.txt not found", Fatal)
    if (build_dir_path == ""):
        p_err("CmakeBuildDir cant be null specified", Fatal)

    p_msg(f"Deleting:  {build_dir_path}"+c_del(build_dir_path))

    # @ todo: currently specifying source directory is not supported
    cmake_command = f"cmake -S./ -B {build_dir_path}"

    if (not cmake_build_type == ""):
        cmake_command += f" -D CMAKE_BUILD_TYPE={cmake_build_type}"

    if (not cmake_compiler == ""):
        cmake_command += f" -D CMAKE_CXX_COMPILER={cmake_compiler}"

    if (not cmake_generator == ""):
        pass
        cmake_command += f" -G {cmake_generator}"

    if conan and cmake_toolchain_path == "":
        cmake_toolchain_path = join(
            conan_build_dir_path, "generators", "conan_toolchain.cmake")

    if (not cmake_toolchain_path == ""):
        #cmake_command += f" -D CMAKE_TOOLCHAIN_FILE={cmake_toolchain_path}"
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

    c_run(cmake_command, True)

    pr_time(str(time.time()-fTime))
    pass


def cmake_build():
    fTime = time.time()
    p_fnc("executing")
    if not os.path.isdir(build_dir_path):
        p_nfy("Try calling the script with f/r or full/run")
        p_err("Build Directory not found", Fatal)
    config_r = f" --config {cmake_build_type}"
    cmake_build_command = f"cmake --build {build_dir_path} {config_r} -j8 "

    if not (args.cba == ""):
        cmake_build_command += f"{args.cba}"

    c_run(cmake_build_command)

    p_wrn("NOT! Copyting compile_commands.json")
    # & CopyCopileCommands
    #if isfile(join(build_dir_path, "compile_commands.json")):
    #    if isfile(join(cfd, "compile_commands.json")):
    #        os.remove(join(cfd, "compile_commands.json"))
    #    else:
    #        p_wrn(
    #            f"can'nt find compile_commands.json in cfd trying new copy: {cfd}")
    #    p_wrn(" Copyting compile_commands.json")
    #    shutil.copy(
    #        join(build_dir_path, "compile_commands.json"),
    #        join(cfd, "compile_commands.json"),
    #    )
    #else:
    #    p_wrn(
    #        f"ERR: can'nt find compile_commands.json in build dir: {build_dir_path}")
    pr_time(str(time.time()-fTime))


def run_target():
    fTime = time.time()
    p_fnc("Executing")
    if TargetApp == False:
        p_wrn("TargetApp is DEFINED FALSE")
        return
    global target

    if args.target != "":
        target = args.target

    if target == "":
        p_wrn("NO TARGET TO RUN")
        return False

    target_path = join(build_dir_path, target_src_dir, target)
    if (cmake_generator == "\"Ninja Multi-Config\""):
        target_path = join(build_dir_path, target_src_dir,
                           cmake_build_type, target)

    if not isfile(target_path):
        p_err(f"NotFound {target_path}")
        return

    c_run(f"{target_path} {args.exa}")

    pr_time(str(time.time()-fTime))


def run_test():
    fTime = time.time()
    p_fnc("executing")
    if EnableTest == False:
        p_wrn("EnableTest is FALSE")
        return
    # $CAN USE CTEST FOR ITS FEATURES
    #test=f"ctest  --output-on-failure --verbose --gtest_color=yes"
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


def clean():
    fTime = time.time()
    p_fnc("Executing")

    p_wrn(c_del(join(cfd, "conan.lock")))
    p_wrn(c_del(join(cfd, "conanbuildinfo.txt")))
    p_wrn(c_del(join(cfd, "conaninfo.txt")))
    p_wrn(c_del(join(cfd, "graph_info.json")))
    p_wrn(c_del(join(cfd, "CMakeUserPresets.json")))

    p_wrn(c_del(join(cfd, ".vscode")))
    p_wrn(c_del(join(cfd, ".cache")))
    p_wrn(c_del(build_dir_path))
    p_wrn(c_del(conan_build_dir_path))

    if godot:
        for i in godot_lib:
            target_lib = join(godot_dir, i)
            if isfile(target_lib):
                os.remove(target_lib)
    pr_time(str(time.time()-fTime))


def conan_create():
    fTime = time.time()
    p_fnc("Executing")
    #conan create . --user=xzijoq --channel=testing

    co_crt=f"conan create {conan_dir_path} --user=xzijoq --channel=testing"
    c_run(co_crt)
    pr_time(str(time.time()-fTime))
    pass
def conan_test():
    fTime = time.time()
    p_fnc("Executing")

    #conan test test_package sockets_p/0.1@xzijoq/testing
    tf_path=join(cfd,"test_package")
    co_tst=f"conan test {tf_path} sockets_p/0.1@xzijoq/testing"
    c_run(co_tst)
    pr_time(str(time.time()-fTime))
    pass

def godot_copy():
    fTime = time.time()
    p_fnc("executing")
    if godot == False:
       # p_wrn("Godot is set to False")
        return False

    if not isdir(godot_project_path):
        p_err("Godot ProjectDir NOT FOUND:\n{godot_project_path} ", Fatal)

    if not isfile(join(godot_project_path, "project.godot")):
        p_err(
            "MostLikely Invalid godot project Directoey:\n{godot_project_path}")
    if not isdir(godot_dir):
        p_err("Godot Library folder  not found:\n{godot_dir}", Fatal)

    if not isdir(godot_dir):
        p_err(f"{godot_dir} Not FOund", Fatal)

    for i in godot_lib:
        target_lib = join(godot_dir, i)
        src_lib = join(build_dir_path, godot_relative_src_path, i)

        if not isfile(src_lib):
            p_err(f"Godot Built Library Not FOund:\n{src_lib} ", Fatal)
        if isfile(target_lib):
            p_msg(f"removing {target_lib}:")
            os.remove(target_lib)
        else:
            p_wrn(f"{target_lib} not fouind")
        p_msg(f"copying {src_lib} --> {target_lib}")
        ts = shutil.copy(src_lib, target_lib)
    pr_time(str(time.time()-fTime))





def godot_run():
    fTime = time.time()
    p_fnc("executing")
    if godot == False:
        #p_wrn("Godot is set to False")
        return False

    global godot_scene
    if not args.scene == "":
        godot_scene = args.scene
    if not str(godot_scene).endswith(".tscn"):
        godot_scene = godot_scene + ".tscn"

    os.chdir(godot_project_path)
    scene_path = join(godot_scene_dir, godot_scene)
    if not isfile(godot_executable):
        p_err("Godot Executable not found at {godot_executable}")
        return False
    if not isdir(godot_scene_dir):
        p_err(f"Does Not Exist {godot_scene_dir}  ")
        return False
    if not isfile(scene_path):
        p_err(f"Does Not Exist:--- {godot_scene} --AT \n {scene_path} ")
        return False

    runs = f"{godot_executable} -d {scene_path}"
    result = subprocess.run(f"{runs}", shell=True)
    p_nfy(f"{result}")

    pr_time(str(time.time()-fTime))


# ---------------HELPER---------------------------


def c_run(command, isFatal=False):
    fTime = time.time()
    # p_err(command)
    result = subprocess.run(f"{command}", shell=True)
    p_nfy(f"----------\n{result}\n")
    p_nfy(f"done")
    short_command = (
        command[:15] + '..                     ') if len(command) > 15 else data
    pr_time(f"{short_command} "+str(time.time()-fTime))

    if not result.returncode == 0:
        p_err(f"Failed : {result.returncode}", isFatal)
    pass


def c_del(what, isFatal=False):
    if os.path.isfile(what):
        os.remove(what)
        return ""
    elif os.path.isdir(what):
        shutil.rmtree(what)
        return ""
    else:
        if (isFatal):
            p_err(f"Can't Delete {what} not found", Fatal)
        return f"Can't Delete {what} not found"
    pass


def goRun_check():
    fTime = time.time()
    p_fnc("executing")
    validLis = ['c', 'r', 'b', 'x', 't','ct','cr', 'gc', 'gx', 'clean']
    isValid = False
    # isValid = goRun_has('clean') or goRun_has('c') or goRun_has(
    #    'r') or goRun_has('b') or goRun_has('x') or goRun_has('gc') or goRun_has('gx')
    for i in args.goRun:
        if i in validLis:
            isValid = True
        else:
            p_wrn(f"Unused argument: {i}")
        pass
    if not isValid:
        p_msg(f"Valid Arguments to Run:\n\
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
        p_err("Please Enter a Valid Command", Fatal)

    if (('c' in args.goRun) and conan == False):
        p_wrn(f"Coan is set to false, yet coanan_run() was requested via arg 'c'\n")

    if (('gc' in args.goRun) and godot == False):
        p_wrn("Godot is set to false, yet godot_copy() was requested via arg 'gc' \n")
    if (('gx' in args.goRun) and godot == False):
        p_wrn("Godot is set to false, yet  godot_run() was requested via arg 'gx'\n")

    if (('gx' in args.goRun) and not 'gc' in args.goRun):
        p_err("Will Try To Run Godot Scene Without Copying THe LIBRARY !!!! \n")

    if (('x' in args.goRun) and TargetApp == False):
        p_wrn("TargetApp is set to false, yet run_target() was requested via arg 'x'\n")
    if (('t' in args.goRun) and EnableTest == False):
        p_wrn("EnableTest is set to false, yet run_test) was requested via arg 't'\n")
    pr_time(str(time.time()-fTime))

# ------------------HELPER END------------


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

# ---------------- PRINT FUNCS ---------------


def p_msg(what):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[30;102mMsg:\033[00m {what}\
        func:{info.function}\
        line:{info.lineno}\
        ")


def p_wrn(what):
    if (what == ""):
        return
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[30;103;3;4mWarn: {what}\
        func:{info.function}\
        line:{info.lineno}\
        \033[00m")


def p_mwg(what):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[30;106;3;4m {what}\
        func:{info.function}\
        line:{info.lineno}\
        \033[00m")


def p_nfy(what):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[30;44mNotice:\033[00m {what}\
        func:{info.function}\
        line:{info.lineno}")


def p_fnc(what):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[30;45m{what}\033[00m\
        func:{info.function}\
        line:{info.lineno}")


def p_err(what, isFatal=False):
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print(f"\033[30;101;3;4mErr: {what}\
        line:{info.lineno}\
        func:{info.function}\
        \033[00m")
    if isFatal:
        quit()


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


MainFunc()
# scons platform=android android_arch=arm64v8 generate_bindings=yes -j8
