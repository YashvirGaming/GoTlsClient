from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx
import os
import uvicorn
from typing import Optional
import asyncio
from urllib.parse import quote, urljoin, urlparse
from collections import OrderedDict

app = FastAPI()

def format_proxy(raw_proxy: str) -> Optional[str]:
    # Remove protocol temporarily
    raw = raw_proxy.replace("http://", "").replace("https://", "")

    parts = raw.split(":")
    if len(parts) == 4:
        ip, port, user, pwd = parts
        user_enc = quote(user)
        pwd_enc = quote(pwd)
        return f"http://{user_enc}:{pwd_enc}@{ip}:{port}"

    # Already formatted?
    if "@" in raw_proxy:
        return raw_proxy

    return None

@app.api_route("/", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
async def reverse_proxy(request: Request):
    headers = request.headers

    kc_url = headers.get("x-kc-url")
    kc_proxy = headers.get("x-kc-proxy")
    kc_protocol = headers.get("x-kc-protocol")
    kc_headerorder = headers.get("x-kc-headerorder")

    if not kc_url:
        return JSONResponse(status_code=400, content={"error": "Missing x-kc-url header"})

    # Auto-convert relative URL to full URL using the Host header
    if kc_url.startswith("/"):
        host = headers.get("host")
        scheme = "https" if kc_protocol == "2" else "http"
        kc_url = urljoin(f"{scheme}://{host}", kc_url)

    kc_delay = headers.get("x-kc-delay")
    if kc_delay and kc_delay.isdigit():
        await asyncio.sleep(int(kc_delay) / 1000)

    body = await request.body()

    # Step 1: Collect headers that should be forwarded
    forward_headers_dict = {
        key: value for key, value in headers.items()
        if not key.lower().startswith("x-kc-") and key.lower() != "host"
    }

    # Step 2: Enforce header order if provided
    if kc_headerorder:
        ordered_headers = OrderedDict()
        for key in kc_headerorder.split(","):
            key = key.strip()
            if key in forward_headers_dict:
                ordered_headers[key] = forward_headers_dict[key]
        for key, value in forward_headers_dict.items():
            if key not in ordered_headers:
                ordered_headers[key] = value
        forward_headers = ordered_headers
    else:
        forward_headers = forward_headers_dict

    # Step 3: Format proxy
    transport = None
    if kc_proxy:
        formatted = format_proxy(kc_proxy)
        if not formatted:
            return JSONResponse(status_code=400, content={"error": "Invalid proxy format"})

        transport = httpx.AsyncHTTPTransport(proxy=formatted)

    # Step 4: Make the request
    try:
        method = request.method.upper()

        async with httpx.AsyncClient(transport=transport, verify=False, timeout=30.0) as client:
            if method == "POST":
                resp = await client.post(kc_url, content=body, headers=forward_headers)
            elif method == "GET":
                resp = await client.get(kc_url, headers=forward_headers)
            elif method == "PUT":
                resp = await client.put(kc_url, content=body, headers=forward_headers)
            elif method == "DELETE":
                resp = await client.delete(kc_url, content=body, headers=forward_headers)
            else:
                return JSONResponse(status_code=405, content={"error": f"Unsupported method: {method}"})

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers={k: v for k, v in resp.headers.items()
                     if k.lower() not in ["content-encoding", "transfer-encoding", "content-length"]},
        )

    except Exception as e:
        return JSONResponse(status_code=502, content={"error": str(e)})

if __name__ == "__main__":
    port = int(input("Enter port (Default 9000): ") or 9000)
    print(f"Starting proxy on http://localhost:{port}")
    uvicorn.run("Gotlsclient:app", host="0.0.0.0", port=port, reload=False)
