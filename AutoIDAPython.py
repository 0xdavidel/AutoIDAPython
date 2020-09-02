from __future__ import unicode_literals, print_function

import subprocess
import argparse
import os
import sys
import json

# Create absulute path and check if file / folder exists
def abs_path_check_existing(src_path, must_exist=True):
    if must_exist and not os.path.exists(src_path):
        print('[X] File / Folder: "{}" does not exist'.format(src_path))
        sys.exit(1)
    abs_path = os.path.abspath(src_path)
    return abs_path


# Run an ida script, return script output
def run_ida_script(target, script, slave, output_idb, ida_path):
    # print(
    #     "target = {}\nScript = {}\nSlave = {}\nOutput = {}\nIda path = {}".format(
    #         target, script, slave, output_idb, ida_path
    #     )
    # )
    s = subprocess.Popen(
        [
            ida_path,
            "-c",
            "-A",
            "-S{} {}".format(slave, script),
            "-o{}".format(output_idb),
            target,
        ]
    )
    s.wait()
    script_stdout = ""
    script_stderr = ""
    try:
        with open("script_output.txt", "r") as f:
            script_stdout = f.read()
        os.remove("script_output.txt")
        with open("script_error.txt", "r") as f:
            script_stderr = f.read()
        os.remove("script_error.txt")
    except:
        pass
    finally:
        return {"stdout": script_stdout, "stderr": script_stderr}


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("target_path", help="Target file or folder")
parser.add_argument("target_script", help="Target script file")
parser.add_argument("--slave_script", help="Slave script path", default=r"slave.py")
parser.add_argument("--temp_idb", help="Temporary idb name", default=r"temp_idb")
parser.add_argument(
    "--ida_path",
    help="IDA Pro executable path",
    default=r"c:\Program Files\IDA 7.0\idat64.exe",
)
parser.add_argument(
    "--output_json_file",
    "-o",
    help="Path to json folder that will contain all the outputs in a JSON",
    default="AutoIda.json",
)
parser.add_argument("-r", help="Run on all files in a directory", action="store_true")
args = parser.parse_args()

# Argument handeling \ sanity checking
abs_target_path = abs_path_check_existing(args.target_path)

abs_script_path = abs_path_check_existing(args.target_script)

abs_slave_path = abs_path_check_existing(args.slave_script)

abs_ida_path = abs_path_check_existing(args.ida_path)

abs_output_idb_path = abs_path_check_existing(args.temp_idb, must_exist=False)

outputs_dict = {}
print('Running "{}" using our slave'.format(abs_script_path))


def run_ida_script_single_file(target_file_path):
    output = run_ida_script(
        target_file_path,
        abs_script_path,
        abs_slave_path,
        abs_output_idb_path,
        abs_ida_path,
    )
    return output


def run_script_on_multiple_files(files):
    outputs_dict = {}
    if not files:
        print("[X] No files where given")
        return outputs_dict

    for file in files:
        print("[?] current file: {}".format(file))
        output = run_ida_script_single_file(file)
        outputs_dict[file] = output

    return outputs_dict


all_outputs_dict = {}


def list_non_idb_files_in_directory(directory):
    target_files = []
    for filename in os.listdir(directory):
        if filename.split(".")[-1] in ("idb", "nam", "til", "id0", "id1", "id2"):
            continue
        full_path = os.path.join(directory, filename)
        if not os.path.isfile(full_path):
            print("[X] {} is not a file".format(full_path))
            continue
        target_files.append(full_path)
    return target_files


if not args.r:
    print("[?] Single file mode")
    all_outputs_dict = run_script_on_multiple_files([abs_target_path])

else:
    print("[?] Whole directory mode")
    all_files = list_non_idb_files_in_directory(abs_target_path)
    all_outputs_dict = run_script_on_multiple_files(all_files)

print("")
print("[?] Done running, here are the results")

for file in all_outputs_dict:
    if all_outputs_dict[file]:
        print("{} : Output len = {}".format(file, len(all_outputs_dict[file])))
    else:
        print("{} : No output from script".format(file))

if "output_json_file" in args:
    try:
        with open(args.output_json_file, "w") as f:
            f.write(json.dumps(all_outputs_dict))
        print("")
        print('[?] Results are stored @ "{}"'.format(args.output_json_file))
    except:
        print('[X] Error writing to file "{}"'.format(args.output_json_file))
