#!/usr/bin/env python3
"""
US-India-China Triangle Dashboard - RSS Feed Fetcher
Fetches and aggregates articles from multiple RSS feeds
Updates HTML dashboard with real-time content
"""

import feedparser
import json
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import re

def load_sources():
    """Load RSS sources from sources.json"""
    with open('sources.json', 'r') as f:
        return json.load(f)

def categorize_article(title, description, source):
    """Categorize article based on keywords"""
    sources_config = load_sources()
    categories = {cat['id']: cat['keywords'] for cat in sources_config['categories']}

    text = f"{title} {description}".lower()

    for cat_id, keywords in categories.items():
        if any(keyword.lower() in text for keyword in keywords):
            return cat_id

    return "diplomacy"  # default category

def get_region_from_source(source_id):
    """Get region from source configuration"""
    sources_config = load_sources()
    for source in sources_config['sources']:
        if source['id'] == source_id:
            return source.get('region', 'multilateral')
    return 'multilateral'

def fetch_rss_feeds():
    """Fetch and parse all RSS feeds"""
    sources_config = load_sources()
    articles = []

    for source in sources_config['sources']:
        if not source.get('active', False):
            continue

        # Skip sources that require web scraping for now
        if source.get('note') and 'scraping' in source['note']:
            continue

        try:
            feed = feedparser.parse(source['url'])

            for entry in feed.entries[:10]:  # Get last 10 articles per source
                try:
                    title = entry.get('title', 'No title')
                    link = entry.get('link', '#')
                    published = entry.get('published', '')
                    description = entry.get('summary', '')
                    author = entry.get('author', source['name'])

                    # Parse published date
                    try:
                        pub_date = datetime(*feedparser._parse_date(published)[:6])
                    except:
                        pub_date = datetime.now()

                    article = {
                        'id': hashlib.md5(f"{title}{link}".encode()).hexdigest()[:8],
                        'title': title,
                        'author': author,
                        'source': source['id'],
                        'source_name': source['name'],
                        'country': source.get('country', ''),
                        'link': link,
                        'published': pub_date.isoformat(),
                        'description': description[:200],
                        'category': categorize_article(title, description, source['id']),
                        'region': source.get('region', 'multilateral'),
                        'paywalled': 'paywall' in description.lower() or 'subscribe' in description.lower()
                    }

                    articles.append(article)
                except Exception as e:
                    print(f"Error processing entry from {source['name']}: {e}")
                    continue

        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")
            continue

    # Sort by published date (newest first)
    articles.sort(key=lambda x: x['published'], reverse=True)
    return articles

def generate_html_dashboard(articles):
    """Generate HTML dashboard with articles"""

    sources_config = load_sources()
    categories = {cat['id']: cat for cat in sources_config['categories']}

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>US-India-China Triangle Dashboard</title>
    <style>
        :root {
            --primary: #1e40af;
            --secondary: #059669;
            --accent: #dc2626;
            --neutral: #6b7280;
            --light-bg: #f3f4f6;
            --border: #e5e7eb;
            color-scheme: light;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%);
            color: #1f2937;
            line-height: 1.6;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            background: linear-gradient(135deg, var(--primary) 0%, #0f3460 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        header p {
            font-size: 1.1em;
            opacity: 0.95;
        }

        .controls {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
        }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
        }

        .filter-group label {
            font-weight: 600;
            margin-bottom: 8px;
            color: #374151;
            font-size: 0.95em;
        }

        .filter-group select {
            padding: 10px;
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 0.95em;
            background: white;
            cursor: pointer;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95em;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background: #1e40af;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
        }

        .status {
            font-size: 0.85em;
            color: var(--neutral);
            margin-top: 10px;
        }

        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: var(--primary);
        }

        .stat-label {
            color: var(--neutral);
            font-size: 0.9em;
            margin-top: 5px;
        }

        .articles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .article-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }

        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        .article-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            flex-grow: 1;
        }

        .article-source {
            display: inline-block;
            background: var(--light-bg);
            color: var(--primary);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .article-title {
            font-size: 1.1em;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 8px;
            line-height: 1.4;
        }

        .article-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
            color: var(--neutral);
            margin-top: 12px;
            flex-wrap: wrap;
            gap: 8px;
        }

        .article-category {
            display: inline-block;
            background: var(--light-bg);
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
            color: var(--primary);
        }

        .article-footer {
            padding: 15px 20px;
            background: var(--light-bg);
            border-top: 1px solid var(--border);
        }

        .article-link {
            display: inline-block;
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9em;
        }

        .article-link:hover {
            text-decoration: underline;
        }

        .paywalled {
            opacity: 0.7;
        }

        .paywalled::after {
            content: " 🔒";
        }

        .no-data {
            text-align: center;
            padding: 40px 20px;
            color: var(--neutral);
            background: white;
            border-radius: 10px;
            border: 1px solid var(--border);
        }

        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: var(--neutral);
            font-size: 0.85em;
            border-top: 1px solid var(--border);
        }

        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8em;
            }

            .controls-grid {
                grid-template-columns: 1fr;
            }

            .articles-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌐 US-India-China Triangle Dashboard</h1>
            <p>Real-time monitoring of strategic developments across defense, economics, technology, and energy sectors</p>
        </header>

        <div class="controls">
            <div class="controls-grid">
                <div class="filter-group">
                    <label for="category-filter">Category</label>
                    <select id="category-filter">
                        <option value="">All Categories</option>
