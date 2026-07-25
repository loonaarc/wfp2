# Cooperation Is Not Enough — Exploring Social-Ecological Micro-Foundations for Sustainable Common-Pool Resource Use

Read status: 🟢 noted from the published article (PLOS ONE, open access). Full-text
re-read recommended before citing specific figures.

## Citation
Schill, C., Wijermans, N., Schlüter, M., & Lindahl, T. (2016). Cooperation is not
enough — Exploring social-ecological micro-foundations for sustainable common-pool
resource use. *PLOS ONE*, 11(8), e0157796.
https://doi.org/10.1371/journal.pone.0157796

## Research Problem
Does cooperation among resource users guarantee *sustainable* common-pool-resource
(CPR) use? Behavioural experiments show cooperative groups sometimes still over- or
under-exploit, so cooperation and sustainability are not the same thing. The paper
asks what *additional* micro-level factors turn cooperation into sustainability.

## Why the Problem Is Difficult
Sustainability depends not just on willingness to restrain (a social preference) but
on *knowing* how much restraint the ecology requires — and that ecological knowledge
is uncertain, unevenly distributed, and held with varying confidence across a group.
Separating "wanting to cooperate" from "knowing the sustainable yield" is subtle.

## Proposed Method
An agent-based model grounded in CPR lab experiments. Agents communicate to form
group agreements on extraction, hold individual ecological knowledge with a
*confidence* level, update it from feedback, and choose group vs. individual
extraction based on trust and social preferences.

## Experimental Setup
Discrete logistic resource: **maximum stock 50, minimum 5, maximum sustainable yield
(MSY) ≈ 9 units/round**. Perfect information about dynamics is available in
principle; uncertainty arises from agents' varying *confidence* and from mismatches
between expected and actual stock.

## Metrics
Exploitation pattern (over/optimal/under), cooperative vs. non-cooperative outcome,
resource-stock trajectories, group knowledge development, individual confidence/trust.

## Main Results
- **Cooperation is necessary but not sufficient** for sustainability; the decisive
  extra factors are the *distribution of ecological knowledge* and *confidence* in
  it, plus social skills.
- A single informed, confident agent can pull a low-knowledge group toward optimal
  exploitation.
- Two confident agents with *conflicting* knowledge undermine sustainability.
- Low confidence among the uninformed can *help* — it promotes learning toward
  optimal levels.

## Limitations
Perfect-information experimental roots limit real-world transfer; simplified ecology
(no regime shifts / external uncertainty); knowledge-formation mechanism is one of
several possible.

## Future Work
Incorporate ecological regime shifts and external uncertainty; explore alternative
social-learning and knowledge-formation mechanisms.

## Relevance to This Project
**Directly challenges a hidden assumption in our model.** Our `cooperative` strategy
is sustainable *by construction* — we hand it `g` and `K` (perfect ecological
knowledge) and it harvests only the surplus. So in our current model
"cooperation ⇒ sustainability" is baked in, which this paper says is exactly the
conflation to avoid.

Crucially, our `private`/blind cooperator (which cannot see the stock and collapses
it when it starts depleted — hypothesis H1) is really an instance of *this paper's
thesis*: **cooperative restraint without adequate ecological information fails to be
sustainable.** This reframes our information axis as a knowledge axis and connects
our result to established literature.

## Possible Follow-Up Contribution
Separate the two ingredients our cooperative agent currently fuses: a **social
preference** (willingness to restrain/share) and **ecological knowledge** (an
estimate of the sustainable yield, with a confidence/error level). Then study *when
cooperative intent translates into sustainable outcomes* as a function of information
and (later) communication. This is bachelor-feasible, well-grounded, and sets up the
communication phase (can communication substitute for missing ecological knowledge?).

## Important Terms
Social-ecological system; ecological knowledge vs. social preference; confidence;
maximum sustainable yield (MSY); over-/under-exploitation.

## Questions
- How exactly do they parameterise "confidence", and could we adopt a simple version
  (a noisy/biased estimate of the sustainable share)?
- Is their discrete-logistic (max 50 / MSY 9) parameterisation worth matching so our
  results are comparable to this lineage?
