# SimpSave: A Simple Way to Store Your Python Variables

**SimpSave** is an open-source, ultra lightweight key-value database. It works out of the box, offering a functional-style API that is extremely easy to use, with a "read-and-use" design that makes it perfect for small projects such as student assignments where simple data persistence is needed.

**SimpSave 10** introduces multiple storage engines — from the light-weight, python-builtin `XML` engine, to common formats like `YML` and `TOML`, and even the more advanced yet production-grade like `SQLITE` engine — greatly enhancing overall flexibility and usability.

You can install SimpSave using the following command:

```bash
pip install simpsave
```

Then import SimpSave (commonly aliased as `ss`) in your project and start using it:

```python
import simpsave as ss
```

Example of "read-and-use" behavior:

```python
import simpsave as ss

ss.write("key1", ["Hello"])
result = ss.read("key1") + ["World"]  # result = ["Hello", "World"]
```

Dependencies are optional at installation time. In its simplest form, `simpsave` is extremely lightweight and requires no third-party libraries:

```bash
pip install simpsave[xml]
pip install simpsave[json]
pip install simpsave[sqlite]
```

For more detailed tutorials, refer to:

* [English Documentation](./source/README.md)
* [Chinese Documentation](./source/README-zh.md)
