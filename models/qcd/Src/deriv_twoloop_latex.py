# %% [markdown]
# # Appendix check: the two-loop class tables of note.tex against the pipeline
#
# Research note models/qcd, derivations of the appendices (sympy).  Parses the two LaTeX tables tab:twoloopclass and tab:twoloopclassgh of
# ../ResearchNote/note.tex (app:rg 「図の組ごとの値と z_21、z~_21（式 (z2)）。」) and compares every b, s and pole entry
# with the class sums of the pipeline (results/twoloop_latex_ref.txt, written by deriv_twoloop_export.wl from results/twoloop_perdiag.m);
# also checks the sum (和), counterterm (対抗項) and z rows of the tables by adding the parsed entries.
# Reads ../ResearchNote/note.tex, results/twoloop_latex_ref.txt.  Writes nothing; run_deriv_check.sh saves the printed output as results/deriv_twoloop_latex.txt.
# Usage (from Src/): ~/miniforge3/envs/qft/bin/python deriv_twoloop_latex.py   (a few seconds)
#
# Batch: as in the usage line above.  Interactive: open in VS Code (qft interpreter) and "Run Cell" (# %%) one by one;
# a bare expression at the end of a cell shows its value, and figures are drawn inline.

# %%
import os
import sys
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:          # run cell by cell (VS Code interactive window): the working directory is the script's folder
    HERE = os.getcwd()
INTERACTIVE = "ipykernel" in sys.modules
eps = sp.Symbol('eps')
TR = standard_transformations + (implicit_multiplication_application,)


# %% [markdown]
# ## LaTeX helpers

# %%
def frac_to_py(t):
    # \frac{A}{B}, \frac{A}B, \frac AB, \frac{A}{B} with nested braces
    while '\\frac' in t:
        i = t.index('\\frac')
        j = i + 5
        args = []
        for _ in range(2):
            while t[j] == ' ':
                j += 1
            if t[j] == '{':
                depth, k = 1, j + 1
                while depth:
                    depth += {'{': 1, '}': -1}.get(t[k], 0)
                    k += 1
                args.append(t[j + 1:k - 1]); j = k
            else:
                args.append(t[j]); j += 1
        t = t[:i] + '((' + args[0] + ')/(' + args[1] + '))' + t[j:]
    return t


def cells_of(r):
    c = [x.strip() for x in r.split('&')]
    if len(c) == 4 and '\\multicolumn{2}' in c[1]:   # the (c) C_A row: b, s given in words (-1/2 times the C_F row)
        c = [c[0], 'MC', 'MC', c[2], c[3]]
    return c


def is_row(r):
    return r.count('&') == 4 or (r.count('&') == 3 and '\\multicolumn{2}' in r)


def tex2sym(t):
    t = t.strip().strip('$')
    t = frac_to_py(t)
    t = t.replace('\\epsilon', ' eps ').replace('^', '**').replace('{', '(').replace('}', ')')
    return parse_expr(t, transformations=TR, local_dict={'eps': eps})


# %% [markdown]
# ## The two tables of note.tex and the pipeline values

# %%
note = open(os.path.join(HERE, '..', 'ResearchNote', 'note.tex')).read()


def table_float(label):
    """the table float of note.tex that carries \\label{label}"""
    i = note.index('\\label{' + label + '}')
    return note[note.rindex('\\begin{table}', 0, i):note.index('\\end{table}', i)]


snip = table_float('tab:twoloopclass') + table_float('tab:twoloopclassgh')
tabs = re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}', snip, flags=re.S)
assert len(tabs) == 2
ref = [l.split('|') for l in open(os.path.join(HERE, 'results', 'twoloop_latex_ref.txt')).read().strip().split('\n')]
ref = {r[0]: [parse_expr(x, local_dict={'eps': eps}) for x in r[1:]] for r in ref}

ref['c_CF']          # inspect: b, s, eps^-2, eps^-1 of the C_F T_F n_f row (c) from the pipeline

# %% [markdown]
# ## Comparison

# %%
order = [['a_gc', 'c_se', 'b', 'd_tri', 'ef', 'a_q', 'q_tri', 'c_CA', 'c_CF', 'q_se'], ['g_gc', 'c_se_line', 'h', 'crossed', 'g_q']]
ok = True
for ti, tab in enumerate(tabs):
    rows = [r for r in tab.split('\\\\') if is_row(r)]
    cls, sums = [], []
    for r in rows[1:]:                       # skip the header
        cells = cells_of(r)
        name = cells[0].split('\n')[-1]
        if '\\midrule' in name:
            name = name.split('\\midrule')[-1].strip()
        p2, p1 = tex2sym(cells[3]), tex2sym(cells[4])
        if cells[1] == '' and cells[2] == '':
            sums.append((name, p2, p1))
        else:
            cls.append((name, cells, p2, p1))
    print(f'--- table {ti + 1}: {len(cls)} class rows, {len(sums)} sum rows')
    keys = order[ti] + (['scaleless'] if True else [])
    for k, (name, cells, p2, p1) in zip(keys, cls):
        if k == 'scaleless':
            good = cells[1] == '$0$' and cells[2] == '$0$' and p2 == 0 and p1 == 0
        elif k == 'c_CA':
            good0 = cells[1] == 'MC'
            rb, rs, r2, r1 = ref['c_CA']
            cb, cs, _, _ = ref['c_CF']
            good = good0 and sp.simplify(rb + cb / 2) == 0 and sp.simplify(rs + cs / 2) == 0 and sp.simplify(p2 - r2) == 0 and sp.simplify(p1 - r1) == 0
        else:
            b, s = tex2sym(cells[1]), tex2sym(cells[2])
            rb, rs, r2, r1 = ref[k]
            good = sp.simplify(b - rb) == 0 and sp.simplify(s - rs) == 0 and sp.simplify(p2 - r2) == 0 and sp.simplify(p1 - r1) == 0
        ok = ok and good
        print(f'{k:10s} {name[:30]:30s} b, s, poles = pipeline: {good}')
    # sum rows: per colour block, "和" = sum of the class rows of the block; "z" = 和 + 対抗項 (gluon) or 和 + 対抗項 (ghost, shown as -z)
    blocks = tab.split('\\multicolumn{5}{l}')[1:]
    for blk in blocks:
        brs = [r for r in blk.split('\\\\') if is_row(r)]
        vals = []
        for r in brs:
            c = cells_of(r)
            vals.append((c[0].split('\n')[-1], tex2sym(c[3]), tex2sym(c[4]), c[1] == '' and c[2] == ''))
        cl = [v for v in vals if not v[3]]
        sm = {v[0]: v for v in vals if v[3]}
        tot2, tot1 = sum(v[1] for v in cl), sum(v[2] for v in cl)
        head = blk.split('}')[0][:40]
        if '和' in sm:
            g = sm['和'][1] == tot2 and sm['和'][2] == tot1
            ok = ok and g
            print(f'   block {head}: 和 = sum of rows: {g}')
        zrow = [v for k2, v in sm.items() if 'z_{22}' in k2]
        if zrow:
            ct = sm.get('対抗項', (None, 0, 0))
            g = zrow[0][1] == tot2 + ct[1] and zrow[0][2] == tot1 + ct[2]
            ok = ok and g
            print(f'   block {head}: z row = 和 + 対抗項: {g}  ({zrow[0][1]}, {zrow[0][2]})')
print('ALL OK' if ok else 'SOME CHECK FAILED')
