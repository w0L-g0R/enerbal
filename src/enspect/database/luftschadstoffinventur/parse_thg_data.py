# %%

import itertools
from pathlib import Path

import openpyxl
import pandas as pd
import PyPDF2
import xlwings as xw

IDX = pd.IndexSlice


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


pages = 5
p = Path("THG_2010.pdf")
pdfFileObj = open(p, "rb")
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages

c = [
    "THG-Emissionen des Burgenlands in 1.000 t CO",
    "THG-Emissionen Kärntens in 1.000 t CO",
    "THG-Emissionen Niederösterreichs in 1.000 t CO",
    "THG-Emissionen Oberösterreichs in 1.000 t CO",
    "THG-Emissionen Salzburgs in 1.000 t CO",
    "THG-Emissionen der Steiermark in 1.000 t CO",
    "THG-Emissionen Tirols in 1.000 t CO",
    "THG-Emissionen Vorarlbergs in 1.000 t CO",
    "THG-Emissionen Wiens in 1.000 t CO",
]

emittents = [
    "Energie",
    "Kleinverbraucher",
    "Industrie",
    "Verkehr",
    "Landwirtschaft",
    "Sonstige",
    "Gesamt",
]

# pageObj = pdfReader.getPage(0)
# mytext = pageObj.extractText()
# print('mytext: ', mytext)
# # print('mytext: ', mytext.find("THG"))
# mytext = mytext.split("\n")
# # print('mytext: ', mytext)


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


df_index = [
    1990.0,
    1991.0,
    1992.0,
    1993.0,
    1994.0,
    1995.0,
    1996.0,
    1997.0,
    1998.0,
    1999.0,
    2000.0,
    2001.0,
    2002.0,
    2003.0,
    2004.0,
    2005.0,
    2006.0,
]

wb = xw.Book()
ws = wb.sheets["Tabelle1"]
dfs = []

for x in range(pages):

    pageObj = pdfReader.getPage(x)
    mytext = pageObj.extractText()
    mytext = mytext.split("\n")
    # print('mytext: ', mytext)

    idx_1 = mytext.index(c[0])
    name_1 = mytext[idx_1]
    print("idx_1: ", idx_1)

    if x == 4:
        idx_2 = -1
        name_2 = None
    else:
        idx_2 = mytext.index(c[1])
        print("idx_2: ", idx_2)
        name_2 = mytext[idx_2]
    # except BaseException:
    # idx_2 = -1
    # name_2 = "None"

    bl_1 = mytext[idx_1:idx_2]
    bl_2 = mytext[idx_2:]

    bl_1 = [x.replace(".", "") for x in bl_1 if is_float(x)]
    bl_1 = [float(x) for x in bl_1 if is_float(x)]

    bl_2 = [x.replace(".", "") for x in bl_2 if is_float(x)]
    bl_2 = [float(x) for x in bl_2 if is_float(x)]

    for bl, name in zip([bl_1, bl_2], [name_1, name_2]):

        if name is None:
            break

        df = pd.DataFrame(
            # index=emittents,
            # columns=k
            data=list(chunks(bl, len(df_index))),
        )

        df.columns = df.iloc[0, :].astype(int)
        df = df.iloc[1:, :]
        df.index = emittents
        # name = next(iter(c))
        # print('name: ', name)

        name = name.split("Emissionen ")[1].split("in")[0]
        df = df.T
        print()
        # print('next(iter(c)): ', next(iter(c)))
        # print('df: ', df.T)

        df.columns = pd.MultiIndex.from_product(iterables=[[name], df.columns])
        print(df)
        dfs.append(df)

        print()
    del c[:2]

df = pd.concat(dfs, axis=1)
df_total = df.loc[IDX[:], IDX[:, "Gesamt"]]

# print('df: ', df)
ws.range("A1").value = df_total

# %%
