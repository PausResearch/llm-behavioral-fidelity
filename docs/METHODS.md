# Methods and interpretation

## Design and sample

The thesis compares five LLM conditions within one repeated exchange game. Each
condition contains six cohorts of six agents observed for 15 rounds: 30 cohorts,
180 agents, and 2,700 recorded allocation decisions. Primary analyses use rounds
1–12 (2,160 allocation decisions); rounds 13–15 are an endgame extension.
The human comparison uses an existing control sample with 12 cohorts and
72 participants from Teubner and Camacho (2023).

The model identifier recorded for every condition is `mistral-medium-3-5`.
Temperature is 0.7. Provider reasoning effort is `none` except in the high
reasoning condition. No new model calls are made by the public example code.

## Questions and comparisons

The main question is where the inherited LLM baseline differs from the human
control evidence, and whether interventions reduce those differences. This
contains a diagnostic question (RQ1: the baseline's behavioral and structural
limitations) and an intervention question (RQ2: changes under framing,
reasoning effort, and MRP).

- **H1, prompt framing:** one sentence emphasizing individual payoff
  maximization is added to the otherwise fixed game instructions. The
  expectation is some responsiveness, but limited correction of selective and
  adaptive behavior. Framing sensitivity in Lorè and Heydari (2024) motivates
  the test; this is a single framing contrast within this game.
- **H2, high reasoning:** the provider's reasoning effort changes from `none`
  to `high`, retaining the baseline game prompt. The expectation is reduced
  indiscriminate cooperation and more differentiated choices. Li and Shirado
  (2025) help motivate this expectation. The intervention operates through the
  provider setting; the study does not identify the model's internal reasoning
  algorithm or test a researcher-supplied chain-of-thought prompt.
- **H3, MRP:** factual history, periodic reflection, and a persistent plan are
  organized into a complete agent protocol while retaining the baseline game
  prompt. Expected signatures include heterogeneity, selective tie removal,
  reinforcement, rising reciprocity, and stronger responses to past partner
  behavior. Park et al. (2023) supply the architectural precedent. The effect
  of the whole protocol is assessed, rather than the isolated effect of each
  component. The reciprocity-trend result remains inconclusive.
- **Post hoc single-call control:** substantively similar reflection/planning
  tasks and the same factual record are used inside one allocation call,
  without persistent MRP state. The comparison probes whether wording alone
  accounts for the MRP pattern; persistence, separate calls, timing, and compute
  are not independently identified.

Intervention effects in `hypothesis_evidence.csv` compare with the LLM baseline
(or estimate the named slope interaction). Distances to human condition means
are a separate descriptive comparison. Moving an outcome toward the benchmark
does not establish equivalence to humans. The MRP relationship tests are post
hoc extensions of H3's relational expectations.

The conditions share the game rules, group size, number of rounds, model
identifier, temperature, and available factual feedback. They alter the
specified instructions, reasoning setting, or state organization. The human
benchmark is an existing experiment with a different decision interface, not
a concurrently randomized human arm. See [the source map](REFERENCES.md) for
what each cited work supports.

## Exchange game

Each participant receives 100 units of a distinct resource per round. Transfers
are non-negative integers, their sum cannot exceed 100, and self-transfers are
not allowed. Each positive outgoing transfer incurs a cost of one unit of
payoff. A participant's payoff equals the square root of the amount kept, plus
the sum of square roots of the amounts received from each other participant,
minus the total transaction cost.

The fixed group interacts repeatedly. Agents receive factual feedback about
exchange and payoff outcomes. The human benchmark is the paper's control
treatment; the thesis comparison does not manipulate profile images.

## What the outcomes mean

| Outcome | Definition |
| :--- | :--- |
| Total sent | Mean amount sent by one participant/agent in a round |
| Recipients | Mean number of partners receiving a positive transfer |
| Transfer per recipient | Mean of the allocation-level amount sent per active recipient, as defined in the archived analysis |
| Density | Active directed transfers divided by 30 possible directed ties in a six-person group |
| Reciprocity | Unordered pairs with transfers in both directions divided by unordered pairs with any positive transfer |
| Network value | Total group payoff normalized using the game's feasible integer minimum and maximum |

Recipient count and density are linked exactly: mean recipient count divided
by five equals density. They should not be treated as two independent sources
of evidence. Transfer per recipient is an average of allocation-level ratios;
it is not obtained by dividing the displayed mean total by the displayed mean
recipient count. The archive assigns zero intensity to zero-recipient rounds.

For network value, the group-payoff normalization uses
`minimum = 6 × (√96 + 4 × √1 − 5)` and
`maximum = 6 × (4 × √17 + 2 × √16 − 5)`.
The showcase uses the archived normalized means directly.

## Reading the gap figure

For condition mean `x`, human mean `h`, and baseline mean `b`, the displayed
ratio is `abs(x − h) / abs(b − h)`. A value below one means a smaller absolute
gap than the baseline. Zero means matching means. This calculation is undefined
when the baseline already equals the human mean.

The ratios are descriptive. They have no confidence intervals and do not
measure whether a condition is statistically equivalent to the human sample.
They are deliberately shown separately rather than averaged into a composite
score. The supplied code recalculates them from full-precision stored means.

## Relationship dynamics

The relationship results use adjacent-round transitions ending in rounds 2–12.
A directed tie is active when the sender gives the recipient a positive amount.

- **Retention:** fraction of previously active ties still active next round.
- **Cutting:** fraction of previously active ties inactive next round.
- **Formation:** fraction of previously inactive ties becoming active.
- **Reinforcement:** mean change in amount on ties active in both rounds.
- **Tie-set overlap:** directed Jaccard similarity of adjacent active-tie sets.

The included table averages cohort summaries with equal weight, matching the
final analysis. Missing formation rates are excluded where a cohort has no
previously inactive ties. Reinforcement follows the same sender–recipient pair;
it is distinct from a change in average transfer size over a changing set of
partners.

## Statistical evidence

The included hypothesis table is a direct export of the final analysis.
Effects describe differences from the LLM baseline or condition interactions,
depending on the named test. The table identifies the relevant outcome and
test; intervals and p-values should be read in that context.

For example, high reasoning reduces total sent by about 55.5 units relative to
baseline (95% interval: −61.0 to −50.0; within-hypothesis Holm-adjusted p < .001).
This is evidence of a change from baseline, not a direct equivalence test
against humans. Prompt framing's recipient-count difference is sensitive to
multiple-testing adjustment: raw p = .027, Holm-adjusted p = .163.

The research analysis includes random-effects models, cohort-level contrasts,
and exact permutation sensitivity checks. The six cohorts in each LLM
condition, rather than the thousands of repeated decisions, are the relevant
independent experimental units. The complete robustness analysis remains in
the research archive; the public scripts reproduce descriptive views only.

## Limits

The study was adaptive and exploratory, not preregistered. Several
relationship-level analyses and the single-call comparison are post hoc.
That comparison changes the organization of reflection/planning and state
persistence together; it cannot identify the causal effect of one MRP module.
The interventions also differ in computational cost, which this overview does
not estimate.

Results apply to the tested model, task, prompts, and recorded runs. Matching
means is weaker than matching distributions, individual behavior, and the
process that generates choices. A lagged association between received and
sent transfers is not by itself proof that memory caused later behavior.

## References

Full bibliographic entries and their roles in the design are in
[REFERENCES.md](REFERENCES.md). Teubner and Camacho provide the human game and
benchmark; Kral provides the original LLM implementation; Aher and colleagues
motivate comparison with human experimental evidence; Lorè and Heydari, Li and
Shirado, and Park and colleagues motivate the selected interventions.
