import os
import shutil
import tempfile

from os.path import join

import nose
from nose.tools import *

from paver.easy import path

from fileset import *

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
	actual = sorted(Fileset(root, [includes(pattern)]))
	eq_(sorted(expected), actual)


ALL_THE_PIES = ["zero.py", "foo/one.py", "foo/bar/two.py", "foo/bar/baz/three.py"]

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
		("*.py", ["zero.py"]),
		("foo/*.py", ["foo/one.py"]),
		("*/*", ["foo/one.py", "foo/one"]),
		("**/*a*/**/*.py", ["foo/bar/two.py", "foo/bar/baz/three.py"])
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
		("**/*.py", ALL_THE_PIES),
		("**/baz/**/*.py", ["foo/bar/baz/three.py"]),
	)

	for pattern, results in cases:
		yield check, pattern, results


def check_multi((paths, expected)):
	actual = sorted(paths)
	eq_(sorted(expected), actual)


def test_multi():
	a = Fileset(root, [
		includes("*.py"),
		includes("*/*.py"),
	])

	b = Fileset(root, [
		includes("**/zero*"),
		includes("**/one*"),
	])

	c = Fileset(root, [
		includes("**/*"),
		excludes("**/*.py"),
		excludes("**/baz/*"),
	])

	d = Fileset(root, [
		includes("**/*.py"),
		excludes("**/foo/**/*"),
		includes("**/baz/**/*.py"),
	])

	e = Fileset(root, [
		includes("**/*.py"),
		excludes("**/two.py"),
		excludes("**/three.py"),
	])

	cases = (
		(a, ["zero.py", "foo/one.py"]),
		(b, ["zero.py", "zero", "foo/one.py", "foo/one"]),
		(c, ["zero", "foo/one", "foo/bar/two"]),
		(d, ["zero.py", "foo/bar/baz/three.py"]),
		(e, ["zero.py", "foo/one.py"]),
	)

	for case in cases:
		yield check_multi, case

def test_set():
	a = Fileset(root, [
		includes("**/*.py")
	])

	b = Fileset(root, [
		includes("**/*"),
		excludes("**/bar/**/*"),
	])

	c = Fileset(root, [])


	cases = (
		(a | b, ALL_THE_PIES + ["zero", "foo/one"]),
		(a & b, ["zero.py", "foo/one.py"]),
		(a | c, a),
		(a & c, []),
		(a | b | c, ALL_THE_PIES + ["zero", "foo/one"]),
		((a | b) & c, []),
		(a & b & c, []),
	)

	for case in cases:
		yield check_multi, case


if __name__ == "__main__":
	nose.main()
