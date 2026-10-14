"""Publish a version-bound catalogue with explicit per-manuscript progress."""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'source-manifest.json').read_text());sha=manifest['commit'];text=(ROOT/'catalogue-source.md').read_text()
family=None;records=[]
completed={m['upstream_directory']:slug for slug,m in manifest['papers'].items()}
for line in text.splitlines():
 match=re.match(r'^\*\*(\d+)\. (.+?)\*\*',line)
 if match:family={'number':match[1],'title':match[2]}
 for title,path in re.findall(r'\[([^\n]*?)\]\((preprints/.*?\.pdf)\)',line):
  directory=path.split('/')[1];slug=completed.get(directory);external=directory=='Integer-multiplication-below-n-log-n-September-23-2026'
  records.append({'title':title,'family':family,'source_pdf':f'https://github.com/openai/math/blob/{sha}/{path}','source_path':path,'status':'published_here' if slug else 'published_external' if external else 'pending','edition':f'papers/{slug}/README.md' if slug else 'https://github.com/rohanarun/integer-multiplication-illustrated' if external else None})
assert len(records)==719 and len({x['source_path'] for x in records})==719
assert len({x['family']['number'] for x in records})==372
(ROOT/'catalogue.json').write_text(json.dumps({'source_commit':sha,'snapshot_date':'2026-10-14','scope':'OpenAI math manuscript map; one record per listed manuscript, not every preprints directory.','manuscripts':records},indent=2,ensure_ascii=False)+'\n')
counts={state:sum(r['status']==state for r in records) for state in ['published_here','published_external','pending']}
header='# Manuscript catalogue and progress\n\n'+f'Source snapshot: [`{sha[:12]}`](https://github.com/openai/math/tree/{sha}). **719 manuscripts / 372 families.**\n\n'
header+=f"**{counts['published_here']} new editions here; {counts['published_external']} existing edition linked; {counts['pending']} pending.** A catalogue entry is not an expanded edition. Pending manuscripts have no generated guide or figures.\n\nThe current priority is the user’s existing research topics. This is a recorded work queue, not an unattended publishing service. Source titles describe the manuscripts’ claims and are not independent verification of them.\n\n"
header+='| Family | Manuscript | Reading edition |\n| --- | --- | --- |\n'
for r in records:
 title=r['title'].replace('|',r'\|');link=r['source_pdf'].replace('(','\(').replace(')','\)')
 status='Pending' if not r['edition'] else f"[{'Published here' if r['status']=='published_here' else 'Existing edition'}]({r['edition']})"
 header+=f"| {r['family']['number']} | [{title}]({link}) | {status} |\n"
(ROOT/'CATALOGUE.md').write_text(header)
print(counts)
