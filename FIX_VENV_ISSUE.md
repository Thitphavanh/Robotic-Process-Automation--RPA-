# 🔧 Fix Virtual Environment Issue

## ❌ Problem:
You're in a virtual environment (venv) that doesn't have google-generativeai installed.

```
(venv) python stock_bot_macos_gemini.py
ModuleNotFoundError: No module named 'google'
```

---

## ✅ Solutions:

### **Solution 1: Deactivate venv (Recommended)**

```bash
# Exit the virtual environment
deactivate

# Now run the script
python stock_bot_macos_gemini.py
```

This will use the system Python (Anaconda) which has the package installed.

---

### **Solution 2: Install in venv**

If you want to keep using venv:

```bash
# Make sure you're in venv (you'll see (venv) in prompt)
pip install google-generativeai pyautogui pillow python-dotenv

# Then run
python stock_bot_macos_gemini.py
```

---

### **Solution 3: Use Anaconda Python directly**

```bash
# Deactivate venv first
deactivate

# Use Anaconda's Python
/opt/anaconda3/bin/python stock_bot_macos_gemini.py
```

---

## 🎯 Quick Fix (Copy-Paste This):

```bash
# Deactivate venv
deactivate

# Run the script
python stock_bot_macos_gemini.py
```

---

## 📋 Verify Installation:

After deactivating venv, check:

```bash
# Should NOT show (venv) in prompt
python -c "import google.generativeai as genai; print('✅ OK')"
```

If you see `✅ OK`, you're ready!

---

## 💡 Understanding the Issue:

**Virtual Environment (venv):**
- Isolated Python environment
- Has its own packages
- Doesn't share with system Python

**System Python (Anaconda):**
- Where you installed google-generativeai
- Has all the packages

**Solution:**
- Either use system Python (deactivate venv)
- Or install packages in venv too

---

## 🚀 Ready to Run:

```bash
# 1. Deactivate venv
deactivate

# 2. Set API key (if not set)
export GEMINI_API_KEY='AIzaSy-your-key'

# 3. Run!
python stock_bot_macos_gemini.py
```

---

**Common Commands:**

```bash
# Check if in venv
echo $VIRTUAL_ENV

# Deactivate venv
deactivate

# Activate venv (if you want back in)
source venv/bin/activate

# Check Python location
which python

# Check installed packages
pip list | grep google
```

---

**Quick Test:**

```bash
deactivate
python test_gemini_api.py
```

Should work! ✅
