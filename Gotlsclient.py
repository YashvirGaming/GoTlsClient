from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import os, asyncio
from urllib.parse import quote, urljoin
from collections import OrderedDict
import tls_client   # pip install tls-client
import uvicorn

app = FastAPI()

def format_proxy(raw_proxy: str):
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

    if not kc_url:
        return JSONResponse(status_code=400, content={"error": "Missing x-kc-url header"})

    # Handle relative paths
    if kc_url.startswith("/"):
        host = headers.get("host")
        scheme = "https" if kc_protocol == "2" else "http"
        kc_url = urljoin(f"{scheme}://{host}", kc_url)

    # Optional delay
    kc_delay = headers.get("x-kc-delay")
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
            if key.strip() in forward_headers_dict:
                ordered[key.strip()] = forward_headers_dict[key.strip()]
        for k, v in forward_headers_dict.items():
            if k not in ordered:
                ordered[k] = v
        forward_headers = ordered
    else:
        forward_headers = forward_headers_dict

    # Proxy handling
    proxy_url = format_proxy(kc_proxy) if kc_proxy else None

    try:
        session = tls_client.Session(
            client_identifier=kc_fingerprint,   # e.g. "chrome_120", "safari_17"
            random_tls_extension_order=True
        )

        method = request.method.upper()
        if method == "POST":
            resp = session.post(kc_url, headers=forward_headers, data=body, proxy=proxy_url, timeout_seconds=30)
        elif method == "GET":
            resp = session.get(kc_url, headers=forward_headers, proxy=proxy_url, timeout_seconds=30)
        elif method == "PUT":
            resp = session.put(kc_url, headers=forward_headers, data=body, proxy=proxy_url, timeout_seconds=30)
        elif method == "DELETE":
            resp = session.delete(kc_url, headers=forward_headers, data=body, proxy=proxy_url, timeout_seconds=30)
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
    port = int(input("Enter port (Default 9000): ") or 9000)
    print(f"Starting TLS proxy with global fingerprinting on http://localhost:{port}")
    uvicorn.run("Gotlsclient:app", host="0.0.0.0", port=port, reload=False)
