<h1 align="center">
  MS Crawler & Scraper
</h1>

Crawler and Scraper used to get data to populate a MongoDB that serves a backend and frontend **[here](https://ms-db.up.railway.app/)**.
<br>
More about it can be found **[here](https://github.com/RodrigoFreitas-L/ms_database)**.

<br>

<h1 align="center">
  Setup
</h1>

Get to the cloned directory:
<pre><code>cd ms_crawler_scraper</code></pre>

Create your virtual environment and access it:
<pre><code>python3 -m venv .venv && source .venv/bin/activate</code></pre>

Install all dependencies:
<pre><code>python3 -m pip install -r requirements.txt</code></pre>

Run it and wait until its done (since the list of monsters is long, it can take 2 to 3 hours to finish):
<pre><code>python3 scrapper.py</code></pre>
