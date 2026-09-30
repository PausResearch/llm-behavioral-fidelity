# References and what they support

This is a focused source list for the public showcase. Each entry identifies
what the thesis takes from the source and what the present experiment tests.
All five LLM conditions are evaluated within one repeated gift-exchange game.

## Human game and benchmark

**Teubner, T., & Camacho, S. (2023).** Facing Reciprocity: How Photos and Avatars
Promote Interaction in Micro-communities. *Group Decision and Negotiation*,
32, 435–467. [Publisher and DOI](https://doi.org/10.1007/s10726-023-09814-4).

This is the empirical foundation: the repeated exchange game, human control
data, and network outcomes. The thesis examines the control treatment and uses
the paper's primary analysis window of rounds 1–12. Its human aggregates are
reconstructed from the control data. The paper also studies photographs and
avatars; those treatment effects are outside this thesis's tested scope.

## Original LLM implementation

**Kral, D. (2026).** *P1* [Research software; private repository], version
`1534a41ac07748724cf62b198046da9235de6c3c`. GitHub, `Sertorius73/P1`.

Daniel Kral provided the LLM recreation of the game and supervised the thesis.
Pau Kraus extended this foundation for the interventions and analysis. This is
a software attribution, not a claim that Kral published a peer-reviewed article
with the thesis results. The private simulator is not included in this public
showcase; its small visualization and schedule examples were written separately.

## Evaluating behavior against human evidence

**Aher, G. V., Arriaga, R. I., & Kalai, A. T. (2023).** Using Large Language
Models to Simulate Multiple Humans and Replicate Human Subject Studies.
*Proceedings of the 40th International Conference on Machine Learning*,
PMLR 202, 337–371.
[Proceedings](https://proceedings.mlr.press/v202/aher23a.html).

This paper motivates assessing simulated populations against established human
experimental findings. It informs the evaluation approach. Its experimental
tasks are not additional benchmarks run in this thesis, and its results are
not used as evidence that the present agents match humans.

## Prompt framing

**Lorè, N., & Heydari, B. (2024).** Strategic behavior of large language models
and the role of game structure versus contextual framing. *Scientific Reports*,
14, 18490. [Publisher and DOI](https://doi.org/10.1038/s41598-024-69032-z).

The study examines how game structure and contextual framing affect LLM
strategic behavior. It motivates H1's limited wording intervention. Here the
game stays fixed and one sentence emphasizes individual payoff maximization;
the thesis does not repeat the source's matrix of games, contexts, and models.

## Reasoning and giving

**Li, Y., & Shirado, H. (2025).** Spontaneous Giving and Calculated Greed in
Language Models. *Proceedings of the 2025 Conference on Empirical Methods in
Natural Language Processing*, 5271–5286.
[Proceedings](https://aclanthology.org/2025.emnlp-main.267/).
[DOI](https://doi.org/10.18653/v1/2025.emnlp-main.267).

This paper supplies prior evidence linking explicit reasoning to lower
cooperation in its tested games. It helps motivate H2's expectation of less
indiscriminate giving. The thesis tests the `none` versus `high` setting of
one recorded model in the repeated exchange game; this is a separate test,
with its own data and limits.

## Memory, reflection, and planning

**Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein,
M. S. (2023).** Generative Agents: Interactive Simulacra of Human Behavior.
[Author manuscript, arXiv:2304.03442](https://arxiv.org/abs/2304.03442).

The paper supplies the architectural precedent for combining memories,
reflection, and planning. The thesis adapts that idea to a periodic MRP protocol
inside the fixed repeated game, preserving its original rules. It tests the
complete protocol and does not reproduce the paper's town simulation or
identify the separate causal contribution of every architectural component.

## Thesis results shown in this repository

**Kraus, P. (2026).** *Engineering Behavioral Fidelity in LLM Agents for Economic
Simulations*. Master's thesis, TU Berlin; submitted 20 September 2026.

The LLM condition means, relationships, and effect estimates in this showcase
come from this thesis's final recorded runs and analysis. Only selected
aggregate results are shared here. The thesis manuscript is not publicly
distributed in this repository. See [data provenance](../data/README.md) for
the source-table hashes and [CITATION.cff](../CITATION.cff) to cite the public
showcase itself.
