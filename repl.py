from functools import reduce
from numpy import cumsum
from dice_stats import IDiceStats, DieStats
from typing import Callable



def eval_dice(cmd: str) -> IDiceStats:
	sizes = [int(x.strip()) for x in cmd.split()]
	d = reduce(lambda x, y: x+y, map(DieStats, sizes))
	return d


def print_counts(d: IDiceStats) -> None:
	print(d)
	for n in range(1, d.get_max()+1):
		count = d.get_count(n)
		print(f'{n:>2} : {count}')


def print_percentages(d: IDiceStats) -> None:
	print(d)
	counts = [d.get_count(n) for n in range(1, d.get_max()+1)]
	total = sum(counts)
	for n, count in enumerate(counts):
		n += 1
		pct = count / total
		print(f'{n:>2} : {pct:>6.2%}')


def print_cum_percentages(d: IDiceStats) -> None:
	print(d)

	counts = [d.get_count(n) for n in range(1, d.get_max()+1)]
	cum_counts = cumsum(counts)

	total = sum(counts)

	for n, cum_count in enumerate(cum_counts):
		n += 1
		if cum_count == 0:
			dash = '-'.center(7, ' ')
			print(f'{n:>2} : {dash}')
		else:
			pct = (total - cum_count + 1) / total
			print(f'{n:>2} : {pct:>7.2%}')


def print_table(d: IDiceStats) -> None:
	print(d)
	top = d.get_max()
	print(''.join([f'{n:^3}' for n in range(1, top+1)]))
	print('---' * top)

	values = [d.get_count(n+1) for n in range(top)]
	max_value = max(values)
	for v in range(1, max_value + 1):
		for i in range(top):
			cell = 'XXX' if v <= values[i] else '   '
			print(cell, end='')
		print()

	print()


def print_matrix(d: IDiceStats) -> None:
	print(d.get_matrix())


def repl():
	import re

	dice_regex = re.compile(r'\d+(\s+\d+)*')

	CommandType = Callable[[IDiceStats], None]
	display_map: dict[str, CommandType] = {
		'table': print_table,
		't': print_table,
		'matrix': print_matrix,
		'm': print_matrix,
		'counts': print_counts,
		'c': print_counts,
		'pct': print_percentages,
		'p': print_percentages,
		'cumpct': print_cum_percentages,
		'cp': print_cum_percentages,
	}

	curr_display: CommandType = print_table
	while True:
		cmd = input('> ')
		match cmd:
			case 'q' | 'exit':
				return

			case _ if new_cmd := display_map.get(cmd):
				curr_display = new_cmd

			case _ if m := dice_regex.fullmatch(cmd):
				d = eval_dice(cmd)
				curr_display(d)

			case _:
				print(f'Command {cmd} not recognized')


if __name__ == '__main__':
	repl()
