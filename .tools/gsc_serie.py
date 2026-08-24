# -*- coding: utf-8 -*-
"""
Serie diaria do Search Console + recortes por janela. Complementa o gsc.py
(que mostra o estado atual) mostrando a EVOLUCAO — util pra separar efeito de
correcao tecnica de variacao normal.

  D:\\Claude\\cte_drive\\.venv\\Scripts\\python.exe .tools\\gsc_serie.py [dias]
"""
import sys
from datetime import date, timedelta

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from gsc import credenciais, desempenho, totais, bloco, linha_total  # noqa: E402

LAG = 3


def serie(creds, ini, fim):
    linhas = desempenho(creds, ini, fim, ["date"], 500)
    return {l["keys"][0]: l for l in linhas}


def main():
    dias = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    creds = credenciais()

    fim = date.today() - timedelta(days=LAG)
    ini = fim - timedelta(days=dias - 1)

    bloco(f"SERIE DIARIA — {ini} a {fim}")
    s = serie(creds, ini, fim)
    d = ini
    sem_impr = 0
    while d <= fim:
        k = d.isoformat()
        if k in s:
            l = s[k]
            barra = "#" * int(l["impressions"])
            print(
                f"  {k} {d.strftime('%a')} | impr {l['impressions']:>3.0f} | cliq {l['clicks']:>2.0f}"
                f" | pos {l['position']:>5.1f} | {barra}"
            )
        else:
            sem_impr += 1
            print(f"  {k} {d.strftime('%a')} | impr   0 |")
        d += timedelta(days=1)
    print(f"\n  dias sem nenhuma impressao: {sem_impr} de {dias}")

    # Janelas em torno da correcao do Googlebot (17/08/2026).
    FIX = date(2026, 8, 17)
    janelas = [
        ("pos-fix   ", FIX + timedelta(days=1), fim),
        ("bloqueio  ", date(2026, 8, 4), FIX),
        ("pre-bloqueio", date(2026, 7, 18), date(2026, 8, 3)),
    ]
    bloco("JANELAS (media diaria normaliza o tamanho diferente)")
    for nome, a, b in janelas:
        t = totais(desempenho(creds, a, b))
        n = (b - a).days + 1
        print(
            f"  {nome} {a} a {b} ({n:>2}d) | impr {t['impressions']:>4.0f}"
            f" ({t['impressions']/n:>4.1f}/dia) | cliq {t['clicks']:>3.0f} | pos {t['position']:>5.1f}"
        )

    # Detalhe do periodo pos-correcao.
    a, b = FIX + timedelta(days=1), fim
    bloco(f"POS-CORRECAO {a} a {b} — paginas")
    for l in desempenho(creds, a, b, ["page"], 30):
        print(
            f"  pos {l['position']:>6.1f} | impr {l['impressions']:>4.0f} | cliq {l['clicks']:>3.0f}"
            f" | {l['keys'][0]}"
        )

    bloco(f"POS-CORRECAO {a} a {b} — queries")
    linhas = desempenho(creds, a, b, ["query"], 50)
    if not linhas:
        print("  (nenhuma query com dado)")
    for l in linhas:
        print(
            f"  pos {l['position']:>6.1f} | impr {l['impressions']:>4.0f} | cliq {l['clicks']:>3.0f}"
            f" | {l['keys'][0]}"
        )

    bloco("DISPOSITIVO E APARENCIA (28d)")
    a28 = fim - timedelta(days=27)
    for dim in ("device", "searchAppearance"):
        print(f"  -- {dim} --")
        for l in desempenho(creds, a28, fim, [dim], 10):
            print(
                f"     {l['keys'][0]:<22} impr {l['impressions']:>4.0f} | cliq {l['clicks']:>3.0f}"
                f" | pos {l['position']:>5.1f}"
            )


if __name__ == "__main__":
    main()
