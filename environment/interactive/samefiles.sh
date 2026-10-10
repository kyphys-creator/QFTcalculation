#!/bin/bash
# samefiles.sh FILE... -- compare regenerated outputs with the committed versions (CSV/text byte by byte, PDF by its text);
# a PDF whose text is unchanged is restored from git (only its timestamp differed).
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 1   # paths are relative to the repository root
for f in "$@"; do
  case "$f" in
    *.pdf)
      if [ "$(pdftotext "$f" - 2>/dev/null | md5)" = "$(git show HEAD:"$f" | pdftotext - - 2>/dev/null | md5)" ]; then
        git checkout -- "$f"; echo "same  $f (text; restored)"
      else echo "DIFF  $f"; fi ;;
    *)
      if git diff --quiet -- "$f"; then echo "same  $f"; else echo "DIFF  $f"; fi ;;
  esac
done
