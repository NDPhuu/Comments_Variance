import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.resolve(here, '..', '..', 'docs', 'variance_workbench_demo.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const scripts = [];
let cursor = 0;
while (true) {
  const start = html.indexOf('<script>', cursor);
  if (start < 0) break;
  const end = html.indexOf('</script>', start);
  if (end < 0) throw new Error('Unclosed script element');
  scripts.push(html.slice(start + 8, end));
  cursor = end + 9;
}

for (const [index, source] of scripts.entries()) {
  try {
    new Function(source);
  } catch (error) {
    throw new Error(`Inline script ${index + 1} has invalid syntax: ${error.message}`);
  }
}

const required = [
  'id="queue"',
  'id="investigate"',
  'id="draft"',
  'id="research"',
  'Dữ liệu mô phỏng · Không dùng cho báo cáo thực tế',
  'prefers-reduced-motion',
  'aria-modal="true"',
  'window.VWB_DATA=',
];
for (const token of required) {
  if (!html.includes(token)) throw new Error(`Missing required token: ${token}`);
}
if (html.includes('2026-07_PROP-C_Leasing_revenue')) throw new Error('Obsolete fabricated case remains');
if (html.includes('EV-112 · termination_notice')) throw new Error('Obsolete evidence mapping remains');

console.log(`Validation OK: ${scripts.length} inline scripts compiled; required UI states and provenance markers found.`);
