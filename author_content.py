"""Model-authored reading text. Run to materialize the editable content.json files."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
P={}
def chapter(title,figure,caption,body,source):return dict(title=title,figure=figure,caption=caption,body=body,source=source)
P['van-der-waerden']={
 'title':'How long can a coloring hide a progression?',
 'subtitle':'An illustrated reader for superexponential van der Waerden bounds',
 'source_title':'Quantitative Superexponential Bounds for van der Waerden Numbers',
 'intro':r'''Color the positive integers with two colors. A run of equally spaced numbers is an arithmetic progression: $2,5,8$ has common difference three. A progression is monochromatic when all its entries have the same color, even if other colors occur between them. How long can an interval be colored before a monochromatic progression becomes unavoidable?

This is an avoidance problem, so a long successful coloring proves a \emph{lower} bound. It says that the unavoidable point lies farther away. It does not say that every coloring of that length succeeds. The quantifiers are the heart of the question.

The source claims a construction whose avoided length grows superexponentially in the required progression length. Its argument combines circular coordinates, arithmetic dilation, geometric squared norms, probability, and a digit construction. This guide builds the intuition with small examples before explaining how those ingredients connect. The tiny colorings are checks of definitions, not miniature versions of the full asymptotic proof.''',
 'claim':r'''The source's Theorem 1.1 states that one absolute threshold $K_0$ works for all $r\ge2$ and $k\ge K_0$:
\[W_r(k)>k^{ck\lfloor\log_2r\rfloor},\qquad c=10^{-5}.\]
Here $W_r(k)$ is the least interval length forcing a monochromatic $k$-term progression in every $r$-coloring. For fixed $r$, the source concludes $W_r(k)^{1/k}\to\infty$. The charted formula supplies no numerical value for $K_0$.''',
 'chapters':[
 chapter('Read the quantifiers through an eight-position example','01-coloring','An exhaustively checked coloring of eight positions avoids all monochromatic three-term progressions. The lower rows illustrate three possible spacings; all spacings are checked by the script.',r'''Start with the displayed eight-position coloring. A contiguous run is only one possible progression: step two and step three count too. To check the coloring, list every $a,a+d,a+2d$ with $d\ge1$ and $a+2d\le8$, then inspect the three colors. The script performs this complete check, rather than checking only the three rows drawn.

It also enumerates every binary coloring of nine positions and finds that none avoids every three-term progression. These two finite statements give $W_2(3)=9$: a witness at eight proves $W_2(3)>8$, while exhaustive failure at nine proves $W_2(3)\le9$.

\paragraph{Why this is not the large theorem.} The source addresses arbitrary sufficiently large $k$. A finite search can settle this tiny case but cannot establish an eventual growth law for every larger $k$. The source instead describes families of colorings and bounds all the ways a bad progression could occur.

\paragraph{Try it.} Does a red-blue-red alternating coloring avoid a monochromatic three-term progression? No: positions $1,3,5$ already share a color. Regular-looking colorings can create the very patterns we want to avoid.''','Section 1: definition of W_r(k) and Theorem 1.1.'),
 chapter('A circle has no cut; a coordinate interval does','02-circle','The residues 0, 5, 10, 2, 7 follow a constant step modulo 13. Representatives in an interval jump at the cut; their unwrapped values 0, 5, 10, 15, 20 remain affine.',r'''A cyclic group is a clock with a chosen number of positions. Adding five on a thirteen-position clock moves by the same amount every time. Yet the written representatives jump from ten to two because the display resets after twelve. Confusing the representatives with the underlying circular motion loses information.

The source uses a much larger cyclic group of order $q^D$. Its coordinate maps are $x_i(n)=n/q^i\pmod1$ and a second family $y_i(n)=\lambda x_i(n)$. A coordinate mesh records which short interval contains each coordinate. In the second family the intervals become finer near the cut, where an apparently short circular step can become a large change of real representative.

The proof needs a controlled alternative: a progression has enough of both outer colors, or its centered representatives follow a globally affine line. The little clock illustrates the obstacle, not a proof of that alternative. Getting a consistent lift in all coordinates is an obligation discharged by the paper's mesh and short-period arguments.

\paragraph{Vocabulary.} Affine means ``starting point plus step times index'': $u+jv$. A lift chooses real representatives for circular coordinates in a consistent way.''','Sections 2 and 5: cyclic coordinates, adaptive mesh, balanced-or-affine alternative.'),
 chapter('Squared norm turns a line into a quadratic','03-norm','For the toy affine points (j,1), the squared norm is j²+1. A circle of a fixed radius meets this line at at most two points.',r'''For a vector $(x,y)$, its squared Euclidean norm is $x^2+y^2$. On the horizontal line $(j,1)$ it becomes $j^2+1$, which is quadratic rather than linear. The five points in the diagram therefore have squared norms $5,2,1,2,5$. Equal norm values occur symmetrically on the two sides of the nearest point to the origin.

More generally,
\[\|u+jv\|^2=\|u\|^2+2j\langle u,v\rangle+j^2\|v\|^2.\]
The coefficients are fixed once the line is fixed. This limited structure helps count possible norm patterns along a progression.

The actual construction attaches a random flip to a key made from a coordinate box and an integer squared-norm band. Repeated occurrences of the same key reuse the same random bit. They are not fresh independent coin tosses. The source proves that each key occurs at most four times along the relevant progression and controls how many distinct key words need consideration.

Our exact-circle picture has at most two intersections. It does not replace the source's four-occurrence result for boxes and rounded bands. Its role is to show why squared norms supply usable structure.''','Section 6: norm-indexed perturbation; Section 1 construction overview.'),
 chapter('A dilation removes troublesome small periods','04-periods','In this arithmetic example, λ=144 contains the full powers of 2 and 3 needed for every h≤24. The reduced denominator h/gcd(h,144) is either 1 or greater than 4.',r'''Think of a rational circular step $t/h$. Multiplying by $\lambda$ changes it to $\lambda t/h$, whose reduced denominator is
\[s=\frac{h}{\gcd(h,\lambda t)}.\]
If $\lambda$ contains all the relevant prime-power factors of $h$, that denominator collapses to one: the rational motion vanishes on the circle. Otherwise its remaining prime factors can be forced to be large.

For the plot, take $h\le24$, cutoff four, $t=1$, and $\lambda=2^4 3^2=144$. A denominator of twelve collapses to one; ten leaves five; twenty-one leaves seven. There are no remaining denominators two, three, or four. Every plotted value is computed with integer gcd arithmetic.

The source makes the analogous choice with a growing dimension $D$, cutoff $D^2$, and all potential periods up to $2\lceil k^{1/2}\rceil$. Lemma 2.1 proves that the residual period is one or exceeds $D^2$. This creates a clean separation of scales for the later geometric tests.

The sample parameters explain the arithmetic mechanism only. They are not a valid instance of all the source's simultaneous large-$k$ parameter requirements.''','Lemma 2.1 and equations (2.1)-(2.3).'),
 chapter('Many bad events can still have total probability below one','05-probability','The plotted ratio (k^0.9 log k)/k^0.95 tends to zero. It compares exponent scales from the proof overview, omitting constants; it is not a computed probability of success.',r'''Suppose there are $N$ bad events, each with probability at most $e^{-B}$. Even if the events overlap, the union bound gives probability at most $Ne^{-B}$ that any occurs. Writing $N=e^A$ reveals the useful comparison: $e^{A-B}<1$ when $A<B$. Independence is not needed for that final union bound, although it matters when estimating each event.

The source organizes progressions by their label and key words so that identical words do not get counted repeatedly as different constraints. Its overview gives a logarithmic count $O(k^{9/10}\log k)$, compared with the rare-flip scale $pk=k^{19/20}$ for $p=k^{-1/20}$. Their ratio tends to zero because $\log k$ grows more slowly than $k^{1/20}$.

This convergence is slow. The horizontal axis is already $\log_{10}k$, not $k$. A plot of the bare expressions is not a usable threshold for the source theorem: hidden constants and all other parameter conditions must hold too.

The proof also uses local tests and a finite local lemma in constructing its outer coloring. This schematic union-bound calculation explains the final scale comparison without asserting that the entire construction is one independent random coloring.''','Sections 3-6; overview on original page 3.'),
 chapter('Why the conclusion is stronger than beating one exponential','06-growth','The two-color lower-bound expression has logarithmic kth-root scale c log k. The constant line log 2 represents the kth root of 2^k. The source theorem applies only beyond its unspecified threshold.',r'''An exponential $A^k$ has constant $k$th root $A$. By contrast, $(k^{ck})^{1/k}=k^c$ grows without bound whenever $c>0$. Taking one more logarithm gives the straight line $c\log k$ in the figure. Even a tiny fixed positive $c$ eventually exceeds every constant exponential base on this scale.

This does not mean the bound is numerically impressive at everyday values of $k$. Here $c=10^{-5}$, and the theorem has an unspecified sufficiently-large threshold. The distinction between eventual growth and useful finite sizes is essential.

To pass from two colors to arbitrary $r$, the source uses a deterministic digit product. Combining $\lfloor\log_2r\rfloor$ binary color choices uses at most $r$ colors, which explains why that integer appears in the exponent. The transfer also has to control cyclic progressions and carries; simply writing binary labels is not the whole proof.

\paragraph{Check your understanding.} A successful coloring proves a lower bound on the unavoidable length. A theorem forcing a progression in every coloring proves an upper bound. Reversing those statements reverses the meaning of the result.''','Theorem 1.1 and Section 7: transfer to intervals and additional colors.')],
 'glossary': [('Arithmetic progression','Equally spaced terms with a positive common difference.'),('Monochromatic','All selected terms have the same color.'),('Cyclic group','Addition with wraparound modulo an integer.'),('Affine lift','Consistent real representatives of the form u+jv.'),('Union bound','The probability of any bad event is at most the sum of their probabilities.'),('Superexponential here','For fixed color count, the kth root of W_r(k) tends to infinity.')],
 'limits':r'''The guide checks the finite coloring search, the displayed period reductions, and the arithmetic behind the plots. It does not audit every mesh estimate, local-lemma dependency, word count, or cyclic-to-integer transfer. The original proof and bibliography follow unchanged in the expanded edition. Later coefficient refinements in separate repositories have their own assumptions and are not substituted for the source theorem here.'''}
P['sidorenko']={
 'title':'Can a structured graph contain fewer patterns than randomness?',
 'subtitle':"An illustrated reader for the proposed Sidorenko counterexample",
 'source_title':"A counterexample to Sidorenko's conjecture",
 'intro':r'''A graph is a collection of vertices and edges. A small graph can be used as a pattern to count inside a larger host graph. Sidorenko's question asks whether a bipartite pattern always appears at least as densely as the corresponding random benchmark with the same edge density.

``Appears'' has a precise meaning here: the count includes edge-preserving maps that send different pattern vertices to the same host vertex. We begin with this convention because replacing it by a count of distinct copies changes the problem.

The source claims a counterexample with a particular 35-vertex pattern. That pattern can be drawn and checked directly. The host graph that witnesses the deficit is reached through a much more elaborate weighted-kernel construction. Displaying the pattern alone is not displaying the whole counterexample. This reader separates the explicit combinatorics, the probability mechanism, and the difficult singular-configuration estimates.''',
 'claim':r'''Theorem 1.1 uses the incidence graph $H$ of 22 triples on 13 points. It states that there is a finite simple host $G$ with positive edge density for which
\[t(H,G)<p(G)^{66},\quad t(H,G)=\frac{\operatorname{hom}(H,G)}{|V(G)|^{35}},\quad p(G)=\frac{2|E(G)|}{|V(G)|^2}.\]
This is a claim about all homomorphisms, including noninjective ones. The finite examples below illustrate definitions and mechanisms; none is asserted to be that host $G$.''',
 'chapters':[
 chapter('Count maps, including repeated vertices','01-homomorphisms','For a three-vertex path mapped into a three-leaf star, there are 12 homomorphisms. Its density 12/4³ exceeds the benchmark (6/4²)².',r'''Label a three-vertex path by left endpoint, middle, and right endpoint. Once its middle maps to a host vertex of degree $d$, both endpoints can independently choose any of that vertex's neighbors. There are $d^2$ choices, including choices that give both endpoints the same image. Summing over host vertices gives $\operatorname{hom}(P_3,G)=\sum_v d(v)^2$.

The star has degrees $3,1,1,1$, so the total is $9+1+1+1=12$. Dividing by $4^3=64$ gives $3/16$. Its edge density in the source convention is $2\cdot3/4^2=3/8$, whose square is $9/64$. The path density is larger, as Sidorenko's inequality predicts for this pattern.

The denominator in $p(G)$ is $n^2$, not $n(n-1)$. It corresponds to two independent uniformly chosen vertices, with equal choices contributing no edge in a simple graph. The familiar proportion of unordered pairs that are edges is a different finite normalization.

A constant kernel of mean $p$ gives exactly $p^{|E(H)|}$. That is the clean benchmark used throughout. A finite random graph has additional effects from vertex collisions, so its finite homomorphism expectation should not be casually identified with that expression.''','Section 1: density definitions; Section 8 distinguishes injective counts.'),
 chapter('The actual pattern is a point-face incidence graph','02-incidence','Each dark cell is an edge of the source pattern. Every face column has three entries; the 13 point rows and 22 face columns represent 35 distinct vertices.',r'''A triple system is a list of three-element subsets of a set of points. Build a graph by making one vertex for every point and a different vertex for every triple, then joining a point to a triple exactly when the triple contains it. All edges run between the two kinds of vertices, so this graph is bipartite.

The figure is extracted from Table 1 of the original TeX source. It has 22 columns, each with three entries, giving $22\cdot3=66$ edges. Its two parts have 13 and 22 vertices, giving 35 in all. A point labeled zero and a face labeled zero are still different vertices.

The script also enumerates unordered pairs of points within the triples. There are 33 such pairs, and every pair occurs in exactly two faces. Thus the $22\cdot3=66$ face-pair occurrences are paired up exactly. This double occurrence is what allows a sign used on one face to interact with its counterpart on another.

The source needs additional finite properties: connectedness, special face exposure orders, bit-label separation, and color refinement that distinguishes vertices. Our simple incidence-count checks do not establish all those properties; Section 2 gives the certificates used in the argument.''','Section 2, Table 1 and Proposition 2.1.'),
 chapter('Averaging one random sign retains a four-incidence interaction','03-parity','Faces 0 and 1 share points 0 and 1. Averaging the product over an independent uniform sign η removes the linear terms and retains 1+AB.',r'''Let $\eta$ be equally likely to be $+1$ or $-1$. Then $E\eta=0$ and $\eta^2=1$. For fixed signs $A$ and $B$,
\[E[(1+\eta A)(1+\eta B)]=1+AB.\]
Expanding gives $1+\eta(A+B)+AB$; the middle term averages to zero. If $AB=1$, the result is two. If $AB=-1$, it is zero.

In the source, $A$ is the product of two incidence signs on one face and $B$ is the corresponding product on the other face containing the same point pair. The remaining $AB$ term therefore involves four incidences. A pair that occurs on only one selected face would instead leave no such interaction.

This identity by itself produces a nonnegative factor, not the theorem's strict negative correction. The kernel construction combines selected active coordinate supports, opposite sign biases, and type weights. It arranges cancellation of simpler moments while making a particular combined correction negative. The large finite-field model must then approximate the intended sign calculation with sufficiently controlled error.

\paragraph{Takeaway.} Averaging can erase unwanted terms while retaining a higher-order dependency. The important question is exactly which terms survive, not whether the ingredients look random.''','Section 1 negative-correlation overview and Section 3 activation construction.'),
 chapter('A kernel is a table of edge probabilities','04-kernel','A two-type toy kernel has within-type probability 0.8 and between-type probability 0.2. Its edge mean is 0.5, but its four-cycle density is 0.0706 rather than 0.0625.',r'''Assign each sampled vertex a type. A kernel $W(a,b)$ tells us the probability of an edge between vertices of types $a$ and $b$. The diagram uses two equally likely types. Averaging its four entries gives $(0.8+0.2+0.2+0.8)/4=0.5$.

For a pattern, independently assign a type to every pattern vertex, multiply the edge probabilities along all its edges, and average over type assignments. For a four-cycle in this equal-weight two-type example, this is $\operatorname{tr}(W^4)/2^4=353/5000=0.0706$. The constant-$0.5$ kernel gives $0.5^4=0.0625$. Same edge mean, different higher-order pattern density.

This is a positive four-cycle example and does not disprove Sidorenko. Its purpose is to show what information the edge mean fails to record. The source's much larger kernel is built for its special 35-vertex pattern, first in an oriented rectangular form and then in a symmetric form suitable for sampling an ordinary graph.

Once a strict kernel deficit is established with controlled approximation, a sampling argument can retain it in a finite simple graph. That transfer is a theorem-level step in the source, not evidence provided by our two-by-two table.''','Section 1 kernel definitions; Section 3 construction and finite-host transfer.'),
 chapter('Small probability does not imply a small weighted contribution','05-weighted-tail','A toy event has probability 1/q but weight q², so its contribution to the expectation is q. The two curves deliberately move in opposite directions.',r'''Suppose a rare event occurs with probability one in a million but contributes a trillion when it occurs. Its average contribution is one million. Rarity alone does not justify discarding it.

The source faces this issue for singular matrix differences. Their probability is $O(q^{-1})$, but normalized rank-layer indicators can grow with $q$. Multiplying probability by a large weight can defeat the naive probability bound. The necessary claim is that the \emph{weighted total} tends to zero.

The paper represents symmetric matrices by Lagrangian graph subspaces. The kernel of a matrix difference becomes an intersection of two subspaces. This translates rank defects into dimensions that can be counted. Global profile estimates, propagation through the connected complex, and special treatment of equality cases are then used to obtain strict decay.

The plot is deliberately generic: $q^{-1}\cdot q^2=q$. It is not the actual singular-tail exponent of the construction. It explains why that long analytic and combinatorial part of the paper cannot be replaced by ``singular matrices are rare.''

\paragraph{Check your understanding.} If the event weight were bounded by a constant, a probability tending to zero would suffice. The difficulty is the interaction between rare events and growing weights.''','Sections 5-7; the singular-contribution discussion on original page 3.'),
 chapter('One strict deficit can be amplified, with a density caveat','06-amplification','If an initial normalized pattern-density ratio were 0.9, independent tensor powers would give 0.9^m. The displayed 0.9 is illustrative, not a measured ratio for the source host.',r'''Suppose a constructed host or kernel has normalized ratio $\rho=t(H,W)/(EW)^{66}<1$. Tensoring independent copies multiplies both the pattern densities and the relevant powers of edge means. The new ratio is $\rho^m$, which tends to zero.

The curve uses $\rho=0.9$ simply to make the multiplication visible. Ten copies give about $0.349$; thirty give about $0.0424$. This is the logic behind a result saying the normalized ratio can be made smaller than any prescribed positive constant.

However, the edge density can change under this operation. Arbitrarily strong relative deficit with varying density is different from a fixed deficit at one positive limiting density. The source states these as separate consequences and uses balanced blow-ups for the injective-copy formulation.

Its forcing-conjecture consequence is different again: it constructs a nonconstant kernel whose edge and special-pattern densities match the constant benchmark at one density, while another statistic detects nonrandom structure. Matching a selected pair of measurements need not force full quasirandomness.

These consequences depend on the original strict deficit and the corresponding transfer arguments. The geometric decay calculation alone does not supply a counterexample.''','Section 8 and Corollaries 1.2-1.3.')],
 'glossary':[('Bipartite graph','Vertices split into two parts; every edge crosses between the parts.'),('Homomorphism','An edge-preserving vertex map; repeated images are allowed.'),('Incidence graph','A graph joining points to the subsets containing them.'),('Kernel / graphon','A weighted model of edge probabilities and pattern densities.'),('Singular matrix','A matrix with a nontrivial kernel, hence deficient rank.'),('Quasirandom','A graph sequence whose fixed-pattern densities approach random-model densities.')],
 'limits':r'''Verified examples include source-table extraction, incidence counts, pair multiplicities, the path count in a star, and the two-type kernel calculation. The rank-layer limit, weighted singular estimates, and finite-host transfer are substantial proof obligations not independently certified here. In particular, no small explicit host graph with the claimed deficit is supplied by this guide.'''}
P['unit-distances']={
 'title':'How many pairs of points can be exactly one unit apart?',
 'subtitle':'An illustrated reader for the planar unit-distance upper bound',
 'source_title':'A power saving for planar unit distances',
 'intro':r'''Place finitely many distinct points in the plane and connect pairs at distance exactly one. A square grid supplies many such pairs, but a cleverly arranged configuration might supply more. The problem asks for an upper bound valid for every configuration, not just the grid.

The source claims a fixed improvement below the exponent $4/3$. It argues by contradiction: if configurations approach that exponent arbitrarily closely, their incidence structure would force an impossible algebraic pattern. The route passes through probability laws, information, arithmetic height, and independent signs of square roots.

Those topics can sound remote from a picture of points. The diagrams below trace why each enters: circles encode unit pairs, sampling laws describe which local views are typical, height controls arithmetic size, and a rectangle of ratios packages the final obstruction. The small examples make these objects concrete without pretending to reproduce the full asymptotic contradiction.''',
 'claim':r'''Theorem 1.1 states that there are absolute constants $C>0$ and $1\le\beta<4/3$ such that $u(n)\le Cn^\beta$ for every nonnegative integer $n$, where $u(n)$ is the largest possible number of unordered unit-distance pairs among $n$ distinct planar points. The source establishes existence of a fixed gap; it does not give a numerical value of that gap in this theorem.''',
 'chapters':[
 chapter('Count unordered pairs and exclude the diagonals','01-grid','A 3×3 integer grid has six horizontal and six vertical unit pairs. Diagonal neighbors have distance √2 and are excluded.',r'''There are $\binom92=36$ unordered pairs among nine points, but only twelve are at distance exactly one. In each of three rows there are two horizontal unit segments, giving six. The same count in columns gives six vertical segments. Diagonals are too long.

For a $k\times k$ grid, the same argument gives $2k(k-1)$ unit pairs among $n=k^2$ points. This is a construction lower bound: the maximum $u(n)$ is at least this count at those sizes. It is not an upper bound for arbitrary planar configurations.

The source counts unordered pairs in its headline theorem. Its incidence representation later uses ordered pairs and therefore counts each geometric unit segment twice when both copies of the point set are retained. A factor of two changes a constant, not the exponent, but keeping the conventions straight prevents mistaken numerical examples.

\paragraph{Why an exponent matters.} A bound $Cn^{4/3-\delta}$ with fixed $\delta>0$ eventually beats any fixed multiple of $n^{4/3}$. The statement concerns growth for large $n$, not a claim that the formula accurately predicts the maximum for nine points. Neither the constant nor an explicit gap is derived by the grid illustration.''','Section 1: u(X), u(n), and Theorem 1.1.'),
 chapter('Turn distance equations into circle incidences','02-circles','The unit circles centered at (0,0) and (1,0) meet at (1/2, ±√3/2). Those are the two possible centers one unit from both points.',r'''A point $p$ is one unit from a center $q$ precisely when it lies on the radius-one circle around $q$. This turns pair counting into point-curve incidence counting: count the occasions when a point lies on one of the circles.

Two distinct circles meet in at most two points. Reversing the viewpoint, two distinct points have at most two common unit-circle centers. In the example, solving $x^2+y^2=1$ and $(x-1)^2+y^2=1$ gives $x=1/2$, then $y=\pm\sqrt3/2$.

These bounded intersections help control the incidence graph. The source samples circles to cut the plane into regions meeting relatively few remaining circles, then keeps a graph piece with useful degree and expansion properties. Its handling of boundaries ensures that retained points are assigned consistently.

The elementary two-circle fact does not alone yield the claimed power saving. It supports the incidence reductions that make the later information and algebraic arguments possible. In particular, replacing the carefully retained graph by an arbitrary subset can change its sampling laws and destroy the properties used afterward.''','Section 2.2: point-circle incidences and the cutting construction.'),
 chapter('A random edge does not produce a uniform random vertex','03-edge-law','In a four-vertex path, the endpoint marginal of a uniformly chosen directed edge is (1,2,2,1)/6. The middle vertices are twice as likely as the endpoints.',r'''Choose one of the six directed edges of a four-vertex path uniformly, then look at its first vertex. A vertex occurs once for each incident edge, so its probability is proportional to its degree. The two end vertices have probability $1/6$ and the two middle vertices $2/6$.

Choosing one of the four vertices uniformly would instead give probability $1/4$ each. These experiments are different. An argument that resamples a vertex must preserve the required marginal, not substitute whichever distribution seems convenient.

The source consistently starts with a uniform retained edge. Point and center marginals are degree weighted. A prediction is sampled from the point marginal conditioned on agreeing with recorded test outcomes. Averaging over those histories preserves the original point marginal, an elementary conditional-probability fact with important consequences here.

The short-history argument must also keep a fresh test independent of the entire existing experiment. Allowing that test to depend on a prediction after seeing it would change the claim. The small path teaches the probability bookkeeping; it does not establish the source's low-information or prediction bounds for its dense incidence pieces.''','Sections 2-3: retained-edge law and conditional-copy prediction.'),
 chapter('Sharing a center creates dependence between neighbors','04-wedge','Left: choose a degree-weighted center, then two neighbors independently conditional on that center. Right: choose endpoints independently from their common marginal. The matrices differ.',r'''A wedge is a two-edge path with a specified center. The endpoints are independent once that center is known, but usually not independent after the center is hidden. Both endpoints carry information about the same latent choice.

For the toy path, first choose center $c$ with probability $\deg(c)/6$, then select two neighbors with replacement, each uniformly from that center's neighbors. The joint probability is
\[P(i,j)=\sum_c\frac{\deg(c)}6\frac{A_{ci}}{\deg(c)}\frac{A_{cj}}{\deg(c)},\]
where $A$ is the adjacency matrix. Summing a row or column recovers the degree-weighted endpoint marginal. Repeated endpoints are allowed in this sampling experiment.

Mutual information compares this joint law with the product of its marginals. The expression is\[\sum_{i,j}P(i,j)\log\frac{P(i,j)}{P(i)P(j)},\]omitting zero terms. Zero would mean independence. The displayed toy has a positive value computed from its finite table.

The source proves a much more specific estimate, $o(\log t)$, for wedge endpoints in the retained configurations along its contradiction sequence. Our four-vertex calculation does not model that limit. It explains what quantity is being bounded and why conditional independence is not enough by itself.''','Section 2: wedge law and mutual information; Section 3 prediction.'),
 chapter('A rectangle cancels shared multiplicative factors','05-rectangle','For the toy ratios λᵢⱼ=uᵢ/vⱼ, multiplying opposite corners and dividing gives one exactly. The source obtains small height for analogous rectangle products.',r'''Suppose a table has entries $\lambda_{ij}=u_i/v_j$. Around a two-by-two rectangle,
\[\frac{\lambda_{ij}\lambda_{i'j'}}{\lambda_{ij'}\lambda_{i'j}}=1.\]
Every row factor and every column factor cancels. Taking logarithms turns this into cancellation of alternating sums. This is why rectangles can detect whether pairwise quantities nearly split into endpoint contributions.

The source uses ratios of complex unit-edge jumps through selected centers. It builds a dense pair graph in which individual ratios have large arithmetic height, while every retained rectangle product has height small relative to a growing scale. The exact cancellation in our rational table is a teaching model for that comparison, not a unit-distance configuration realizing the source's hypotheses.

Arithmetic height measures algebraic size across all normalized absolute values of a number field. It is not Euclidean distance, decimal length alone, or the logarithm of one complex modulus. The product formula connects these different absolute values.

A key extraction step removes errors in a height-weighted measure before choosing a common height band. As in any weighted average, rare but very large errors cannot be dismissed by their probability alone.''','Sections 4-7: product formula, scale, and height-weighted rectangle extraction.'),
 chapter('Independent square-root signs provide an obstruction','06-radicals','Over the rationals, √2 and √3 admit four independent sign choices in their common field. For √2 and √8, the relation √8=2√2 allows only two linked choices.',r'''The expression $\sqrt2$ has two algebraic conjugates, $+\sqrt2$ and $-\sqrt2$. In the field containing both $\sqrt2$ and $\sqrt3$, their signs can be changed independently while fixing rational numbers. The four plotted points encode those choices.

By contrast, $\sqrt8=2\sqrt2$. Any transformation fixing rational numbers and preserving multiplication must flip those two radicals together. There are only two possibilities, on the displayed line. Writing two square-root symbols does not guarantee two independent signs.

In the final source argument, radicals arise from pair-distance identities. The proof constructs valuations that are odd on one radicand and zero on the others, ensuring the needed independence over the relevant coefficient field. It then changes an unused radical's sign in differentiated equations and obtains a contradiction. Excluding popular unit circles removes a geometric case that would interfere with that independence.

These rational examples explain the logic of independent versus linked radicals. They do not prove independence for the source's much larger field or its chosen points. Those algebraic and generic-position obligations are the core of Section 8.

The conclusion rules out all sequences approaching the exponent $4/3$ closely enough, which yields an unspecified fixed power saving.''','Section 8: generic configurations, valuations, and radical sign changes.')],
 'glossary':[('Incidence','A point lies on a specified curve.'),('Degree-weighted marginal','A vertex probability proportional to the number of incident edges.'),('Wedge','Two edges sharing a sampled center.'),('Mutual information','Relative entropy of a joint distribution from the product of its marginals.'),('Arithmetic height','A measure of algebraic size using all normalized absolute values.'),('Independent radicals','Square roots whose signs can be changed independently over a specified base field.')],
 'limits':r'''The checked grid, probability tables, and rational rectangle identity are educational examples. This guide does not verify the cutting bounds, prediction theorem, height extraction, generic-position argument, or radical-independence proof. No numerical value of the source's exponent improvement is invented, and no comparison with a claimed current best lower bound is needed for this reading edition.'''}
P['sensitivity']={
 'title':'One switch versus a whole group of switches',
 'subtitle':'An illustrated reader for sensitivity and block sensitivity',
 'source_title':'A superquadratic separation between sensitivity and block sensitivity',
 'intro':r'''A Boolean function takes a string of zeros and ones and returns a single zero or one. Sensitivity asks how many individual input bits can reverse that answer at a given input. Block sensitivity allows groups of bits to flip together, but requires the groups to be pairwise disjoint.

The maximum over all inputs is crucial. A function may be completely insensitive at the all-zero string yet very sensitive somewhere else. A proposed global separation must compare the two global quantities, not just convenient values at one input.

The source claims that block sensitivity can grow faster than every constant multiple of sensitivity squared. Its construction keeps many disjoint ways to activate the function while controlling individual-bit changes at all inputs. Nested predicates and a directed tournament organize that control; tracking joint changes of two predicates closes the recursive argument.''',
 'claim':r'''Theorem 1.1 states that for every $C>0$ there is a nonconstant total Boolean function $f$ with $\operatorname{bs}(f)>Cs(f)^2$. More precisely, the construction yields
\[\frac{\operatorname{bs}(f)}{s(f)^2}\ge\frac{2^d}{4(d+2)^2}\]
for every integer depth $d\ge1$, with sufficiently large construction parameters chosen afterward. The source also amplifies a fixed seed into a power separation with exponent greater than two. This does not contradict the polynomial Sensitivity Conjecture resolved by Huang.''',
 'chapters':[
 chapter('A local gap is not a global separation','01-blocks','For f=(x₀ AND x₁) OR (x₂ AND x₃), no single flip changes f at zero, but either of two disjoint pair flips does. Exhaustive checking gives global sensitivity 2 and block sensitivity 2.',r'''At input $0000$, the displayed function outputs zero. Changing one bit cannot make either AND pair true, so $s(f,0000)=0$. Flipping bits $\{0,1\}$ together makes the first pair true; flipping $\{2,3\}$ makes the second pair true. The blocks are disjoint, so $\operatorname{bs}(f,0000)=2$.

That sounds like a large contrast until we ask for the maximum sensitivity across every input. At $1010$, either currently missing partner can activate one of the pairs. Two individual bits are sensitive there. Exhaustive enumeration of all sixteen inputs confirms $s(f)=2$ and $\operatorname{bs}(f)=2$.

The example therefore supplies intuition for cooperative flips but no superquadratic separation. Dividing the local block count by the squared local sensitivity at zero would be meaningless for the theorem.

\paragraph{Disjointness matters.} Blocks cannot share raw input coordinates. Otherwise many overlapping descriptions of the same decisive change would artificially inflate the measure. The source explicitly builds disjoint block families and separately bounds sensitivity at every input, including inputs far from its convenient all-zero witness.''','Section 1 definitions; Section 2.4 disjoint blocks at zero.'),
 chapter('Nested predicates create distinct boundaries','02-thresholds','The curves accept distances at most 0, 1, and 2. Their vertical offsets separate the drawing; each predicate itself takes only the values zero and one.',r'''A predicate is a yes-or-no test. A family is nested when every input accepted by a stronger test is also accepted by a weaker one. For example, being within distance zero of a center implies being within distance one, which implies being within distance two.

The source starts with separated centers in a Boolean cube and tests the Hamming distance to the nearest center. Hamming distance counts differing bits. Flipping one raw bit changes that nearest-center distance by at most one: this follows from the triangle inequality, in both directions.

Distinct integer radii give distinct boundaries. A one-unit distance change cannot cross two such boundaries at once, so the initial joint sensitivities vanish. Joint sensitivity counts bits that reverse two distinct predicates simultaneously from the same initial value.

The nesting is in the \emph{predicate index}, not in the input coordinates. These predicates need not be monotone Boolean functions under changing zeros to ones. Confusing those two meanings of monotonicity would invalidate the argument.

The plotted distance axis is a summary of a high-dimensional cube, not its geometric embedding. The source's separated centers are chosen so local sensitivity can also be bounded near each acceptance region.''','Sections 2.1 and 2.3: initial predicates and Lemma 2.2.'),
 chapter('A tournament gives every pair of rows one direction','03-tournament','This five-row cyclic tournament is a small structural illustration. Each row has two outgoing neighbors. It is not the paper’s labeled tournament with k=2M²+1 and M≥3.',r'''A tournament orients every edge of a complete graph: for two different rows, exactly one points toward the other. The picture uses five rows so the entire orientation remains visible. It is an indexing device, not a competition simulation.

In the source, each row contains several child inputs. A clause for row $i$ requires all targets in its own row to accept. For every outgoing edge $i\to j$, it also requires a chosen child in row $j$ to fail a weaker predicate. The edge label specifies which child is tested. The parent accepts if any row clause holds.

All conditions within one clause use distinct children. One raw-bit flip therefore changes at most one condition of that clause. If a rejecting clause becomes true after one flip, it must have had exactly one failing condition beforehand.

For clauses failing only one gate, the induced tournament has outdegree at most one. If there are $m$ such clauses, counting edges gives $m(m-1)/2\le m$, hence $m\le3$. The source combines this observation with a forbidden-label condition that controls the clauses failing one target.

The directed structure limits candidate repairs. Random labels alone are not the entire sensitivity proof.''','Sections 2.2 and 3: recursive clauses and candidate-clause counting.'),
 chapter('Track joint sensitivity alongside ordinary sensitivity','04-profiles','The coefficient matrix displays the four inequalities from Proposition 3.1 at M=81 and r=9. Entries multiply previous-level upper bounds; they are not measured sensitivities.',r'''The recursion tracks four quantities: ordinary sensitivity at output zero and one, $S_0,S_1$, and joint sensitivity at output zero and one, $J_0,J_1$. The row labeled $S_0$ reads
\[S_0^{\rm new}\le16S_0^{\rm old}+S_1^{\rm old}+3J_1^{\rm old}.\]
The other rows show the remaining inequalities. Every coefficient is nonnegative, which permits upper bounds to be propagated consistently.

Why introduce $J$? Repairing a gate in a row whose strongest predicate already accepts may require both that strongest predicate and a weaker one to reverse. Counting all such flips by ordinary sensitivity would lose the saving. Joint sensitivity records the more restrictive event.

The source chooses a very large $M$ relative to the intended depth, normalizes the four sequences, and proves a coupled induction. The displayed $M=81$ satisfies the stated size requirement at depth one; it is not a parameter choice for arbitrarily deep recursion.

These are upper-bound recurrences. Equality is neither asserted nor needed. At the final level there is only one parent predicate, so its actual joint profiles vanish even if a generic propagated upper bound remains positive.''','Proposition 3.1 and Section 4 normalization.'),
 chapter('An exponential numerator eventually beats a quadratic denominator','05-ratio','The plotted source lower bound 2^d/[4(d+2)²] exceeds one at d=9 and tends to infinity. The construction dimension also grows enormously with the required parameter choices.',r'''The source builds many disjoint sensitive blocks at zero and bounds global sensitivity everywhere. After an OR of disjoint copies balances the zero and one cases, its estimates give
\[s(f)\le2(d+2)M^{d+1},\qquad \operatorname{bs}(f,0)\ge M^2(2M^2+1)^d.\]
Dividing yields at least $2^d/[4(d+2)^2]$. The powers of $M$ cancel in this ratio, while the extra factor roughly two per level survives.

At $d=9$, the displayed lower bound is $512/484=128/121>1$. That supplies a depth at which the claimed construction can produce a seed beating the quadratic ratio. It does not provide a small truth table: the source requires $M\ge9^{d+1}$ and uses $n=(d+2)M^2(kr)^d$ raw bits, with $k=2M^2+1$ and $r=\lceil\sqrt M\rceil$.

For an arbitrary proposed constant $C$, first choose a depth making the ratio exceed $C$, then choose the remaining parameters. Reversing that order and holding a small $M$ fixed would not follow the proof.

The chart is a plot of a proven expression within the source argument, not experimental measurements of giant Boolean functions.''','Theorem 1.1 proof, equations (7)-(10).'),
 chapter('Composition multiplies disjoint block witnesses','06-composition','Each color labels one Cartesian-product block. Two disjoint outer blocks and two disjoint inner blocks give four pairwise disjoint raw-coordinate blocks.',r'''In a composition $f\circ g$, each input bit of $f$ is replaced by the output of a separate copy of $g$. A raw bit can change the final answer only if it changes its child and the corresponding outer coordinate is sensitive. This gives $s(f\circ g)\le s(f)s(g)$.

At the zero input, assuming $g(0)=0$, disjoint sensitive blocks combine by Cartesian products. If $C_i$ is a block of outer child indices and $D_j$ a block of raw positions within a child, use $C_i\times D_j$. Distinct pairs $(i,j)$ remain disjoint. Flipping that set changes exactly the children in $C_i$, triggering the outer witness.

The colored grid makes this disjointness visible. It is a coordinate bookkeeping example; the block shapes are not extracted from a gigantic seed.

If one fixed seed has $b=\operatorname{bs}(f,0)>s(f)^2$ and $f(0)=0$, repeated composition gives block sensitivity at least $b^m$ and sensitivity at most $s(f)^m$. Thus the exponent $\alpha=\log b/\log s(f)$ exceeds two. This is how a strict finite ratio becomes an unbounded family with a fixed power separation.

The construction of a suitable seed remains indispensable; composition cannot manufacture the strict inequality from our introductory four-bit toy.''','Lemma 4.2 and Corollary 4.3.')],
 'glossary':[('Total Boolean function','A zero-or-one output defined on every binary input of its fixed length.'),('Sensitivity at x','Number of individual bits that reverse the value at x.'),('Block sensitivity','Maximum number of disjoint nonempty flip sets that each reverse the value.'),('Joint sensitivity','Bits that reverse two distinct predicates simultaneously.'),('Tournament','An orientation of every pair of distinct vertices.'),('Composition','Replace each outer input bit by an independent child function output.')],
 'limits':r'''The four-bit toy is exhaustively checked at every input, including a disjoint-block search. The recurrence coefficients and displayed depth ratio are checked arithmetically. This is not a reconstruction or exhaustive evaluation of the source's huge seed, nor an independent audit of its arbitrary-input recurrence proof. The source's attribution to earlier work, including Meiburg's tournament architecture, remains in the reproduced manuscript.'''}
P['matrix-multiplication']={
 'title':'How can a matrix product require fewer multiplications?',
 'subtitle':'An illustrated reader for the source’s 9/4 exponent argument',
 'source_title':'An Upper Bound of 9/4 for the Matrix Multiplication Exponent',
 'intro':r'''A matrix is a rectangular table of numbers. Matrix multiplication combines each row of the first table with each column of the second. The familiar method performs about $n^3$ scalar multiplications for two $n\times n$ matrices, but algebraic identities can reuse intermediate products and reduce the asymptotic exponent.

The source claims an upper bound of $9/4$ over the complex numbers. Its route is indirect: encode bilinear computations as tensors, study numerical invariants called characters, derive inequalities for polynomial multiplication, and use those inequalities to constrain matrix multiplication.

This is not a benchmark report or an implementation ready to replace a numerical library. The theorem is in an arithmetic-operation model, and its asymptotic algorithm can have constants depending on a desired accuracy in the exponent. The figures focus on actual coefficient arrays and the finite separation mechanism, then explain the final growth comparison.''',
 'claim':r'''Theorem 1.1 states that for every $\varepsilon>0$, two $n\times n$ complex matrices can be multiplied in $O_\varepsilon(n^{9/4+\varepsilon})$ scalar arithmetic operations. Equivalently, the source claims $\omega\le9/4$. It does not assert a practical finite-size crossover, a bit-complexity bound of that form, or a competitive floating-point implementation.''',
 'chapters':[
 chapter('Every output entry is a row-column dot product','01-product','The displayed product is [[19,22],[43,50]]. For example, its upper-left entry is 1×5+2×7=19, not the entrywise product 1×5.',r'''To compute one output entry, multiply matching entries of a row and column and add. For the upper-left entry, $(1,2)$ meets $(5,7)$, giving nineteen. The other three entries are $1\cdot6+2\cdot8=22$, $3\cdot5+4\cdot7=43$, and $3\cdot6+4\cdot8=50$.

For $n\times n$ matrices, there are $n^2$ outputs and $n$ products per output, so this direct method uses $n^3$ scalar multiplications. Faster algebraic algorithms change the organization of the calculation rather than the meaning of the result.

A bilinear algorithm first forms linear combinations of the first input and of the second input, multiplies selected pairs of those combinations, then combines the results linearly. A tensor records the coefficients of such a bilinear map. For matrix multiplication the trilinear form is $\sum_{i,j,k}x_{ij}y_{jk}z_{ki}$, where the third variable group records the output pairing.

The three variable groups are called legs. They are not spatial axes or three stages of execution. Keeping track of which variables belong to each leg is essential when combining or separating computations.''','Sections 1-2: arithmetic exponent, tensors, and equation (2.2).'),
 chapter('Polynomial multiplication has a concrete coefficient pattern','02-polynomial','The C(2,4) array has eight input products. A cell (i,j) contributes to output coefficient i+j, producing output indices 0 through 4.',r'''Multiply a polynomial with two coefficients by one with four coefficients. Each first-input coefficient $x_i$ multiplies each second-input coefficient $y_j$, and the result contributes to coefficient $i+j$:
\[C(2,4)=\sum_{i=0}^{1}\sum_{j=0}^{3}x_i y_j z_{i+j}.\]
The table shows exactly which output coordinate receives each product. Equal numbers lie along the relevant anti-diagonals.

For general input lengths $a,b$, the output length is $a+b-1$. Evaluating both polynomials at that many distinct points, multiplying the values, and interpolating gives a rank upper bound of $a+b-1$. The source uses the output flattening to match it with a lower bound, hence $R(C(a,b))=a+b-1$.

Tensor rank is the smallest number of simple bilinear products needed to represent the map, after allowing linear combinations of inputs and outputs. This ordinary tensor rank is not the matrix-multiplication exponent. Its role is to bound the character values of a convenient test family. A character is normalized, additive on full direct sums, multiplicative on tensor products, and monotone under restrictions.

Those properties make characters useful numerical witnesses, but a detecting-character theorem is also needed to connect bounds on all such witnesses back to the matrix-multiplication problem.''','Section 4, equations (4.1)-(4.5); Lemma 2.2.'),
 chapter('Shared variables prevent a full direct sum','03-shared-leg','Left: x·y₀z₀+x·y₁z₁ shares its X variable. Right: x₀y₀z₀+x₁y₁z₁ uses independent variables on all three legs. These are different tensors.',r'''Suppose two useful blocks already have separate second-input and output variables but share the first-input space. They cannot yet be treated as a full direct sum. In a full direct sum, every block has its own variables on every leg.

The left illustration has one common $x$. Relabeling it $x_0$ in one term and $x_1$ in the other would grant an extra independent input without paying for it. It is not a free change of notation. Tensor constructions must implement such separation through legal linear substitutions, copies, and degenerations.

Proposition 3.1 begins with $M$ sectors sharing their first leg. It uses $5M$ copies of the input tensor and produces $M$ fully independent blocks, each carrying an additional $M$-dimensional dot product. The source counts both the copies used and the auxiliary factor retained.

The extra dot-product dimension is not another collection of independent direct-sum blocks. Confusing these multiplicities would overstate the construction's gain. In tensor powers, the balance between the number of sectors and this retained factor yields the entropy inequality used later.''','Proposition 3.1 and Corollary 3.2.'),
 chapter('A Fourier filter and a square enforce matching labels','04-separation','For M=3, the left table counts tuples surviving u−v+2(g−h)=0. Surviving terms have weight (g−h)²; weight zero requires g=h and then u=v.',r'''The finite construction gives the shared leg a tentative sector label $g$, while the other legs know the true sector $h$. Auxiliary indices $u,v$ run from one to $M$. Summing phases over $L=5M$ roots of unity kills all terms except those satisfying
\[u-v+2(g-h)=0.\]
The index range is smaller than $L$, so equality modulo $L$ here means actual integer equality, not an accidental wraparound.

Next the source gives the three legs weights $g^2$, $hu-h^2$, and $-hv$. On a surviving term their sum is
\[g^2+hu-h^2-hv=(g-h)^2.\]
It is nonnegative, and its minimum zero occurs exactly when the tentative and true labels agree. The filter then also forces $u=v$, leaving the desired dot product.

The script exhaustively enumerates all $3^4$ index tuples in this example and checks the identity and zero-weight condition. It does not numerically approximate roots of unity to decide equality.

This finite calculation illustrates the proposition. Its asymptotic use also requires the source's interpolation passage from degenerations to character inequalities and its tensor-power counting argument.''','Proposition 3.1 and Lemma 2.3.'),
 chapter('The three sectors are visible in the support','05-sectors','For a=2 and h=1, the source’s shifted-tripling construction uses C(2,4). Two supported terms receive weight +1 and vanish; six remain in three matched sectors.',r'''A supported term satisfies $z=x+y$. In this example, the left second-input sector is $y=0$, the middle is $y=1,2$, and the right is $y=3$. The corresponding output sectors are $z=0,1$, then $z=2$, then $z=3,4$.

Give weight $+1$ to middle $Y$ coordinates, weight $-1$ to middle $Z$ coordinates, and zero elsewhere. The term $x_0y_1z_1$ has weight one, as does $x_1y_2z_3$. They disappear in the minimum-weight degeneration. Every other supported term has weight zero; none has negative total weight.

The surviving outer blocks have the shape $C(2,1)$. The middle has exchanged second and third legs and a reversed first-leg basis. This individual-branch identification is not permission to apply incompatible first-leg maps to the shared input of the whole tensor.

The paper combines all six permutations of the legs in a symmetrized character profile. Permutation factors then balance correctly, yielding $P(a,3h+a-1)\ge3P(a,h)$. The little support diagram explains the finite sectors; the profile inequality also uses the shared-leg entropy result.''','Lemma 4.2 and original Figure 1.'),
 chapter('Compare forced growth with an interpolation ceiling','06-growth','The curves show bounds from the discrete growth argument, not sampled values of an unknown tensor character. At t=3/4, the interpolation ceiling has the same asymptotic power 4/3.',r'''The source defines a positive symmetric profile $P(a,b)$ from all six permuted character values. It has boundary $P(1,b)=b$, concave successive increments in each variable, and the shifted-tripling inequality. Together these imply $P(a,a)\ge a^{4/3}$.

One intermediate sequence satisfies $H_1=1$ and
\[H_a\ge\prod_{m=1}^{a-1}\left(1+\frac1{3m}\right).\]
Cubing each factor bounds it below by $1+1/m$, whose product telescopes to $a$. The script checks this finite product inequality exactly over the plotted range. The source proves it for every positive integer.

Interpolation separately gives $P(a,a)\le(2a-1)^{1/t}$. If $t>3/4$, its exponent $1/t$ would be smaller than $4/3$, eventually contradicting the lower bound. Thus $t\le3/4$, giving character values on matrix multiplication at most $n^{9/4}$.

The detecting-character argument then bounds exact-rank exponents. Finally, a fixed rank decomposition is recursively applied to matrix blocks, with padding for arbitrary sizes and an arbitrarily small exponent allowance. These last bridges are essential: a favorable plot of an abstract profile does not itself provide an algorithm or prove the headline theorem.''','Lemma 5.1, Theorem 1.1 proof, and Appendix A.')],
 'glossary':[('Bilinear map','Linear in either input when the other input is fixed.'),('Tensor leg','One of the three variable groups in a trilinear encoding.'),('Full direct sum','Independent variables for each component on all three legs.'),('Degeneration','Retain minimum-weight terms after parameterized substitutions.'),('Character','A normalized additive, multiplicative, restriction-monotone tensor invariant.'),('Arithmetic exponent','An asymptotic power counting scalar operations, with arbitrary positive exponent slack.')],
 'limits':r'''The guide checks its numerical matrix product, finite Fourier-label conditions, three-sector support, and finite product inequalities. It does not independently prove the shared-leg construction for every tensor, the determinant-filtration lemma, spectral separation, or the source's final algorithmic claim. The separate matrix-sector refinement repository studies an abstract obstruction with its own hypotheses; it is not substituted for this newer manuscript's argument.'''}
for slug,p in P.items():
 (ROOT/'papers'/slug/'content.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print('Wrote five source-specific reading texts, each with six illustrated chapters.')
