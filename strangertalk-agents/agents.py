"""StrangerTalk AI agents.

Usage: python agents.py guardian|seo|competitor|strategy

guardian   - uptime, speed, SSL and key-page checks (no AI, free)
seo        - on-page SEO audit + PageSpeed, summarised by Claude
competitor - Claude researches competitors with web search
strategy   - Claude turns the latest reports into this week's top 3 actions

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
# Leave empty to let the competitor agent find the top-ranking sites itself.
COMPETITORS = [c for c in os.environ.get("COMPETITORS", "").split(",") if c.strip()]

MODEL = "claude-opus-5-5"
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


def claude(prompt, web=False, effort="medium"):
    """One Claude call. web=True gives it web search + fetch. Returns the text answer."""
    import anthropic

    client = anthropic.Anthropic()
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 15},
             {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 10}] if web else []
    messages = [{"role": "user", "content": prompt}]
    for _ in range(5):  # resume pause_turn a few times at most
        try:
            r = client.beta.messages.create(
                model=MODEL, max_tokens=16000, messages=messages, tools=tools,
                output_config={"effort": effort},
                betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            )
        except anthropic.AuthenticationError:
            sys.exit("ANTHROPIC_API_KEY is missing or invalid - add it in GitHub repo Settings > Secrets.")
        except anthropic.RateLimitError:
            time.sleep(60)
            continue
        if r.stop_reason == "refusal":
            return "_Claude declined this request._"
        if r.stop_reason != "pause_turn":
            return "\n".join(b.text for b in r.content if b.type == "text").strip()
        messages = [messages[0], {"role": "assistant", "content": r.content}]
    return "_Agent stopped after too many web-search rounds._"


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


def seo():
    pages = []
    for p in PAGES:
        code, body, secs = fetch(p)
        if code != 200:
            pages.append({"page": p, "status": code})
            continue
        h = PageInfo()
        h.feed(body)
        words = len(re.findall(r"\w+", " ".join(h.text)))
        pages.append({"page": p, "title": h.title.strip(), "title_len": len(h.title.strip()),
                      "description": h.desc, "desc_len": len(h.desc), "h1": h.h1,
                      "canonical": h.canonical, "words": words, "imgs_without_alt": h.imgs_no_alt,
                      "links": h.links, "has_jsonld": "application/ld+json" in body, "load_s": secs})
    psi = "PageSpeed: not available"
    q = urllib.parse.urlencode({"url": SITE + "/", "strategy": "mobile", "category": "performance",
                                **({"key": os.environ["PAGESPEED_KEY"]} if os.environ.get("PAGESPEED_KEY") else {})})
    code, body, _ = fetch("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + q, timeout=90)
    if code == 200:
        a = json.loads(body)["lighthouseResult"]["audits"]
        psi = {k: a[k]["displayValue"] for k in ("largest-contentful-paint", "cumulative-layout-shift",
                                                  "total-blocking-time", "speed-index") if k in a}
    text = claude(
        "You are an SEO expert for strangertalk.in, a free anonymous 'chat with strangers' site for India.\n"
        f"Target keywords: {KEYWORDS}\n\nPage data (JSON):\n{json.dumps(pages, indent=1)}\n\n"
        f"Mobile PageSpeed: {psi}\n\n"
        "Write a short report in simple English: 1) score out of 10, 2) the 5 most important fixes, "
        "each with the exact new title/description/text to paste, 3) one new long-tail keyword page idea "
        "with low competition. Be concise.", effort="medium")
    f = save("seo", f"# SEO Report – {TODAY}\n\n{text}\n")
    open_issue(f"📈 Weekly SEO report – {TODAY}", f.read_text(encoding="utf-8"))


def competitor():
    who = f"these competitors: {', '.join(COMPETITORS)}" if COMPETITORS else \
        "the top 5 sites currently ranking on Google for 'chat with strangers' and 'omegle alternative'"
    text = claude(
        f"You are a competitor analyst for strangertalk.in (free anonymous stranger chat, India, 18+). "
        f"Research {who}. For each: main features, target keywords in their title/headings, "
        "anything new recently, and one weakness we can beat. Then list 3 things strangertalk.in should "
        "copy or do better, and 3 low-competition long-tail keywords they are ignoring. "
        "Only state facts you found; cite the URL. Keep it short.", web=True, effort="medium")
    f = save("competitor", f"# Competitor Report – {TODAY}\n\n{text}\n")
    open_issue(f"🕵️ Weekly competitor report – {TODAY}", f.read_text(encoding="utf-8"))


def strategy():
    text = claude(
        "You are the growth strategist for strangertalk.in, run by one non-technical owner with little time "
        "and a small budget. Read these reports and give exactly 3 actions for this week, ordered by impact. "
        "Each action: what to do, why, time needed, and how to check it worked. Simple English, short.\n\n"
        f"SEO report:\n{latest('seo')}\n\nCompetitor report:\n{latest('competitor')}", effort="high")
    f = save("strategy", f"# This Week's Plan – {TODAY}\n\n{text}\n")
    open_issue(f"🧠 This week's top 3 actions – {TODAY}", f.read_text(encoding="utf-8"))


if __name__ == "__main__":
    agents = {"guardian": guardian, "seo": seo, "competitor": competitor, "strategy": strategy}
    if len(sys.argv) != 2 or sys.argv[1] not in agents:
        sys.exit(__doc__)
    agents[sys.argv[1]]()
