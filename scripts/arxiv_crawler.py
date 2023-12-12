import os
import subprocess

# 要執行的Python檔案
scripts = ["physics.py", "mathematics.py", "computer_science.py"]


# 使用subprocess執行腳本
for script in scripts:
    script_path = os.path.join("scripts", script)
    subprocess.run(["python3", script_path])
