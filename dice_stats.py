import numpy as np
from itertools import chain


def _dot_sum(a: np.ndarray, b: np.ndarray) -> np.ndarray:
	a1 = np.empty(len(a), dtype=int)
	a1.fill(1)
	am = np.array([a, a1]).swapaxes(0, 1)

	b1 = np.empty(len(b), dtype=int)
	b1.fill(1)
	bm = np.array([b1, b])

	rm: np.ndarray = am.dot(bm)
	r = rm.flatten()

	return r


class IDiceStats:
	def __str__(self) -> str:
		return self.to_str()

	def __add__(self, other: 'IDiceStats') -> 'IDiceStats':
		return self.add_dice(other)

	def sizes(self) -> dict[int, int]:
		raise NotImplementedError

	def to_str(self) -> str:
		raise NotImplementedError

	def add_dice(self, other: 'IDiceStats') -> 'IDiceStats':
		raise NotImplementedError

	def get_array(self) -> np.ndarray:
		raise NotImplementedError

	def get_max(self) -> int:
		raise NotImplementedError

	def get_count(self, value: int) -> int:
		raise NotImplementedError


class DieStats(IDiceStats):
	def __init__(self, size: int) -> None:
		super().__init__()
		self._size = size

	def sizes(self) -> dict[int, int]:
		return {self._size: 1}

	def to_str(self) -> str:
		return ' + '.join([f'{v}d{k}' for k, v in self.sizes().items()])

	def add_dice(self, other: IDiceStats) -> IDiceStats:
		r = _dot_sum(self.get_array(), other.get_array())
		new_sizes = {}

		for k, v in chain(self.sizes().items(), other.sizes().items()):
			new_sizes.setdefault(k, 0)
			new_sizes[k] += v

		return MultipleDiceStats(new_sizes, r)

	def get_array(self) -> np.ndarray:
		return np.arange(1, self._size+1)

	def get_max(self) -> int:
		return max(self.get_array())

	def get_count(self, value: int) -> int:
		return list(self.get_array()).count(value)


class MultipleDiceStats(DieStats):
	def __init__(self, sizes: dict[int, int], stat_array: np.ndarray) -> None:
		super().__init__(0)
		self._sizes = sizes
		self._stat_array = stat_array

	def sizes(self) -> dict[int, int]:
		return dict(self._sizes)

	def get_array(self) -> np.ndarray:
		return self._stat_array.flatten()
