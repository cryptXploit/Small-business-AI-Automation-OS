# ওনার ম্যানুয়াল ও সেটআপ গাইড (OWNER'S MANUAL & SETUP GUIDE)
**প্রজেক্ট:** The Small Business AI Automation Operating System (2026 Enterprise Edition)  
**লেখক ও স্বত্বাধিকারী:** ওমর সানি (OMAR SUNNY / Md Omar Sunny)  
**ফাইল লোকেশন:** `DIGITAL-PUBLISHING-STUDIO/15-DEPLOY-AND-FUNNEL-BRIDGE/`

---

## ১. প্রজেক্টের বাণিজ্যিক আর্কিটেকচার ও মূল পরিচিতি

প্রিয় ওমর সানি ভাই,  
আপনার ফ্ল্যাগশিপ প্রোডাক্ট **"The Small Business AI Automation Operating System"** এখন আন্তর্জাতিক মানের কমপ্লিট প্রোডাক্ট-লেড গ্রোথ (PLG) ফানেলে রূপান্তর করা হয়েছে। বিশ্বজুড়ে ট্রাফিক ড্রাইভ করার আগে এই গাইডটি আপনার ব্যক্তিগত এক্সিকিউশন চেকলিস্ট হিসেবে কাজ করবে।

---

## ২. গামরোড (GUMROAD) ও পেহিপ (PAYHIP) আপলোড চেকলিস্ট

আপনার প্রোডাক্টগুলো আপলোড করার জন্য তৈরি জিপ আর্কাইভগুলোর সঠিক লোকেশন নিচে দেওয়া হলো:

| প্যাকেজ টিয়ার | ফাইলের নাম ও লোকেশন | প্রস্তাবিত মূল্য | বিবরণ |
| :--- | :--- | :---: | :--- |
| **Tier 0 (Free Starter Kit)** | `09-EXPORTS/HYBRID-BUNDLE/Tier0-Free-5Day-Audit-Starter-Kit.zip` | **$0 (Pay What You Want)** | লিড ম্যাগনেট। এতে রয়েছে Ch 1 PDF, Ch 1 Workbook, 3-Tab Excel Sheet, Notion CSV, Blueprint #1 JSON, Web App, এবং Launchpad। |
| **Tier 1 (Book Only Pack)** | `09-EXPORTS/HYBRID-BUNDLE/Tier1-KDP-and-D2D-Retail-Book-Pack.zip` | **$9.99 / $19.99** | সম্পূর্ণ ১০ অধ্যায়ের বই (PDF ও EPUB)। |
| **Tier 2 (Workbook Edition)** | `09-EXPORTS/HYBRID-BUNDLE/Tier2-Interactive-Workbook-and-Atlas-Edition-29.zip` | **$29.00** | বই + ১০টি অ্যাকশন ওয়ার্কবুক + ৫০টি প্রম্পট আনলক কোড (`STUDIO-TIER2-2026`)। |
| **Tier 3 (Flagship Pro OS)** | `09-EXPORTS/HYBRID-BUNDLE/Tier3-Complete-SmallBiz-AI-Automation-OS-Flagship-59.zip` | **$59.00** | সম্পূর্ণ ইকোসিস্টেম: ৮-ট্যাব এক্সেল কমান্ড সেন্টার, ৫টি অটোমেশন ব্লুপ্রিন্ট, ১২টি ইমার্জেন্সি স্ক্রিপ্ট, লাইসেন্স কোড (`STUDIO-PRO-OS-2026`)। |
| **Tier 4 (Living Vault VIP)** | `09-EXPORTS/HYBRID-BUNDLE/Tier4-Living-Automation-Vault-Membership-Drop01.zip` | **$9/mo বা $49/yr** | রিকারিং মেম্বারশিপ ক্লাব। প্রতি মাসে নতুন অটোমেশন ড্রপ। |

### কভার ইমেজ লোকেশন:
- স্কয়ার থাম্বনেইল (৬০০×৬০০): `08-COVER-DESIGN/` ফোল্ডারে প্রতিটি টিয়ারের জন্য স্কয়ার কভার রয়েছে।
- ব্যানার কভার (১২৮০×৭২০): `08-COVER-DESIGN/gumroad-tier0-free-audit-cover.png` ইত্যাদি।

---

## ৩. ৩ মিনিটে ফ্রি ওয়েব অ্যাপ লাইভ হোস্টিং নির্দেশিকা (GITHUB PAGES / NETLIFY / VERCEL)

আপনার ক্লায়েন্ট বা ট্রাফিক যেন কোনো কিছু ডাউনলোড না করেই ব্রাউজারে লাইভ ওয়েব অ্যাপ টেস্ট করতে পারে, তার জন্য একটি রেডি ফোল্ডার তৈরি করা হয়েছে:
`15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/`

### অপশন ক: GitHub Pages (সবচেয়ে সহজ ও পার্মানেন্ট)
১. আপনার গিট রিপোজিটরিতে (`Small-business-AI-Automation-OS`) কোড পুশ করা রয়েছে।
২. GitHub রিপোজিটরি সেটিংসে যান: `Settings` > `Pages`।
৩. Build and deployment সোর্স হিসেবে `Deploy from a branch` সিলেক্ট করুন।
৪. ব্রাঞ্চ `master` বা `main` এবং ফোল্ডার `/15-WEB-DEPLOYMENT/dist` বা `/docs` সিলেক্ট করে সেভ করুন।
৫. আপনার লাইভ লিংক হবে:  
   `https://cryptxploit.github.io/Small-business-AI-Automation-OS/`

