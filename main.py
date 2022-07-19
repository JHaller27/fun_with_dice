from functools import reduce
from dice_stats import IDiceStats, DieStats
from typing import Callable



def print_dice(d: IDiceStats) -> None:
	print(d)
	for n in range(1, d.get_max()+1):
		count = d.get_count(n)
		print(f'{n:>2} : {count}')


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


def main():
	b = DieStats(4)
	print_table(b)

	a = DieStats(20)
	print_table(a)

	c = a + b
	print_table(c)


def table_cmd(cmd: str) -> None:
	sizes = [int(x.strip()) for x in cmd.split()]
	d = reduce(lambda x, y: x+y, map(DieStats, sizes))
	print_table(d)


def matrix_cmd(cmd: str) -> None:
	sizes = [int(x.strip()) for x in cmd.split()]
	d = reduce(lambda x, y: x+y, map(DieStats, sizes))
	print(d.get_matrix())


def repl():
	import re

	dice_regex = re.compile(r'\d+(\s+\d+)*')

	CommandType = Callable[[str], None]
	cmd_map: dict[str, CommandType] = {
		'table': table_cmd,
		't': table_cmd,
		'matrix': matrix_cmd,
		'm': matrix_cmd,
	}

	curr_cmd: CommandType = table_cmd
	while True:
		cmd = input('> ')
		match cmd:
			case 'q' | 'exit':
				return

			case _ if new_cmd := cmd_map.get(cmd):
				curr_cmd = new_cmd

			case _ if m := dice_regex.fullmatch(cmd):
				curr_cmd(cmd)


repl()
