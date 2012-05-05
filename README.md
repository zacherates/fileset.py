paths.py
========

Ant style file matching.

Produces an iterator of all of the files that match the provided pattern.

`**`	matches zero or more directories.
`*`	matches any directory name or acts as a glob style wildcard.
`/`	path separator.

Examples:
	`**/*.py`	recursively match all python files.
	`*/*.txt`	match all the text files in child directories.	

```python
>>> import paths
>>> list(paths.paths(".", "**/*.py"))
['paths.py', 'test_paths.py']
```
