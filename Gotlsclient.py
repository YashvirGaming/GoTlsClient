from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from collections import OrderedDict
from urllib.parse import quote, urljoin
import asyncio
import time

import tls_client   # pip install tls-client
import uvicorn

from colorama import init, Fore, Style
init(autoreset=True)

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    code = response.status_code
    if 200 <= code < 300:
        color = Fore.GREEN
    elif 300 <= code < 400:
        color = Fore.CYAN
    elif 400 <= code < 500:
        color = Fore.YELLOW
    else:
        color = Fore.RED

    print(
        f"{Fore.MAGENTA}[TLS Proxy]{Style.RESET_ALL} "
        f"{request.method} {request.url} "
        f"→ {color}{code}{Style.RESET_ALL} "
        f"({process_time:.1f} ms)"
    )
    return response


def format_proxy(raw_proxy: str):
    if not raw_proxy:
        return None
    raw = raw_proxy.replace("http://", "").replace("https://", "")
    parts = raw.split(":")
    if len(parts) == 4:
        ip, port, user, pwd = parts
        return f"http://{quote(user)}:{quote(pwd)}@{ip}:{port}"
    if "@" in raw_proxy:
        return raw_proxy
    return None


@app.api_route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def reverse_proxy(request: Request):
    headers = request.headers
    kc_url = headers.get("x-kc-url")
    kc_proxy = headers.get("x-kc-proxy")
    kc_protocol = headers.get("x-kc-protocol")
    kc_headerorder = headers.get("x-kc-headerorder")
    kc_fingerprint = headers.get("x-kc-fingerprint", "chrome_120")  # Default fingerprint
    kc_delay = headers.get("x-kc-delay")

    if not kc_url:
        return JSONResponse(status_code=400, content={"error": "Missing x-kc-url header"})

    # Handle relative paths
    if kc_url.startswith("/"):
        host = headers.get("host")
        scheme = "https" if kc_protocol == "2" else "http"
        kc_url = urljoin(f"{scheme}://{host}", kc_url)

    # Optional delay (ms)
    if kc_delay and kc_delay.isdigit():
        await asyncio.sleep(int(kc_delay) / 1000)

    body = await request.body()

    # Forward headers (remove control headers)
    forward_headers_dict = {
        k: v for k, v in headers.items()
        if not k.lower().startswith("x-kc-") and k.lower() != "host"
    }

    # Respect header order if provided
    if kc_headerorder:
        ordered = OrderedDict()
        for key in kc_headerorder.split(","):
            key = key.strip()
            if key in forward_headers_dict:
                ordered[key] = forward_headers_dict[key]
        for k, v in forward_headers_dict.items():
            if k not in ordered:
                ordered[k] = v
        forward_headers = ordered
    else:
        forward_headers = forward_headers_dict

    proxy_url = format_proxy(kc_proxy) if kc_proxy else None

    try:
        session = tls_client.Session(
            client_identifier=kc_fingerprint,
            random_tls_extension_order=True
        )

        method = request.method.upper()

        # run blocking tls_client calls in a thread to avoid blocking the event loop
        if method == "POST":
            def do_post():
                return session.post(kc_url, headers=forward_headers, data=body, proxy=proxy_url, timeout_seconds=30)
            resp = await asyncio.to_thread(do_post)

        elif method == "GET":
            def do_get():
                return session.get(kc_url, headers=forward_headers, proxy=proxy_url, timeout_seconds=30)
            resp = await asyncio.to_thread(do_get)

        elif method == "PUT":
            def do_put():
                return session.put(kc_url, headers=forward_headers, data=body, proxy=proxy_url, timeout_seconds=30)
            resp = await asyncio.to_thread(do_put)

        elif method == "DELETE":
            def do_delete():
                return session.delete(kc_url, headers=forward_headers, data=body, proxy=proxy_url, timeout_seconds=30)
            resp = await asyncio.to_thread(do_delete)

        else:
            return JSONResponse(status_code=405, content={"error": f"Unsupported method: {method}"})

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers={k: v for k, v in resp.headers.items()
                     if k.lower() not in ["content-encoding", "transfer-encoding", "content-length"]}
        )

    except Exception as e:
        return JSONResponse(status_code=502, content={"error": str(e)})


if __name__ == "__main__":
    subtitle = f"""
{Fore.CYAN}====================================================
   🚀 {Fore.GREEN}GoTLS Proxy {Fore.CYAN}• {Fore.MAGENTA}Made with ♥ by Yashvir Gaming
   {Fore.YELLOW}• Telegram: https://t.me/therealyashvirgaming
{Fore.CYAN}===================================================={Style.RESET_ALL}
"""
    print(subtitle)

    port = 9000
    print(f"{Fore.GREEN}Starting TLS proxy with global fingerprinting on {Fore.YELLOW}http://localhost:{port}{Style.RESET_ALL}")
    uvicorn.run("Gotlsclient:app", host="0.0.0.0", port=port, reload=False)
