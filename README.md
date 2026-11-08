# Busca CID-10

Página offline para buscar códigos da CID-10 (base DATASUS) e copiar o código, a descrição ou ambos.

## Usar
Baixe `index.html` e dê duplo clique. Funciona no Chrome, Edge ou Firefox, sem internet.

## Atualizar a base
1. Coloque o arquivo em `data/CID-10-SUBCATEGORIAS.CSV`.
2. Rode `python build.py` (Python 3, sem bibliotecas extras).
3. Publique o `index.html` gerado.

## Publicar no GitHub Pages (opcional, para acessar por link)
Settings → Pages → Deploy from a branch → `main` / `(root)`.