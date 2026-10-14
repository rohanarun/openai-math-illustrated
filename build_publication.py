"""Build illustrated guides, source-preserving expanded editions, and README views."""
from pathlib import Path
import json,re,subprocess,os,hashlib
import fitz
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'source-manifest.json').read_text())
def esc(t):
 t=t.replace("{",r"\{").replace("}",r"\}").replace("^",r"\textasciicircum{}").replace("$",r"\$")
 for a,b in [('&',r'\&'),('%',r'\%'),('#',r'\#'),('_',r'\_'),('×',r'$\times$'),('√',r'$\surd$'),('²',r'$^2$'),('³',r'$^3$'),('₀',r'$_0$'),('₁',r'$_1$'),('₂',r'$_2$'),('₃',r'$_3$'),('ᵢ',r'$_i$'),('ⱼ',r'$_j$'),('−',r'$-$'),('≤',r'$\le$'),('≥',r'$\ge$'),('λ',r'$\lambda$'),('η',r'$\eta$'),('’',"'"),('“','``'),('”',"''"),('–','--'),('—','---')]:t=t.replace(a,b)
 return t
preamble=r'''\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,graphicx,xcolor,booktabs,array,enumitem}
\usepackage[letterpaper,margin=0.78in]{geometry}
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=teal]{hyperref}
\usepackage{fancyhdr}
\definecolor{ink}{HTML}{172C3B}
\definecolor{teal}{HTML}{087F82}
\definecolor{blue}{HTML}{265DAB}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\footnotesize OpenAI math: independent illustrated reading editions}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{7pt}
\setlength{\emergencystretch}{2em}
\hypersetup{pdfauthor={Independent explanatory edition prepared with OpenAI Codex}}
\begin{document}
'''
report={}
for slug,meta in manifest['papers'].items():
 d=ROOT/'papers'/slug;p=json.loads((d/'content.json').read_text())
 for path,sha in meta['files'].items():assert hashlib.sha256((d/'original'/path).read_bytes()).hexdigest()==sha,path
 tex=preamble+r'\begin{center}{\LARGE\bfseries '+esc(p['title'])+r'}\par\vspace{12pt}{\large '+esc(p['subtitle'])+r'}\par\vspace{16pt}Independent reading edition, October 14, 2026\end{center}'+'\n'
 tex+=r'\section*{Start here}'+p['intro']+'\n'+r'\paragraph{Reading prerequisites.} Ordinary arithmetic is enough for the opening examples. Later chapters introduce the specialized vocabulary; checking every original proof requires additional study.\par\textbf{Attribution.} Original manuscript by OpenAI. Added explanations and figures prepared with OpenAI Codex. This is not an official revision or independent theorem validation.\par\href{'+meta['source_url']+r'}{Pinned original manuscript and citation}.'
 tex+=r'\newpage\section*{The source claim, precisely}'+p['claim']+r'\paragraph{How to read this edition.} Each chapter gives one concrete illustration, then explains how it connects to the source. Captions identify toys and original constructions. Source anchors use the original manuscript\textquotesingle s section and page numbering. The expanded PDF places this guide before the complete unchanged original PDF, preserving the original page numbers and bibliography.'
 tex+=r'\subsection*{Your route through the argument}\begin{enumerate}'
 for c in p['chapters']:tex+=r'\item '+esc(c['title'])+'\n'
 tex+=r'\end{enumerate}\paragraph{Verification scope.} The accompanying code checks the displayed finite examples and preserves original-file hashes. These checks do not replace the analytic, algebraic, asymptotic, or formal proof obligations in the source.'
 for i,c in enumerate(p['chapters'],1):
  tex+=r'\newpage\section*{'+esc(c['title'])+'}\n'
  tex+=r'\begin{center}\includegraphics[width=\linewidth,height=2.35in,keepaspectratio]{figures/'+c['figure']+'.pdf}'+r'\end{center}'+'\n'
  tex+=r'{\small\color{teal}\textbf{Figure '+str(i)+'.} '+esc(c['caption'])+r'\par}'+'\n'+c['body']+'\n'
  tex+=r'{\footnotesize\color{blue}\textbf{Source anchor:} '+esc(c['source'])+r'\par}'+'\n'
 tex+=r'\newpage\section*{A vocabulary you can return to}'+'\n'
 for term,meaning in p['glossary']:tex+=r'\paragraph{'+esc(term)+'}'+esc(meaning)+'\n'
 tex+=r'\section*{What this edition checks}'+p['limits']+'\n'+r'\paragraph{A useful self-test.} Explain what each plotted quantity counts, which examples are illustrative, and where the source needs a statement for every input or every sufficiently large size. If a picture seems to establish the full theorem by itself, revisit its caption and source anchor.'
 tex+=r'\paragraph{Sources and reuse.}\href{'+meta['source_url']+r'}{'+esc(p['source_title'])+r'}, OpenAI. Original bibliography and manuscript-specific citation are included with the source. Source snapshot: \texttt{'+manifest['commit'][:12]+r'}. This derivative is distributed under Apache-2.0 with the original attribution; see the repository LICENSE and NOTICE.'+r'\end{document}'
 (d/'illustrated-guide.tex').write_text(tex)
 env=os.environ.copy();env.update(TMPDIR=str(ROOT/'tmp'),XDG_CACHE_HOME=str(ROOT/'tmp/cache'))
 run=subprocess.run(['tectonic','--keep-logs','-o','output/pdf','illustrated-guide.tex'],cwd=d,env=env,capture_output=True,text=True)
 (ROOT/'tmp'/f'{slug}-build.txt').write_text(run.stdout+run.stderr)
 if run.returncode:raise RuntimeError(f'{slug}: {run.stderr[-3000:]}')
 guide=fitz.open(d/'output/pdf/illustrated-guide.pdf');original=fitz.open(d/'original/paper.pdf');combined=fitz.open();combined.insert_pdf(guide);combined.insert_pdf(original)
 combined.set_metadata({'title':p['title']+' - guide and original manuscript','author':'OpenAI (original); independent explanatory edition prepared with Codex','subject':'Reading edition; original manuscript reproduced without page alterations'})
 toc=[[1,'Illustrated reading guide',1],[1,'Original manuscript (unchanged pages)',len(guide)+1]]
 for level,title,page in original.get_toc():toc.append([level+1,title,len(guide)+page])
 combined.set_toc(toc);combined.save(d/'output/pdf/expanded-paper.pdf',garbage=4,deflate=True)
 report[slug]={'guide_pages':len(guide),'original_pages':len(original),'expanded_pages':len(combined),'figures':len(p['chapters'])}
 readme='# '+p['title']+'\n\n'+p['subtitle']+'.\n\n'
 readme+=f"[Illustrated guide ({len(guide)} pages)](output/pdf/illustrated-guide.pdf) · [Expanded edition ({len(combined)} pages)](output/pdf/expanded-paper.pdf) · [Original source]({meta['source_url']})\n\n"
 readme+='Six concrete diagrams with worked examples. The expanded edition pairs the guide with every original manuscript page; the original proof and bibliography retain their numbering. This is an independent explanation, not an official OpenAI revision or independent theorem certification.\n\n'
 for c in p['chapters']:
  readme+='## '+c['title']+'\n\n![ '+c['caption'].replace(']','')+' ](figures/'+c['figure']+'.png)\n\n'+c['caption']+'\n\n**Where it fits:** '+c['source']+'\n\n'
 readme+='## Read and reproduce\n\nThe PDF develops each example step by step and explains what it does and does not establish. Editable prose is in [content.json](content.json); the [generated LaTeX](illustrated-guide.tex) is also included. Original files are under [original/](original/), bound by the collection [source manifest](../../source-manifest.json). See the [collection README](../../README.md) for generation and validation commands.\n'
 (d/'README.md').write_text(readme)
 print(slug,report[slug],flush=True)
(ROOT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
