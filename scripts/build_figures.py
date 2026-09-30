"""Rebuild the research portfolio figures from the included aggregate tables.

These are descriptive views. No raw participant data or model access is needed.
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import FancyBboxPatch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.summarize_results import CONDITIONS, LABELS, METRICS, load_table, relative_gap
from examples.mrp_schedule import stages_for_round

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
INK, MUTED, GRID = '#192E42', '#566779', '#E3E9EE'
COLORS = {
    'human_control': '#192E42', 'baseline': '#8996A3',
    'competitive_framing': '#B17D42', 'reasoning_high': '#168B80',
    'flattened_mrp': '#AF9DAF', 'mrp': '#5261BA',
}
SHORT = dict(LABELS, mrp='MRP')


def style():
    plt.rcParams.update({
        'font.family': 'DejaVu Sans', 'font.size': 11,
        'text.color': INK, 'axes.labelcolor': MUTED, 'xtick.color': MUTED,
        'ytick.color': INK, 'axes.edgecolor': GRID,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.spines.left': False, 'figure.facecolor': 'white',
        'savefig.facecolor': 'white', 'svg.fonttype': 'none', 'svg.hashsalt': 'llm-behavioral-fidelity',
    })


def save(fig, name):
    OUT.mkdir(exist_ok=True)
    credit = ('MRP adaptation: Pau Kraus · Architecture: Park et al. (2023) · Simulator: Daniel Kral, P1'
              if name == 'mrp_protocol' else
              'Thesis: Pau Kraus (2026) · Simulator: Daniel Kral, P1 · Human experiment: Teubner & Camacho (2023)')
    fig.text(0.055, -0.035, credit, fontsize=8.5, color=MUTED)
    fig.savefig(OUT / f'{name}.png', dpi=170, bbox_inches='tight', pad_inches=0.22)
    svg = OUT / f'{name}.svg'
    fig.savefig(svg, bbox_inches='tight', pad_inches=0.22, metadata={'Date': None})
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    plt.close(fig)


def benchmark(results):
    fig, axes = plt.subplots(2, 3, figsize=(13.2, 7.6))
    specs = [
        ('total_sent', 'Amount sent', 'Units per agent per round', (0, 109), '.1f'),
        ('recipients', 'Number of recipients', 'Partners per agent per round', (0, 5.5), '.2f'),
        ('transfer_per_recipient', 'Transfer per recipient', 'Units per active recipient', (0, 26), '.1f'),
        ('network_value', 'Network value', 'Normalized group payoff', (0, 1.02), '.3f'),
        ('density', 'Network density', 'Share of possible directed ties', (0, 1.09), '.3f'),
        ('reciprocity', 'Network reciprocity', 'Mutual ties / active pairs', (0, 1.09), '.3f'),
    ]
    for index, (ax, (metric, title, xlabel, limits, fmt)) in enumerate(zip(axes.flat, specs)):
        human = results['human_control'][metric]
        ax.axvline(human, color=INK, linestyle=(0, (3, 3)), lw=1.4, zorder=1)
        for y, condition in enumerate(CONDITIONS):
            value = results[condition][metric]
            ax.plot([human, value], [y, y], color=COLORS[condition], alpha=0.26, lw=5, solid_capstyle='round')
            ax.scatter(value, y, s=75, color=COLORS[condition], edgecolor='white', linewidth=1.2, zorder=3)
            ax.annotate(format(value, fmt), (value, y), xytext=(8, 0), textcoords='offset points', va='center', fontsize=10, bbox={'facecolor':'white','edgecolor':'none','pad':0.4})
        ax.set_yticks(range(5), [SHORT[c] for c in CONDITIONS] if index % 3 == 0 else [])
        ax.set_ylim(4.6, -0.8)
        ax.set_xlim(*limits)
        ax.set_title(f'{title}\n', loc='left', fontsize=13, fontweight='bold', pad=1)
        ax.text(0, 1.035, f'Human benchmark: {human:{fmt}}', transform=ax.transAxes, color=MUTED, fontsize=10)
        ax.set_xlabel(xlabel, fontsize=10, labelpad=8)
        ax.grid(axis='x', color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis='y', length=0, pad=10)
    fig.suptitle('Behavior in a repeated exchange game', x=0.075, ha='left', fontsize=22, fontweight='bold', y=0.99)
    fig.text(0.075, 0.917, 'Five LLM conditions compared with the same human control benchmark', fontsize=12, color=MUTED)
    fig.subplots_adjust(left=0.16, right=0.98, top=0.82, bottom=0.13, hspace=0.75, wspace=0.38)
    fig.text(0.075, 0.025, 'Rounds 1–12 · Condition means · Dashed lines mark human means · Descriptive comparisons; no uncertainty intervals', fontsize=9, color=MUTED)
    save(fig, 'benchmark')


def gap_matrix(results):
    matrix = np.array([[relative_gap(results[c][m], results['human_control'][m], results['baseline'][m])
                        for m in METRICS] for c in CONDITIONS], dtype=float)
    fig, ax = plt.subplots(figsize=(12.5, 5.5))
    cmap = LinearSegmentedColormap.from_list('distance', ['#167D75', '#D4EBE6', '#F0F2F4', '#E8D3B7'])
    ax.imshow(matrix, cmap=cmap, norm=Normalize(0, 1.5), aspect='auto')
    for (y, x), value in np.ndenumerate(matrix):
        ax.text(x, y, f'{value:.2f}', ha='center', va='center', fontsize=15,
                fontweight='bold' if y in (2, 4) else 'normal', color='white' if value < 0.14 else INK)
    ax.set_xticks(range(6), ['Amount\nsent', 'Number of\nrecipients', 'Transfer per\nrecipient', 'Network\nvalue', 'Network\ndensity', 'Network\nreciprocity'])
    ax.xaxis.tick_top()
    ax.set_yticks(range(5), [SHORT[c] for c in CONDITIONS])
    ax.tick_params(axis='both', length=0, pad=12)
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 5, 1), minor=True)
    ax.grid(which='minor', color='white', linewidth=5)
    ax.tick_params(which='minor', length=0)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.suptitle('Progress depends on what you measure', x=0.05, y=0.985, ha='left', fontsize=22, fontweight='bold')
    fig.text(0.05, 0.855, 'Distance from the human mean, relative to the baseline gap', color=MUTED, fontsize=12)
    fig.subplots_adjust(left=0.2, right=0.98, top=0.69, bottom=0.14)
    fig.text(0.05, 0.025, '0 = matching mean    ·    1 = baseline distance    ·    Above 1 = further away\nDescriptive ratios, not a combined fidelity score or a test of equivalence. Recipient count and density measure the same margin.', fontsize=9, color=MUTED, linespacing=1.7)
    save(fig, 'benchmark_gaps')


def relationships():
    results = load_table('relationship_summary.csv')
    conditions = ('human_control',) + CONDITIONS
    specs = [('cut_rate', 'Previously active ties removed', 'Share of active ties', '.1%'),
             ('retained_tie_mean_change', 'Change on retained ties', 'Units per directed tie', '+.2f')]
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.8))
    for ax, (metric, title, xlabel, fmt) in zip(axes, specs):
        values = [results[c][metric] for c in conditions]
        ax.barh(range(6), values, color=[COLORS[c] for c in conditions], height=0.6)
        ax.set_yticks(range(6), [SHORT[c] for c in conditions])
        ax.invert_yaxis()
        ax.axvline(0, color=MUTED, lw=0.8)
        width = max(values) - min(0, min(values))
        ax.set_xlim(min(0, min(values)) - width * 0.13, max(values) + width * 0.25)
        for y, value in enumerate(values):
            ax.annotate(format(value, fmt), (value, y), xytext=(7, 0),
                        textcoords='offset points', va='center', ha='left', fontsize=10, color=INK if value >= 0 else 'white')
        ax.set_title(title, loc='left', fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.grid(axis='x', color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis='y', length=0)
    fig.suptitle('The structure of relationships also changes', x=0.055, y=0.98, ha='left', fontsize=22, fontweight='bold')
    fig.text(0.055, 0.86, 'MRP makes exchange more selective, while strengthening surviving ties', color=MUTED, fontsize=12)
    fig.subplots_adjust(left=0.175, right=0.98, top=0.72, bottom=0.24, wspace=0.7)
    fig.text(0.055, 0.025, 'Transitions ending in rounds 2–12 · Means of cohort summaries · Retained ties follow the same sender and recipient\nMRP shows the cut-and-reinforce pattern; the size of reinforcement remains above the human benchmark.', fontsize=9, color=MUTED, linespacing=1.7)
    save(fig, 'relationships')


def protocol():
    fig, ax = plt.subplots(figsize=(13, 5.1))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.suptitle('Memory, reflection, planning — over time', x=0.055, y=0.98, ha='left', fontsize=22, fontweight='bold')
    fig.text(0.055, 0.845, 'A persistent plan guides each decision; reflection and planning update every three rounds', fontsize=11, color=MUTED)
    for i, (heading, desc, color) in enumerate([
        ('MEMORY', 'Observed exchange history', '#168B80'),
        ('REFLECTION', 'Interpret past interactions', '#5261BA'),
        ('PLANNING', 'Update the persistent plan', '#5261BA'),
        ('ACTION', 'Choose transfers this round', '#192E42'),
    ]):
        x = 0.2 + i * 4
        ax.add_patch(FancyBboxPatch((x, 3.5), 3.55, 1.15, boxstyle='round,pad=0.09,rounding_size=0.15', facecolor='#F1F5F8', edgecolor='none'))
        ax.text(x+0.15, 4.23, heading, color=color, fontweight='bold', fontsize=11)
        ax.text(x+0.15, 3.83, desc, fontsize=9.3, color=MUTED)
        if i < 3: ax.annotate('', (x+3.95, 4.08), (x+3.58, 4.08), arrowprops={'arrowstyle':'->','color':MUTED})
    # The boxes explain the stages; the schedule shows when they are invoked.
    ax.text(0.15, 2.92, 'Stage timing', fontweight='bold', fontsize=11)
    for r in range(1, 16):
        x = 1.5 + (r-1)*0.94
        ax.text(x, 2.5, str(r), ha='center', fontsize=10, color=MUTED)
        stages = stages_for_round(r)
        for stage, y, color in [('plan', 2.05, '#5261BA'), ('reflect', 1.42, '#168B80'), ('act', 0.79, '#192E42')]:
            ax.scatter(x, y, s=100 if stage in stages else 25, color=color if stage in stages else GRID)
    for label,y in [('Plan',2.05),('Reflect',1.42),('Act',0.79)]:ax.text(0.15,y,label,va='center',fontsize=10)
    ax.text(15.3,2.5,'Round',ha='left',fontsize=9,color=MUTED)
    fig.subplots_adjust(top=0.78, bottom=0.11, left=0.045, right=0.97)
    fig.text(0.055,0.03,'Initial plan before round 1 · Reflection + planning before rounds 4, 7, 10, 13 · New exchange outcomes enter memory after every round',fontsize=9,color=MUTED)
    save(fig, 'mrp_protocol')


def main():
    style()
    results = load_table()
    benchmark(results)
    gap_matrix(results)
    relationships()
    protocol()
    print('Built four figures in assets/ (PNG and SVG).')


if __name__ == '__main__':
    main()
