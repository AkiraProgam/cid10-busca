#!/usr/bin/env python3
"""
Gera index.html a partir de template.html e data/CID-10-SUBCATEGORIAS.CSV.
Uso: python build.py
"""
import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
CSV_PATH = RAIZ / "data" / "CID-10-SUBCATEGORIAS.CSV"
TEMPLATE = RAIZ / "template.html"
SAIDA = RAIZ / "index.html"
MARCADOR = "/*__DADOS__*/[]"


def ler_texto(caminho):
    bruto = caminho.read_bytes()
    try:
        return bruto.decode("utf-8-sig")
    except UnicodeDecodeError:
        return bruto.decode("cp1252")  # o DATASUS costuma usar Windows-1252


def formatar_codigo(cod):
    cod = cod.strip().upper()
    if "." not in cod and len(cod) > 3:   # A000 -> A00.0
        cod = cod[:3] + "." + cod[3:]
    return cod


def ler_cid(caminho):
    linhas = [l for l in ler_texto(caminho).splitlines() if l.strip()]
    sep = ";" if linhas[0].count(";") >= linhas[0].count(",") else ","
    leitor = csv.reader(linhas, delimiter=sep)
    cab = [c.strip().upper() for c in next(leitor)]
    try:
        i_cod = cab.index("SUBCAT")
        i_desc = cab.index("DESCRICAO")
    except ValueError:
        sys.exit(f"Colunas SUBCAT/DESCRICAO não encontradas. Cabeçalho lido: {cab}")

    vistos, saida = set(), []
    for linha in leitor:
        if len(linha) <= max(i_cod, i_desc):
            continue
        cod = formatar_codigo(linha[i_cod])
        desc = " ".join(linha[i_desc].split())
        if not cod or not desc or cod in vistos:
            continue
        vistos.add(cod)
        saida.append({"codigo": cod, "descricao": desc})
    return saida


def main():
    if not CSV_PATH.exists():
        sys.exit(f"Arquivo não encontrado: {CSV_PATH}")
    dados = ler_cid(CSV_PATH)
    js = json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    modelo = TEMPLATE.read_text(encoding="utf-8")
    if MARCADOR not in modelo:
        sys.exit("Marcador de dados não encontrado no template.html")
    SAIDA.write_text(modelo.replace(MARCADOR, js), encoding="utf-8")
    print(f"OK: {len(dados)} registros -> {SAIDA.name}")


if __name__ == "__main__":
    main()