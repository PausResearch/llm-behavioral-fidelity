# Data in this showcase

These are aggregate outputs of Pau Kraus's submitted master's thesis. No
participant-level records, individual model transcripts, or manuscript files
are included.

| File | Content and provenance |
| :--- | :--- |
| `descriptive_means.csv` | Unmodified final condition means for rounds 1–12: six rows, one per LLM condition plus the human control benchmark |
| `relationship_summary.csv` | Six condition-level summaries calculated from the final cohort metrics, matching the averaging used in the thesis results |
| `hypothesis_evidence.csv` | Unmodified final table of exploratory effect estimates, confidence intervals, and p-values |
| `provenance.json` | Source-table hashes, archive version, sample sizes, model configuration, and export details |

Internal condition names are preserved so the tables can be traced back to the
research archive. `competitive_framing` means prompt framing;
`flattened_mrp` means the single-call control; `mrp` means the final periodic
MRP condition, with reflection and planning updated every three rounds.

The benchmark uses 12 control cohorts from
[Teubner and Camacho (2023)](https://doi.org/10.1007/s10726-023-09814-4).
The full underlying human dataset is not redistributed here.

Relationship statistics average non-missing cohort summaries. For formation
rate only, the baseline contributes five cohorts and the single-call control
contributes four: the remaining cohorts have no previously inactive ties, so
formation is undefined. Other displayed relationship measures use all cohorts.

The visualization scripts are newly written for this showcase. Figures are
generated directly from these tables. The original simulator, statistical
fitting code, and raw experimental archive are maintained separately.
