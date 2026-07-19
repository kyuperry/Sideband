import os

import sh
from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import current_directory, shprint


class OpusFileRecipe(Recipe):
    version = "0.12"
    url = "https://downloads.xiph.org/releases/opus/opusfile-{version}.tar.gz"

    # Opusfile requires both libraries.
    depends = ["libogg", "libopus"]

    built_libraries = {
        "libopusfile.so": ".libs",
    }

    def build_arch(self, arch):
        with current_directory(self.get_build_dir(arch.arch)):
            env = self.get_recipe_env(arch)

            ogg_recipe = Recipe.get_recipe("libogg", self.ctx)
            opus_recipe = Recipe.get_recipe("libopus", self.ctx)

            ogg_dir = ogg_recipe.get_build_dir(arch.arch)
            opus_dir = opus_recipe.get_build_dir(arch.arch)
            libs_dir = self.ctx.get_libs_dir(arch.arch)

            # Opusfile's configure script supports these variables as an
            # alternative to pkg-config, which cannot locate Android's
            # cross-compiled dependency files in this build environment.
            env["DEPS_CFLAGS"] = " ".join([
                f"-I{os.path.join(ogg_dir, 'include')}",
                f"-I{os.path.join(opus_dir, 'include')}",
            ])

            env["DEPS_LIBS"] = " ".join([
                f"-L{libs_dir}",
                "-logg",
                "-lopus",
            ])

            flags = [
                "--host=" + arch.command_prefix,
                "--disable-http",
                "--disable-examples",
                "--disable-doc",
                "--disable-largefile",
            ]

            configure = sh.Command("./configure")
            shprint(configure, *flags, _env=env)
            shprint(sh.make, _env=env)


recipe = OpusFileRecipe()
