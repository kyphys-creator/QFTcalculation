# Tools for interactive (cell-structured) scripts

These tools convert batch scripts into files that run both ways:
- in batch (`wolframscript -file`, `python`);
- cell by cell, as a Mathematica notebook (`~/hep/bin/wopen`) or in the VS Code interactive window (`# %%` cells).

They also check that the conversion changed nothing.  They were used for all 25 scripts of `models/phi3/Src`
(2026-10-10).  See the environment record (`environment/environment.pdf`, Sec. 6, 「対話的な実行」).

| file | what it does |
|---|---|
| `wlcells.py` | `.wl`: header comment → Title/Text cells; `(* ---------- x ---------- *)` → Section cells; Inspect cells `If[$Notebooks, ...]` after given statements; trailing cleanup → Cleanup section. `add_sections()` inserts separators where a script has none. |
| `pycells.py` | `.py`: docstring → markdown cell; `# %%` (+ markdown) before given lines; `HERE` falls back to the cwd; matplotlib Agg only in batch (`INTERACTIVE = "ipykernel" in sys.modules`). |
| `nbcheck.wl` | Opens a converted `.wl` in a hidden front end, evaluates its code cells with `$Notebooks = True`, reports each Inspect cell and exports their output to a PDF. |
| `pycheck.py` | Runs a converted `.py` cell by cell in an IPython kernel, as VS Code does, and reports the outputs (stream, value, image) and errors. |
| `samefiles.sh` | Compares regenerated outputs with the committed ones: CSV and text byte by byte, PDF by its text. A PDF that differs only in its timestamp is restored from git. |

## Convert

The code lines are never retyped.  Only markup is inserted, so a mistake cannot change a result.

```python
import sys; sys.path.insert(0, "<repo>/environment/interactive")
from wlcells import convert, add_sections
add_sections("x_feyncalc.wl", [("diags$ = InsertFields", "(a) diagrams and amplitude")])   # only if needed
convert("x_feyncalc.wl",
        {'Print["(a) number of diagrams': ("the diagrams",
            'Show[#, ImageSize -> 560] & /@ Render[Paint[diags$, ColumnsXRows -> {4, 3}, Numbering -> Simple, DisplayFunction -> Identity]]')},
        "x_feyncalc.wl", title="Step (n): ...")
from pycells import convert as pyconvert
pyconvert("x_numeric.py", "Step (n): ...", [("def tree", "## Helper functions"), ("rows = []", "## Comparison")])
```

- An Inspect cell is inserted after the statement that contains the anchor: at the next blank line or section start.
- For scripts whose last lines are not a cleanup (FeynRules), pass `cleanup_markers=()`.
- Diagrams need `Render`. A bare `Paint` shows only labels, and `SheetHeader -> None` breaks `Render`.
- Separate kernels: the FeynRules, FormCalc (unpatched FeynArts) and NLOCT scripts must not share a kernel with
  FeynCalc. Say so in the How-to-run cell.

## Check

Before converting, note which committed outputs the script writes. Then:

```bash
wolframscript -file x_feyncalc.wl                 # batch: the (a)/(b)/(c) check lines must not change
environment/interactive/samefiles.sh models/phi3/Src/results/x.csv models/phi3/figs/x.pdf
NBFILE=$PWD/x_feyncalc.wl NBPDF=/tmp/x_nb.pdf wolframscript -code 'ToExpression[ReadString["<repo>/environment/interactive/nbcheck.wl"]]'
~/miniforge3/envs/qft/bin/python <repo>/environment/interactive/pycheck.py x_numeric.py    # from the script's folder
```

What to look out for:
- Run `nbcheck.wl` with `-code` and `ReadString`, as above. With `-file`, `$InputFileName` points to nbcheck.wl
  instead of being empty, as it is in a notebook.
- The front end splits a package file into cells only at cell markers and double blank lines, not at single
  blank lines. A cell can therefore hold several statements, for example `Get["FeynCalc`"]` together with the
  source-directory line. This is why `nbcheck.wl` evaluates whole cells, with `$InputFileName` replaced by the
  file path.
- Messages in the `nbcheck.wl` output come from the script, for example Package-X's `CompiledFunction::cfn`,
  which also appear in batch runs. Compare them with a batch run.
- Generated model files (FeynRules/NLOCT) carry date lines. After regenerating, require that
  `git diff -U0 -- generated | grep -v -i date` shows nothing else, then `git checkout -- generated`.
- In zsh, an unquoted `$var` holding several paths is passed as one argument. Pass the file names explicitly.
