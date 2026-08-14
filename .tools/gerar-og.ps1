#Requires -Version 5.1
# Gera os cards Open Graph (1200x630) de cada pagina em og/{slug}.png.
#
# Rodar quando publicar case novo:  powershell -File .tools\gerar-og.ps1
# Ao publicar um case, adicione a linha dele em $paginas.
#
# Cores: azul = operacao/fiscal/logistica · verde = dinheiro/dados · roxo = pessoal.

Add-Type -AssemblyName System.Drawing
$outDir = Join-Path $PSScriptRoot "..\og"

$paginas = @(
    @{ slug="home";                  cat="LABORATÓRIO OPERACIONAL"; title="Automações reais. Problemas reais.";                              accent="#3B82F6" },
    @{ slug="lucratividade";         cat="FINANCEIRO · DADOS";      title="Lucro real por venda, calculado sozinho 3× por dia";              accent="#22C55E" },
    @{ slug="hub-de-dados";          cat="INFRA · DADOS";           title="R$ 17 mil por ano a menos no ERP, com um banco de R$ 30/mês";     accent="#22C55E" },
    @{ slug="tray-frete";            cat="LOGÍSTICA";               title="Testar preço de frete dependia da fila de outra empresa";         accent="#3B82F6" },
    @{ slug="romaneio-scanner";      cat="LOGÍSTICA";               title="O romaneio da coleta virou bipe de celular";                      accent="#3B82F6" },
    @{ slug="crm-reativacao";        cat="VENDAS";                  title="Nenhum relatório mostra o cliente que está esfriando";            accent="#3B82F6" },
    @{ slug="crm-por-dentro";        cat="VENDAS";                  title="CRM por dentro";                                                  accent="#3B82F6" },
    @{ slug="atendimento-insights";  cat="ATENDIMENTO";             title="Análise diária do WhatsApp Business com IA";                      accent="#3B82F6" },
    @{ slug="motoboy-impressao";     cat="OPERAÇÃO";                title="Do pagamento à entrega em 10 minutos, sem clique humano";         accent="#3B82F6" },
    @{ slug="fretes-consolidado";    cat="FINANCEIRO";              title="Custo real de frete por NF";                                      accent="#3B82F6" },
    @{ slug="ml-cancelamentos";      cat="OPERAÇÃO";                title="Cancelamento pago no ML chega no Slack em 5 min";                 accent="#3B82F6" },
    @{ slug="nf-auto-correcao";      cat="OPERAÇÃO · FISCAL";       title="Correção automática de NF rejeitada (quando a IA diz que não dá)"; accent="#3B82F6" },
    @{ slug="nf-emissao-automatica"; cat="OPERAÇÃO · FISCAL";       title="Bot fazendo a atividade principal de uma pessoa";                 accent="#3B82F6" },
    @{ slug="gym-app";               cat="PESSOAL · PWA";           title="Tracker de academia no navegador, configurado por uma foto";      accent="#A78BFA" }
)

function HexToColor($hex) {
    $hex = $hex.TrimStart('#')
    [System.Drawing.Color]::FromArgb(255,
        [Convert]::ToInt32($hex.Substring(0,2),16),
        [Convert]::ToInt32($hex.Substring(2,2),16),
        [Convert]::ToInt32($hex.Substring(4,2),16))
}

$bg    = HexToColor "0B0F14"
$text  = HexToColor "F3F4F6"
$muted = HexToColor "9CA3AF"

foreach ($p in $paginas) {
    $accent = HexToColor $p.accent
    $bmp = New-Object System.Drawing.Bitmap(1200, 630)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear($bg)

    $accBrush = New-Object System.Drawing.SolidBrush($accent)
    $g.FillRectangle($accBrush, 0, 0, 1200, 8)      # faixa no topo
    $g.FillRectangle($accBrush, 80, 170, 6, 300)     # barra lateral (estilo callout)

    $fCat = New-Object System.Drawing.Font("Consolas", 20, [System.Drawing.FontStyle]::Bold)
    $g.DrawString($p.cat, $fCat, $accBrush, 120, 180)

    $fTitle = New-Object System.Drawing.Font("Segoe UI", 44, [System.Drawing.FontStyle]::Bold)
    $tBrush = New-Object System.Drawing.SolidBrush($text)
    $g.DrawString($p.title, $fTitle, $tBrush, (New-Object System.Drawing.RectangleF(118, 230, 1000, 260)))

    $fLogo = New-Object System.Drawing.Font("Consolas", 24, [System.Drawing.FontStyle]::Bold)
    $g.DrawString("nak.api.br", $fLogo, $tBrush, 80, 545)
    $fTag = New-Object System.Drawing.Font("Segoe UI", 16)
    $mBrush = New-Object System.Drawing.SolidBrush($muted)
    $g.DrawString("laboratório operacional · dor real, solução real", $fTag, $mBrush, 330, 552)

    $liveBrush = New-Object System.Drawing.SolidBrush((HexToColor "22C55E"))
    $g.FillEllipse($liveBrush, 62, 557, 10, 10)

    $bmp.Save((Join-Path $outDir ($p.slug + ".png")), [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    Write-Output ("ok  " + $p.slug)
}
Write-Output "--- fim ---"
