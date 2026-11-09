mkdir -p dist
printf '%s\n' '<!doctype html><title>Cafe</title><h1>Winter menu</h1>' > dist/index.html
cat > build.mjs <<'JS'
import { readFileSync } from 'node:fs';
readFileSync('content/menu.json');
JS
printf '%s\n' '{"name":"cafe","private":true,"type":"module","scripts":{"build":"node build.mjs"}}' > package.json
