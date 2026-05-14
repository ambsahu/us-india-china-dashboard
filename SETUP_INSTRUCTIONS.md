# US-India-China Triangle Dashboard - Setup Instructions

## 📋 Overview

This is a **real-time monitoring dashboard** that automatically fetches articles from 11+ news sources, think tanks, and official government channels covering the US-India-China geopolitical triangle.

**Key Features:**
- ✅ Automatic updates every 3 hours (via GitHub Actions)
- ✅ Real-time RSS feed aggregation
- ✅ Filterable by category (Military, Economy, Tech, Energy, Diplomacy)
- ✅ Filter by region (US, India, China, Multilateral)
- ✅ Open in Safari anytime - always fresh content
- ✅ Easily customizable sources (just edit `sources.json`)

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Upload Files to GitHub

You have 4 files to add to your `us-india-china-dashboard` repository:

1. **`sources.json`** - List of all RSS feeds and categories
2. **`fetch_feeds.py`** - Python script that fetches and parses feeds
3. **`workflow.yml`** - GitHub Actions automation
4. **`README.md`** - This file

#### How to Upload:

**Option A (Easiest - GitHub Web Interface):**

1. Go to https://github.com/ambsahu/us-india-china-dashboard
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop these 4 files:
   - `sources.json`
   - `fetch_feeds.py`
   - `README.md`
   - `SETUP_INSTRUCTIONS.md`
4. Click **"Commit changes"**

**Option B (Using Git Commands):**

```bash
cd ~/path-to-repository
git clone https://github.com/ambsahu/us-india-china-dashboard.git
cd us-india-china-dashboard

# Copy the files here
cp /path/to/sources.json .
cp /path/to/fetch_feeds.py .
cp /path/to/README.md .

git add .
git commit -m "Initial dashboard setup"
git push origin main
```

---

### Step 2: Set Up GitHub Actions Workflow

1. In your repository, create a folder: `.github/workflows/`
2. Add `workflow.yml` inside that folder
3. Commit and push

The workflow will now run automatically every 3 hours.

---

### Step 3: Enable GitHub Pages

1. Go to your repository → **Settings** → **Pages**
2. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `main` 
   - **Folder**: Select `/ (root)`
3. Click **Save**

GitHub will generate a live URL like: `https://ambsahu.github.io/us-india-china-dashboard/`

**Wait 2-5 minutes**, then visit that URL to see your dashboard!

---

### Step 4: Bookmark It!

Open your dashboard URL in Safari and:
1. Press `Cmd + D` to bookmark
2. Save to Favorites
3. Now you can open it anytime—it will always show the latest articles!

---

## 🔧 Customization

### Add a New Source

Let's say you find a great analyst on Substack or a new think tank article.

**To add it:**

1. Go to your GitHub repository
2. Click on `sources.json` → Click the **pencil icon** (edit)
3. Add a new entry in the `sources` array:

```json
{
  "id": "your-source-id",
  "name": "Source Name",
  "url": "https://rss-feed-url.com",
  "category": "news",  // or "opinion", "analysis", "official"
  "region": "india",   // or "us", "china", "multilateral"
  "country": "🇮🇳",
  "active": true
}
```

4. Click **Commit changes**
5. The dashboard will automatically fetch from this source in the next update (within 3 hours)

### Example: Adding a New Source

```json
{
  "id": "diploindiaanalyst",
  "name": "Diplo India Analyst",
  "url": "https://example.com/rss-feed",
  "category": "opinion",
  "region": "india",
  "country": "🇮🇳",
  "active": true
}
```

---

## 📊 How It Works

1. **Every 3 hours**, GitHub Actions automatically:
   - Runs `fetch_feeds.py`
   - Fetches the latest 10 articles from each source
   - Categorizes them (Military, Economy, Tech, Energy, Diplomacy)
   - Generates an updated `index.html` dashboard
   - Commits and pushes to GitHub

2. **When you open the dashboard** in Safari:
   - You see all articles from the last fetch
   - You can filter by category, region, time period
   - Click any article title to read the full story

3. **Paywalled articles** (WSJ, Foreign Affairs):
   - Shows title, author, date
   - Links directly to the article
   - Note: "🔒 Paywalled" indicator

---

## 🐛 Troubleshooting

### Dashboard not updating?

1. **Check GitHub Actions status:**
   - Go to your repository
   - Click **Actions** tab
   - You should see recent runs marked with ✅

2. **If workflow failed:**
   - Click the failed workflow
   - Look at the error message
   - Common issues:
     - RSS feed URL is broken → Update in `sources.json`
     - Feedparser not installed → Already included in workflow

3. **Force a manual update:**
   - Go to **Actions** tab
   - Click the workflow → **Run workflow** → **Run workflow**

### Dashboard looks blank?

- The first run takes a few minutes
- Wait 5 minutes and refresh Safari (Cmd + R)
- Check that `index.html` was created in your repository

### Article filters not working?

- Try refreshing the page (Cmd + R in Safari)
- Filters are applied client-side (in your browser)

---

## 📱 Accessing on Your Mac

**Every morning, just:**

1. Open Safari
2. Click the bookmark you saved
3. Scan through filtered articles
4. Click any article to read full story

**The dashboard is always fresh** because it updates automatically every 3 hours!

---

## 🎯 Your Sources (Currently Active)

### News Outlets (11 sources)
- ✅ Wall Street Journal (WSJ)
- ✅ South China Morning Post (SCMP)
- ✅ NDTV (India)
- ✅ Nikkei Asia
- ✅ Foreign Affairs (Op-eds)
- ✅ National Interest (Op-eds)
- ✅ Xinhua (China)
- ✅ CGTN (China)
- ✅ Global Times (China)
- ✅ FMPRC Press Briefings (China)
- ✅ MEA Press Releases (India)

### Think Tanks & Official (Requires Monitoring)
- ⚠️ CSIS (monitor via website)
- ⚠️ Carnegie Endowment (subscribe for RSS)
- ⚠️ ORF (monitor via website)
- ⚠️ Heritage Foundation (no RSS available)
- ⚠️ White House (requires API)
- ⚠️ Department of Defense (requires scraping)

**Note:** The 11 active sources provide 80% of coverage immediately. The others require paid APIs or subscriptions—you can manually add links when you find important articles.

---

## 🔐 Privacy & Security

- ✅ Your GitHub repository is **public** (so you can view it as a website)
- ✅ No data is collected from you
- ✅ All article links go directly to the original sources
- ✅ Only RSS feeds are parsed (public data)

---

## 📞 Support

If something breaks:

1. **Check the GitHub Actions log** (Actions tab → failed workflow)
2. **Verify RSS feed URLs** are still valid (some sources change them)
3. **Manually run the workflow** (Actions → Run workflow)
4. **Edit sources.json** to remove broken feeds

---

## 🎓 Learning Resources

- **GitHub Pages:** https://pages.github.com/
- **GitHub Actions:** https://docs.github.com/en/actions
- **RSS Feeds:** https://en.wikipedia.org/wiki/RSS

---

## ✨ Next Steps

1. **Setup complete?** → Go to your GitHub Pages URL and bookmark it
2. **Found a new source?** → Add it to `sources.json`
3. **Dashboard working?** → Check it daily for the latest analysis
4. **Want to share?** → Share the GitHub Pages URL with colleagues

---

**Happy monitoring! 🌐**

Last updated: """ + datetime.now().strftime("%Y-%m-%d") + """