### অপশন খ: Netlify Drop (১ মিনিটে জিরো-কোড হোস্টিং)
১. [app.netlify.com/drop](https://app.netlify.com/drop) সাইটে যান (ফ্রি অ্যাকাউন্ট লগইন করুন)।
২. আপনার কম্পিউটারের `15-DEPLOY-AND-FUNNEL-BRIDGE/web-live-demo/` ফোল্ডারটি মাউস দিয়ে ড্র্যাগ করে নেটলিফাই ব্রাউজারে ড্রপ করুন।
৩. নেটলিফাই তাৎক্ষণিকভাবে একটি ফ্রি HTTPS লিংক দিয়ে দিবে (যেমন `smallbiz-os.netlify.app`)।

---

## ৪. ফানেল লিংক ইনজেকশন স্ক্রিপ্ট ব্যবহারের নিয়ম

যখনই আপনি গামরোড বা পেহিপে প্রোডাক্টগুলো পাবলিশ করবেন, তখন আপনার প্রোডাক্ট ইউআরএলগুলো সিস্টেমের সাথে সিঙ্ক করতে হবে:

১. `15-DEPLOY-AND-FUNNEL-BRIDGE/funnel-links-config.json` ফাইলটি ওপেন করুন।
২. সেখানে আপনার রিয়েল লিংকগুলো পেস্ট করুন:
```json
{
  "gumroad_tier0_free_url": "আপনার_টিয়ার০_ফ্রি_লিংক",
  "gumroad_tier2_workbook_url": "আপনার_টিয়ার২_লিংক",
  "gumroad_tier3_flagship_url": "আপনার_টিয়ার৩_লিংক",
  "gumroad_tier4_vip_url": "আপনার_টিয়ার৪_লিংক",
  "payhip_store_url": "আপনার_পেহিপ_লিংক",
  "live_web_app_demo_url": "আপনার_লাইভ_ওয়েব_অ্যাপ_লিংক"
}
```
৩. টার্মিনাল বা কমান্ড প্রম্পটে গিয়ে শুধু এই কমান্ডটি চালান:
```bash
python inject_funnel_links.py
```
৪. এটি স্বয়ংক্রিয়ভাবে সমস্ত মার্কেটিং পেইজ, ব্রাউজার লঞ্চপ্যাড, এবং ওয়েব অ্যাপে আপনার লিংক আপডেট করে দেবে এবং জিপ ফাইলগুলো রিবিল্ড করবে।

---

## ৫. প্যাসিভ অ্যাফিলিয়েট ইনকাম সেটআপ (FREE USERS TO CASH)

ফ্রি টিয়ার (Tier 0) ডাউনলোডকারী ইউজাররা যাতে আপনার জন্য প্যাসিভ রেভিনিউ তৈরি করে, সেজন্য নিচের সার্ভিসগুলোর অ্যাফিলিয়েট পার্টনার প্রোগ্রামে জয়েন করুন এবং আপনার ইউনিক লিংক ব্যবহার করুন:

১. **Make.com অ্যাফিলিয়েট লিংক:**
   - Free users যখন Blueprint #1 ইমপোর্ট করতে Make.com এ ফ্রি অ্যাকাউন্ট খুলবে, তখন আপনি প্রতি পেইড আপগ্রেডে লাইফটাইম ২০% কমিশন পাবেন।
   - সাইন আপ: [make.com/en/affiliates](https://www.make.com/en/affiliates)
২. **Notion অ্যাফিলিয়েট লিংক:**
   - Notion Starter CRM ব্যবহারের সময় ইউজাররা নশনে যোগ দিলে আপনি ৫০% রেভিনিউ শেয়ার পাবেন।
   - সাইন আপ: [notion.so/affiliates](https://www.notion.so/affiliates)
৩. **Payoneer / Wise অ্যাফিলিয়েট:**
   - আন্তর্জাতিক পেমেন্ট রিসিভ করার জন্য গামরোড থেকে বাংলাদেশে সরাসরি পেওনিয়ারের মাধ্যমে ফান্ড উইথড্র করতে পারবেন।

---

## ৬. সোশ্যাল মিডিয়া ট্রাফিক এক্সিকিউশন রুটিন (দৈনিক ৩০ মিনিট)

১. **সপ্তাহে ৩ দিন (সোম, বুধ, শুক্র):** `VIRAL-TRAFFIC-AND-FUNNEL-PLAYBOOK.md` থেকে রিলস স্ক্রিপ্ট অনুযায়ী মোবাইল স্ক্রিন রেকর্ড করে ইনস্টাগ্রাম রিলস, ফেসবুক রিলস এবং ইউটিউব শর্টসে পোস্ট করুন। ক্যাপশনে লিখুন: *"Comment 'OS' for the free diagnostic tool."*
২. **সপ্তাহে ২ দিন (মঙ্গল, বৃহস্পতি):** রেডিটের `r/smallbusiness` বা `r/entrepreneur` সাবরেডিটে পোস্ট ১ ও ২ ড্রপ করুন। সরাসরি লিংক দেবেন না; কমেন্টে কেউ আগ্রহ প্রকাশ করলে ইনবক্স বা কমেন্টে ফ্রি কিট লিংক শেয়ার করুন।
৩. **অটো-রেসপন্স:** যারা কমেন্ট করবে তাদেরকে সরাসরি গামরোডের Tier 0 Free Starter Kit লিংক দিন। বাকি কাজ গামরোডের ৩-ইমেইল অটোমেশন করবে!

---
**অভিনন্দন ওমর সানি ভাই! আপনার সম্পূর্ণ ডিজিটাল পাবলিশিং অ্যান্ড অটোমেশন ফানেল এখন লাইভ সেলসের জন্য ১০০% প্রস্তুত।**
