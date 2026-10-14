"""Verify source integrity, PDF structure, examples, and unchanged appended pages."""
from pathlib import Path
import json,hashlib,re
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'source-manifest.json').read_text())
build=json.loads((ROOT/'build-report.json').read_text())
preview=ROOT/'preview';preview.mkdir(exist_ok=True)
report={'scope':'Document integrity and finite examples, not full theorem verification.','source_commit':manifest['commit'],'papers':{},'visual_review':'Pending inspection of this render.'}
for slug,meta in manifest['papers'].items():
 d=ROOT/'papers'/slug;out=preview/slug;out.mkdir(exist_ok=True)
 for name,sha in meta['files'].items():assert hashlib.sha256((d/'original'/name).read_bytes()).hexdigest()==sha,(slug,name)
 text=(d/'output/pdf/illustrated-guide.log').read_text()
 for marker in ['Overfull','Missing character','undefined']:assert marker not in text,(slug,marker)
 guide=fitz.open(d/'output/pdf/illustrated-guide.pdf');expanded=fitz.open(d/'output/pdf/expanded-paper.pdf');original=fitz.open(d/'original/paper.pdf')
 assert len(guide)==build[slug]['guide_pages'] and len(expanded)==len(guide)+len(original)
 full='\n'.join(p.get_text() for p in guide)
 for i in range(1,7):assert f'Figure {i}.' in full,(slug,i)
 assert '??' not in full
 thumbs=[]
 for i,page in enumerate(expanded):
  pix=page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
  if i<len(guide):
   for b in page.get_text('dict')['blocks']:
    for line in b.get('lines',[]):
     for span in line['spans']:
      x0,y0,x1,y1=span['bbox'];assert x0>=0 and y0>=0 and x1<=page.rect.width and y1<=page.rect.height,(slug,i+1,span['text'])
   assert len(page.get_text().strip())>150
   fn=out/f'guide-{i+1:02}.png';pix.save(fn)
   im=Image.open(fn).convert('RGB');im.thumbnail((306,396));tile=Image.new('RGB',(326,430),'#edf0f4');tile.paste(im,((326-im.width)//2,10));ImageDraw.Draw(tile).text((12,412),f'{slug} / {i+1}',fill='black');thumbs.append(tile)
  else:
   source=original[i-len(guide)]
   assert source.get_text()==page.get_text(),(slug,i,'text changed')
   sourcepix=source.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
   assert (pix.width,pix.height)==(sourcepix.width,sourcepix.height)
   assert hashlib.sha256(pix.samples).digest()==hashlib.sha256(sourcepix.samples).digest(),(slug,i,'pixels changed')
   pix.save(out/f'original-{i-len(guide)+1:03}.png')
 sheet=Image.new('RGB',(978,430*((len(thumbs)+2)//3)),'white')
 for i,im in enumerate(thumbs):sheet.paste(im,((i%3)*326,(i//3)*430))
 sheet.save(preview/f'{slug}-guide.png')
 report['papers'][slug]={**build[slug],'original_files_hash_verified':len(meta['files']),'all_expanded_pages_rendered':True,'original_pages_pixel_identical':len(original),'no_missing_glyphs_or_overflow':True,'pdf_sha256':{n:hashlib.sha256((d/'output/pdf'/f'{n}.pdf').read_bytes()).hexdigest() for n in ['illustrated-guide','expanded-paper']}}
 # All illustrated README references resolve to actual figures.
 readme=(d/'README.md').read_text();imgs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',readme);assert len(imgs)==6
 for img in imgs:assert (d/img).is_file(),img
report['examples']=json.loads((ROOT/'example-checks.json').read_text())
cat=json.loads((ROOT/'catalogue.json').read_text());assert len(cat['manuscripts'])==719
for row in cat['manuscripts']:
 if row['status']=='published_here':assert (ROOT/row['edition']).is_file()
report['catalogue']={'listed_manuscripts':len(cat['manuscripts']),'families':len({x['family']['number'] for x in cat['manuscripts']}),'completed_here':sum(x['status']=='published_here' for x in cat['manuscripts']),'existing_external':sum(x['status']=='published_external' for x in cat['manuscripts']),'pending':sum(x['status']=='pending' for x in cat['manuscripts'])}
(ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({slug:report['papers'][slug] for slug in report['papers']},indent=2))
