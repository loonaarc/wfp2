# The Logic of Collective Action: Public Goods and the Theory of Groups

Read status: 🟢 read — Chapter I ("A Theory of Groups and Organizations," pp.
1–43, the theoretical core this project's mechanism is built from) read in
full, plus Chapter II sections A and C (pp. 52, 60–61, group-size effectiveness
and social incentives) for context. The later, largely case-study chapters
(labor unions, Marxist theory of class, orthodox pressure-group theory, the
"by-product"/"special interest" theory, ch. III–VI) were not read — they apply
the Chapter I logic to specific historical institutions (US labor law, farm
lobbies, professional associations) rather than adding new formal machinery,
and are not load-bearing for the mechanism this project builds. Scanned copy
supplied by the user (`references/papers/olsen1965.pdf`, no OCR text layer —
read directly as page images).

## 1. Citation
Olson, M. (1965). *The Logic of Collective Action: Public Goods and the Theory
of Groups*. Harvard University Press. (Harvard Economic Studies, vol. 124.)

## 2. Research Problem
The received view across economics, political science, and sociology — from
Aristotle's "men journey together with a view to particular advantage" through
1960s American "group theory" of politics — holds that a group of individuals
with a common interest will, if its members are rational, act to further that
interest, much as a single rational individual acts on his own behalf. Olson
asks whether this actually follows from the premise of rational, self-interested
behavior — and answers no: it does not follow, and is in fact usually false for
large groups.

## 3. Why the Problem Is Difficult
The intuitive argument for the traditional view seems airtight: if every member
of a group would gain from some common goal (a union's higher wage, a cartel's
higher price, a state's public order), and members are rational and
self-interested, surely they will act to secure it. The flaw is not obvious
because it requires distinguishing an individual's *total* stake in the group
goal from the *share of that goal's marginal cost* rational self-interest
actually weighs — a distinction the traditional theory collapses. Once a goal
is a genuine **public/collective good** (Olson's definition, p. 14: if any
member `X_i` of a group consumes it, it cannot feasibly be withheld from the
rest of the group), no member can be excluded from enjoying it regardless of
whether that member paid any of its cost — exactly the structure that breaks
the naive argument, but only becomes visible once "the group's interest" is
decomposed into who pays for it versus who benefits from it.

## 4. Proposed Method
A formal analogy between an organization pursuing a collective good and firms
in a market (pp. 9–12): just as a firm in a perfectly competitive industry has
no individual incentive to restrict its own output to raise the industry price
(its own output is too small a share of the market to matter, and it bears the
full cost of restricting alone), a rational member of a large group has no
individual incentive to contribute toward a collective good — their own
contribution is imperceptible to the outcome, and free others' contributions
(if the good is provided) accrue to them regardless. Formally: let `F_i` be
member `i`'s share of the total gain the group receives from the collective
good, `V_g` the total value of a given quantity of the good to the group, and
`C` the total cost of providing it. A member has an individual incentive to
provide the good unilaterally only when `F_i > C/V_g` (p. 33) — i.e., only when
that one member's own slice of the benefit alone exceeds the good's total cost
relative to its total value. **Group size matters because `F_i` shrinks as
group size grows** (more members splitting a fixed total benefit), so in a
"large" group no single `F_i` clears the bar and the good is not provided at
all without coercion or a **selective incentive** (p. 51: some separate,
excludable reward or penalty tied to individual contribution, not the
collective good itself).

**The mechanism specifically relevant to this project (pp. 27–36, "Small
groups"):** in a *small* group, some member's `F_i` can be large enough to
clear `F_i > C/V_g` even alone — that member will unilaterally provide the
good rather than go without it, and everyone else free-rides on their
provision. Crucially, `F_i` depends not just on group size but on member
*size* `S_i` — how much a given member individually benefits from a unit of
the good (p. 29: "An owner of vast estates will save more from a given
reduction in property taxes than the man with only a modest cottage... and
will have a larger `F_i`"). Where group members have unequal `S_i`, the
member with the largest `F_i` bears a **disproportionate share of the
burden**, because once that member has unilaterally purchased the amount they
individually want, no one else has any incentive to contribute more — "there
is a systematic tendency for 'exploitation' of the great by the small" (p.
29, Olson's own term; footnote 47 notes the word's moral connotation is
unintended, chosen only because it is the standard term for a disproportion
between benefits and sacrifices).

## 5. Experimental Setup
Not an empirical or simulation study — a purely analytical/logical argument
(supply-and-demand and Cournot-style market analogies, a formal marginal-cost/
marginal-benefit derivation for public-goods provision, pp. 22–36), illustrated
with historical and institutional examples (labor unions, cartels, the state)
developed at length in the book's later chapters, which were not read in
detail for this project (see Read status above).

## 6. Metrics
None in the simulation sense — the "results" are logical propositions (a
member provides the good iff `F_i > C/V_g`; suboptimality and disproportionate
burden-sharing follow from unequal `F_i`) rather than measured quantities.

## 7. Main Results
- **Large latent groups do not voluntarily organize to pursue their common
  interest**, however great the shared benefit, without either coercion (e.g.
  compulsory union membership, taxation) or a selective incentive distinct
  from the collective good itself (p. 2, p. 51).
- **Small groups can and sometimes do provide themselves with a collective
  good through independent, voluntary action alone** (p. 33) — but even then,
  the provided amount is generally suboptimal for the group as a whole unless
  members arrange to share marginal costs in exactly the proportion they share
  marginal benefits (p. 29), an arrangement that itself requires either
  coordination or luck.
- **Where group members are unequal in size/stake (`S_i`), the largest member
  bears a disproportionate share of the burden of providing the good — "the
  exploitation of the great by the small"** (p. 29) — because the smaller
  members' own `F_i` never clears the threshold for unilateral provision, so
  they free-ride entirely on the largest member's self-interested
  contribution.

## 8. Limitations
- The formal argument assumes **independent behavior** — it explicitly
  brackets strategic interaction and bargaining among group members
  (footnote 48, p. 29), which the author acknowledges can complicate small-
  group outcomes considerably, though he argues (footnote accompanying p. 30)
  that bargaining dynamics tend to reinforce, not reverse, the same
  disproportionate-burden conclusion.
- The book is squarely about the **decision to contribute to/provide** a
  collective good, not about **collective choice/voting** over the good's
  terms — Olson's own analysis has no vote, no rule-setting stage, and no
  concept of "voting weight." Any wealth-*weighted-vote* mechanism (as
  originally sketched for this project's item 11, before this reading) is
  Olson's own machinery applied to a decision Olson himself never models.
- No treatment of monitoring, sanctions, or enforcement of a collective
  agreement once made — the analysis stops at whether the good gets provided
  voluntarily at all, not at how (or whether) a provided rule gets enforced.

## 9. Future Work
Not stated as a dedicated section; the book's own later chapters (labor
unions, the state, orthodox and "by-product" pressure-group theories) are
themselves applications of the Chapter I/II logic to specific institutions,
not named open problems.

## 10. Relevance to This Project
- **The originally-sketched item 11 framing ("wealth-weighted collective
  choice": ADR-0011's one-agent-one-vote enforcement vote, made
  payoff-weighted, to test whether a high-payoff minority can vote down
  enforcement a healthy population would otherwise pass) does not match
  Olson's own mechanism, and should not be built as first sketched.** Olson's
  logic runs the *opposite* direction from plutocratic vote-capture: it
  predicts the *largest* stakeholder voluntarily *over*-contributes (bears a
  disproportionate share of the cost), not that wealth buys the power to
  block a common-interest outcome others want. Building a payoff-weighted
  vote would test a real and separate political-economy question (regulatory
  capture), but it would not be an application of Olson (1965) — see
  ADR-0020 for the resulting design pivot.
- **The `F_i > C/V_g` unilateral-provision result is directly and cheaply
  testable in this project's existing engine.** This project already has an
  exact analogue of "member size" `S_i`: `total_payoff` (an agent's
  accumulated wealth) and, more directly, a monitor's own stake in the
  resource surviving. A wealth-proportional willingness to unilaterally
  *fund monitoring* (rather than vote), where an agent's own probability or
  intensity of volunteering as a sanctioner scales with its own accumulated
  payoff (its own `F_i`-like stake in the pool's survival), is a direct,
  literature-faithful test of Olson's actual mechanism — and connects
  naturally to this project's own second-order free-rider thread (E3, E5,
  E12, E23): does the wealthiest agent become the de facto, self-interested
  monitor, exploited by everyone poorer, exactly as Olson predicts?
- **This reframes item 11 from a voting mechanism to a contribution
  mechanism** — closer in shape to E12's evolutionary pool-punishment
  machinery or E23's wealth-gate machinery than to ADR-0011's vote. See
  ADR-0020 for the concrete design.

## 11. Possible Follow-Up Contribution
Make the (already-evolutionary or already-fixed) probability that an agent
volunteers to `sanctioning` scale with its own relative accumulated wealth —
operationalizing `F_i` as an agent's own share of total population wealth (or
of the resource's own value to it) — and test whether (a) the wealthiest
agent ends up bearing a disproportionate share of monitoring cost relative to
its population share (Olson's "exploitation of the great by the small,"
directly measurable via existing `total_payoff`/Gini machinery), and (b)
whether this happens *without* coercion, i.e., purely from each agent's own
`F_i > C/V_g` calculation, reusing the E5/E11/E12 evolutionary-dynamics loop
rather than inventing new machinery.

## 12. Important Terms
- **Collective/public good** — a good such that if any member of a group
  consumes it, it cannot feasibly be withheld from the rest of the group (p.
  14). The shared resource pool's *sustained availability* (not the resource
  itself, which is rival) is this project's own collective good.
- **`F_i` (fractional share of group benefit)** — member `i`'s share of the
  total gain the group receives from a given amount of the collective good.
- **Selective incentive** — a separate, excludable reward or penalty tied to
  individual contribution, distinct from the collective good itself; the only
  thing (besides coercion) that can mobilize a *large* latent group (p. 51).
- **Exploitation of the great by the small** — the systematic tendency, in
  small groups with unequal-sized members, for the largest member to bear a
  disproportionate share of a collective good's cost, because everyone
  smaller free-rides on that member's own self-interested provision (p. 29).
- **Latent group** — a large group in which no single member's `F_i` clears
  the threshold for unilateral provision, and which therefore requires
  coercion or selective incentives to organize at all (used throughout ch.
  I, III).

## 13. Questions
- Olson's own worked examples (labor unions, cartels, national defense) are
  all *large-latent-group* cases; the small-group "exploitation" result (pp.
  27–36) is the more purely formal, less historically-illustrated part of the
  book — worth double-checking against a secondary source if the eventual
  E22 write-up leans heavily on the exact `F_i > C/V_g` inequality, since it
  is this project's single load-bearing citation from the whole monograph.
- The book predates, and is silent on, Ostrom (1990)'s empirical finding that
  many real commons *do* self-organize monitoring without collapsing into
  Olson's large-group prediction — worth a one-line cross-reference in the
  eventual ADR/report, since this project's own E3/E12 already show
  voluntary monitoring *can* be stabilized (evolutionarily, at a cost) in a
  large "group," a partial answer to the tension Olson's own theory raises
  but does not resolve.
