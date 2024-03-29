"""
These commands, and sub-commands, are used by pre-commit.
"""
import pathlib

from ptscripts import Context
from ptscripts import command_group

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

cgroup = command_group(
    name="pre-commit",
    help="Pre-Commit Related Commands",
    description=__doc__,
)


@cgroup.command(
    name="cleanup-duplicates",
)
def cleanup_duplicates(ctx: Context):
    """
    Clean duplicate entries.
    """
    community_modules_path = REPO_ROOT / "community-ext-modules.txt"
    core_ext_modules_path = REPO_ROOT / "core-ext-modules.txt"
    core_modules_path = REPO_ROOT / "core-modules.txt"
    delete_modules_path = REPO_ROOT / "delete-modules.txt"
    test_support_path = REPO_ROOT / "test-support.txt"
    community_modules = community_modules_path.read_text().splitlines()
    initial_community_modules = community_modules[:]
    core_ext_modules = core_ext_modules_path.read_text().splitlines()
    initial_core_ext_modules = core_ext_modules[:]
    core_modules = core_modules_path.read_text().splitlines()
    initial_core_modules = core_modules[:]
    delete_modules = delete_modules_path.read_text().splitlines()
    initial_delete_modules = delete_modules[:]
    test_support_modules = test_support_path.read_text().splitlines()
    initial_test_support_modules = test_support_modules[:]

    for mod in delete_modules:
        for modlist in (core_modules, core_ext_modules, community_modules, test_support_modules):
            if mod in modlist:
                modlist.remove(mod)
    for mod in test_support_modules:
        for modlist in (core_modules, core_ext_modules, community_modules):
            if mod in modlist:
                modlist.remove(mod)
    for mod in community_modules:
        for modlist in (core_ext_modules, core_modules):
            if mod in modlist:
                modlist.remove(mod)
    for mod in core_ext_modules:
        if mod in test_support_modules:
            core_modules.remove(mod)

    delete_modules = sorted({m for m in delete_modules if m}, key=str.casefold)
    community_modules = sorted({m for m in community_modules if m}, key=str.casefold)
    core_ext_modules = sorted({m for m in core_ext_modules if m}, key=str.casefold)
    core_modules = sorted({m for m in core_modules if m}, key=str.casefold)
    test_support_modules = sorted({m for m in test_support_modules if m}, key=str.casefold)
    if delete_modules != initial_delete_modules:
        ctx.info(f"Writing updated {delete_modules_path} ...")
        delete_modules_path.write_text("\n".join(delete_modules) + "\n")
    if community_modules != initial_community_modules:
        ctx.info(f"Writing updated {community_modules_path} ...")
        community_modules_path.write_text("\n".join(community_modules) + "\n")
    if core_ext_modules != initial_core_ext_modules:
        ctx.info(f"Writing updated {core_ext_modules_path} ...")
        core_ext_modules_path.write_text("\n".join(core_ext_modules) + "\n")
    if core_modules != initial_core_modules:
        ctx.info(f"Writing updated {core_modules_path} ...")
        core_modules_path.write_text("\n".join(core_modules) + "\n")
    if test_support_modules != initial_test_support_modules:
        ctx.info(f"Writing updated {test_support_path} ...")
        test_support_path.write_text("\n".join(test_support_modules) + "\n")
