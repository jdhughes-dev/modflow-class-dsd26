"""Set a top-level assignment in a notebook's code cells, for shortened CI runs.

    python set_notebook_value.py NOTEBOOK NAME VALUE

replaces the one line ``NAME = ...`` at the start of a line in the code cells
with ``NAME = VALUE``, and fails unless there is exactly one such line.
"""

import re
import sys

import nbformat

path, name, value = sys.argv[1:4]
nb = nbformat.read(path, as_version=4)
pattern = re.compile(rf"(?m)^{re.escape(name)} = .*$")
hits = 0
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.source, n = pattern.subn(f"{name} = {value}", cell.source)
        hits += n
if hits != 1:
    sys.exit(f"expected one '{name} = ' line in {path}, found {hits}")
nbformat.write(nb, path)
print(f"{path}: {name} = {value}")
