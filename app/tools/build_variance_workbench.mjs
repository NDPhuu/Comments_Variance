import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..');
const backend = path.join(root, 'app', 'backend');
const dataset = path.join(backend, 'data', 'dataset_v1');
const results = path.join(backend, 'results');
const templatePath = path.join(here, 'variance_workbench.template.html');
const outputPath = path.join(root, 'docs', 'variance_workbench_demo.html');

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const readCsv = (file) => {
  const lines = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '').trim().split(/\r?\n/);
  const headers = lines.shift().split(',');
  return lines.map((line) => {
    const values = line.split(',');
    return Object.fromEntries(headers.map((header, index) => [header, values[index] ?? '']));
  });
};

const records = fs.readFileSync(path.join(results, 'raw', 'records_full.jsonl'), 'utf8')
  .split(/\r?\n/)
  .filter(Boolean)
  .map(JSON.parse);

const payload = {
  generatedFrom: {
    cases: 'app/backend/data/dataset_v1/cases.json',
    evidence: 'app/backend/data/dataset_v1/evidence.json',
    evidencePacks: 'app/backend/data/dataset_v1/evidence_packs.json',
    records: 'app/backend/results/raw/records_full.jsonl',
    summary: 'app/backend/results/summary.csv',
    summaryByRep: 'app/backend/results/summary_by_rep.csv',
    runConfig: 'app/backend/results/run_config.json',
  },
  manifest: readJson(path.join(dataset, 'manifest.json')),
  runConfig: readJson(path.join(results, 'run_config.json')),
  cases: readJson(path.join(dataset, 'cases.json')),
  evidence: readJson(path.join(dataset, 'evidence.json')),
  evidencePacks: readJson(path.join(dataset, 'evidence_packs.json')),
  records,
  summary: readCsv(path.join(results, 'summary.csv')),
  summaryByRep: readCsv(path.join(results, 'summary_by_rep.csv')),
};

const template = fs.readFileSync(templatePath, 'utf8');
const marker = '/*__EMBEDDED_REPOSITORY_DATA__*/';
if (!template.includes(marker)) throw new Error(`Missing marker ${marker}`);

const serialized = JSON.stringify(payload).replace(/</g, '\\u003c');
const output = template.replace(marker, `window.VWB_DATA=${serialized};`);
fs.writeFileSync(outputPath, output, 'utf8');
console.log(`Built ${path.relative(root, outputPath)} from repository data (${records.length} benchmark records).`);
