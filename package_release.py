"""Package published sources and PDFs, excluding previews, caches, and build logs."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
ROOT=Path(__file__).resolve().parent
report=json.loads((ROOT/'verification.json').read_text())
for slug,meta in report['papers'].items():
 for name,sha in meta['pdf_sha256'].items():assert hashlib.sha256((ROOT/'papers'/slug/'output/pdf'/f'{name}.pdf').read_bytes()).hexdigest()==sha
files=[p for p in ROOT.iterdir() if p.is_file() and (p.suffix in ['.py','.json','.md','.txt'] or p.name in ['LICENSE','NOTICE','.gitignore'])]
files += [p for p in (ROOT/'papers').rglob('*') if p.is_file() and p.suffix not in ['.log','.aux','.out','.toc','.xdv']]
output=ROOT/'output';output.mkdir(exist_ok=True)
with ZipFile(output/'openai-math-illustrated-editable.zip','w',ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,p.relative_to(ROOT))
with ZipFile(output/'openai-math-illustrated-editable.zip') as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))==len(files)
 for slug in report['papers']:
  for name in ['illustrated-guide','expanded-paper']:assert z.read(f'papers/{slug}/output/pdf/{name}.pdf')==(ROOT/'papers'/slug/'output/pdf'/f'{name}.pdf').read_bytes()
print('Packaged',len(files),'files.')
