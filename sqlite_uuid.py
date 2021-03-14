import importlib.util


def extension_path():
    x = importlib.util.find_spec("sqlite_uuid_ext").origin
    print("\n\n", x, "\n")
    return x
