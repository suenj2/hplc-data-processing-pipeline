# HPLC Data Processing Pipline - local setup

This workspace contains an end-to-end Python pipeline for processing HPLC soil extraction experiments.
It:
- loads raw HPLC export files (.xlsx) from Excel
- loads calibration / spike concentration tables and biosolid masses
- performs all calculations (concentrations, recoveries, etc.)
- writes a processed Excel file and a summary report for all experiments

Quick setup (Windows PowerShell):

1. Create and activate a virtual environment

On Windows PowerShell:
```powershell
python -m venv .venv
\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```
On macOS/Linux:
```powershell
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Input / output layout

RDKit is not always available on pip. It's recommended to install via conda:

```powershell
conda create -n rdkit-env -c conda-forge rdkit python=3.10
conda activate rdkit-env
pip install -r requirements.txt
```

3. Run the pipeline

```powershell
python main.py
```

Files added
- `requirements.txt` - minimal dependencies
