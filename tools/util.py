import pathlib

from ptscripts import Context
from ptscripts import command_group

from .precommit import REPO_ROOT

KINDMAP = {
    "modules": "module",
    "states": "state",
    "runners": "runner",
    "grains": "grain",
    "utils": "util",
    "netapi": "netapi",
    "auth": "auth",
    "beacons": "beacon",
    "returners": "returner",
    "cloud": "cloud",
    "engines": "engine",
    "sdb": "sdb",
    "renderers": "renderer",
    "pillar": "pillar",
    "proxy": "proxy",
    "executors": "executor",
    "log_handlers": "log_handler",
    "output": "output",
    "fileserver": "fileserver",
    "queues": "queue",
    "roster": "roster",
    "serializers": "serializer",
}


REVERSE_KINDMAP = {KINDMAP[k]: k for k in KINDMAP}
UNKNOWN = "UNKNOWN"


class Module:
    def __init__(self, path):
        self.path = pathlib.Path(path)

    @property
    def kind(self):
        parts = self.path.parts
        for part in parts:
            if part in KINDMAP:
                return KINDMAP[part]
        return UNKNOWN

    @property
    def ident(self):
        if self.is_test:
            return self.path.stem.split("test_")[-1]
        return self.path.stem

    @property
    def parts(self):
        return self.path.parts

    def __repr__(self):
        return f"<Module({self.path})>"

    def __str__(self):
        return str(self.path)

    @property
    def is_test(self):
        if self.path.parts[0] == "tests":
            return True
        return False


cgroup = command_group(
    name="util",
    help="Pre-Commit Related Commands",
    description=__doc__,
)


@cgroup.command(
    name="find-tests",
    arguments={
        "saltroot": {
            "help": "The root of a salt repository checkout.",
        },
        "modules": {
            "help": "A file containing a list of modules.",
        },
    },
)
def find_tests(ctx: Context, saltroot: pathlib.Path, modules: pathlib.Path):
    """
    Find test files for a list of modules.
    """
    saltroot = saltroot.absolute().resolve()
    modules = modules.absolute().resolve()
    if not saltroot.exists() or not modules.exists():
        ctx.error("Both saltroot and modules must exist")
        ctx.exit(1)
    if not saltroot.is_dir():
        ctx.error("saltroot should be a directory")
        ctx.exit(1)
    supporting = (REPO_ROOT / "test-support.txt").read_text().splitlines()
    modules = [Module(_) for _ in modules.read_text().splitlines()]
    tests = []
    testsdir = saltroot / "tests"
    for path in testsdir.rglob("*.py"):
        rpath = path.relative_to(saltroot)
        tmod = Module(rpath)
        tests.append(tmod)

    found = []
    module_paths = [a.path for a in modules]
    for mod in modules:
        if mod.is_test:
            continue
        for tmod in tests:
            if tmod.path in module_paths:
                continue
            if str(tmod.path) in supporting:
                continue
            if tmod.kind == mod.kind and (tmod.ident == mod.ident or mod.ident in tmod.parts):
                found.append(tmod)
    found = sorted(found, key=lambda x: x.path)
    for test in found:
        ctx.info(f"Found '{test.path}'")
