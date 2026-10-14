"""Source-bound mathematical figures and exact checks for the first reading batch."""
from pathlib import Path
import os,json,itertools,math,re
from fractions import Fraction as F
from collections import Counter
ROOT=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
B,T,G,I='#265DAB','#087F82','#C36C25','#172C3B'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':I,'axes.labelcolor':I,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
checks={}
def save(fig,slug,name):
 fig.tight_layout();p=ROOT/'papers'/slug/'figures'/name
 fig.savefig(p.with_suffix('.png'),dpi=180,bbox_inches='tight',pad_inches=.15)
 fig.savefig(p.with_suffix('.pdf'),bbox_inches='tight',pad_inches=.15);plt.close(fig)
def matrix(ax,a,title,cmap='Blues',labels=True,vmin=None,vmax=None):
 im=ax.imshow(a,cmap=cmap,aspect='auto',vmin=vmin,vmax=vmax);ax.set_title(title)
 if labels:
  for (i,j),v in np.ndenumerate(a):
   red,green,blue,_=im.cmap(im.norm(v));color='white' if .2126*red+.7152*green+.0722*blue<.48 else I
   ax.text(j,i,f'{v:.3g}',ha='center',va='center',color=color,fontsize=10)
 ax.set_xticks(range(a.shape[1]));ax.set_yticks(range(a.shape[0]))

s='van-der-waerden'
def aps(n,k=3):return [tuple(a+j*d for j in range(k)) for d in range(1,n) for a in range(1,n+1-(k-1)*d)]
def avoiding(n):
 triples=[tuple(x) for x in aps(n)]
 return [v for v in itertools.product(range(2),repeat=n) if all(len({v[i-1] for i in p})>1 for p in triples)]
a8=avoiding(8);a9=avoiding(9);assert a8 and not a9;v=a8[0]
fig,ax=plt.subplots(figsize=(9,3));ax.scatter(range(1,9),[0]*8,c=[B if x==0 else G for x in v],s=350)
for i,c in enumerate(v,1):ax.text(i,0,str(i),ha='center',va='center',color='white')
for row,p in enumerate([(1,2,3),(1,3,5),(2,5,8)]):
 ax.plot(p,[-.5-row*.4]*3,'-',color='#9CAAB4');ax.scatter(p,[-.5-row*.4]*3,c=[B if v[i-1]==0 else G for i in p],s=60,zorder=3);ax.text(8.6,-.5-row*.4,f'step {p[1]-p[0]}',va='center')
ax.set(xlim=(.4,10),ylim=(-1.6,.5),title='Eight positions can avoid every one-color 3-term progression');ax.axis('off');save(fig,s,'01-coloring')
fig,axes=plt.subplots(1,2,figsize=(9,3.6));r=[(5*j)%13 for j in range(5)];theta=2*np.pi*np.arange(13)/13
axes[0].plot(np.cos(theta),np.sin(theta),'o',color='#CCD6E0')
for i,n in enumerate(r):
 x,y=np.cos(theta[n]),np.sin(theta[n]);axes[0].text(1.2*x,1.2*y,str(n),ha='center',va='center',color=B)
 if i<4:axes[0].annotate('',xy=(np.cos(theta[r[i+1]]),np.sin(theta[r[i+1]])),xytext=(x,y),arrowprops={'arrowstyle':'->','color':T})
