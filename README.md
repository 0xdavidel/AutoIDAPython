# Welcome to AutoIDAPython!

Ever wanted to run a single IDA Pro Python script over a whole directory? 
This project is exactly for that, simply give it the file you want to run on, and the script file you want to run and you are set!

Tested using Python 2.7 and Python 3.5 + IDA Pro 7.0 (running python 2.7)

# Usage

```
usage: AutoIDAPython.py [-h] [--slave_script SLAVE_SCRIPT] [--temp_idb TEMP_IDB] [--ida_path IDA_PATH]
                     [--output_json_file OUTPUT_JSON_FILE] [-r]
                     target_path target_script

positional arguments:
  target_path           Target file or folder
  target_script         Target script file

optional arguments:
  -h, --help            show this help message and exit
  --slave_script SLAVE_SCRIPT
                        Slave script path
  --temp_idb TEMP_IDB   Temporary idb name
  --ida_path IDA_PATH   IDA Pro executable path
  --output_json_file OUTPUT_JSON_FILE, -o OUTPUT_JSON_FILE
                        Path to json folder that will contain all the outputs in a JSON
  -r                    Run on all files in a directory
```
### Examples
* AutoIDAPython.py myRansomeware.exe GimmeYourEncryptionKey.py
* AutoIDAPython.py RansomewareCollectionDir GimmeYourEncryptionKey.py -r -o AllRansomKeys.json

For examples of scripts to use and how I develop them feel free to visit [my website](0xdavid.com), someday I will upload how I develop scripts for this system. 
## Project structure

* AutoIDAPython.py - The "Orchestrator" of the whole operation, runs IDA Pro and uses the slave.py to capture the output of your script
* slave.py - The default slave script. It gets a python script from argument #1 and runs it while capturing all the STDOUT and STDERR with some python magic.

#### Json output structure
```{"Filename":{"stderr": ... , "stdout": ...}}```

## How it works

IDA Pro can receive command-line arguments, the useful ones for this project are:
* -A: Autonomous mode, meaning no need for user interaction for each file.
* -c: Dissasemble a new file, so that even if the target IDB (IDA database file) exists, we will override it.
* -S: A script file to run, we can pass arguments to the script by adding them after the script path - like this " **-S**myScript.py ARGUMENT1 ARGUMENT2"
* -o: Output IDB path, I decided not to inflate your disks and use a single temporary IDB that is overridden every new file.

The script file you send is running using the "slave.py" script
The slave is responsible for :
* Reading the script path from the first argument
* Executing it and capturing the stdout and stderr using contextlib magic
* Writing stdout into "script_output.txt" and stderr into "script_error.txt"

## Disclaimer
Running IDA on malware samples is never recommended outside of a correctly configured VM. Any damages or errors this might give are not my responsibility.