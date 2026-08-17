# -*- coding: utf-8 -*-
"""
Leitura do Google Search Console do nak.api.br pela API, pra não depender de abrir o painel.

Uso (python do cte_drive, que já tem as libs):
  D:\\Claude\\cte_drive\\.venv\\Scripts\\python.exe .tools\\gsc.py auth     # uma vez, abre o navegador
  D:\\Claude\\cte_drive\\.venv\\Scripts\\python.exe .tools\\gsc.py          # relatório

O que imprime:
  - Desempenho 28d (impressões, cliques, CTR, posição média) e o mesmo dos 28d anteriores
  - Top queries e top páginas do período
  - Status dos sitemaps
  - Inspeção de URL de todas as URLs do sitemap (indexada ou não) — mesma coisa que
    clicar uma a uma no painel, que é o único jeito de ver o estado real (o relatório
    agregado tem ~7 dias de lag).

Token OAuth em .tools/gsc_token.json (fora do git). Cliente OAuth reusado do tiny_hub.
"""
import json
import re
import sys
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SITE = "sc-domain:nak.api.br"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
CLIENT_SECRET = Path(r"D:\Claude\tiny_hub\client_secret.json")

# O cliente OAuth reusado pertence a um projeto GCP de outra conta, onde a API do
# Search Console não está ligada e não dá pra ligar. O header x-goog-user-project
# manda a cobrança de cota/habilitação pra um projeto da conta kashinha, onde está.
PROJETO_COTA = "angelic-artwork-357614"

BASE = Path(__file__).parent
TOKEN = BASE / "gsc_token.json"
RAIZ = BASE.parent

API = "https://searchconsole.googleapis.com"
SITE_ENC = urllib.parse.quote(SITE, safe="")

# O GSC fecha o dia com 2-3 dias de atraso. Sem isso, os últimos dias entram zerados.
LAG = 3


def autorizar():
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    print("\nAbrindo o navegador. Faça login com a conta dona da propriedade do GSC")
    print("e autorize o acesso de LEITURA ao Search Console.\n")
    creds = flow.run_local_server(port=0, prompt="consent")
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
    print(f"Token salvo em {TOKEN}")
    return creds


def credenciais():
    if not TOKEN.exists():
        print("Sem token. Rode:  gsc.py auth")
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            TOKEN.write_text(creds.to_json(), encoding="utf-8")
        else:
            print("Token inválido. Rode:  gsc.py auth")
            sys.exit(1)
    return creds


def cabecalho(creds):
    return {
        "Authorization": f"Bearer {creds.token}",
        "x-goog-user-project": PROJETO_COTA,
        "Content-Type": "application/json",
    }


def get(creds, url):
    return requests.get(url, headers=cabecalho(creds), timeout=60)


def post(creds, url, body):
    return requests.post(url, headers=cabecalho(creds), json=body, timeout=60)


def erro(r, contexto):
    print(f"\nERRO {r.status_code} em {contexto}:")
    print(r.text[:1200])
    if "accessNotConfigured" in r.text or "has not been used" in r.text:
        print("\n>> Ative a 'Google Search Console API' no projeto GCP e rode de novo.")
    sys.exit(1)


def desempenho(creds, ini, fim, dimensoes=None, limite=25):
    body = {
        "startDate": ini.isoformat(),
        "endDate": fim.isoformat(),
        "rowLimit": limite,
        "dataState": "final",
    }
    if dimensoes:
        body["dimensions"] = dimensoes
    r = post(creds, f"{API}/webmasters/v3/sites/{SITE_ENC}/searchAnalytics/query", body)
    if r.status_code != 200:
        erro(r, "searchAnalytics")
    return r.json().get("rows", [])


def totais(linhas):
    if not linhas:
        return {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    return linhas[0]


def urls_do_sitemap():
    xml = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def inspecionar(creds, url):
    r = post(
        creds,
        f"{API}/v1/urlInspection/index:inspect",
        {"inspectionUrl": url, "siteUrl": SITE, "languageCode": "pt-BR"},
    )
    if r.status_code != 200:
        return {"erro": f"{r.status_code} {r.text[:200]}"}
    return r.json().get("inspectionResult", {})


def bloco(titulo):
    print(f"\n{'=' * 72}\n{titulo}\n{'=' * 72}")


def linha_total(rotulo, t):
    print(
        f"{rotulo:<22} impressões {t['impressions']:>6.0f} | cliques {t['clicks']:>4.0f} "
        f"| CTR {t['ctr'] * 100:>5.2f}% | posição {t['position']:>5.1f}"
    )


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "auth":
        autorizar()
        return

    creds = credenciais()

    fim = date.today() - timedelta(days=LAG)
    ini = fim - timedelta(days=27)
    fim_ant = ini - timedelta(days=1)
    ini_ant = fim_ant - timedelta(days=27)

    bloco(f"DESEMPENHO — {ini} a {fim} (28d) vs 28d anteriores")
    atual = totais(desempenho(creds, ini, fim))
    anterior = totais(desempenho(creds, ini_ant, fim_ant))
    linha_total(f"{ini} a {fim}", atual)
    linha_total(f"{ini_ant} a {fim_ant}", anterior)

    bloco("TOP QUERIES (28d)")
    linhas = desempenho(creds, ini, fim, ["query"], 30)
    if not linhas:
        print("(nenhuma query com dado)")
    for l in linhas:
        print(
            f"  pos {l['position']:>6.1f} | impr {l['impressions']:>5.0f} | cliq {l['clicks']:>3.0f}"
            f" | {l['keys'][0]}"
        )

    bloco("TOP PÁGINAS (28d)")
    for l in desempenho(creds, ini, fim, ["page"], 30):
        print(
            f"  pos {l['position']:>6.1f} | impr {l['impressions']:>5.0f} | cliq {l['clicks']:>3.0f}"
            f" | {l['keys'][0]}"
        )

    bloco("PAÍSES E DISPOSITIVOS (28d)")
    for l in desempenho(creds, ini, fim, ["country"], 10):
        print(f"  {l['keys'][0]:<6} impr {l['impressions']:>5.0f} | cliq {l['clicks']:>3.0f}")

    bloco("SITEMAPS")
    r = get(creds, f"{API}/webmasters/v3/sites/{SITE_ENC}/sitemaps")
    if r.status_code != 200:
        erro(r, "sitemaps")
    for s in r.json().get("sitemap", []):
        conteudo = ", ".join(
            f"{c['type']}: {c['submitted']} enviadas" for c in s.get("contents", [])
        )
        print(f"  {s['path']}")
        print(
            f"    último download: {s.get('lastDownloaded', '—')} | avisos: {s.get('warnings', 0)}"
            f" | erros: {s.get('errors', 0)} | {conteudo or 'sem conteúdo lido'}"
        )

    bloco("INSPEÇÃO DE URL — estado real de indexação")
    urls = urls_do_sitemap()
    indexadas = 0
    for u in urls:
        res = inspecionar(creds, u)
        if "erro" in res:
            print(f"  ?   {u}  ({res['erro']})")
            continue
        idx = res.get("indexStatusResult", {})
        veredito = idx.get("verdict", "?")
        estado = idx.get("coverageState", "?")
        if veredito == "PASS":
            indexadas += 1
        marca = "OK " if veredito == "PASS" else "NAO"
        print(f"  {marca} {u}")
        print(f"      {estado}")
        if idx.get("lastCrawlTime"):
            print(f"      último rastreio: {idx['lastCrawlTime'][:10]}")
    print(f"\n  >> {indexadas}/{len(urls)} URLs do sitemap indexadas")


if __name__ == "__main__":
    main()
