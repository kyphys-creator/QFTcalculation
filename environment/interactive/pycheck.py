"""Run a # %%-celled script cell by cell in an IPython kernel (as the VS Code interactive window does) and report
each cell's outputs and errors.  Usage: python pycheck.py script.py  (run from the script's folder)."""
import re
import sys

from jupyter_client.manager import start_new_kernel

src = open(sys.argv[1]).read()
heads = re.findall(r"^# %%.*$", src, flags=re.M)
cells = re.split(r"^# %%.*$", src, flags=re.M)[1:]
km, kc = start_new_kernel(kernel_name="python3", cwd=".")
nerr = 0
try:
    for h, c in zip(heads, cells):
        if "[markdown]" in h or not c.strip():
            continue
        msg_id = kc.execute(c)
        kinds, err = [], None
        while True:
            m = kc.get_iopub_msg(timeout=3600)
            if m["parent_header"].get("msg_id") != msg_id:
                continue
            t = m["msg_type"]
            if t == "error":
                err = m["content"]["ename"] + ": " + m["content"]["evalue"][:200]
            elif t in ("display_data", "execute_result"):
                d = m["content"]["data"]
                kinds.append("image" if "image/png" in d else ("value: " + d.get("text/plain", "")[:60].replace("\n", " ")))
            elif t == "stream":
                if "stream" not in kinds:
                    kinds.append("stream")
            if t == "status" and m["content"]["execution_state"] == "idle":
                break
        nerr += err is not None
        first = c.strip().splitlines()[0][:45]
        print(f"  cell [{first}] -> {kinds or 'no output'}" + (f"   ERROR {err}" if err else ""))
finally:
    kc.stop_channels()
    km.shutdown_kernel()
print("errors:", nerr)
