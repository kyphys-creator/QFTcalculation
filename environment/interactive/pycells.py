"""Convert a batch Python script into the # %%-cell form used for interactive work (environment record, Sec. 6;
README.md in this folder).  The same file then runs with python (batch) and cell by cell in the VS Code interactive window.

The code lines are kept verbatim except for three mechanical changes:
  - HERE = os.path.dirname(os.path.abspath(__file__))  ->  try/except falling back to the working directory;
  - matplotlib.use("Agg")  ->  used only outside an IPython kernel (INTERACTIVE = "ipykernel" in sys.modules);
  - "import sys" is added if missing, and INTERACTIVE is defined after the imports if there is no HERE line.
Added: the module docstring -> a markdown cell (title "Step (n): ..."), and cells: [(anchor_substring, markdown or None)];
a "# %%" marker (with an optional markdown cell before it) is inserted before the first line containing the anchor.
"""
import re


def convert(path, title, cells, extra_note=""):
    src = open(path).read()
    m = re.match(r'"""(.*?)"""\n', src, flags=re.S)
    assert m, path
    doc, body = m.group(1), src[m.end():]
    lines = [l.rstrip() for l in doc.strip("\n").split("\n")]
    md = ["# %% [markdown]", f"# # {title}", "#"] + ["# " + l if l else "#" for l in lines]
    md += ["#", "# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and \"Run Cell\" (# %%) one by one;",
           "# a bare expression at the end of a cell shows its value, and figures are drawn inline."]
    if extra_note:
        md += ["# " + extra_note]
    body = body.replace("HERE = os.path.dirname(os.path.abspath(__file__))",
                        "try:\n    HERE = os.path.dirname(os.path.abspath(__file__))\n"
                        "except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder\n"
                        "    HERE = os.getcwd()\nINTERACTIVE = \"ipykernel\" in sys.modules")
    body = body.replace('matplotlib.use("Agg")', 'if not INTERACTIVE:\n    matplotlib.use("Agg")')
    if not re.search(r"^import sys$", body, flags=re.M):
        body = re.sub(r"^(import os)$", r"\1\nimport sys", body, count=1, flags=re.M)
    assert re.search(r"^import sys$", body, flags=re.M), "add import sys by hand"
    if "INTERACTIVE = " not in body:              # no HERE line: define INTERACTIVE after the leading imports
        bl = body.split("\n")
        last = max(i for i, l in enumerate(bl[:60]) if l.startswith(("import ", "from ")))
        bl.insert(last + 1, 'INTERACTIVE = "ipykernel" in sys.modules')
        body = "\n".join(bl)
    out = md + ["", "# %%"]
    blines = body.split("\n")
    pending = list(cells)
    for line in blines:
        for k, (a, note) in enumerate(pending):
            if a in line:
                if note:
                    out += ["", "# %% [markdown]"] + ["# " + l for l in note.split("\n")]
                out += ["", "# %%"]
                pending.pop(k)
                break
        out.append(line)
    assert not pending, f"anchors not found: {[a for a, _ in pending]}"
    text = "\n".join(out)
    text = re.sub(r"\n# %%\n\n+", "\n# %%\n", text)
    text = re.sub(r"\n{3,}(# %%)", r"\n\n\n\1", text)
    open(path, "w").write(text)
    return text
