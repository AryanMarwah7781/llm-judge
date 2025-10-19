# How to Run the Research Notebook

## Quick Start (One Command)

```bash
source llmjudgevenv/bin/activate && cd examples && jupyter notebook groundbreaking_research_demo.ipynb
```

## Step-by-Step Instructions

### 1. Activate the Virtual Environment

```bash
source llmjudgevenv/bin/activate
```

You should see `(llmjudgevenv)` appear in your terminal prompt.

### 2. Navigate to Examples Directory

```bash
cd examples
```

### 3. Start Jupyter Notebook

```bash
jupyter notebook groundbreaking_research_demo.ipynb
```

This will:
- Open your web browser automatically
- Load the research notebook
- You can now run cells!

### 4. Select the Kernel (If Needed)

If prompted to select a kernel:
- Choose **"LLM Judge Research"** from the dropdown
- Or select `llmjudgevenv` from Python environments

### 5. Run the Notebook

- Click **"Run All"** from the Cell menu, OR
- Press `Shift + Enter` to run each cell individually

### 6. When Done

Press `Ctrl+C` in terminal to stop Jupyter, then:

```bash
deactivate
```

---

## Using VS Code (Recommended)

If you prefer VS Code:

1. Open the notebook: `examples/groundbreaking_research_demo.ipynb`
2. Click **"Select Kernel"** (top-right)
3. Choose **"LLM Judge Research"** or `llmjudgevenv`
4. Click **"Run All"** or run cells individually

---

## Troubleshooting

### Kernel Not Found?

Re-register the kernel:

```bash
source llmjudgevenv/bin/activate
python -m ipykernel install --user --name=llmjudgevenv --display-name="LLM Judge Research"
```

### Missing Packages?

Reinstall dependencies:

```bash
source llmjudgevenv/bin/activate
pip install jupyter ipykernel matplotlib seaborn pandas numpy
```

### Can't Find `llmjudgevenv`?

Make sure you're in the project root directory:

```bash
cd /Users/aryanmarwah/Documents/LLMasjudge
ls llmjudgevenv  # Should exist
```

---

## What's Installed

The `llmjudgevenv` virtual environment includes:

- All project requirements (FastAPI, OpenAI, Anthropic, etc.)
- Jupyter and IPyKernel for notebooks
- Visualization libraries (matplotlib, seaborn)
- Data analysis libraries (pandas, numpy)
- All groundbreaking AI safety modules

**Python Version:** 3.9.21
**Kernel Name:** llmjudgevenv
**Display Name:** LLM Judge Research

---

## Quick Reference

```bash
# Activate
source llmjudgevenv/bin/activate

# Run notebook
cd examples && jupyter notebook groundbreaking_research_demo.ipynb

# Deactivate
deactivate

# Check kernel is registered
jupyter kernelspec list | grep llmjudgevenv
```

---

**Everything is ready to go!** The environment is clean, fresh, and has all dependencies installed.
