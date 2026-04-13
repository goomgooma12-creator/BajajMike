# 🤖 Mike's Bajaj Life AI Chatbot — Vercel Deployment Guide

## 📁 Project Structure
```
bajaj-chatbot/
├── api/
│   └── chat.py          ← AI chatbot backend (Groq API)
├── index.html           ← Your website with fixed chatbot
├── vercel.json          ← Vercel configuration
├── requirements.txt     ← Python dependencies (none needed!)
└── README.md
```

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: Create GitHub Repository
1. Go to https://github.com → Click "New Repository"
2. Name: `mike-bajaj-life-chatbot`
3. Set to **Public** (Free Vercel works with public repos)
4. Click "Create Repository"

### STEP 2: Upload Files to GitHub
Upload these files in this EXACT structure:
```
/ (root)
├── api/
│   └── chat.py
├── index.html
├── vercel.json
└── requirements.txt
```

**Upload method:** 
- Click "uploading an existing file" on GitHub
- Upload all files maintaining folder structure
- OR use Git: `git add . && git commit -m "Initial" && git push`

### STEP 3: Deploy on Vercel
1. Go to https://vercel.com → Sign up/Login with GitHub
2. Click "Add New Project"
3. Select your `mike-bajaj-life-chatbot` repository
4. Click "Deploy" (settings auto-detected from vercel.json)

### STEP 4: Add GROQ_API_KEY Environment Variable ⚠️ CRITICAL
1. After deploy, go to your project on Vercel dashboard
2. Click **Settings** → **Environment Variables**
3. Add:
   - **Name:** `GROQ_API_KEY`
   - **Value:** Your Groq API key (get from https://console.groq.com)
   - **Environment:** Production, Preview, Development (check all 3)
4. Click **Save**
5. Go to **Deployments** → Click **Redeploy** (top right "..." menu)

### STEP 5: Get Your Groq API Key (FREE)
1. Go to: https://console.groq.com
2. Sign up for FREE account
3. Click "API Keys" → "Create API Key"
4. Copy the key → paste in Vercel environment variables

---

## ✅ WHAT'S FIXED

| Issue | Fix |
|-------|-----|
| `llama3-8b-8192` decommissioned | Updated to `llama-3.3-70b-versatile` (latest) |
| No CORS headers | Added proper CORS in Python handler |
| flask/groq dependencies | Removed! Using Python stdlib only |
| Basic responses | Added 800+ lines of Bajaj Life knowledge base |
| No conversation memory | Added chat history (last 6 messages) |
| Poor error messages | Graceful errors with Mike's WhatsApp link |

---

## 🤖 AI MODEL USED
- **Model:** `llama-3.3-70b-versatile` (Latest Groq model, Dec 2024)
- **Why:** Fastest, most capable, FREE tier available
- **Knowledge:** Deep Bajaj Life Insurance expertise built into system prompt

---

## 🧪 TEST THE CHATBOT
After deployment, try asking:
- "AWG mein 1 lakh premium pe kitna milega?"
- "Term insurance kya hota hai?"
- "Retirement ke liye best plan kya hai?"
- "AWG vs FD mein kaun better hai?"
- "Zero GST wali policy ke baare mein batao"

---

## 📞 SUPPORT
If any issue: WhatsApp Mike at +91 93821 81126

---

## ⚠️ ENVIRONMENT VARIABLES NEEDED
```
GROQ_API_KEY = gsk_xxxxxxxxxxxxxxxxxxxx  (from console.groq.com)
```
