# 📋 Installation & Setup Guide

## System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **RAM**: 4 GB
- **Disk**: 500 MB free space
- **OS**: Windows, Mac, or Linux

### Recommended
- **Python**: 3.9 or higher
- **RAM**: 8 GB
- **Disk**: 1 GB free space
- **Modern OS** (Windows 10+, macOS 10.14+, Ubuntu 18.04+)

---

## Installation Steps

### Step 1: Verify Python Installation

#### Windows
```bash
python --version
```

#### Mac/Linux
```bash
python3 --version
```

**Expected output:** `Python 3.7.0` or higher

**If not installed:**
- Download from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Step 2: Navigate to Project Directory

```bash
cd "c:\SALES PREDICTION USING PYTHON"
```

### Step 3: Create Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` in your command prompt.**

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**This installs:**
- numpy (numerical computing)
- pandas (data analysis)
- scikit-learn (machine learning)
- matplotlib (plotting)
- seaborn (statistical visualization)
- joblib (model serialization)
- Pillow (image processing)

### Step 5: Verify Installation

```bash
python -c "import numpy, pandas, sklearn; print('✓ All packages installed!')"
```

---

## Quick Start Commands

### Option 1: Run GUI Application (Recommended)

```bash
python gui_app.py
```

**Expected:** A window opens with sales prediction interface

### Option 2: Run Models Training

```bash
python models.py
```

**Expected:** Outputs model performance metrics

### Option 3: Run Jupyter Notebook

```bash
jupyter notebook comprehensive_sales_prediction.ipynb
```

**Expected:** Jupyter opens in browser with analysis

### Option 4: Run Validation

```bash
python setup_validation.py
```

**Expected:** Displays all system checks

---

## Troubleshooting Installation

### Issue: `python: command not found`

**Cause:** Python not in PATH or not installed

**Solutions:**
1. Reinstall Python (check "Add to PATH")
2. Use full path: `C:\Python39\python.exe --version`
3. Try `python3` instead of `python`

### Issue: `No module named 'sklearn'`

**Cause:** Scikit-learn not installed

**Solution:**
```bash
pip install scikit-learn
```

### Issue: `Permission denied`

**Cause:** Virtual environment not activated

**Solution:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Issue: Slow package installation

**Cause:** Pip using slow mirror

**Solution:**
```bash
pip install -r requirements.txt -i https://pypi.org/simple/
```

### Issue: Out of disk space

**Cause:** Virtual environment too large

**Solution:**
```bash
# Remove and recreate
rmdir /s venv
python -m venv venv
```

---

## Verify Complete Installation

Run this to check everything:

```python
import sys
print(f"Python: {sys.version}")

import numpy as np
print(f"NumPy: {np.__version__}")

import pandas as pd
print(f"Pandas: {pd.__version__}")

import sklearn
print(f"Scikit-learn: {sklearn.__version__}")

import matplotlib
print(f"Matplotlib: {matplotlib.__version__}")

print("\n✓ All packages installed successfully!")
```

---

## Next Steps After Installation

### Beginners
1. Run `python gui_app.py`
2. Make some predictions
3. Compare models
4. Check feature importance

### Intermediate Users
1. Open Jupyter notebook
2. Run each cell to understand flow
3. Modify parameters
4. Train your own models

### Advanced Users
1. Use your own dataset
2. Implement custom models
3. Optimize hyperparameters
4. Deploy in production

---

## Environment Variables (Optional)

Set data path:
```bash
set DATA_PATH="c:\SALES PREDICTION USING PYTHON"
```

---

## Using with IDEs

### VS Code
1. Open folder: `File → Open Folder`
2. Select Python interpreter: `Ctrl+Shift+P → Python: Select Interpreter`
3. Choose virtual environment
4. Run: `F5` or `Ctrl+F5`

### PyCharm
1. Open project
2. Configure interpreter: `Settings → Project → Python Interpreter`
3. Add virtual environment
4. Run: `Shift+F10`

### Jupyter Lab
```bash
pip install jupyterlab
jupyter lab
```

---

## Performance Optimization

### For Faster Execution
```python
# Reduce dataset size
data = generate_sales_data(n_samples=100)  # Instead of 300

# Reduce model complexity
n_estimators = 50  # Instead of 100
max_depth = 5      # Instead of 10
```

### For Lower Memory Usage
```python
# Use smaller batch sizes
batch_size = 32

# Use data types wisely
df['column'] = df['column'].astype('float32')
```

---

## Upgrading Packages

Check for updates:
```bash
pip list --outdated
```

Upgrade specific package:
```bash
pip install --upgrade scikit-learn
```

Upgrade all packages:
```bash
pip install -r requirements.txt --upgrade
```

---

## Uninstalling

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# Mac/Linux
rm -rf venv
```

### Remove All Packages
```bash
pip freeze | xargs pip uninstall -y
```

---

## Getting Help

If you encounter issues:

1. Check **README.md** for documentation
2. Review **QUICKSTART.md** for examples
3. Check code comments for explanations
4. Search error messages on Stack Overflow
5. Test with sample data first

---

## Support Resources

- 🐍 Python: https://www.python.org/
- 🤖 Scikit-learn: https://scikit-learn.org/
- 📊 Pandas: https://pandas.pydata.org/
- 📈 Matplotlib: https://matplotlib.org/
- 📚 Real Python: https://realpython.com/

---

## FAQ

### Q: Can I use Python 2.7?
**A:** No, Python 3.7+ is required.

### Q: Can I use on Mac/Linux?
**A:** Yes! Same installation process, use `python3` instead of `python`.

### Q: Do I need GPU?
**A:** No, CPU is sufficient for this project.

### Q: How much storage?
**A:** ~500 MB for all packages and data.

### Q: Can I use without virtual environment?
**A:** Not recommended, but possible. Just skip the `venv` steps.

### Q: Is internet required?
**A:** Yes, for initial installation. After that, no.

---

## Verification Checklist

After installation, verify:

- [ ] Python version 3.7+ installed
- [ ] Virtual environment created
- [ ] All packages installed
- [ ] GUI application starts
- [ ] Models train successfully
- [ ] Jupyter notebook runs
- [ ] Predictions work
- [ ] No error messages

---

**You're all set!** 🚀

Run `python gui_app.py` to get started!