axes[0].set(aspect='equal',xlim=(-1.4,1.4),ylim=(-1.4,1.4),title='Add 5 around the 13-point circle');axes[0].axis('off')
axes[1].plot(range(5),r,'o-',label='Residue in [0, 13)',color=G);axes[1].plot(range(5),[5*j for j in range(5)],'o-',label='Unwrapped: 5j',color=B);axes[1].set(xlabel='Step j',ylabel='Position',title='A cut creates jumps in representatives');axes[1].legend(fontsize=8);save(fig,s,'02-circle')
fig,axes=plt.subplots(1,2,figsize=(9,3.4));tt=np.arange(-2,3);norm=tt**2+1
axes[0].scatter(tt,[1]*5,c=norm,cmap='viridis',s=120)
for radius in [1,np.sqrt(2),np.sqrt(5)]:axes[0].add_patch(Circle((0,0),radius,fill=False,color=T,alpha=.4))
axes[0].set(aspect='equal',xlim=(-2.6,2.6),ylim=(-.3,2.7),title='Affine points (j, 1) on norm shells')
axes[1].plot(tt,norm,'o-',color=T);axes[1].set(xlabel='j',ylabel='Squared norm j² + 1',title='One shell meets this line at most twice');save(fig,s,'03-norm')
h=np.arange(1,25);lam=2**4*3**2;den=[int(x)//math.gcd(int(x),lam) for x in h];assert all(x==1 or x>4 for x in den)
fig,ax=plt.subplots(figsize=(9,3.6));ax.scatter(h,den,c=[T if x==1 else B for x in den]);ax.axhspan(1.1,4,color=G,alpha=.12,label='No reduced denominator here');ax.set(xlabel='Original period h ≤ 24',ylabel='h / gcd(h, 144)',title='Dilation removes every primary factor for primes ≤ 4');ax.legend(fontsize=9);save(fig,s,'04-periods')
fig,ax=plt.subplots(figsize=(9,3.5));x=np.linspace(1,180,400);ratio=np.log(10)*x/10**(.05*x);ax.semilogy(x,ratio,color=B);ax.axhline(1,color=G,ls='--');ax.set(xlabel='log₁₀ k (k itself is enormous)',ylabel='(k⁰·⁹ log k) / k⁰·⁹⁵',title='The event-count exponent is eventually smaller');ax.text(90,5,'Ratio tends to zero; constants omitted',fontsize=10);save(fig,s,'05-probability')
fig,ax=plt.subplots(figsize=(9,3.5));x=np.linspace(0,160000,200);ax.plot(x,1e-5*x,color=T,label='c log k, c = 10⁻⁵');ax.axhline(np.log(2),color=G,ls='--',label='log 2');ax.set(xlabel='log k',ylabel='log of kth-root bound expression',title='Superexponential means the kth-root scale keeps growing');ax.legend(fontsize=9);save(fig,s,'06-growth')
checks[s]={'avoiding_colorings_n8':len(a8),'avoiding_colorings_n9':len(a9),'example':v,'period_lambda':lam,'reduced_periods':den}

s='sidorenko';source=(ROOT/'papers'/s/'original/sections/complex.tex').read_text();rows=re.findall(r'^\s*(\d+)\s*&\s*(\d+)&(\d+)&(\d+)\s*&\s*\d+&\d+&\d+\s*&\s*([01]{3})',source,re.M);assert len(rows)==22
faces=[tuple(map(int,row[1:4])) for row in rows];inc=np.zeros((13,22),int)
for j,face in enumerate(faces):inc[list(face),j]=1
pairs=Counter(tuple(sorted(e)) for face in faces for e in itertools.combinations(face,2));assert inc.sum()==66 and len(pairs)==33 and set(pairs.values())=={2}
fig,axes=plt.subplots(1,2,figsize=(9,3.5));xy=np.array([[0,0],[1,1],[1,-1],[2,0]])
for j in [1,2,3]:axes[0].plot(xy[[0,j],0],xy[[0,j],1],color=T,lw=2)
axes[0].scatter(xy[:,0],xy[:,1],s=250,color=[G,B,B,B])
for i,(x,y) in enumerate(xy):axes[0].text(x,y,str(i),color='white',ha='center',va='center')
axes[0].axis('off');axes[0].set_title('Host: a three-leaf star')
axes[1].bar(['t(P₃, G)','p(G)²'],[12/64,(6/16)**2],color=[T,B]);axes[1].set(ylabel='Density',title='A positive example, not the counterexample');save(fig,s,'01-homomorphisms')
fig,ax=plt.subplots(figsize=(10,4.4));matrix(ax,inc,'The actual 13 × 22 incidence matrix (66 edges)',labels=False);ax.set(xlabel='Face vertex j',ylabel='Point vertex i');save(fig,s,'02-incidence')
fig,axes=plt.subplots(1,2,figsize=(9,3.5));
points={0:(-1,0),1:(1,0),3:(0,1),9:(0,-1)}
for face,col in zip(faces[:2],[B,G]):
 tri=np.array([points[i] for i in (*face,face[0])]);axes[0].plot(*tri.T,color=col,lw=2)
axes[0].plot([-1,1],[0,0],color=I,lw=3)
for label,(xx,yy) in points.items():axes[0].text(xx,yy+.12 if yy>=0 else yy-.2,str(label),ha='center')
axes[0].text(0,.4,'face 0',ha='center',color=B);axes[0].text(0,-.4,'face 1',ha='center',color=G)
axes[0].set(title='Faces 0 and 1 share the point pair {0, 1}',ylim=(-1.4,1.4));axes[0].axis('off')
axes[1].bar(['AB = +1','AB = −1'],[2,0],color=[T,G]);axes[1].set(ylim=(0,2.5),ylabel='Average over η = ±1',title='E[(1 + ηA)(1 + ηB)] = 1 + AB');save(fig,s,'03-parity')
W=np.array([[.8,.2],[.2,.8]]);p=W.mean();c4=np.trace(np.linalg.matrix_power(W,4))/16;assert abs(c4-.0706)<1e-12
WF=[[F(4,5),F(1,5)],[F(1,5),F(4,5)]]
exact_c4=sum(math.prod(WF[ids[k]][ids[(k+1)%4]] for k in range(4)) for ids in itertools.product(range(2),repeat=4))/16
assert exact_c4==F(353,5000)
for signs in itertools.product([-1,1],repeat=4):
 aa,bb=signs[0]*signs[1],signs[2]*signs[3]
 assert sum((1+eta*aa)*(1+eta*bb) for eta in [-1,1])/2==1+math.prod(signs)
fig,axes=plt.subplots(1,2,figsize=(9,3.5));matrix(axes[0],W,'A two-type toy kernel, equal type probabilities');axes[1].bar(['Edge mean','4-cycle density'],[p,c4],color=[T,B]);axes[1].scatter([0,1],[.5,.5**4],color=G,label='Constant kernel benchmark',zorder=3);axes[1].legend(fontsize=8);axes[1].set_title('Same edge mean does not fix every pattern');save(fig,s,'04-kernel')
fig,ax=plt.subplots(figsize=(9,3.5));q=np.arange(2,101);ax.loglog(q,1/q,label='Rare-event probability: 1/q',color=B);ax.loglog(q,q,label='Weighted contribution: (1/q) × q²',color=G);ax.set(xlabel='q',ylabel='Toy scale',title='Rare configurations can dominate a weighted average');ax.legend(fontsize=9);save(fig,s,'05-weighted-tail')
fig,ax=plt.subplots(figsize=(9,3.5));m=np.arange(1,31);ax.plot(m,.9**m,'o-',color=T);ax.set(xlabel='Tensor-power count m',ylabel='Normalized density ratio 0.9ᵐ',title='A strict deficit multiplies (illustrative starting ratio)');ax.axhline(1,color=G,ls=':');save(fig,s,'06-amplification')
checks[s]={'faces_extracted_from_source':faces,'incidence_edges':int(inc.sum()),'point_pairs':len(pairs),'pair_multiplicity':2,'star_path_homomorphisms':sum(d*d for d in [3,1,1,1]),'toy_kernel_c4':str(F(353,5000))}

s='unit-distances';xy=np.array(list(itertools.product(range(3),repeat=2)));edges=[(i,j) for i in range(9) for j in range(i) if sum((xy[i]-xy[j])**2)==1];assert len(edges)==12
fig,ax=plt.subplots(figsize=(8,4));
for i,j in edges:ax.plot(xy[[i,j],0],xy[[i,j],1],color=T,lw=2)
ax.scatter(xy[:,0],xy[:,1],color=B,s=80);ax.plot([0,1],[0,1],':',color=G,label='Diagonal length √2: excluded');ax.set(aspect='equal',title='Nine grid points, twelve unordered unit pairs',xticks=range(3),yticks=range(3));ax.legend(loc='upper left',bbox_to_anchor=(1,1),fontsize=9);save(fig,s,'01-grid')
fig,ax=plt.subplots(figsize=(8,4));
for x in [0,1]:ax.add_patch(Circle((x,0),1,fill=False,color=B if x==0 else T,lw=2))
ax.scatter([0,1],[0,0],color=I);ax.scatter([.5,.5],[np.sqrt(3)/2,-np.sqrt(3)/2],color=G,s=80)
ax.set(aspect='equal',xlim=(-1.2,2.2),ylim=(-1.2,1.2),title='Two points have at most two common unit-circle centers');save(fig,s,'02-circles')
A=np.zeros((4,4),int)
for i in range(3):A[i,i+1]=A[i+1,i]=1
deg=A.sum(axis=1);marg=deg/6;joint=sum(deg[c]/6*np.outer(A[c]/deg[c],A[c]/deg[c]) for c in range(4));assert np.allclose(joint.sum(axis=0),marg)
mi=sum(joint[i,j]*np.log(joint[i,j]/(marg[i]*marg[j])) for i in range(4) for j in range(4) if joint[i,j]>0)
fig,axes=plt.subplots(1,2,figsize=(9,3.4));axes[0].plot(range(4),[0]*4,'o-',color=T,ms=12)
for i in range(4):axes[0].text(i,.03,f'{i}: degree {deg[i]}',ha='center',fontsize=9)
axes[0].axis('off');axes[0].set_title('Four-point path as a toy incidence graph');axes[1].bar(np.arange(4)-.15,marg,.3,label='Endpoint of uniform directed edge',color=T);axes[1].bar(np.arange(4)+.15,[.25]*4,.3,label='Uniform vertex (different law)',color=G);axes[1].set_xticks(range(4));axes[1].legend(fontsize=7);save(fig,s,'03-edge-law')
fig,axes=plt.subplots(1,2,figsize=(9,3.8));matrix(axes[0],joint,'Two neighbors of the same random center',vmin=0,vmax=.25);matrix(axes[1],np.outer(marg,marg),'Independent endpoints with same marginals',vmin=0,vmax=.25);axes[0].images[0].set_clim(0,.25);axes[1].images[0].set_clim(0,.25);fig.suptitle(f'Toy wedge mutual information: {mi:.3f} nats',y=1.05);save(fig,s,'04-wedge')
rat=np.array([[2/5,2/7],[3/5,3/7]])
fig,ax=plt.subplots(figsize=(9,3.5));matrix(ax,rat,'Toy ratios λᵢⱼ = uᵢ/vⱼ: opposite products agree');ax.set_xticklabels(['v = 5','v = 7']);ax.set_yticklabels(['u = 2','u = 3']);ax.set_xlabel('(2/5)(3/7) / [(2/7)(3/5)] = 1',labelpad=12);save(fig,s,'05-rectangle')
fig,axes=plt.subplots(1,2,figsize=(9,3.5));pnts=np.array(list(itertools.product([-np.sqrt(2),np.sqrt(2)],[-np.sqrt(3),np.sqrt(3)])))
axes[0].scatter(pnts[:,0],pnts[:,1],s=80,color=T);axes[0].set(title='Independent: √2 and √3',xlabel='First radical',ylabel='Second radical')
axes[1].scatter([-np.sqrt(2),np.sqrt(2)],[-np.sqrt(8),np.sqrt(8)],s=80,color=G);axes[1].plot([-2,2],[-4,4],':',color=G);axes[1].set(title='Dependent: √8 = 2√2',xlabel='First radical',ylabel='Second radical')
for ax in axes:ax.axhline(0,color='gray',lw=.6);ax.axvline(0,color='gray',lw=.6)
save(fig,s,'06-radicals');checks[s]={'grid_points':9,'unordered_unit_pairs':len(edges),'edge_marginal':marg.tolist(),'wedge_joint':joint.tolist(),'wedge_mutual_information_nats':mi,'rectangle_cross_ratio':str((F(2,5)*F(3,7))/(F(2,7)*F(3,5)))}

s='sensitivity'
def fn(x):return int((x[0] and x[1]) or (x[2] and x[3]))
def flip(x,block):return tuple(1-v if i in block else v for i,v in enumerate(x))
def sen(x):return sum(fn(flip(x,{i}))!=fn(x) for i in range(4))
def bs(x):
 good=[mask for mask in range(1,16) if fn(flip(x,{i for i in range(4) if mask>>i&1}))!=fn(x)]
 best={0:0}
 for mask in good:
  for used,count in list(best.items()):
   if not mask&used:best[mask|used]=max(best.get(mask|used,0),count+1)
 return max(best.values())
inputs=list(itertools.product([0,1],repeat=4));assert max(map(sen,inputs))==2 and max(map(bs,inputs))==2
fig,ax=plt.subplots(figsize=(9,3.6));states=[(0,0,0,0),(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(0,0,1,1)];arr=np.array(states);matrix(ax,arr,'f(x) = (x₀ AND x₁) OR (x₂ AND x₃)',cmap='Blues');ax.set_yticklabels(['Start: f=0']+['One flip: f=0']*4+['Block {0,1}: f=1','Block {2,3}: f=1']);ax.set_xlabel('Input-bit index');save(fig,s,'01-blocks')
fig,ax=plt.subplots(figsize=(9,3.4));d=np.arange(6)
for radius,col in [(0,B),(1,T),(2,G)]:ax.step(d,(d<=radius).astype(int)+radius*1.4,where='mid',color=col,label=f'Accept distance ≤ {radius}')
ax.set(xlabel='Distance to nearest chosen center',ylabel='Acceptance (rows offset for clarity)',title='A one-step distance change crosses one integer boundary');ax.legend(fontsize=9);save(fig,s,'02-thresholds')
fig,ax=plt.subplots(figsize=(7,4.2));ang=np.pi/2+2*np.pi*np.arange(5)/5;pos=np.stack([np.cos(ang),np.sin(ang)],axis=1)
for i in range(5):
 for jump in [1,2]:
  j=(i+jump)%5;ax.annotate('',xy=pos[j]*.91,xytext=pos[i]*.91,arrowprops={'arrowstyle':'->','color':T,'alpha':.55})
 ax.scatter(*pos[i],s=380,color=B);ax.text(*pos[i],str(i),ha='center',va='center',color='white')
ax.set(aspect='equal',xlim=(-1.3,1.3),ylim=(-1.2,1.3),title='A five-row toy tournament: every pair has one direction');ax.axis('off');save(fig,s,'03-tournament')
M=81;r=9;R=np.array([[16,1,0,3],[M*M,r,0,0],[16,0,0,3],[0,r,M*M,0]],int);initial=np.array([3,243,0,0]);nxt=R@initial
fig,ax=plt.subplots(figsize=(8,4));matrix(ax,R,'Source recurrence coefficients at M = 81, r = 9');ax.set_xticklabels(['S₀ previous','S₁ previous','J₀ previous','J₁ previous'],rotation=15);ax.set_yticklabels(['S₀ bound','S₁ bound','J₀ bound','J₁ bound']);save(fig,s,'04-profiles')
fig,ax=plt.subplots(figsize=(9,3.5));d=np.arange(1,25);bound=2.**d/(4*(d+2)**2);ax.semilogy(d,bound,'o-',color=T);ax.axhline(1,color=G,ls='--',label='A seed must beat 1');ax.set(xlabel='Depth d (choose M ≥ 9^(d+1) afterward)',ylabel='Guaranteed lower bound on bs(f)/s(f)²',title='The paper’s depth-dependent ratio is unbounded');ax.legend(fontsize=9);save(fig,s,'05-ratio')
outer=[{0,1},{2}];inner=[{0,1},{2}];grid=np.zeros((3,3),int)
for i,C in enumerate(outer):
 for j,D in enumerate(inner):
  for a,b in itertools.product(C,D):grid[a,b]=1+2*i+j
fig,ax=plt.subplots(figsize=(7,3.8));matrix(ax,grid,'Two outer blocks × two inner blocks = four disjoint blocks',cmap='viridis');ax.set(xlabel='Inner raw-bit coordinate',ylabel='Outer child index');save(fig,s,'06-composition');checks[s]={'toy_sensitivity_max':2,'toy_block_sensitivity_max':2,'zero_sensitivity':sen((0,0,0,0)),'zero_block_sensitivity':bs((0,0,0,0)),'recurrence_M81_initial':initial.tolist(),'recurrence_upper_step':nxt.tolist(),'depth9_ratio':str(F(2**9,4*11**2))}

s='matrix-multiplication';A=np.array([[1,2],[3,4]]);Bmat=np.array([[5,6],[7,8]]);C=A@Bmat;assert C.tolist()==[[19,22],[43,50]]
fig,axes=plt.subplots(1,3,figsize=(10,3.3));
for ax,a,title in zip(axes,[A,Bmat,C],['A','B','AB: row meets column']):matrix(ax,a,title)
save(fig,s,'01-product')
fig,ax=plt.subplots(figsize=(9,3.5));coef=np.full((2,4),0)
for i,j in itertools.product(range(2),range(4)):coef[i,j]=i+j
matrix(ax,coef,'C(2,4): each input pair contributes to output index z = i+j');ax.set(xlabel='Second-input index j',ylabel='First-input index i');save(fig,s,'02-polynomial')
fig,axes=plt.subplots(1,2,figsize=(9,3.6))
for ax,shared in zip(axes,[True,False]):
 for h,col in [(0,B),(1,T)]:
  yx=.5 if shared else h;ax.plot([0,1,2],[yx,h,h],color=col,lw=2);ax.scatter([0,1,2],[yx,h,h],color=col,s=120)
  ax.text(1,h+.13,f'y{h}',ha='center');ax.text(2,h+.13,f'z{h}',ha='center')
 if shared:ax.text(0,.7,'x shared',ha='center')
 else:
  for h in [0,1]:ax.text(0,h+.13,f'x{h}',ha='center')
 ax.set(xlim=(-.4,2.4),ylim=(-.3,1.5),title='Only Y and Z separate' if shared else 'All three legs separate');ax.axis('off')
save(fig,s,'03-shared-leg')
M=3;counts=np.zeros((M,M),int);weights=np.full((M,M),np.nan);surv=[]
for g,h,u,v in itertools.product(range(1,M+1),repeat=4):
 if u-v+2*(g-h)==0:
  w=g*g+h*u-h*h-h*v;assert w==(g-h)**2;counts[g-1,h-1]+=1;weights[g-1,h-1]=w;surv.append((g,h,u,v,w))
assert sum(w==0 for *_,w in surv)==M*M and all((g==h and u==v)==(w==0) for g,h,u,v,w in surv)
fig,axes=plt.subplots(1,2,figsize=(9,3.5));matrix(axes[0],counts,'Fourier survivors for each pair of labels');matrix(axes[1],np.nan_to_num(weights,nan=-1),'Weight (g − h)²; −1 means no survivor')
for ax in axes:ax.set(xlabel='True sector h − 1',ylabel='Tentative label g − 1')
save(fig,s,'04-separation')
fig,ax=plt.subplots(figsize=(9,3.7));ax.set(xlim=(-.5,4.5),ylim=(3.5,-.5),xticks=range(5),yticks=range(4),xlabel='Output coefficient index z',ylabel='Second-input index y',title='C(2,4): six terms survive, two cross-sector terms vanish')
kept=[]
for y in range(4):
 for x in range(2):
  z=x+y;w=int(y in [1,2])-int(z==2);assert w>=0;col=G if w else [B,T,T,B][y];ax.scatter(z,y,s=550,marker='x' if w else 's',color=col);ax.text(z,y-.18,f'x{x}',ha='center');kept.append(w==0)
assert sum(kept)==6;save(fig,s,'05-sectors')
fig,ax=plt.subplots(figsize=(9,3.6));a=np.arange(1,101);H=[F(1)]
for m in range(1,100):H.append(H[-1]*(1+F(1,3*m)))
D=np.array([float((3*n-1)*h/2) for n,h in zip(a,H)]);assert all(h**3>=int(n) for n,h in zip(a,H))
ax.loglog(a,D,label='Recurrence lower bound',color=T);ax.loglog(a,a**(4/3),'--',label='a^(4/3)',color=B);ax.loglog(a,(2*a-1)**(4/3),':',label='Interpolation ceiling at t = 3/4',color=G);ax.set(xlabel='Polynomial input length a',ylabel='Bounds, not measured character values',title='Lower and upper growth constrain the exponent');ax.legend(fontsize=9);save(fig,s,'06-growth')
checks[s]={'matrix_product':C.tolist(),'separation_M3_survivors':len(surv),'weight_zero_terms':sum(w==0 for *_,w in surv),'three_sector_survivors':sum(kept),'exact_growth_checks':len(H)}
(ROOT/'example-checks.json').write_text(json.dumps({'scope':'Finite examples and source formulas; not full theorem verification.','papers':checks},indent=2)+'\n')
print('Generated 30 mathematical figures; all example checks passed.')
