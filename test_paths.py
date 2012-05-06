import os
import shutil
import tempfile

from os.path import join

import nose
from nose.tools import *

from paver.easy import path

import paths

def setup():
	global root
	root = tempfile.mkdtemp()
	foo = join(root, "foo")
	bar = join(foo, "bar")
	baz = join(bar, "baz")
	os.makedirs(baz)

	new = (
		join(root, "zero.py"),
		join(root, "zero"),
		join(foo, "one.py"),
		join(foo, "one"),
		join(bar, "two.py"),
		join(bar, "two"),
		join(baz, "three.py"),
		join(baz, "three"),
		join(baz, "..."),
	)

	def touch(path):
		with open(path, "a"):
			pass

	for p in new:
		touch(p)

def teardown():
	shutil.rmtree(root)

def check(pattern, expected):
	actual = sorted(paths.paths(root, pattern))
	eq_(sorted(expected), actual)


def test_empty():
	cases = (
		("foo/blah/*.py", []),
		("*.blah", []),
		("**/hree.py", []),
		("foo/", []),
		("bar/foo/two.py", []),
	)

	for pattern, results in cases:
		yield check, pattern, results


def test_glob():
	cases = [
		("./*.py", ["zero.py"]),
		("foo/*.py", ["foo/one.py"]),
		("*/*", ["foo/one.py", "foo/one"]),
	]

	for pattern, results in cases:
		yield check, pattern, results


def test_exact():
	cases = [
		("zero.py", ["zero.py"]),
		("foo/bar/baz/three.py", ["foo/bar/baz/three.py"]),
	]

	for pattern, results in cases:
		yield check, pattern, results


def test_recursive():
	cases = (
		("**/...", ["foo/bar/baz/..."]),
		("*.py", ["zero.py", "foo/one.py", "foo/bar/two.py", "foo/bar/baz/three.py"]),
		("**/*.py", ["foo/bar/baz/three.py", "foo/bar/two.py", "foo/one.py", "zero.py"]),
		("**/baz/**/*.py", ["foo/bar/baz/three.py"]),
	)

	for pattern, results in cases:
		yield check, pattern, results


def check_multi((paths, expected)):
	actual = sorted(paths)
	eq_(sorted(expected), actual)


def test_multi():
	a = paths.Paths(root) \
		.includes("./*.py") \
		.includes("*/*.py")

	b = paths.Paths(root) \
		.includes("**/zero*") \
		.includes("**/one*")

	c = paths.Paths(root) \
		.includes("**/*") \
		.excludes("**/*.py") \
		.excludes("**/baz/*")

	d = paths.Paths(root) \
		.includes("**/*.py") \
		.excludes("**/foo/**/*") \
		.includes("**/baz/**/*.py")

	e = paths.Paths(root) \
		.includes("**/*.py") \
		.excludes("two.py", "three.py")

	cases = (
		(a, ["zero.py", "foo/one.py"]),
		(b, ["zero.py", "zero", "foo/one.py", "foo/one"]),
		(c, ["zero", "foo/one", "foo/bar/two"]),
		(d, ["zero.py", "foo/bar/baz/three.py"]),
		(e, ["zero.py", "foo/one.py"]),
	)

	for case in cases:
		yield check_multi, case


if __name__ == "__main__":
	nose.main()
