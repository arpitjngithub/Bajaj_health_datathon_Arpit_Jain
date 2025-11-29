# app/startup_debug.py  (TEMP — remove after debugging)
import sys, traceback, importlib, os, time

print("=== STARTUP DEBUG ===")
print("CWD:", os.getcwd())
print("List /app:")
try:
    for e in sorted(os.listdir("/app")):
        print(" -", e)
except Exception as ex:
    print("Cannot list /app:", ex)

print("\nPYTHONPATH:")
for p in sys.path:
    print(" -", p)

print("\nTRY IMPORT main now...\n")
try:
    importlib.import_module("main")
    print("\nIMPORT OK: main imported successfully")
except Exception:
    print("\nIMPORT FAILED: TRACEBACK BELOW\n")
    traceback.print_exc()

# keep container alive briefly so logs are visible
time.sleep(20)
