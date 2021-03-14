# SQLite UUID extension wrapper

> Easy way to install the SQLite loadable extension in a Python environment.

## Installation

```sh
pip install sqlite_uuid
```

## Notes

When you install this package, an SQLite [loadable extension](https://sqlite.org/loadext.html) will get built. In Python, you can load extensions in 2 ways. The first step is enabling the loadable extensions using `conn.enable_load_extension(True)`. Then you can use `conn.load_extension(path)`. However, there's a problem with this. The SQLite UUID extension has a name that conflicts with a Python module from the standard library that has the same name. To avoid confusion, this module is built with the filename `sqlite_uuid_ext.[py-ver].[extension]`.

When you try to load an extension in SQLite, it needs an entrypoint function. According to [the docs](https://sqlite.org/c3ref/load_extension.html) of the `sqlite3_load_extension` C function, if an entrypoint is not provided, it will try to guess one base on the filename. In this case it will try to load an entrypoint called `sqlite3_sqlite_uuid_ext_init`, because the file has the name `sqlite_uuid_ext`. However, the entrypoint in this extension has the name `sqlite3_uuid_init`, so it won't work. The good news is that there's also an SQL function to load extensions, and it lets you specify the entrypoint. With that we can do:

```python
conn.execute("select load_extension('path/to/loadable/extension/sqlite_uuid_ext.[py-ver].[extension]', 'sqlite3_uuid_init')")
```

The first option is the path to our compiled extension, the second one is the entrypoint function.

## SQLite version

This extension uses the `SQLITE_INNOCUOUS` flag.

The SQLITE_INNOCUOUS flag is a new feature for SQLite version 3.31.0. Make sure you have at least that version installed, although you may be able to [get around it](https://sqlite.org/forum/forumpost/703601f60f?t=h).

## Examples

```python
import sqlite3
import sqlite_uuid

from uuid import UUID

# create an in-memory DB
conn = sqlite3.connect(":memory:")

# enable loadable extensions
conn.enable_load_extension(True)

# load UUID extension as explained above
conn.execute(
    "select load_extension(:path, 'sqlite3_uuid_init')",
    {"path": sqlite_uuid.extension_path()},
)

# disable loadable extensions
conn.enable_load_extension(False)
print("OK")

# create a UUID (as a string)
res = conn.execute("SELECT uuid()").fetchall()
print(res)

# convert it to a BLOB (bytes) and return it
res = conn.execute("SELECT uuid_blob(uuid())").fetchall()

# get the returned result
bx = res[0][0]

# build python UUID object from the bytes
u = UUID(bytes=bx, version=4)

# make sure they are the same
assert u.bytes == bx
assert u.hex == bx.hex()

exit()
```

(the script above should run correctly as it's written)

## Release History

* 0.9
    * Initial release

## Meta


Ricardo Ander-Egg Aguilar – [@ricardoanderegg](https://twitter.com/ricardoanderegg) –

- [ricardoanderegg.com](http://ricardoanderegg.com/)
- [github.com/polyrand](https://github.com/polyrand/)
- [linkedin.com/in/ricardoanderegg](http://linkedin.com/in/ricardoanderegg)

Distributed under the MIT license. See ``LICENSE`` for more information.

## Credits

I initially took the repository [karlb/sqlite-spellfix](https://github.com/karlb/sqlite-spellfix) as a template to create this Python package.
