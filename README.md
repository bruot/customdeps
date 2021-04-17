# CustomDeps

CustomDeps is a tool that manages your modules paths and that lets you import specific versions of modules designated by their Git commit hashes. CustomDeps does this by keeping, in a directory, one copy of the source code of the module(s) for each version you have used at least once.

CustomDeps usually helps you to track the versions of the modules you import *directly*. However, it does not track imports within the imported modules. If this is relevant to you, please consider other alternatives such as virtual environments.


## Installation

```
pip install CustomDeps
```


## Usage

Let's say you use a module `some_module` located in a Git project `some-project`, and you want to do this:

```
import some_module  # yes, but I want the version at commit 14b2b29a6a5231146245d7b2cc9ce8841eef293c!
```

With CustomDeps, this is simply done with:

```
import custom_deps
gr = custom_deps.GitRepos()
gr.insert_path('some-project', '14b2b29a6a5231146245d7b2cc9ce8841eef293c')
import some_module
```

To be able to use the script above, you first need to register the Git repository `some-project`. This only needs to be done once, for example in a Python console:

```
>>> import custom_deps
>>> gr = custom_deps.GitRepos()
>>> gr.add('https://example.com/some-project.git', 'some-project')
```

`add()` takes two arguments. The first one is the clone URL of the Git project. The second one is a label that you can freely assign and that designates the project within CustomDeps. Note that the clone URL can also be a local path.

After that, you can start writing scripts that use various versions of `some_module` as shown above, with `insert_path()`. This method appends an appropriate directory, containing the project checked out at the relevant commit, to the search paths used to find modules. After the `import` statement, you can check what file is used by the import like this:

```
import custom_deps
gr = custom_deps.GitRepos()
gr.insert_path('some-project', '14b2b29a6a5231146245d7b2cc9ce8841eef293c')
import some_module
print(some_module.__file__)
...
```

which prints something like this:

```
/home/username/.local/share/CustomDeps/snaps/some-project/14b2b29a6a5231146245d7b2cc9ce8841eef293c/some_module/__init__.py
```

`insert_path()` manages automatically the creation of directories with different project versions. When `insert_path()` is used with a new commit hash, CustomDeps will also perform a `git pull` from the external repository at the location you indicated when using `add()`. Therefore, project updates are retrieved transparently, without further action than calling `insert_path()`.

If the module to import is not located at the root of the Git project, you can specify the modules location relative to the project root by passing a third argument to `insert_path()`:

```
gr.insert_path('some-project', '14b2b29a6a5231146245d7b2cc9ce8841eef293c', 'src/python/modules')
```


## CustomDeps internal directories

Directories used by CustomDeps to manage the different project versions are by default in your user data directory (for example, `~/.local/share/CustomDeps` on Ubuntu). For each project, CustomDeps always keeps there working trees checked out at all the versions you have requested once. The location of these directories can be changed by editing the CustomDeps user configuration file (`~/.config/CustomDeps/config` on Ubuntu).


## Licence

Copyright (C) 2018, 2021 Nicolas Bruot (https://www.bruot.org/hp/)

CustomDeps is published under the GPLv3.0 licence.
