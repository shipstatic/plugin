cat > server.js <<'JS'
const express = require('express');
const { Pool } = require('pg');
const db = new Pool();
const app = express();
app.get('/api/todos', async (req, res) => res.json((await db.query('select * from todos')).rows));
app.listen(3000);
JS
printf '%s\n' '{"name":"todo-api","private":true,"scripts":{"start":"node server.js"},"dependencies":{"express":"^4.21.0","pg":"^8.13.0"}}' > package.json
