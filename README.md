# DeDRM CLI

Clone with
```bash
git clone --recurse-submodules https://github.com/Penacillin/dedrm.git
```

Put your `AdobeKey.der` in `~/`
```bash
mkdir outdir
pip install -r requirements.txt
python main.py -i book.epub -o outdir -k ~/
```

## Description

This script is just a hack to run [DeDRM](https://github.com/apprenticeharper/DeDRM_tools)
with just python.
