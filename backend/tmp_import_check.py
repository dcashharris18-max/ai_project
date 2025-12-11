import sys
sys.path.insert(0, r"C:\Users\DEll\Desktop\ai_project\backend")
try:
    print('APP_IMPORT_OK')
except Exception:
    print('APP_IMPORT_ERROR')
    import traceback
    traceback.print_exc()
