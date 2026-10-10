# StrangerTalk AI Agents (Step 3)

| Agent | Kya karta hai | Kab chalta hai | AI kharcha |
|---|---|---|---|
| 🩺 Guardian | Site down/slow, SSL expiry, pages 404 check | Har ghante | Free (AI nahi) |
| 🔍 SEO | Title, description, H1, speed check + fixes | Har Monday | Haan |
| 🕵️ Competitor | Top competitors ki research (web search) | Har Monday | Haan |
| 🧠 Strategy | Is hafte ke top 3 kaam | Har Monday | Haan |

Report GitHub **Issue** ban kar aati hai, aur GitHub app ki notification se phone pe dikhti hai. Reports `reports/` folder mein bhi save hoti hain.
Guardian ek problem pe ek hi issue kholta hai. Problem fix ho jaaye to issue close kar dena, taaki agli baar naya alert aa sake.

## Setup (ek baar)

1. **Claude API key lo:** https://console.anthropic.com → API Keys → Create key. Thoda credit bhi add karo (shuruaat ke liye $5 kaafi hai).
2. GitHub repo mein **Settings → Secrets and variables → Actions → New repository secret** pe jaao:
   - Name: `ANTHROPIC_API_KEY`, Value: apni key
3. (Optional) Usi page pe **Variables** tab mein `COMPETITORS` naam ka variable banao, jaise `site1.com,site2.com`. Khali chhod doge to agent khud Google pe top sites dhoondh lega.
4. Test: **Actions** tab → "StrangerTalk AI agents" → **Run workflow** → `weekly` chuno.

## Kharcha (andaza)

Guardian free hai. Weekly AI agents ka kharcha **lagbhag $1–3 har hafte** (₹80–250) ho sakta hai. Ye andaza hai: asli kharcha web search aur report ki lambai pe depend karega, aur console.anthropic.com pe dikhta rahega. Kharcha kam karna ho to `agents.py` mein `effort` ko `"low"` kar do.

## Note

- Agents tabhi sahi report denge jab Step 1 aur Step 2 ki files website pe upload ho chuki hongi.
- Model `claude-opus-5-5` hai. Isse badalna ho to `agents.py` mein `MODEL` ki value badlo.
