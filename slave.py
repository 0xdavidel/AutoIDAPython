import contextlib

from idc import *
from idaapi import *
from idautils import *
import idc


@contextlib.contextmanager
def capture():
    import sys
    from cStringIO import StringIO

    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()


def run(runfile):
    with open(runfile) as f:
        d = dict(locals(), **globals())
        exec(compile(f.read(), os.path.abspath(runfile), "exec"), d, d)


def call_script(runfile):
    with capture() as out:
        run(runfile)
    return out[0], out[1]


autoWait()
script_path = idc.ARGV[1]

script_output, script_error = call_script(script_path)

open("script_output.txt", "w").write(script_output)
open("script_error.txt", "w").write(script_error)
idc.Exit(0)
