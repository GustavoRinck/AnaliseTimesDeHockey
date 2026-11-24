import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

print("Iniciando o Web Scraping...")
url = "https://www.scrapethissite.com/pages/forms/"
visitadas = set()
fila = [url]
times = []

while fila and len(visitadas) < 24:
    atual = fila.pop(0)
    if atual in visitadas:
        continue

    try:
        r = requests.get(atual, timeout=15)
        r.raise_for_status()
        visitadas.add(atual)
        soup = BeautifulSoup(r.text, "html.parser")

        print(f"Processando página {len(visitadas)}: {atual}")

        linhas = soup.select("tr.team")
        for linha in linhas:
            nome_time = linha.select_one("td.name").text.strip()
            ano = linha.select_one("td.year").text.strip()
            vitorias = linha.select_one("td.wins").text.strip()
            derrotas = linha.select_one("td.losses").text.strip()
            derrotas_prorroga = linha.select_one("td.ot-losses").text.strip()
            percentual_vitorias = linha.select_one("td.pct").text.strip()
            gols_pro = linha.select_one("td.gf").text.strip()
            gols_contra = linha.select_one("td.ga").text.strip()

            times.append({
                "time_nome": nome_time,
                "ano": int(ano) if ano.isdigit() else None,
                "vitorias": int(vitorias) if vitorias.isdigit() else 0,
                "derrotas": int(derrotas) if derrotas.isdigit() else 0,
                "derrotas_prorroga": int(derrotas_prorroga) if derrotas_prorroga.isdigit() else 0,
                "percentual_vitorias": float(percentual_vitorias) if percentual_vitorias else 0.0,
                "gols_pro": int(gols_pro) if gols_pro.isdigit() else 0,
                "gols_contra": int(gols_contra) if gols_contra.isdigit() else 0,
            })

        proxima = soup.select_one("ul.pagination li a[aria-label='Next']")
        if proxima:
            link = urljoin(atual, proxima["href"])
            if link not in visitadas and link not in fila:
                fila.append(link)

        time.sleep(1)
    except Exception as e:
        print(f"Erro ao processar {atual}: {e}")

if times:
    df = pd.DataFrame(times)
    df = df.drop_duplicates()
    df.to_csv("times_hockey.csv", index=False)
    print("Dados coletados e salvos com sucesso em 'times_hockey.csv'!")
else:
    print("Nenhum dado pôde ser coletado.")