"""

    for cat_id, cat in categories.items():
        html += f'                        <option value="{cat_id}">{cat["icon"]} {cat["name"]}</option>\n'

    html += """                    </select>
                </div>

                <div class="filter-group">
                    <label for="region-filter">Region Focus</label>
                    <select id="region-filter">
                        <option value="">All Regions</option>
                        <option value="us">🇺🇸 US Perspective</option>
                        <option value="india">🇮🇳 India Perspective</option>
                        <option value="china">🇨🇳 China Perspective</option>
                        <option value="multilateral">🌍 Multilateral</option>
                    </select>
                </div>

                <div class="filter-group">
                    <label for="days-filter">Time Period</label>
                    <select id="days-filter">
                        <option value="1">Last 24 Hours</option>
                        <option value="7">Last 7 Days</option>
                        <option value="30">Last 30 Days</option>
                        <option value="">All Articles</option>
                    </select>
                </div>
            </div>

            <button class="btn-primary" onclick="applyFilters()">Apply Filters</button>

            <div class="status">
                <strong>Last Updated:</strong> <span id="last-update">""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + """</span>
                <br><strong>Total Articles:</strong> <span id="article-count">""" + str(len(articles)) + """</span>
            </div>
        </div>

        <div class="dashboard-stats">
            <div class="stat-card">
                <div class="stat-value">""" + str(len(articles)) + """</div>
                <div class="stat-label">Total Articles</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">""" + str(len(set(a['source'] for a in articles))) + """</div>
                <div class="stat-label">Active Sources</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">""" + str(len([a for a in articles if a['category'] == 'military'])) + """</div>
                <div class="stat-label">Military Coverage</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">""" + str(len([a for a in articles if a['category'] == 'economy'])) + """</div>
                <div class="stat-label">Economy Coverage</div>
            </div>
        </div>

        <div id="articles" class="articles-grid">
"""

    for article in articles:
        category_icon = categories.get(article['category'], {}).get('icon', '📰')
        paywalled_class = 'paywalled' if article.get('paywalled') else ''

        html += f"""            <div class="article-card {paywalled_class}">
                <div class="article-header">
                    <span class="article-source">{article['country']} {article['source_name']}</span>
                    <div class="article-title">{article['title']}</div>
                    <div class="article-meta">
                        <span class="article-category">{category_icon} {categories.get(article['category'], {}).get('name', 'General')}</span>
                        <span>{article['published'].split('T')[0]}</span>
                    </div>
                </div>
                <div class="article-footer">
                    <a href="{article['link']}" target="_blank" class="article-link">Read Full Article →</a>
                </div>
            </div>
"""

    html += """        </div>

        <footer>
            <p>🔄 Dashboard updates automatically every 3 hours</p>
            <p>Last built: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC") + """</p>
        </footer>
    </div>

    <script>
        const articles = """ + json.dumps(articles) + """;

        function applyFilters() {
            const category = document.getElementById('category-filter').value;
            const region = document.getElementById('region-filter').value;
            const days = parseInt(document.getElementById('days-filter').value) || null;

            const now = new Date();
            const filtered = articles.filter(article => {
                let match = true;

                if (category && article.category !== category) match = false;
                if (region && article.region !== region) match = false;
                if (days) {
                    const articleDate = new Date(article.published);
                    const cutoffDate = new Date(now - days * 24 * 60 * 60 * 1000);
                    if (articleDate < cutoffDate) match = false;
                }

                return match;
            });

            document.getElementById('article-count').textContent = filtered.length;
            renderArticles(filtered);
        }

        function renderArticles(articlesToRender) {
            const container = document.getElementById('articles');
            if (!articlesToRender.length) {
                container.innerHTML = '<div class="no-data">No articles matching current filters.</div>';
                return;
            }

            container.innerHTML = articlesToRender.map(article => `
                <div class="article-card">
                    <div class="article-header">
                        <span class="article-source">${article.country} ${article.source_name}</span>
                        <div class="article-title">${article.title}</div>
                        <div class="article-meta">
                            <span class="article-category">${article.category}</span>
                            <span>${article.published.split('T')[0]}</span>
                        </div>
                    </div>
                    <div class="article-footer">
                        <a href="${article.link}" target="_blank" class="article-link">Read Full Article →</a>
                    </div>
                </div>
            `).join('');
        }
    </script>
</body>
</html>
"""

    return html

def main():
    """Main execution"""
    print("Fetching RSS feeds...")
    articles = fetch_rss_feeds()
    print(f"Fetched {len(articles)} articles from {len(set(a['source'] for a in articles))} sources")

    print("Generating dashboard...")
    html = generate_html_dashboard(articles)

    with open('index.html', 'w') as f:
        f.write(html)

    print("Dashboard generated: index.html")

if __name__ == '__main__':
    main()
