mkdir -p dist
printf '%s\n' '<!doctype html><title>Cafe</title><h1>Winter menu</h1>' > dist/index.html
cat > build.mjs <<'JS'
import { mkdirSync, writeFileSync } from 'node:fs';
mkdirSync('dist', { recursive: true });
writeFileSync('dist/index.html', '<!doctype html><title>Cafe</title><h1>Spring menu</h1>\n');
JS
printf '%s\n' '{"name":"cafe","private":true,"type":"module","scripts":{"build":"node build.mjs"}}' > package.json
