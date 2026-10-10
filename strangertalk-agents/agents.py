"""StrangerTalk AI agents.

Usage: python agents.py guardian|seo|competitor|strategy

guardian   - uptime, speed, SSL and key-page checks (no AI, free)
seo        - on-page SEO audit + PageSpeed, with AI advice
competitor - compares competitor home pages (title, keywords, headings)
strategy   - turns the latest reports into this week's top 3 actions

100% free: AI comes from GitHub Models (free with any GitHub account, uses the
built-in GITHUB_TOKEN). If AI is unavailable, reports still contain the raw checks.

Reports are written to reports/<date>-<agent>.md. When an agent finds a
problem or finishes a weekly report it also opens a GitHub issue (in Actions).
"""
import datetime
import json
import os
import re
import socket
import ssl
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SITE = os.environ.get("SITE_URL", "https://strangertalk.in").rstrip("/")
HOST = urllib.parse.urlparse(SITE).hostname
PAGES = ["/", "/chat-with-strangers-india.html", "/anonymous-chat-no-login.html",
         "/talk-to-strangers-when-bored.html", "/omegle-alternative.html", "/faq.html"]
KEYWORDS = ["chat with strangers online free", "chat with strangers india",
            "anonymous chat no login", "talk to strangers when bored", "omegle alternative india"]
COMPETITORS = [c.strip() for c in (os.environ.get("COMPETITORS") or
               "ome.tv,emeraldchat.com,chatrandom.com,chitchat.gg").split(",") if c.strip()]

# Free model on GitHub Models; change via the AI_MODEL repo variable if it is retired.
MODEL = os.environ.get("AI_MODEL") or "openai/gpt-4.1-mini"
ROOT = Path(__file__).parent
REPORTS = ROOT / "reports"
TODAY = datetime.date.today().isoformat()
UA = {"User-Agent": "StrangerTalkAgent/1.0 (+https://strangertalk.in)"}


# ---------- helpers ----------
def fetch(path_or_url, timeout=20):
    url = path_or_url if path_or_url.startswith("http") else SITE + path_or_url
    start = time.time()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            body = r.read(2_000_000).decode("utf-8", "replace")
            return r.status, body, round(time.time() - start, 2)
    except urllib.error.HTTPError as e:
        return e.code, "", round(time.time() - start, 2)
    except Exception as e:  # DNS, timeout, TLS
        return 0, str(e), round(time.time() - start, 2)


