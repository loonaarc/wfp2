Read status: 🟢 analysed — the framework/model/complexity chapters read and
analysed in full; the solution-algorithm chapters (4–8) are out of scope (see the
scope note below), as this project uses Dec-POMDPs as vocabulary, not machinery.

<!--
Scope note: this is a ~140-page SpringerBrief. These notes cover the Preface,
Chapter 1 (Multiagent Systems Under Uncertainty), and Chapter 2 (The Dec-POMDP
Framework) in full, plus Chapter 3's optimality/policy sections and the complexity
result in Section 3.5. The solution-algorithm chapters (4-8) were not read in depth
and are out of scope for this note. Every claim below is grounded in those pages.
-->

## Citation

Oliehoek, Frans A., and Christopher Amato. *A Concise Introduction to Decentralized POMDPs.* SpringerBriefs in Intelligent Systems (Artificial Intelligence, Multiagent Systems, and Cognitive Robotics). Springer International Publishing, 2016. ISBN 978-3-319-28927-4 (print), 978-3-319-28929-8 (eBook). DOI 10.1007/978-3-319-28929-8. Authors: F. A. Oliehoek (University of Liverpool) and C. Amato (MIT CSAIL).

## What It Is

A short, self-described "concise" graduate-level book that formally defines the **decentralized partially observable Markov decision process (Dec-POMDP)** and surveys methods for solving it. The Dec-POMDP is a model for **planning** the behaviour of a **team of fully cooperative agents** (they share one reward) that act in a **stochastic, partially observable** environment and — crucially — each act on **only their own local observations**, with no free communication assumed (Ch. 2). It generalises the single-agent MDP (fully observable) and POMDP (partially observable, one agent) to *n* agents.

Two framings to keep straight:
- It is a **planning** framework, not a learning one: the model (transition, observation, reward probabilities) is assumed **known**, and the task is to compute good policies offline (contrast with reinforcement learning, where the model is unknown; §2.1.1).
- "Solving" a Dec-POMDP means finding a **joint policy** (one policy per agent) that maximises an optimality criterion (e.g. expected cumulative reward). The book is largely about how hard that optimisation is and how to do it.

The book distinguishes three sources of uncertainty the model handles (§1.3): **outcome uncertainty** (stochastic action effects), **state uncertainty** (partial observability, i.e. noisy/limited sensors and *perceptual aliasing*), and **multiagent uncertainty** (each agent is uncertain about what the others observed and will do). The last is not a substitute for partial observability but is *added on top* of it: even if agents could instantaneously share all their observations, the joint observation would still generally not reveal the true state.

## The Dec-POMDP Model

The core formal object (Definition 2, §2.2). A Dec-POMDP is a tuple

**M_DecP = ⟨D, S, A, T, O, 𝒪, R, h, b⁰⟩**

