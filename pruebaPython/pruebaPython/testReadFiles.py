import os, glob, re

def sortNumberNames(file) -> int:
	found = re.search(r"\d+", file)
	return int(found.group()) if found else 0

listaFiles: list[str] = os.listdir("./secuenciasUsuario")
listaJsonNames: list[str] = [j for j in listaFiles if j.endswith(".json")]
listaJsonNames = sorted(listaJsonNames, key=str.lower)
listaJsonNames = sorted(listaJsonNames, key=sortNumberNames)
print(listaJsonNames)