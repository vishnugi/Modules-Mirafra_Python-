import shutil

total, used, free = shutil.disk_usage("/")

print(total)
print(used)

usage = (used / total) * 100

if usage < 80:
    print("PASS")
else:
    print("FAIL")