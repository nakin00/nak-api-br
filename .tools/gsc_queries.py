# -*- coding: utf-8 -*-
"""
Todas as queries que ja renderam impressao, desde uma data. Responde a pergunta
"o que o Google acha que este site e?" — que e diferente de "pra que ele quer
ranquear". Sem isso, a decisao de conteudo vira palpite.

  D:\\Claude\\cte_drive\\.venv\\Scripts\\python.exe .tools\\gsc_queries.py [dias]
"""
import sys
from datetime import date, timedelta

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from gsc import credenciais, desempenho, bloco  # noqa: E402

LAG = 3


def main():
    dias = int(sys.argv[1]) if len(sys.argv) > 1 else 180
    creds = credenciais()
    fim = date.today() - timedelta(days=LAG)
    ini = fim - timedelta(days=dias - 1)

    bloco(f"TODAS AS QUERIES — {ini} a {fim} ({dias}d)")
    linhas = desempenho(creds, ini, fim, ["query"], 200)
    if not linhas:
        print("  (nenhuma)")
    tot = 0
    for l in linhas:
        tot += l["impressions"]
        print(
            f"  pos {l['position']:>6.1f} | impr {l['impressions']:>4.0f} | cliq {l['clicks']:>3.0f}"
            f" | {l['keys'][0]}"
        )
    print(f"\n  {len(linhas)} queries distintas | {tot:.0f} impressoes com query conhecida")

    bloco(f"QUERY x PAGINA — {ini} a {fim}")
    for l in desempenho(creds, ini, fim, ["query", "page"], 200):
        pag = l["keys"][1].replace("https://nak.api.br", "") or "/"
        print(f"  pos {l['position']:>6.1f} | impr {l['impressions']:>4.0f} | {l['keys'][0]:<38} -> {pag}")

    bloco(f"TODAS AS PAGINAS — {ini} a {fim}")
    for l in desempenho(creds, ini, fim, ["page"], 100):
        pag = l["keys"][0].replace("https://nak.api.br", "") or "/"
        print(
            f"  pos {l['position']:>6.1f} | impr {l['impressions']:>4.0f} | cliq {l['clicks']:>3.0f} | {pag}"
        )


if __name__ == "__main__":
    main()
