"""Explore the showcase's aggregate results using only Python's standard library."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ('baseline', 'competitive_framing', 'reasoning_high', 'flattened_mrp', 'mrp')
LABELS = {
    'human_control': 'Human benchmark',
    'baseline': 'LLM baseline',
    'competitive_framing': 'Prompt framing',
    'reasoning_high': 'High reasoning',
    'flattened_mrp': 'Single-call control',
    'mrp': 'Memory / reflection / planning',
}
METRICS = ('total_sent', 'recipients', 'transfer_per_recipient', 'network_value', 'density', 'reciprocity')


def load_table(name='descriptive_means.csv'):
    with (ROOT / 'data' / name).open(newline='', encoding='utf-8') as stream:
        return {row['condition']: {key: float(value) for key, value in row.items()
                                  if key not in ('condition', 'label')}
                for row in csv.DictReader(stream)}


def relative_gap(value: float, human: float, baseline: float) -> float | None:
    """Absolute distance from the human mean, divided by the baseline distance.

    A value of 1 equals the baseline gap; 0 is an exact match of means. Return
    None when the baseline already matches, because the ratio is undefined.
    This descriptive quantity is not a test of statistical equivalence.
    """
    baseline_gap = abs(baseline - human)
    return abs(value - human) / baseline_gap if baseline_gap else None


def main():
    results = load_table()
    print('Absolute gap to the human mean, relative to the LLM baseline (1.00).')
    print('Below 1 = closer mean; above 1 = further away. No significance test.\n')
    print('| Condition | ' + ' | '.join(METRICS) + ' |')
    print('| --- | ' + ' | '.join(['---:'] * len(METRICS)) + ' |')
    for condition in CONDITIONS:
        gaps = [relative_gap(results[condition][m], results['human_control'][m], results['baseline'][m])
                for m in METRICS]
        print('| ' + LABELS[condition] + ' | ' + ' | '.join('undefined' if x is None else f'{x:.2f}' for x in gaps) + ' |')


if __name__ == '__main__':
    main()
