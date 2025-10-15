# 🚀 Quick Setup - Get Your API Keys

## ✅ Everything is Installed & Working!

You just need to add an API key to start evaluating. Here are your options:

---

## 💡 RECOMMENDED: OpenAI GPT-4o-mini (CHEAPEST)

### Why GPT-4o-mini?
- ⭐ **Only $0.002 per Q&A evaluation** (~$0.20 per 100 Q&As)
- 🚀 Fast and reliable
- 🎯 Great quality for most use cases
- 📊 100 evaluations = cost of a coffee!

### Get Your OpenAI API Key (5 minutes):

1. **Sign up:** Go to https://platform.openai.com/signup
   - Use your email or Google/Microsoft account
   
2. **Get API Key:** Visit https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it "LLM Judge API"
   - Copy the key (starts with `sk-...`)
   - ⚠️ Save it now! You can't see it again
   
3. **Add Credit:** Go to https://platform.openai.com/account/billing
   - Click "Add payment method"
   - Add $5-10 to start
   - This will last for thousands of evaluations!

4. **Add to .env:** Open `/Users/aryanmarwah/Documents/LLMasjudge/.env`
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

5. **Test it:**
   ```bash
   cd /Users/aryanmarwah/Documents/LLMasjudge
   source .venv/bin/activate
   python verify_setup.py
   ```

---

## 🆓 FREE ALTERNATIVE: Groq (If you don't want to pay)

### Get Groq API Key (3 minutes):

1. **Sign up:** Go to https://console.groq.com/
   
2. **Get API Key:** 
   - Go to API Keys section
   - Click "Create API Key"
   - Copy the key
   
3. **I'll add Groq support to your API** (just ask me!)

---

## 📝 Current Status

✅ Virtual environment created  
✅ All packages installed  
✅ Server code working  
✅ .env file created  
⏳ **Just need API key!**

---

## 🎯 Next Steps

1. Choose one option above
2. Get your API key (takes 3-5 minutes)
3. Add it to `.env` file
4. Run: `python verify_setup.py` to confirm
5. Start the server: `uvicorn app.main:app --reload`
6. Visit: http://localhost:8000/docs

---

## 💰 Cost Breakdown (GPT-4o-mini)

| Evaluations | Approximate Cost |
|-------------|------------------|
| 10 Q&As     | $0.02           |
| 100 Q&As    | $0.20           |
| 1,000 Q&As  | $2.00           |
| 10,000 Q&As | $20.00          |

**With $5 credit = ~2,500 evaluations!**

---

## 🤔 Which Should I Choose?

### Choose OpenAI GPT-4o-mini if:
- ✅ You want the best quality
- ✅ You're okay spending ~$0.20 per 100 evaluations
- ✅ You want reliable, production-ready results

### Choose Groq (FREE) if:
- ✅ You want to test without paying
- ✅ You're okay with slightly lower quality
- ✅ You want very fast responses

---

## 🆘 Need Help?

If you have your API key and need help adding it:
1. Open `.env` file
2. Replace `your_openai_api_key_here` with your actual key
3. Make sure there are no extra spaces or quotes
4. Save the file
5. Run `python verify_setup.py`

Example:
```env
# Before:
OPENAI_API_KEY=your_openai_api_key_here

# After:
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

---

## ✨ You're Almost There!

Just one more step and you'll have a fully working LLM evaluation API! 🎉
