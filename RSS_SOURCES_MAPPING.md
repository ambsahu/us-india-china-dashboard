# US-India-China Triangle Dashboard - RSS Sources Mapping

## ✅ SOURCES WITH ACTIVE RSS FEEDS (Ready to Use)

### News Outlets
| Source | RSS Feed URL | Category | Notes |
|--------|-------------|----------|-------|
| **WSJ** | `https://feeds.content.dowjones.io/public/rss/RSSUSnews` | News | US News feed; India/China coverage via paywalls |
| **SCMP** | `https://www.scmp.com/rss` | News | China perspective; multiple category feeds |
| **NDTV** | `https://feeds.feedburner.com/ndtvnews-top-stories` | News | India news; top stories |
| **Nikkei Asia** | `https://asia.nikkei.com/rss/feed/nar` | News | Regional Asia perspective |

### Opinion & Analysis
| Source | RSS Feed URL | Category | Notes |
|--------|-------------|----------|-------|
| **Foreign Affairs** | `https://www.foreignaffairs.com/rss.xml` | Opinion | Op-eds & analysis on global affairs |
| **National Interest** | `https://nationalinterest.org/feed` | Opinion | Defense & foreign policy focus |

### Think Tanks
| Source | RSS Feed URL | Category | Notes |
|--------|-------------|----------|-------|
| **CSIS** | Google News search RSS (via Feeder) | Analysis | Center for Strategic Studies; requires monitoring |
| **Carnegie** | Via subscription (see website) | Analysis | carnegieendowment.org/subscribe |
| **ORF** | No official RSS | Analysis | Monitor via X (@orfonline) or direct website |

### Chinese State Media
| Source | RSS Feed URL | Category | Notes |
|--------|-------------|----------|-------|
| **Xinhua** | `http://www.xinhuanet.com/english/rss/index.htm` | State Media | Official news agency; English feed |
| **CGTN** | `https://www.cgtn.com/subscribe/rss.html` | State Media | China Global Television; breaking news |
| **Global Times** | `https://www.globaltimes.cn/rss/` | State Media | Opinion-focused state media |

### Official Government Statements
| Source | RSS Feed URL | Category | Notes |
|--------|-------------|----------|-------|
| **MEA (India)** | `https://www.mea.gov.in/` (check for RSS) | Official | Ministry of External Affairs; may require web scraping |
| **White House** | Via whitehouse.gov/news | Official | Requires API or scraping |
| **FMPRC (China)** | `https://www.fmprc.gov.cn/eng/xw/` | Official | Foreign Ministry; daily briefings available |
| **DoD (US)** | `https://www.defense.gov/News/Releases` | Official | Department of Defense press releases |

---

## ⚠️ SOURCES REQUIRING WEB SCRAPING (Harder - Need Automation)

| Source | Method | Category | Notes |
|--------|--------|----------|-------|
| **Heritage Foundation** | Web scraping | Analysis | No official RSS; publications on heritage.org |
| **CICIR** | Web scraping | Analysis | Chinese think tank; cicir.ac.cn (limited English) |
| **MEA Press Releases** | Web scraping | Official | mea.gov.in/press-releases.htm |
| **State Department** | API/Scraping | Official | Limited direct RSS for press briefings |

---

## 📊 SUMMARY FOR DASHBOARD SETUP

**Total Sources: 15+**
- ✅ **With Active RSS Feeds: 11** (can auto-fetch immediately)
- ⚠️ **Requiring Web Scraping: 4** (need more complex setup)

**Recommended Phase 1 (Launch):**
All 11 RSS-enabled sources (gets you 80% of coverage immediately)

**Phase 2 (Enhancement):**
Add web scraping for paywalled/official sources (Heritage, CICIR, MEA press releases)

**Update Frequency:**
- GitHub Actions will fetch RSS feeds every **2-4 hours** (free tier)
- You can trigger manual refresh anytime

---

## 🔧 NEXT STEPS

1. Create GitHub account (free)
2. Set up GitHub Actions workflow to:
   - Fetch all 11 RSS feeds every 3 hours
   - Parse & categorize articles
   - Generate HTML dashboard with live data
3. Host dashboard on GitHub Pages (free)
4. You can add/remove sources by editing `sources.json`

**Estimated Setup Time: 30-45 minutes**

