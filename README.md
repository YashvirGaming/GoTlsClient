<h1 align="center">🚀 Gotlsapi-windows</h1>

<p align="center">
  <b>EXE-based Reverse Proxy with TLS Fingerprinting</b><br>
  Built with FastAPI + TLS-Client + Uvicorn
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge">
  <img src="https://img.shields.io/badge/FastAPI-115.0-brightgreen.svg?style=for-the-badge">
  <img src="https://img.shields.io/badge/TLS--Client-1.0.1-orange.svg?style=for-the-badge">
  <img src="https://img.shields.io/badge/Uvicorn-0.30.6-purple.svg?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg?style=for-the-badge">
</p>

<hr>

<p>
  Gotlsapi is a powerful standalone <b>EXE-based reverse proxy</b> built with FastAPI + TLS-Client. 
  It allows you to forward HTTP requests with custom headers, proxy rotation, enforced header order, 
  optional protocol switching (HTTP/2), and <b>browser-like TLS fingerprinting</b>. 
  Designed especially for scenarios like <b>API tunneling, automated checkers, or bypass flows</b>, 
  it works without installing Python or any dependencies.
</p>

<blockquote>
  🟢 Works out of the box — just run the EXE, and you're good to go.
</blockquote>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li>✅ Supports <code>GET</code>, <code>POST</code>, <code>PUT</code>, <code>DELETE</code>, <code>PATCH</code>, and more</li>
  <li>🔀 Proxy injection with <code>ip:port:user:pass</code> auto-format</li>
  <li>🔒 HTTP/2 protocol switch via <code>x-kc-protocol</code> header</li>
  <li>🧠 Header order enforcement for bot protection bypassing</li>
  <li>⏱️ Delay support via <code>x-kc-delay</code></li>
  <li>🎭 TLS Fingerprint emulation via <code>x-kc-fingerprint</code> (Chrome, Safari, Firefox, etc.)</li>
  <li>🎨 Colorized request logging with response codes</li>
  <li>📦 No dependencies needed — just run the EXE!</li>
</ul>

<hr>

<h2>🖥️ How to Use</h2>
<ol>
  <li>
    <b>Download</b> the EXE from the 
    <a href="https://github.com/YashvirGaming/GoTlsClient/releases/tag/v1.0">Releases</a> section.<br>
    <img src="https://github.com/user-attachments/assets/44fef1eb-00b6-4515-8e6e-274962eb936a" alt="screenshot">
  </li>
  <li><b>Run</b> the program:
    <pre><code>Gotlsapi.exe</code></pre>
  </li>
  <li><b>Select port</b> (Default: <code>9000</code>).</li>
  <li>Send your request through the proxy:
    <pre><code>POST http://localhost:9000/</code></pre>
  </li>
</ol>

<hr>

<h2>🔧 Supported Headers</h2>
<table>
  <thead>
    <tr>
      <th>Header</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>x-kc-url</code></td>
      <td>Target URL to forward the request to (can be full or relative)</td>
    </tr>
    <tr>
      <td><code>x-kc-proxy</code></td>
      <td>Proxy in format <code>ip:port:user:pass</code> or full URL</td>
    </tr>
    <tr>
      <td><code>x-kc-protocol</code></td>
      <td><code>2</code> for HTTPS (HTTP/2), otherwise uses HTTP</td>
    </tr>
    <tr>
      <td><code>x-kc-headerorder</code></td>
      <td>Force header order (comma-separated)</td>
    </tr>
    <tr>
      <td><code>x-kc-delay</code></td>
      <td>Add delay (in ms) before forwarding request</td>
    </tr>
    <tr>
      <td><code>x-kc-fingerprint</code></td>
      <td>Choose TLS fingerprint (e.g. <code>chrome_120</code>, <code>safari_17</code>)</td>
    </tr>
  </tbody>
</table>

<p><i>All non-<code>x-kc-</code> headers will be forwarded as-is to the target.</i></p>

<hr>

<h2>📁 Example Usage (Python)</h2>
<pre><code class="language-python">import requests

headers = {
    "x-kc-url": "https://web.prod.cloud.netflix.com/graphql",
    "x-kc-proxy": "Http:&lt;Proxy&gt;",
    "x-kc-protocol": "2",
    "x-kc-headerorder": "User-Agent,Accept,Content-Type",
    "x-kc-fingerprint": "chrome_120",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "application/json",
}

r = requests.post("http://localhost:9000/", headers=headers, data='{}')
print(r.text)
</code></pre>

<hr>

<h2>🛠️ Setup Instructions</h2>
<pre><code class="language-bash"># 1. Clone the repo
$ git clone https://github.com/YashvirGaming/GoTlsClient.git

# 2. Install dependencies
$ pip install -r requirements.txt

# 3. Run locally (for development)
$ python Gotlsclient.py

# 4. Or compile with Nuitka
</code></pre>

<hr>

<h2>📦 Build Info</h2>
<ul>
  <li><img src="https://img.shields.io/badge/python-3.10%2B-blue"> Written in: Python 3.10+</li>
  <li>Compiled with: <b>Nuitka</b></li>
  <li>Frameworks: <code>FastAPI</code>, <code>tls-client</code>, <code>uvicorn</code>, <code>colorama</code></li>
</ul>

<hr>

<h2>📸 Screenshots</h2>

<p>✅ Working login capture:</p>
<img src="https://github.com/user-attachments/assets/840128f0-0bd6-4be5-a1c9-3e636a095608" alt="Login success">

<p>🔄 Reverse Proxy Flow:</p>
<img src="https://github.com/user-attachments/assets/4218e7cf-01e7-4552-9664-133dc62ed636" alt="Proxy Flow">

<hr>

<h2>🎨 Colorized Logs Example</h2>
<pre><code>[TLS Proxy] GET https://www.google.com → 200 (123.4 ms)
[TLS Proxy] POST https://api.example.com/login → 401 (78.9 ms)
[TLS Proxy] GET https://redirect.test → 302 (45.1 ms)
[TLS Proxy] POST https://api.example.com/data → 500 (212.7 ms)
</code></pre>
<p>
  ✅ <span style="color:green;">200 (Green)</span> &nbsp;&nbsp;
  🔄 <span style="color:cyan;">300 (Cyan)</span> &nbsp;&nbsp;
  ⚠️ <span style="color:gold;">400 (Yellow)</span> &nbsp;&nbsp;
  ❌ <span style="color:red;">500 (Red)</span>
</p>

<hr>

<h2>📜 License</h2>
<p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>

<hr>

<h2>🤝 Credits</h2>
<p align="center">
  <b>Built with ❤️ by <a href="https://github.com/YashvirGaming">@YashvirGaming</a></b><br>
  <a href="https://t.me/therealyashvirgaming">Telegram: @therealyashvirgaming</a><br><br>
  <img src="https://img.shields.io/github/stars/YashvirGaming/GoTlsClient?style=social"> 
  <img src="https://img.shields.io/twitter/follow/yashvir__gaming?style=social">
</p>
<p align="center">Thanks to all testers and contributors for feedback!</p>
