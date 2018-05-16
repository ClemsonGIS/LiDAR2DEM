
from glob import glob
from zipfile import ZipFile
badFiles = []

for z in glob("*.zip"):
    ret = ZipFile(z).testzip()
    if ret is not None:
        print z
        print ret
        badFiles.append(z)
    else:
        print z
        print ret
        continue
print badFiles
