import sqlite3
import sqlite_uuid

from uuid import UUID

conn = sqlite3.connect(":memory:")

conn.enable_load_extension(True)

conn.execute(
    "select load_extension(:path, 'sqlite3_uuid_init')",
    {"path": sqlite_uuid.extension_path()},
)

conn.enable_load_extension(False)
print("OK")

res = conn.execute("SELECT uuid()").fetchall()
print(res)

res = conn.execute("SELECT uuid_blob(uuid())").fetchall()

# UUID as bytes
bx = res[0][0]

# build python UUID object from the bytes
u = UUID(bytes=bx, version=4)

assert u.bytes == bx
assert u.hex == bx.hex()

exit()
