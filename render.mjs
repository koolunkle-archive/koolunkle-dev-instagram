// 카드 PNG 렌더러: node render.mjs [폴더id...]  (인자 없으면 전체) → out/<id>/NN.png
// Chrome headless로 template/card.html?s=ID&p=N 을 1080x1350 스크린샷.
import { execFileSync } from 'node:child_process';
import { readFileSync, mkdirSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import vm from 'node:vm';

const CHROME = [process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find(p => p && existsSync(p));
if (!CHROME) throw new Error('Chrome/Edge not found; set CHROME env');

const ctx = { window: {} };
vm.runInNewContext(readFileSync('content/series.js', 'utf8'), ctx);
const only = process.argv.slice(2);
const page = pathToFileURL(resolve('template/card.html')).href;

for (const s of ctx.window.SERIES.filter(s => !only.length || only.includes(s.id))) {
  mkdirSync(resolve('out', s.id), { recursive: true });
  s.slides.forEach((_, i) => {
    const out = resolve('out', s.id, String(i + 1).padStart(2, '0') + '.png');
    execFileSync(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
      '--window-size=1080,1350', '--virtual-time-budget=8000', '--allow-file-access-from-files',
      `--screenshot=${out}`, `${page}?s=${s.id}&p=${i + 1}`], { stdio: 'ignore' });
    console.log(out);
  });
}
