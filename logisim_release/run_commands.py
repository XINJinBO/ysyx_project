import subprocess
import sys


def run_command_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        cmd = line.strip()
        if not cmd or cmd.startswith("#"):
            continue
        print(f"[{i}] 执行: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[{i}] 命令执行失败，返回码: {e.returncode}")
        except FileNotFoundError:
            print(f"[{i}] 找不到命令或文件")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        filepath = "logisim.txt"
    else:
        filepath = sys.argv[1]

    print(f"读取命令文件: {filepath}")
    run_command_file(filepath)
