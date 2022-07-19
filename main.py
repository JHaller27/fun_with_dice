from functools import reduce
from dice_stats import IDiceStats, DieStats



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


def handle_dice_cmd(cmd: str) -> None:
	sizes = [int(x.strip()) for x in cmd.split()]
	d = reduce(lambda x, y: x+y, map(DieStats, sizes))
	print_table(d)


def repl():
	import re

	dice_regex = re.compile(r'\d+(\s+\d+)*')

	while True:
		cmd = input('> ')
		match cmd:
			case 'q' | 'exit':
				return

			case _ if m := dice_regex.fullmatch(cmd):
				handle_dice_cmd(cmd)


repl()
