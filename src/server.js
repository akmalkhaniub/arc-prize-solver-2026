import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { ArcSolver } from './arc_solver.js';
import { TTCRefinementLoop } from './ttc_refinement_loop.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PUBLIC_DIR = path.join(__dirname, 'public');
const PORT = process.env.PORT || 3007;

const solver = new ArcSolver();
const ttc = new TTCRefinementLoop();

const PRESET_TASKS = {
  reflection: {
    name: 'Horizontal Reflection',
    train: [
      { input: [[1, 0, 0], [1, 2, 0]], output: [[0, 0, 1], [0, 2, 1]] },
      { input: [[3, 1], [0, 2]], output: [[1, 3], [2, 0]] }
    ],
    test: [{ input: [[2, 1, 0], [0, 0, 3]], output: [[0, 1, 2], [3, 0, 0]] }]
  },
  substitution: {
    name: 'Color Substitution (Blue -> Red)',
    train: [
      { input: [[1, 0], [0, 1]], output: [[2, 0], [0, 2]] },
      { input: [[1, 1], [0, 0]], output: [[2, 2], [0, 0]] }
    ],
    test: [{ input: [[0, 1, 1], [1, 0, 0]], output: [[0, 2, 2], [2, 0, 0]] }]
  },
  gravity_reflect: {
    name: 'Composite: Gravity Down + Reflect',
    train: [
      { input: [[1, 0, 0], [0, 0, 0], [0, 0, 0]], output: [[0, 0, 0], [0, 0, 0], [0, 0, 1]] },
      { input: [[2, 0, 0], [3, 0, 0], [0, 0, 0]], output: [[0, 0, 0], [0, 0, 2], [0, 0, 3]] }
    ],
    test: [{ input: [[1, 2, 0], [0, 0, 0], [0, 0, 0]], output: [[0, 0, 0], [0, 0, 0], [0, 2, 1]] }]
  }
};

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Health check endpoint for container probes & cloud orchestrators
  if (req.url === '/api/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'online',
      service: 'ARC Prize Solver 2026',
      timestamp: new Date().toISOString()
    }));
    return;
  }

  // REST API Routes
  if (req.url === '/api/tasks' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(PRESET_TASKS));
    return;
  }

  if (req.url === '/api/solve' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const { task } = JSON.parse(body);
        const result = ttc.refineSolution(task);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(result));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // Static files
  let filePath = path.join(PUBLIC_DIR, req.url === '/' ? 'index.html' : req.url);
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.json': 'application/json; charset=utf-8'
  };

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Server Error: ' + err.code);
      }
    } else {
      res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
      res.end(content);
    }
  });
});

server.listen(PORT, () => {
  console.log(`🧩 ARC Prize Solver Server running at http://localhost:${PORT}`);
});