def ssl_days_left():
    ctx = ssl.create_default_context()
    with socket.create_connection((HOST, 443), timeout=10) as s, ctx.wrap_socket(s, server_hostname=HOST) as t:
        exp = ssl.cert_time_to_seconds(t.getpeercert()["notAfter"])
    return int((exp - time.time()) // 86400)


def save(agent, text):
    REPORTS.mkdir(exist_ok=True)
    f = REPORTS / f"{TODAY}-{agent}.md"
    f.write_text(text, encoding="utf-8")
    print(text)
    return f


def open_issue(title, body, dedupe=None):
    """Opens a GitHub issue when running in Actions (gh + GH_TOKEN are present).
    dedupe: skip if an open issue with this text in its title already exists."""
    if not os.environ.get("GITHUB_ACTIONS") or not os.environ.get("GH_TOKEN"):
        return
    if dedupe:
        found = subprocess.run(["gh", "issue", "list", "--state", "open", "--search", f"{dedupe} in:title",
                                "--json", "number", "--jq", "length"], capture_output=True, text=True)
        if found.stdout.strip() not in ("", "0"):
            return
    subprocess.run(["gh", "issue", "create", "--title", title, "--body", body[:60000]], check=False)


class PageInfo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = self.desc = self.canonical = ""
        self.h1, self.imgs_no_alt, self.links, self._tag, self.text = [], 0, 0, None, []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "meta" and a.get("name", "").lower() == "description":
            self.desc = a.get("content", "")
        elif tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "img" and not a.get("alt"):
            self.imgs_no_alt += 1
        elif tag == "a":
            self.links += 1
        self._tag = tag

    def handle_endtag(self, tag):
        self._tag = None

    def handle_data(self, d):
        if self._tag == "title":
            self.title += d
        elif self._tag == "h1":
            self.h1.append(d.strip())
        if self._tag not in ("script", "style"):
            self.text.append(d)


def ai(prompt):
    """Free AI call via GitHub Models. Returns text, or a note if AI is unavailable."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "_AI skipped (no GITHUB_TOKEN). Raw data below._"
    req = urllib.request.Request(
        "https://models.github.ai/inference/chat/completions",
        data=json.dumps({"model": MODEL, "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"_AI unavailable ({e}). Raw data below._"


def latest(agent):
    files = sorted(REPORTS.glob(f"*-{agent}.md"))
    return files[-1].read_text(encoding="utf-8") if files else "(no report yet)"


# ---------- agents ----------
def guardian():
    problems, rows = [], []
    for p in PAGES + ["/robots.txt", "/sitemap.xml"]:
        code, body, secs = fetch(p)
        ok = code == 200 and secs < 3
        rows.append(f"| {p} | {code} | {secs}s | {'✅' if ok else '❌'} |")
        if code != 200:
            problems.append(f"{p} returned {code or body[:80]}")
        elif secs >= 3:
            problems.append(f"{p} is slow ({secs}s)")
    try:
        days = ssl_days_left()
        if days < 14:
            problems.append(f"SSL certificate expires in {days} days")
    except Exception as e:
        days = f"error: {e}"
        problems.append(f"SSL check failed: {e}")
    report = (f"# Website Guardian – {TODAY}\n\nSSL days left: {days}\n\n"
              "| Page | Status | Time | OK |\n|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
              + ("## Problems\n" + "\n".join(f"- {p}" for p in problems) if problems else "All good ✅"))
    print(report)  # hourly: print only, don't fill the repo with files
    if problems:  # one open issue at a time; close it once fixed to get new alerts
        open_issue(f"🚨 strangertalk.in problem: {problems[0]}", report, dedupe="strangertalk.in problem")


def page_info(path_or_url):
    code, body, secs = fetch(path_or_url)
    if code != 200:
        return {"page": path_or_url, "status": code}
    h = PageInfo()
    h.feed(body)
    return {"page": path_or_url, "title": h.title.strip(), "description": h.desc, "h1": h.h1[:3],
            "canonical": h.canonical, "words": len(re.findall(r"\w+", " ".join(h.text))),
            "imgs_without_alt": h.imgs_no_alt, "has_jsonld": "application/ld+json" in body, "load_s": secs}


def seo_checks(p):
    """Free rule-based checks, no AI needed."""
    if "status" in p:
        return [f"page returns {p['status']}"]
    out = []
    if not 20 <= len(p["title"]) <= 60: out.append(f"title is {len(p['title'])} chars (best 20-60)")
    if not 70 <= len(p["description"]) <= 160: out.append(f"description is {len(p['description'])} chars (best 70-160)")
    if len(p["h1"]) != 1: out.append(f"{len(p['h1'])} H1 tags (need exactly 1)")
    if not p["canonical"]: out.append("no canonical link")
    if p["words"] < 150: out.append(f"only {p['words']} words")
    if p["imgs_without_alt"]: out.append(f"{p['imgs_without_alt']} images without alt text")
    if not p["has_jsonld"]: out.append("no structured data (JSON-LD)")
    if p["load_s"] > 2: out.append(f"slow ({p['load_s']}s)")
    return out


def seo():
    pages = [page_info(p) for p in PAGES]
    psi = "not available"
    q = urllib.parse.urlencode({"url": SITE + "/", "strategy": "mobile", "category": "performance"})
    code, body, _ = fetch("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + q, timeout=90)
    if code == 200:
        a = json.loads(body)["lighthouseResult"]
        psi = {"score": round(a["categories"]["performance"]["score"] * 100),
               **{k: a["audits"][k]["displayValue"] for k in ("largest-contentful-paint", "cumulative-layout-shift")}}
    checks = "\n".join(f"- `{p['page']}`: " + ("; ".join(seo_checks(p)) or "✅ OK") for p in pages)
    advice = ai(
        "You are an SEO expert for strangertalk.in, a free anonymous 'chat with strangers' site for India.\n"
        f"Target keywords: {KEYWORDS}\nPage data: {json.dumps(pages)}\nMobile PageSpeed: {psi}\n"
        "Give the 5 most important fixes with the exact new title/description text to paste, "
        "and one new low-competition long-tail keyword page idea. Short, simple English.")
    f = save("seo", f"# SEO Report – {TODAY}\n\n**Mobile PageSpeed:** {psi}\n\n## Checks\n{checks}\n\n## AI advice\n{advice}\n")
    open_issue(f"📈 Weekly SEO report – {TODAY}", f.read_text(encoding="utf-8"))


def competitor():
    rows = []
    for c in COMPETITORS:
        p = page_info("https://" + c.removeprefix("https://").removeprefix("http://"))
        rows.append(p)
    table = "\n".join(f"| {p['page']} | {p.get('title', p.get('status'))} | {p.get('description', '')[:120]} | "
                      f"{', '.join(p.get('h1', []))[:80]} | {p.get('words', '')} |" for p in rows)
    advice = ai(
        "You are a competitor analyst for strangertalk.in (free anonymous stranger chat, India, 18+). "
        f"Here is data from competitor home pages: {json.dumps(rows)}\n"
        "Using ONLY this data: which keywords they target, 3 things strangertalk.in should do better, "
        "and 3 low-competition long-tail keywords they ignore. Short, simple English.")
    f = save("competitor", f"# Competitor Report – {TODAY}\n\n| Site | Title | Description | H1 | Words |\n"
                           f"|---|---|---|---|---|\n{table}\n\n## AI analysis\n{advice}\n")
    open_issue(f"🕵️ Weekly competitor report – {TODAY}", f.read_text(encoding="utf-8"))


def strategy():
    text = ai(
        "You are the growth strategist for strangertalk.in, run by one non-technical owner with no budget. "
        "Read these reports and give exactly 3 free actions for this week, ordered by impact. "
        "Each: what to do, why, time needed, how to check it worked. Short, simple English.\n\n"
        f"SEO report:\n{latest('seo')}\n\nCompetitor report:\n{latest('competitor')}")
    f = save("strategy", f"# This Week's Plan – {TODAY}\n\n{text}\n")
    open_issue(f"🧠 This week's top 3 actions – {TODAY}", f.read_text(encoding="utf-8"))


if __name__ == "__main__":
    agents = {"guardian": guardian, "seo": seo, "competitor": competitor, "strategy": strategy}
    if len(sys.argv) != 2 or sys.argv[1] not in agents:
        sys.exit(__doc__)
    agents[sys.argv[1]]()
