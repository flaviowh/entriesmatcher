from decimal import Decimal
import re
from bb_parser import BBParser

from pdf.methods import fix_value
from pdf.pdfreader import PDFreader 

PTRN = {
    "acc_id": r"conta corrente (\d+\-?\d?)",
    "start_kw": "saldo anterior",
    "end_kw": "s a l d o"
}


path = r"C:\Users\flavi\Desktop\demonstração\study\EXTRATO BB 01-2023 PDF (01-02-2023).pdf"
path2 = r"C:\Users\flavi\Desktop\demonstração\01-2022\EXTRATO - JANEIRO-22.pdf"
parser = BBParser(path2)
df = parser.to_dataframe()

   
values = []
parser.preprocess()
lines = parser.lines
for line in lines:
    value = parser.get_bb_value(line)
    if value:
        values.append(value)

print("max value: ", max(values))
print("min value: ", min(values))

sample_str = '12/01/2023 082099012870 transferência recebida 520.820.000.077.297100.000,00 c'
query =  100000
found = query in values
print("value from sample :",  parser.get_bb_value(parser.clean_line(sample_str)))
print(f"{query} in values : {found}")

print("sum of values from lines", sum(values))
print("sum of values from df", df.value.sum())

print(f"direct values {len(values)}, df values {df.shape[0]}")

missing = []
found = df.value.astype(float).tolist()
for value in values:
    if value not in found:
        missing.append(value)


print("values missing in df ", missing)
   
