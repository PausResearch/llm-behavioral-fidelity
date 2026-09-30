"""A standalone illustration of the thesis protocol, without model calls.

This demonstrates stage timing. It is not the simulator used to collect the
thesis data and does not generate empirical results.
"""
from __future__ import annotations


def stages_for_round(round_number: int, update_interval: int = 3) -> tuple[str, ...]:
    if round_number < 1 or update_interval < 1:
        raise ValueError('Rounds and update intervals must be positive integers.')
    if round_number == 1:
        return ('plan', 'act')
    if (round_number - 1) % update_interval == 0:
        return ('reflect', 'plan', 'act')
    return ('act',)


def main():
    print('MRP stage schedule — 15 rounds; a persistent plan guides each action.\n')
    for round_number in range(1, 16):
        print(f'Round {round_number:2}: ' + ' → '.join(stages_for_round(round_number)))
    print('\nAfter every action, observed exchange outcomes enter the factual record.')


if __name__ == '__main__':
    main()
