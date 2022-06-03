# cf-scraper
Scraper de codeforces

# Instalación

Crea un ambiente virtual con tu herramienta de preferencia (virtualenv, virtualenv-wrapper, etc) e instala las dependencias:

```bash
pip install -r requirements.txt
```

# Uso

Corre el script de la siguiente forma:

```bash
python scrap.py
```

# Como obtener un token RCPC

Para obtener un token RCPC, necesitas ver las cookies de codeforces.com en tu navegador, y buscar una llamada `RCPC`. Copia el valor asociado, esa sería tu cookie