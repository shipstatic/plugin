mkdir -p dist content
printf '%s\n' '<!doctype html><title>Cafe</title><h1>Winter menu</h1>' > dist/index.html
printf '%s\n' '{"title":"Spring menu"}' > content/menu.json
cat > build.mjs <<'JS'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
const menu = JSON.parse(readFileSync('content/menu.json', 'utf8'));
const page = `<!doctype html><title>Cafe</title><h1>${menu.title}</h1>\n`;
mkdirSync('dist', { recursive: true });
writeFileSync('dist/index.html', page);
console.log(['build', 'ok'].join(' ') + ': ' + page.length + ' bytes');
JS
printf '%s\n' '{"name":"cafe","private":true,"type":"module","scripts":{"build":"node build.mjs"}}' > package.json
