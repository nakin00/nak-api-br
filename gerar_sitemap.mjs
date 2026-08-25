// Gera o sitemap com lastmod real (data do ultimo commit que tocou cada arquivo).
// Rodar depois de commitar as mudancas de conteudo.
import { writeFileSync, globSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { basename } from 'node:path';

process.chdir('D:/Claude/nak_api_br');
const BASE = 'https://nak.api.br';
const dataDe = (f) => execSync(`git log -1 --format=%ad --date=short -- "${f}"`).toString().trim();

const paginas = [
  { arquivo: 'index.html', loc: `${BASE}/`, freq: 'weekly', prio: '1.0' },
  { arquivo: 'cases.html', loc: `${BASE}/cases`, freq: 'weekly', prio: '0.9' },
  { arquivo: 'sobre.html', loc: `${BASE}/sobre`, freq: 'monthly', prio: '0.7' },
];

// Cases: ordenados do mais recente pro mais antigo, pelo commit.
const cases = globSync('cases/*.html')
  .filter((f) => basename(f) !== 'index.html')
  .map((f) => ({
    arquivo: f,
    loc: `${BASE}/cases/${basename(f, '.html')}`,
    freq: 'monthly',
    prio: '0.8',
    data: dataDe(f),
  }))
  .sort((a, b) => b.data.localeCompare(a.data));

// Em observacao: no ar sem resultado medido. Prioridade menor que case.
const observacao = globSync('observacao/*.html')
  .map((f) => ({
    arquivo: f,
    loc: `${BASE}/observacao/${basename(f, '.html')}`,
    freq: 'weekly',
    prio: '0.6',
    data: dataDe(f),
  }))
  .sort((a, b) => b.data.localeCompare(a.data));

const todas = [...paginas, ...cases, ...observacao];

const xml =
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
  todas
    .map((p) => {
      const lastmod = p.data || dataDe(p.arquivo);
      if (!lastmod) throw new Error(`sem data de commit para ${p.arquivo}`);
      return `  <url>\n    <loc>${p.loc}</loc>\n    <lastmod>${lastmod}</lastmod>\n    <changefreq>${p.freq}</changefreq>\n    <priority>${p.prio}</priority>\n  </url>`;
    })
    .join('\n') +
  `\n</urlset>\n`;

writeFileSync('sitemap.xml', xml, 'utf8');
console.log(`${todas.length} URLs`);
todas.forEach((p) => console.log(`  ${p.data || dataDe(p.arquivo)}  ${p.loc}`));
