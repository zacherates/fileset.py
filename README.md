fileset.py
==========

Ant style file matching.

Produces an iterator of all of the files that match the provided pattern.  

Directory specifiers:  
`**`	matches zero or more directories.  
`*`		matches any directory name.  
`/`		path separator.  
`.`		matches current directory.

File specifiers:
`*`		glob style wildcard.

Patterns without directory parts are evaluated recursively.

Examples:  
	`**/*.py`		recursively match all python files.  
	`foo/**/*.py`	recursively match all python files in the foo/ directory.  
	`*.py`			match all the python files in the current diretory.  
	`*/*.txt`		match all the text files in child directories.  

```python
>>> from fileset import *
>>> list(Fileset(".", [includes("*.py")]))
['fileset.py', 'test_fileset.py']
```
