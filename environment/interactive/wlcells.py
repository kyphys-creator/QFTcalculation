"""Convert a batch Wolfram Language script into the cell-structured form used for interactive work
(environment record, Sec. 6; README.md in this folder).  The same file then runs with wolframscript (batch) and
cell by cell as a Mathematica notebook (~/hep/bin/wopen).

The code lines are kept verbatim.  Added:
  - the leading comment block -> a Title cell (its first line) and a Text cell (the rest), plus a "How to run" Text cell;
  - "(* ---------- title ---------- *)" separators -> Section cells; a "Setup" section before the first code line;
  - Inspect cells: {anchor_substring: (heading, code)}; the cell is inserted after the statement that contains the anchor
    (after the first line at the same or lower indentation that ends the statement, i.e. the next blank line);
  - the trailing cleanup lines (LToolsUnLoadLibrary / DeleteDirectory / CloseKernels at the end) -> a "Cleanup" section.
Usage (as a module):
  add_sections(path, [(anchor, title), ...])     # optional: separators for scripts that have none
  convert(path, {anchor: (heading, code)}, run_name, title=None, cleanup_markers=(...))
The file is rewritten in place; check the result with nbcheck.wl and the batch output with samefiles.sh.
"""
import re

SEP = re.compile(r"^\(\* -{3,} (.*?) -{3,} \*\)\s*$")


def text_cell(style, text):
    lines = [l.rstrip() for l in text.strip("\n").split("\n")]
    lines = [l.replace("(*", "( *").replace("*)", "* )") for l in lines]
    return [f"(* ::{style}:: *)"] + [f"(*{l}*)" for l in lines] + ["", ""]


def add_sections(path, seps):
    """Insert "(* ---------- title ---------- *)" before the line containing each anchor (each must occur once)."""
    s = open(path).read()
    for anchor, title in seps:
        assert s.count(anchor) == 1, (path, anchor)
        s = s.replace(anchor, f"(* ---------- {title} ---------- *)\n" + anchor)
    open(path, "w").write(s)


def convert(path, inspects, runname, title=None,
            cleanup_markers=("LToolsUnLoadLibrary[]", "DeleteDirectory[", "CloseKernels[")):
    """Rewrite path.  inspects: {anchor substring: (heading, Wolfram code)}; the Inspect cell goes after the statement
    containing the anchor (at the next blank line or section).  title replaces the first line of the header comment.
    Pass cleanup_markers=() when the trailing lines are not a cleanup (e.g. FeynRules scripts)."""
    src = open(path).read().split("\n")
    assert src[0].strip() == "(* ::Package:: *)", path
    # leading comment block
    i = 1
    while src[i].strip() == "":
        i += 1
    assert src[i].startswith("(*"), src[i]
    j = i
    while "*)" not in src[j]:
        j += 1
    block = "\n".join(src[i:j + 1])
    block = block[2:]
    block = block[:block.rfind("*)")]
    blines = block.strip("\n").split("\n")
    first = blines[0].strip()
    if title is None:
        title = first.split(" -- ", 1)[-1] if " -- " in first else first
    rest = "\n".join(l[3:] if l.startswith("   ") else l for l in blines[1:]).strip("\n")
    body = src[j + 1:]
    # trailing cleanup lines
    k = len(body)
    while k > 0 and (body[k - 1].strip() == "" or (cleanup_markers and any(m in body[k - 1] for m in cleanup_markers))):
        k -= 1
    tail = [l for l in body[k:] if l.strip()]
    body = body[:k]
    out = ["(* ::Package:: *)", ""]
    out += text_cell("Title", title)
    if rest:
        out += text_cell("Text", rest)
    out += text_cell("Text", f"How to run.  Batch:  wolframscript -file {runname}.  Interactive:  ~/hep/bin/wopen {runname}, then "
                     "\"Run All Code\" or Shift+Return cell by cell; the cells under \"Inspect\" headings run only in the notebook "
                     "(If[$Notebooks, ...]) and show intermediate objects without changing anything.")
    started = False
    pending = []                     # inspect cells waiting for the end of the current statement
    used = set()
    for line in body:
        m = SEP.match(line)
        if m:
            for head, code in pending:          # a section starts: flush the inspect cells of the previous statement
                out += ["", ""] + text_cell("Subsubsection", "Inspect: " + head) + ["If[$Notebooks,"] + \
                       ["  " + c for c in code.strip("\n").split("\n")] + ["]", ""]
            pending = []
            out += [""] + text_cell("Section", m.group(1))
            started = True
            continue
        if not started and line.strip() and not line.strip().startswith("(*"):
            out += text_cell("Section", "Setup")
            started = True
        if line.strip() == "" and pending:
            for head, code in pending:
                out += ["", ""] + text_cell("Subsubsection", "Inspect: " + head) + ["If[$Notebooks,"] + \
                       ["  " + c for c in code.strip("\n").split("\n")] + ["]", ""]
            pending = []
        out.append(line)
        for a, (head, code) in inspects.items():
            if a not in used and a in line:
                pending.append((head, code))
                used.add(a)
    if pending:
        for head, code in pending:
            out += ["", ""] + text_cell("Subsubsection", "Inspect: " + head) + ["If[$Notebooks,"] + \
                   ["  " + c for c in code.strip("\n").split("\n")] + ["]", ""]
    missing = set(inspects) - used
    assert not missing, f"anchors not found: {missing}"
    if tail:
        out += ["", ""] + text_cell("Section", "Cleanup") + \
               text_cell("Text", "Skip this cell while you are still inspecting: it releases libraries and temporary files.")
        out += tail + [""]
    text = "\n".join(out)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    open(path, "w").write(text)
    return text
