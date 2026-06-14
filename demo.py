import subprocess
import os
db_path = os.path.join(os.getcwd(), "sandbox", "memory", "agent.db")

result = subprocess.run(
    ["npx", "-y", "mcp-memory-libsql"],
    capture_output=True,
    text=True,
    timeout=15,
    env={**os.environ, "LIBSQL_URL": f"file:///{db_path.replace(os.sep, '/')}"}
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)