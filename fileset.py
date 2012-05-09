import itertools
import os, os.path
import re
import sys


class Pattern(object):
	def __init__(self, spec, inclusive):
		self.compiled = self.compile(spec)
		self.inclusive = inclusive

	def compile(self, spec):
		parse = "".join(self.parse(spec))
		regex = "^{0}$".format(parse)
		return re.compile(regex)

	def parse(self, pattern):
		def globify(part):
			return "[^/]*".join(re.escape(bit) for bit in part.split("*"))


		if not pattern:
			raise StopIteration

		bits = pattern.split("/")
		dirs, file = bits[:-1], bits[-1]

		for dir in dirs:
			if dir == "**":
				yield  "(|.+/)"

			else:
				yield globify(dir) + "/"

		yield globify(file)

	def matches(self, path):
		return self.compiled.match(path) is not None


class Fileset(object):
	"""
		Ant style file matching.

		Produces an iterator of all of the files that match the provided pattern.  

		Directory specifiers:  
		**		matches zero or more directories.  
		*		matches any directory name.  
		/		path separator.  

		File specifiers:
		*		glob style wildcard.

		Examples:
			**/*.py		recursively match all python files.  
			foo/**/*.py recursively match all python files in the foo/ directory.
			*.py		match all the python files in the current diretory.
			*/*.txt		match all the text files in child directories.  
	"""

	def __init__(self, root, patterns):
		self.root = root
		self.patterns = patterns

	def __iter__(self):
		for path in self.walk():
			included = False

			for pattern in self.patterns:
				if pattern.matches(path):
					included = pattern.inclusive

			if included:
				yield path

	def __or__(self, other):
		return set(self) | set(other)

	def __ror__(self, other):
		return self | other

	def __and__(self, other):
		return set(self) & set(other)

	def __rand__(self, other):
		return self & other

	def walk(self):
		for abs, dirs, files in os.walk(self.root):
			prefix = abs[len(self.root):].lstrip(os.sep)
			bits = prefix.split(os.sep) if prefix else []

			for file in files:
				yield "/".join(bits + [file])


def includes(pattern):
	return Pattern(pattern, inclusive = True)

def excludes(pattern):
	return Pattern(pattern, inclusive = False)
