import itertools
import os, os.path
import re
import sys


class Pattern(object):
	def __init__(self, spec):
		self.compiled = self.compile(spec)

	def compile(self, spec):
		parse = "".join(self.parse(spec))
		regex = "^{0}$".format(parse)
		return re.compile(regex)

	def parse(self, pattern):
		if not pattern:
			raise StopIteration

		bits = pattern.split("/")
		dirs, file = bits[:-1], bits[-1]

		for dir in dirs:
			if dir == "**":
				yield  "(|.+/)"

			elif dir == "*":
				yield "[^/]+/"

			elif dir == ".":
				yield ""

			else:
				yield re.escape(dir) + "/"

		if not dirs:
			yield "(|.+/)"

		yield "[^/]*".join(re.escape(bit) for bit in file.split("*"))

	def matches(self, path):
		return self.compiled.match(path) is not None


class Paths(object):
	def __init__(self, root):
		self.root = root
		self.filters = []

	def includes(self, *patterns):
		for pattern in patterns:
			self.filters.append((Pattern(pattern), True))
		return self

	def excludes(self, *patterns):
		for pattern in patterns:
			self.filters.append((Pattern(pattern), False))
		return self

	def __iter__(self):
		for path in self.walk():
			included = False

			for pattern, inclusive in self.filters:
				if pattern.matches(path):
					included = inclusive

			if included:
				yield path

	def walk(self):
		for abs, dirs, files in os.walk(self.root):
			prefix = abs[len(self.root):].lstrip(os.sep)
			bits = prefix.split(os.sep) if prefix else []

			for file in files:
				yield "/".join(bits + [file])


def paths(root, pattern):
	"""
		Ant style file matching.

		Produces an iterator of all of the files that match the provided pattern.  

		Directory specifiers:  
		**		matches zero or more directories.  
		*		matches any directory name.  
		/		path separator.  
		.		matches current directory.

		File specifiers:
		*		glob style wildcard.

		Patterns without directory parts are evaluated recursively.

		Examples:
			*.py		recursively match all python files.  
			foo/**/*.py recursively match all python files in the foo/ directory.
			./*.py		match all the python files in the current diretory.
			*/*.txt		match all the text files in child directories.  
	"""

	return Paths(root).includes(pattern)
