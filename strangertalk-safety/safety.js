/*
 * StrangerTalk Safety Kit — ek hi file, kisi bhi website pe chalegi.
 *
 * Kya karta hai:
 *   1. 18+ Age Gate  — pehli baar site khulne pe confirm karwata hai
 *   2. Cookie / Privacy consent banner (DPDP Act 2023)
 *   3. Footer mein legal links (Terms, Privacy, Guidelines, Grievance, Safety)
 *   4. window.StrangerTalkSafety.filterMessage(text) — chat message filter
 *
 * Lagane ka tareeka: apni har page ke </body> se just pehle ye line daalo:
 *   <script src="/safety.js" defer></script>
 */
(function () {
  "use strict";

  // ====== SETTINGS (sirf yahan badlo) ======
  var CONFIG = {
    siteName: "StrangerTalk",
    minAge: 18,
    links: {
      terms: "/terms.html",
      privacy: "/privacy.html",
      guidelines: "/guidelines.html",
      grievance: "/grievance.html",
      safety: "/safety-tips.html"
    },
    // Age gate kitne din tak yaad rakhe
    rememberDays: 30
  };
  // ==========================================

  var AGE_KEY = "st_age_ok";
  var CONSENT_KEY = "st_consent";

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  var css = [
    ".st-overlay{position:fixed;inset:0;background:rgba(5,8,15,.92);z-index:2147483646;display:flex;align-items:center;justify-content:center;padding:16px;font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}",
    ".st-box{background:#151a26;color:#e9edf5;max-width:420px;width:100%;border-radius:16px;padding:28px 22px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.5)}",
    ".st-box h2{margin:0 0 10px;font-size:22px}",
    ".st-box p{margin:0 0 14px;font-size:14px;line-height:1.55;color:#b8c0d0}",
    ".st-box ul{text-align:left;font-size:13px;color:#b8c0d0;padding-left:20px;margin:0 0 18px;line-height:1.6}",
    ".st-box a{color:#7aa7ff}",
    ".st-btn{display:block;width:100%;border:0;border-radius:10px;padding:13px;font-size:15px;font-weight:600;cursor:pointer;margin-top:8px}",
    ".st-yes{background:#3b82f6;color:#fff}",
    ".st-no{background:transparent;color:#b8c0d0;border:1px solid #3a4256}",
    ".st-cookie{position:fixed;left:12px;right:12px;bottom:12px;max-width:560px;margin:0 auto;background:#151a26;color:#e9edf5;border-radius:12px;padding:14px 16px;z-index:2147483645;font:13px/1.5 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;box-shadow:0 10px 40px rgba(0,0,0,.4);display:flex;gap:10px;align-items:center;flex-wrap:wrap}",
    ".st-cookie span{flex:1 1 240px}",
    ".st-cookie a{color:#7aa7ff}",
    ".st-cookie button{border:0;border-radius:8px;padding:9px 14px;font-weight:600;cursor:pointer}",
    ".st-footer{text-align:center;padding:18px 12px;font:12px/1.8 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#8a93a6}",
    ".st-footer a{color:inherit;margin:0 8px;text-decoration:underline}"
  ].join("");

  function addStyle() {
    var s = document.createElement("style");
    s.textContent = css;
    document.head.appendChild(s);
  }

  // ---------- 1. AGE GATE ----------
  function ageOk() {
    var v = parseInt(store(AGE_KEY), 10);
    return v && Date.now() - v < CONFIG.rememberDays * 864e5;
  }

  function showAgeGate() {
    var o = document.createElement("div");
    o.className = "st-overlay";
    o.setAttribute("role", "dialog");
    o.setAttribute("aria-modal", "true");
    o.innerHTML =
      '<div class="st-box">' +
      "<h2>Kya aap " + CONFIG.minAge + "+ hain?</h2>" +
      "<p>" + CONFIG.siteName + " sirf " + CONFIG.minAge + " saal ya usse zyada umar ke logon ke liye hai.</p>" +
      "<ul>" +
      "<li>Aap ajnabi (strangers) se baat karenge \u2014 apni personal info share na karein.</li>" +
      "<li>Galat behaviour ko turant <b>Report</b> karein.</li>" +
      "<li>Nudity, gaali, harassment aur bachchon se jude content pe permanent ban.</li>" +
      "</ul>" +
      '<p>Aage badh kar aap hamari <a href="' + CONFIG.links.terms + '">Terms</a>, ' +
      '<a href="' + CONFIG.links.privacy + '">Privacy Policy</a> aur ' +
      '<a href="' + CONFIG.links.guidelines + '">Community Guidelines</a> se sahmat hain.</p>' +
      '<button class="st-btn st-yes" type="button">Haan, main ' + CONFIG.minAge + '+ hoon \u2014 Aage badhein</button>' +
      '<button class="st-btn st-no" type="button">Nahi, main ' + CONFIG.minAge + ' se kam hoon</button>' +
      "</div>";
    document.body.appendChild(o);
    document.documentElement.style.overflow = "hidden";

    o.querySelector(".st-yes").onclick = function () {
      store(AGE_KEY, String(Date.now()));
      o.remove();
      document.documentElement.style.overflow = "";
      maybeShowConsent();
    };
    o.querySelector(".st-no").onclick = function () {
      o.querySelector(".st-box").innerHTML =
        "<h2>Maaf kijiye \ud83d\ude4f</h2><p>Ye website " + CONFIG.minAge +
        " saal se kam umar ke logon ke liye nahi hai. Aap ye page band kar sakte hain.</p>";
    };
  }

  // ---------- 2. COOKIE / PRIVACY CONSENT ----------
  function maybeShowConsent() {
    if (store(CONSENT_KEY)) return;
    var b = document.createElement("div");
    b.className = "st-cookie";
    b.innerHTML =
      "<span>Hum site chalane ke liye zaroori cookies aur basic data (jaise IP, safety ke liye) use karte hain. " +
      'Details: <a href="' + CONFIG.links.privacy + '">Privacy Policy</a>.</span>' +
      '<button type="button" style="background:#3b82f6;color:#fff">Theek hai</button>' +
      '<button type="button" style="background:#2a3142;color:#e9edf5">Sirf zaroori</button>';
    document.body.appendChild(b);
    var btns = b.querySelectorAll("button");
    btns[0].onclick = function () { store(CONSENT_KEY, "all"); b.remove(); };
    btns[1].onclick = function () { store(CONSENT_KEY, "essential"); b.remove(); };
  }

  // ---------- 3. FOOTER LEGAL LINKS ----------
  function addFooter() {
    if (document.querySelector(".st-footer")) return;
    var f = document.createElement("div");
    f.className = "st-footer";
    var L = CONFIG.links;
    f.innerHTML =
      '<a href="' + L.terms + '">Terms</a>' +
      '<a href="' + L.privacy + '">Privacy</a>' +
      '<a href="' + L.guidelines + '">Community Guidelines</a>' +
      '<a href="' + L.safety + '">Safety Tips</a>' +
      '<a href="' + L.grievance + '">Grievance / Report</a>' +
      "<div>\u00a9 " + new Date().getFullYear() + " " + CONFIG.siteName + " \u00b7 Sirf " + CONFIG.minAge + "+</div>";
    document.body.appendChild(f);
  }

  // ---------- 4. CHAT MESSAGE FILTER ----------
  // Ye basic filter hai. Apne chat code mein message bhejne se pehle use karein:
  //   var r = StrangerTalkSafety.filterMessage(text);
  //   if (r.blocked) { alert(r.reason); return; }  else send(r.text);
  // Note: browser wala filter koi bhi bypass kar sakta hai \u2014 server pe bhi same check lagana zaroori hai.
  var BAD_WORDS = [
    // Apni list yahan badhayein (lowercase)
    "madarchod", "behenchod", "bhenchod", "chutiya", "bhosdi", "randi", "gandu",
    "fuck", "bitch", "slut", "whore", "nude", "nudes", "sex chat", "sexchat"
  ];
  var BLOCK_PATTERNS = [
    { re: /\b(child|minor|underage|kid|bachch[ai]|nabalig)\b.*\b(nude|sex|porn|pic|video)\b/i,
      reason: "Ye message bachchon ki safety policy ke against hai. Aisa content strictly mana hai." },
    { re: /(\+?91[\s-]?)?[6-9]\d{9}\b/, reason: "Safety ke liye phone number share karna allowed nahi hai." },
    { re: /\b[\w.+-]+@[\w-]+\.[\w.]{2,}\b/, reason: "Safety ke liye email share karna allowed nahi hai." },
    { re: /\b(upi|paytm|gpay|phonepe)\b.*\b(pay|send|bhej|paise)\b/i, reason: "Paise maangna / bhejna allowed nahi hai (scam se bachein)." }
  ];

  function filterMessage(text) {
    var t = String(text || "");
    for (var i = 0; i < BLOCK_PATTERNS.length; i++) {
      if (BLOCK_PATTERNS[i].re.test(t)) return { blocked: true, reason: BLOCK_PATTERNS[i].reason, text: "" };
    }
    var clean = t;
    BAD_WORDS.forEach(function (w) {
      var re = new RegExp(w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
      clean = clean.replace(re, function (m) { return m[0] + "*".repeat(Math.max(m.length - 1, 1)); });
    });
    return { blocked: false, reason: "", text: clean, censored: clean !== t };
  }

  window.StrangerTalkSafety = { filterMessage: filterMessage, config: CONFIG };

  // ---------- START ----------
  function start() {
    addStyle();
    addFooter();
    if (ageOk()) maybeShowConsent();
    else showAgeGate();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
