# POSS-Client

Python based client for uploading files to POSS.
You can download a precompiled version for Windows x64 on the releases page (no requirements, you can skip to step 3).

## Requirements
* git (for installing/upgrading)
* Python 3
* virtualenv

## Install
**1)** Clone the project and checkout the latest tag
```
git clone https://github.com/fnkr/POSS-Client.git
git checkout 1.0
cd poss
```

**2)** Set up your environment
```
virtualenv env

# Windows
env\scripts\pip install -r requirements.txt

# Linux
env/bin/pip install -r requirements.txt
```

**3)** Configure
Copy `config.dist.py` to `config.py` and modify as needed.

## Usage

Run `poss --help` for help.

```
usage: poss [-h] --upload file [file ...] [--randomize-filename] [--clipboard]

POSS Client

optional arguments:
  -h, --help            show this help message and exit
  --upload file [file ...]
                        upload files
  --randomize-filename  randomize filenames
  --clipboard           copy result to clipboard
```

## Build the exe
Just run `build_exe.bat`. Make sure you have installed `cx_freeze`.
