# StrangerTalk AI Agents (Step 3), 100% free

| Agent | Kya karta hai | Kab chalta hai |
|---|---|---|
| 🩺 Guardian | Site down/slow, SSL expiry, pages 404 check | Har ghante |
| 🔍 SEO | Title, description, H1, speed check aur AI ke fixes | Har Monday |
| 🕵️ Competitor | Competitor sites ke title, keywords aur headings ki tulna | Har Monday |
| 🧠 Strategy | Is hafte ke top 3 free kaam | Har Monday |

**Kharcha ₹0.** Ye sab GitHub Actions pe chalta hai, aur AI ke liye **GitHub Models** use hota hai jo GitHub ke saath free milta hai. Koi API key nahi chahiye.
AI kaam na kare (jaise free limit khatam ho jaaye), tab bhi report mein saare checks aate rahenge.

Report GitHub **Issue** ban kar aati hai, aur GitHub app ki notification se phone pe dikhti hai. Reports `reports/` folder mein bhi save hoti hain.
Guardian ek problem pe ek hi issue kholta hai. Problem fix hone pe issue close kar dena.

## Setup

1. PR merge karo. Bas itna hi.
2. Test: **Actions** tab → "StrangerTalk AI agents" → **Run workflow** → `weekly` chuno.

## Optional

Repo ke **Settings → Secrets and variables → Actions → Variables** mein ye set kar sakte ho:
- `COMPETITORS`: apne competitors, jaise `site1.com,site2.com`. Default list: ome.tv, emeraldchat.com, chatrandom.com, chitchat.gg
- `AI_MODEL`: agar default free model (`openai/gpt-4.1-mini`) band ho jaaye, to github.com/marketplace/models se koi aur free model ka naam daal do.
