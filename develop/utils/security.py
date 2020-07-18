def add_same_site(response):
    for idx, header in enumerate(response.raw_headers):
        if header[0].decode("utf-8") == "set-cookie":
            cookie = header[1].decode("utf-8")
            if "SameSite=None" not in cookie:
                cookie = cookie + "; SameSite=None"
                response.raw_headers[idx] = (header[0], cookie.encode())
    return response
