# StrangerTalk Safety Kit (Step 1: Safety aur Legal)

strangertalk.in ke liye safety aur legal files. Ye kisi bhi website pe chalengi, chahe site Next.js, React, WordPress ya plain HTML mein bani ho.

## Files

| File | Kya hai |
|---|---|
| `safety.js` | Ek hi script jo 18+ age gate, cookie/privacy banner, footer legal links aur chat message filter deti hai |
| `terms.html` | Terms of Service |
| `privacy.html` | Privacy Policy (DPDP Act 2023) |
| `guidelines.html` | Community Guidelines |
| `grievance.html` | Grievance Officer page (IT Rules 2021 ke hisaab se zaroori) |
| `safety-tips.html` | Users ke liye safety tips (SEO ke liye bhi achha page) |
| `legal.css` | In pages ka design |

## Kaise lagayein (3 steps)

1. **Details check karo.** Naam (Amit Kumar), email (strangertalk.in@gmail.com) aur date pages mein bhar di gayi hain. Bas ye dhyan do:
   - IT Rules ke hisaab se Grievance page pe **poora postal address** hona chahiye. Abhi wahan sirf "India" likha hai, isliye `grievance.html` mein address daal dena.
   - `privacy.html` ki table maan kar chalti hai ki chat messages server pe save **nahi** hote. Agar aap save karte ho, to wo line badal dena.

2. **Upload karo.** Saari 7 files website ke main (root) folder mein daalo, jahan `index.html` ya `public/` folder hai.
   - Next.js / React (Vite) mein inhe `public/` folder mein daalo.
   - WordPress mein `safety.js` ko plugin "WPCode" se footer mein daalo, aur pages ka content naye WordPress pages mein copy karo.

3. **Script jodo.** Website ke har page mein `</body>` se just pehle ye line daalo:
   ```html
   <script src="/safety.js" defer></script>
   ```
   Next.js mein ye `app/layout.js` ya `pages/_document.js` mein jaati hai.

## Chat filter kaise use karein

Apne chat code mein message bhejne se pehle ye check lagao:

```js
const r = StrangerTalkSafety.filterMessage(text);
if (r.blocked) { alert(r.reason); return; }
send(r.text); // gaali wale shabd *** ho jayenge
```

Ye filter phone number, email, paise maangna aur bachchon se jude sexual messages block karta hai. **Dhyan do:** browser wala filter koi bhi bypass kar sakta hai, isliye server pe bhi same check lagana padega.

## Jo abhi baaki hai (iske liye site ka chat code chahiye)

- [ ] Har chat mein **Report** aur **Block** button
- [ ] Server pe reports save karna, aur 3 report hone pe auto temporary ban
- [ ] IP ya device ban list
- [ ] Server-side message filter
- [ ] Video chat mein nudity detection (AI moderation)

## Zaroori note

Ye legal pages ek **template** hain, legal advice nahi. Live karne se pehle kisi lawyer ya CA se ek baar check karwa lena achha rahega, khaas kar agar aap paid plans shuru karte ho.
