(* Notebook-mode check of a cell-structured .wl: evaluates its code cells in order with $Notebooks = True
   ($InputFileName in the cell text is replaced by the file path, as a notebook has none), collects the Inspect
   outputs and exports them to a PDF.  All names end in NBC$ so that they do not collide with the script's symbols.
   Usage: NBFILE=/abs/path/x.wl NBPDF=/abs/path/out.pdf \
     wolframscript -code 'ToExpression[ReadString["<this folder>/nbcheck.wl"]]'
   (-code with ReadString keeps $InputFileName empty, as in a notebook; -file would set it to nbcheck.wl).
   The messages printed are those of the script; e.g. Package-X's CompiledFunction::cfn also appear in batch runs. *)
fileNBC$ = Environment["NBFILE"]; pdfNBC$ = Environment["NBPDF"];
UsingFrontEnd[
  nbNBC$ = NotebookOpen[fileNBC$, Visible -> False];
  txtNBC$[cellNBC$_] := First[FrontEndExecute[FrontEnd`ExportPacket[NotebookRead[cellNBC$], "InputText"]]];
  Print["cells: ", Tally[Map[CurrentValue[#, "CellStyleName"] &, Cells[nbNBC$]]]];
  outNBC$ = {}; countNBC$ = 0;
  Do[Module[{codeNBC$ = txtNBC$[cNBC$], rNBC$},
     rNBC$ = Block[{$Notebooks = True}, ToExpression[StringReplace[codeNBC$, "$InputFileName" -> ToString[fileNBC$, InputForm]]]];
     If[StringStartsQ[StringTrim[codeNBC$], "If[$Notebooks"],
       countNBC$++;
       Print["inspect -> ", Head[rNBC$], If[rNBC$ === $Failed || rNBC$ === Null, "   <- NO OUTPUT", ""]];
       outNBC$ = Join[outNBC$, {Cell[StringTake[codeNBC$, UpTo[90]], "Input"], ExpressionCell[rNBC$, "Output"]}]]],
    {cNBC$, Cells[nbNBC$, CellStyle -> "Code"]}];
  Print["inspect cells: ", countNBC$];
  nb2NBC$ = CreateDocument[outNBC$, Visible -> False, WindowSize -> {900, Automatic}];
  Export[pdfNBC$, nb2NBC$]; NotebookClose[nb2NBC$]; NotebookClose[nbNBC$, Interactive -> False]];