where (taking the book's wording directly):

- **D = {1, …, n}** — the set of *n* agents.
- **S** — a finite set of **states** of the environment.
- **A = ×_{i∈D} A_i** — the set of **joint actions**, the Cartesian product of the individual action sets. **A_i** is the set of actions available to agent *i* (may differ per agent). At each stage *t* every agent *i* takes an individual action *a_{i,t}*; together these form one joint action *a = ⟨a₁, …, aₙ⟩*. Agents know only their own action — they **do not observe each other's actions**. A_i is assumed independent of stage/state.
- **T** — the **transition (probability) function**, specifying Pr(s′ | s, a): the probability of moving to next state *s′* given current state *s* and joint action *a*.
- **O = ×_{i∈D} O_i** — the set of **joint observations**; **O_i** is the observation set of agent *i*. Each step the environment emits one joint observation *o = ⟨o₁, …, oₙ⟩*, of which **agent *i* sees only its own component *o_i***.
- **𝒪** — the **observation (probability) function**, specifying Pr(o | a, s′): the probability of joint observation *o* given the joint action *a* just taken and the resulting state *s′*.
- **R : S × A → ℝ** — the **immediate reward function**, mapping a state and joint action to a real number. It gives only the *immediate* reward; the *team* goal is defined by combining these over the horizon via a chosen optimality criterion. Note: agents are assumed **not to observe the rewards** during execution (observing them could leak state information; if rewards are meant to be seen they must be encoded into the observations).
- **h** — the **horizon**: the number of discrete time steps (stages) *t = 0, 1, …, h−1* over which the agents interact.
- **b⁰ ∈ Δ(S)** — the **initial state distribution** at *t = 0* (Δ(S) is the probability simplex over states).

Dynamics per stage (Fig. 2.4): the environment is in state *sₜ*; it emits a joint observation per 𝒪, each agent sees its own *o_i*; each agent picks an action; the resulting joint action causes a transition per *T* to *s_{t+1}*.

**Optimality criterion (Ch. 3).** The tuple alone does not fix the objective; one chooses a criterion. Finite horizon commonly uses the **undiscounted expected cumulative reward** E[Σ_{t=0}^{h−1} R(sₜ, aₜ)]; a **discounted** variant with factor 0 ≤ γ < 1 is also standard (and is needed to keep the value bounded in the infinite-horizon case).

**Policies (§3.2).** During execution each agent has access only to its own **action–observation history (AOH)** *θ̄_i,t = (a_{i,0}, o_{i,1}, …, a_{i,t−1}, o_{i,t})*. A key point: unlike a single-agent POMDP, an individual agent in a Dec-POMDP **cannot compress its history into a belief** — there is no known Markovian statistic to summarise the local history without sacrificing optimality, because *T* and 𝒪 are defined over *joint* actions/observations. So a policy π_i is a mapping from (observation) histories to actions, and a **joint policy** π = ⟨π₁, …, πₙ⟩ is a tuple of these. The decentralization constraint: a joint policy is *not* an arbitrary map from joint histories to joint actions — each agent's action may depend only on that agent's own history.

**A sharper, communication-explicit reformulation (§2.4.4).** The book notes the classic tuple is *underspecified* — it doesn't state what information agents may condition on. It therefore separates a **Markov Multiagent Environment (MME)** = ⟨D, S, A, T, O, 𝒪, R, h, b⁰⟩ (the environment) from an **agent component** that specifies each agent's *information states*, *information-state (belief-update) function* κ_i, *action-selection policy* π_i, and any *auxiliary observations* Z_i (e.g. from communication). A Dec-POMDP is then M_DecP = ⟨OC, M, m⟩ where the agent component sets **Z_i = ∅** — i.e. *no auxiliary observations*, so each agent acts on its **local actions and observations only**. Contrast: an **MPOMDP** is the same MME but with Z_i = observations of the others via instantaneous broadcast, so every agent shares a **joint belief**. This is the cleanest place the book pins down exactly what "decentralized" means.

## Why Decentralized Decision-Making Is Hard

Complexity results stated in the book (§3.5, and §2.4):

- **Number of joint policies is doubly exponential in the horizon *h*.** At stage *t* there are (|A_i|·|O_i|)^t possible histories; a policy assigns an action to each, so the count of individual policies is doubly exponential, and joint policies compound that across *n* agents. (The book tabulates e.g. Dec-Tiger with *h*=6 having ≈1.31×10⁶⁰ joint policies.)
- **Theorem 1 (Bernstein et al., 2002):** finding the optimal solution of a **finite-horizon Dec-POMDP with n ≥ 2 is NEXP-complete** (proof by reduction from the TILING problem). NEXP = nondeterministic exponential time; in practice, assuming NEXP ≠ EXP, solving takes **doubly exponential time** in the worst case.
- **Approximation is no escape (Rabinovich et al., 2003):** even finding an **ε-approximate** joint policy is **NEXP-complete**.
- **Infinite horizon is undecidable** (follows from the undecidability of infinite-horizon single-agent POMDPs, Madani et al., 1999).
- **Hardness comes from decentralization, not just hidden state.** A jointly/collectively observable Dec-POMDP is a **Dec-MDP** (Definition 3) — the *joint* observation identifies the state — yet its worst-case complexity is **still NEXP-complete** (Bernstein et al., 2002). The book's own gloss: "hardness comes from being distributed, not (only) from having a hidden state."

For comparison / context (the observability spectrum, §2.4):
- **Individually (fully) observable** — each agent's own observation identifies the state → reduces to a **centralized** model (MMDP; the underlying MDP is P-complete, though exponential in *n*).
- **Non-observable** — a single null observation, agents run open-loop; **NP-complete**.
- **Collectively observable** (Dec-MDP) and general partial observability — **NEXP-complete**.
- Centralized-with-communication baselines: an **MPOMDP** is a POMDP over joint beliefs (**PSPACE-complete**), "usually easier than solving a Dec-POMDP in practice."
- Even for Dec-MDPs, only very strong independence assumptions lower the class (Table 3.2): transitions **and** observations **and** rewards independent → P-complete; transitions and observations independent → NP-complete; **any** other subset → NEXP-complete.

Intuition (§3.2, §3.5): the two compounding costs are (1) evaluating a joint policy is exponential (a value per joint observation history), and (2) the number of joint policies is doubly exponential — and the deeper obstacle is that no agent has a Markovian summary of its local history to plan against.

## Relevance to This Project

Our project is a reproducible agent-based common-pool-resource (CPR) simulation with **rule-based** agents (not optimal, not learning). We already speak informally of "information models" — a **global-observation** model vs. a **private-observation** model. The Dec-POMDP formalism is useful here as **precise vocabulary and as a framing of difficulty**, not as machinery we run.

How it can sharpen our information-model definitions:

- **Our observation models map onto the book's observability spectrum.** The **global** model — every agent sees the full resource state — is (individual / full) observability, which the book says *reduces to a centralized model*; if global information is achieved by sharing rather than by direct sensing, it is exactly the **MPOMDP / joint-belief** case. The **private** model — each agent sees only a local component — is genuine partial observability: a **Dec-MDP** if the agents' observations *jointly* would pin down the state, or a full **Dec-POMDP** if not. Deciding which of these our "private" model actually is (do the private observations, if pooled, determine the state?) is a real, answerable design question the formalism forces us to state.
- **It gives us named slots for what we currently leave implicit.** The observation *set* O_i and observation *function* 𝒪 = Pr(o | a, s′) are precisely "what each agent can perceive and with what noise." Writing our information models as (O_i, 𝒪) — even informally — removes ambiguity about *what* an agent knows and *when*.
- **The MME / agent-component split matches our architecture.** The book separates the environment (MME) from an **agent component** that fixes each agent's information-state function κ_i and action-selection policy π_i. Our rule-based agents *are* a **fully specified agent component**: our hand-coded rule *is* π_i, and "global vs. private" is a choice of Z_i / O_i. In their terms, we **fix the agent component instead of optimizing it** — a clean way to describe, in the thesis, exactly how we differ from the standard Dec-POMDP setup.
- **The complexity results justify our methodological choice.** NEXP-completeness (and even NEXP-complete *approximation*, undecidability in the infinite horizon) is precisely why computing *optimal* decentralized policies under partial information is off the table for a bachelor-scale, reproducibility-first study. "Decentralized decisions under partial information are hard" is not a hand-wave — it is a theorem. Rule-based agents are a defensible response to that intractability, and the "hardness is from being distributed, not only from hidden state" result is a good sentence to cite when motivating why even simple decentralized coordination is non-trivial.

**Honesty / what we are NOT doing.** We do **not** solve Dec-POMDPs. We do not maintain beliefs or joint beliefs, do not optimize policies, and none of the NEXP/PSPACE machinery is executed anywhere in our code. Our agents apply fixed rules; the Dec-POMDP is a **descriptive lens** for stating our information assumptions rigorously and for explaining *why* the optimal version of our problem is intractable — nothing more. We should avoid implying our simulation "is a Dec-POMDP solver" or that our results speak to Dec-POMDP optimality.

**Verdict on adopting the notation (also in the summary below):** worth borrowing the *tuple vocabulary* (S, A_i, O_i, 𝒪, R, h, b⁰) and the *observability spectrum* to define our information models precisely and to cite the hardness result — this is genuinely clarifying and low-cost. Adopting the *full* apparatus (agent components, information-state functions, joint beliefs, formal policy trees) would be overkill for rule-based agents and risks implying a solver we don't have.

## Important Terms

- **Dec-POMDP** — decentralized POMDP: model for a *team* of cooperative agents acting under stochastic dynamics and partial observability, each acting on **local observations only**, no free communication.
- **Joint action / joint observation** — the tuple across all agents, *a = ⟨a₁,…,aₙ⟩*, *o = ⟨o₁,…,oₙ⟩*; each agent sees/controls only its own component.
- **Transition function T** — Pr(s′ | s, a). **Observation function 𝒪** — Pr(o | a, s′).
- **Horizon h** — number of decision stages. **b⁰** — initial state distribution over S.
- **Optimality criterion** — the rule (e.g. (discounted) expected cumulative reward) that turns per-stage rewards into one number to maximise; not part of the raw tuple.
- **Action–observation history (AOH)** — an agent's own sequence of actions and observations; the information a decentralized agent actually has.
- **Joint policy** — one policy per agent; decentralized ⇒ each agent's action depends only on its own history.
- **Perceptual aliasing** — different states producing the same observation, so the same reading may require different actions.
- **Observability classes** — *individually/fully observable* (→ centralized), *jointly/collectively observable* (= **Dec-MDP**), *non-observable*, and general *partial observability*.
- **Dec-MDP** — a jointly observable Dec-POMDP (pooled observations identify the state); still NEXP-complete.
- **MMDP / MPOMDP** — centralized baselines: multiagent MDP (state known to all) and multiagent POMDP (agents broadcast observations, share a **joint belief**).
- **MME (Markov Multiagent Environment) / agent component** — the book's split of "the world" from "the agents' information + policies," used to make the decentralization constraint (Z_i = ∅, no auxiliary observations) explicit.
- **NEXP-complete** — the worst-case complexity class of optimally solving finite-horizon Dec-POMDPs (n ≥ 2).

## Questions

- Is our "private-observation" model a **Dec-MDP** (pooled local observations would determine the resource state) or a genuine full **Dec-POMDP**? Answering this pins down which complexity class our idealized problem sits in and sharpens the write-up.
- Is our "global-observation" model better described as **full observability** (each agent directly senses the whole state) or as an **MPOMDP** (agents effectively share observations)? The distinction changes which baseline we're implicitly invoking.
- Should the thesis state our information models explicitly as (O_i, 𝒪) pairs in Dec-POMDP notation, or keep them prose-level? (Recommendation: a small formal table for precision, with an explicit disclaimer that we do not solve the model.)
- The book assumes rewards are *not* observed by agents. In our CPR sim, do agents "see" their payoff (harvest) and condition rules on it? If so, we differ from the standard Dec-POMDP assumption and should say so.
- We cite the NEXP-completeness result to justify rule-based agents. Do we ever risk over-claiming that our simulation results bear on *optimal* decentralized behaviour? (They do not — keep the descriptive/normative line clear.)
- Chapters 4–8 (solution methods, communication, factored models, RL) were not read in depth. Is any of the *factored / independence* structure (Table 3.2) worth reading later as a lens on how our resource/agent structure could in principle reduce coupling? Likely low priority for a rule-based study.
