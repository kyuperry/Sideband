# Android Bluetooth Low Energy
# -*- coding: utf-8 -*-

from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.toolchain import current_directory, info, shprint
import sh
import os
from os.path import abspath, join


class LXSTRecipe(PythonRecipe):
    name = "lxst_recipe"
    depends = ["python3", "setuptools", "android", "cffi"]
    call_hostpython_via_targetpython = False
    install_in_hostpython = True

    def prepare_build_dir(self, arch):
        build_dir = self.get_build_dir(arch)
        assert build_dir.endswith(self.name)
        shprint(sh.rm, "-rf", build_dir)
        shprint(sh.mkdir, build_dir)

        # GitHub Actions checks LXST out beside the Sideband directory.
        # From recipes/lxst, move up to the Actions workspace and use LXST.
        workspace = os.environ.get("GITHUB_WORKSPACE")

        if workspace:
            lxst_root = join(workspace, "LXST")
        else:
            lxst_root = abspath(
                join(self.get_recipe_dir(), "..", "..", "..", "LXST")
            )

        srcs = (
            join(lxst_root, "LXST"),
            join(lxst_root, "setup.py"),
            join(lxst_root, "README.md"),
        )

        for filename in srcs:
            print(f"Copy {filename} to {build_dir}")
            shprint(sh.cp, "-a", filename, build_dir)

    def postbuild_arch(self, arch):
        super(LXSTRecipe, self).postbuild_arch(arch)
        info("LXST native build completed")


recipe = LXSTRecipe()
