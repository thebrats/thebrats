# StrangerTalk SEO Kit (Step 2)

strangertalk.in ko Google (aur ChatGPT, Perplexity jaise AI search) mein dikhane ke liye files.

## Files

| File | Kya hai | Kahan daalna hai |
|---|---|---|
| `head-tags.html` | Homepage ke liye title, description, social sharing aur Google structured data | Homepage ke `<head>` ke andar paste karo |
| `robots.txt` | Google ko batata hai ki kya crawl kare | Site ka root folder |
| `sitemap.xml` | Site ke saare pages ki list | Root folder |
| `llms.txt` | AI search engines (ChatGPT, Perplexity) ke liye site ka summary | Root folder |
| `omegle-alternative.html` | Landing page: "omegle alternative india" keyword | Root folder |
| `chat-with-strangers-india.html`, `anonymous-chat-no-login.html`, `talk-to-strangers-when-bored.html` | Long-tail keyword landing pages | Root folder |
| `faq.html` | FAQ page, Google FAQ schema ke saath | Root folder |
| `blog/` | Blog home + 2 articles | Root folder mein `blog/` naam se |

Ye pages Step 1 ki `legal.css` aur `safety.js` use karte hain, isliye un dono ka bhi root folder mein hona zaroori hai.
Next.js ya React mein saari files `public/` folder mein jayengi.

## ⚠️ Upload se pehle check karo

- Pages maan kar chalte hain ki site **free** hai, **signup nahi** chahiye. Agar koi baat aapki site pe sach nahi hai, to bata do, main text badal dunga. Google ko galat jaankari dena ranking ke liye nuksaan karta hai.
- Video chat ka zikr maine jaan-boojh kar nahi kiya, kyunki pata nahi aapki site pe hai ya nahi. Hai to bata do, "random video chat" keyword ke liye alag page bana dunga.
- `og-image.png` banao (1200×630, logo aur "Talk to Strangers" text) aur root folder mein daalo. Isse WhatsApp pe link share karne pe photo dikhegi.
- Agar site pe chat ka URL `/chat?` ya `/room/` se alag hai, to `robots.txt` theek kar dena.

## Google Search Console setup (sabse zaroori, free hai)

1. https://search.google.com/search-console kholo aur `strangertalk.in@gmail.com` se login karo.
2. **Add property → URL prefix** chuno aur `https://strangertalk.in/` daalo.
3. **HTML tag** wala option chuno. Wahan jo `<meta name="google-site-verification" ...>` line mile, use `head-tags.html` wali commented line ki jagah daal do.
4. Site update karke **Verify** dabao.
5. Left menu mein **Sitemaps** mein jaao, `sitemap.xml` likho aur Submit karo.
6. **URL Inspection** mein har naye page ka URL daalo aur **Request indexing** dabao.

Isi tarah **Bing Webmaster Tools** (https://www.bing.com/webmasters) bhi setup karo. Wahan Search Console se import ka option hai, aur ChatGPT search Bing ka data use karta hai.

## Target keywords

| Keyword | Page |
|---|---|
| chat with strangers online free, chat with strangers no login | Homepage |
| chat with strangers india, talk to strangers india | `chat-with-strangers-india.html` |
| anonymous chat no login, chat with strangers without registration | `anonymous-chat-no-login.html` |
| talk to strangers when bored, someone to talk to online free | `talk-to-strangers-when-bored.html` |
| omegle alternative, omegle alternative india, sites like omegle | `omegle-alternative.html` |
| is stranger chat safe, how to report on chat site | `faq.html`, `safety-tips.html` |
| why did omegle shut down | `blog/omegle-shut-down-what-now.html` |
| make friends online india | `blog/make-friends-online-safely.html` |

## Aage kya karna hai (har hafte)

- [ ] Har hafte 1 naya blog post (topic ideas: "Best time to find people online", "Chat etiquette", "How to spot fake profiles")
- [ ] Instagram Reels / YouTube Shorts mein site ka link
- [ ] Reddit, Quora pe "omegle alternative" waale sawaalon ka jawab dena (spam mat karna, kaam ka jawab do)
- [ ] Search Console mein dekhna ki kaunse keywords se log aa rahe hain
- [ ] PageSpeed check: https://pagespeed.web.dev/ (green score ka target rakho)

Ye "har hafte" wala kaam baad mein **SEO Agent** apne aap karega (Step 3).
