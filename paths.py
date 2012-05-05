import itertools
import os, os.path
import re
import sys

__all__ = ["paths"]

def walk(root):
	for abs, dirs, files in os.walk(root):
		prefix = abs[len(root):].lstrip(os.sep)
		bits = prefix.split(os.sep) if prefix else []

		for file in files:
			yield "/".join(bits + [file])


def parse(pattern):
	if not pattern:
		raise StopIteration

	bits = pattern.split("/")
	dirs, file = bits[:-1], bits[-1]

	for dir in dirs:
		if dir == "**":
			yield  "(|.+/)"

		elif dir == "*":
			yield "[^/]+/"

		else:
			yield re.escape(dir) + "/"

	yield "[^/]*".join(re.escape(bit) for bit in file.split("*"))


def compile(spec):
	regex = "^{0}$".format("".join(parse(spec)))
	return re.compile(regex)


def paths(root, pattern):
	"""
		Ant style file matching.

		Produces an iterator of all of the files that match the provided pattern.

		**	matches zero or more directories.
		*	matches any directory name or acts as a glob style wildcard.
		/	path separator.

		Examples:
			**/*.py		recursively match all python files.
			*/*.txt		match all the text files in child directories.	
	"""

	return itertools.ifilter(
		compile(pattern).match,
		walk(root)
	)
