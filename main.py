import asyncio
import aiohttp

# =========================================================
# CONFIG
# =========================================================

URL = "https://api.narendramodi.in/mlapiv1"  # Updated endpoint
BOUNDARY = "Boundary+3EFF4B5BF5FFFFD3"

CONCURRENCY = 4
MAX_RETRIES = 3
TOTAL_REQUESTS = 500000000

stop_flag = False

# =========================================================
# HEADERS
# =========================================================

HEADERS = {
    "Host": "api.narendramodi.in",
    "Accept": "*/*",
    "Requestfrom": "ios",
    "Upload-Draft-Interop-Version": "6",
    "Upload-Complete": "?1",
    "Accept-Language": "en-IN;q=1, hi-IN;q=0.9, hi-Latn-IN;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Narendra Modi App/7.8 (iPhone; iOS 18.5; Scale/2.00)",
    "Connection": "keep-alive",
    # Updated Cookie from your dump
    "Cookie": "ADRUM_BT=R%3A0%7Cg%3Aca36fb37-397c-4cc1-a2d8-a0f0ba2568461308%7Cn%3Atmp_bjp_fb49d1de-d391-478a-ab5f-c84d7b25602e%7Ci%3A37735%7Cs%3Af%7Ce%3A82; NSC_10.10.24.75_443=ffffffff0902067c45525d5f4f58455e445a4a423660; _abck=E921128DDAE2823E0112175943B9E330~-1~YAAQOUw5F1DF3+uaAQAAyGm7Aw88nBvXf/7Mm9M4Sa7w+SWwuch4AizghjyXVocHwPhnZoraCBDi2up9XIBPeu3yZ1eqROIZgD3U29odo1IzG5TmiVvOMMa/zaQfGbjslAsp3Yp2mYERp1DJd6/ixYjJQW51wUHxCDhd1+TYe35py4SPhxdJfL7vf58gnFfamjz07ARsKEZuYaRq1ubMf/4ruAJ4n6sEVQGhOcoxIhjiF9jPHyHJSF4NLi2A7a5TjhyYPLIr/WZK2wK4AAK27rLw4guHNxPeA0a426FnaUisjHtjTUSHifEhK9mmMc7zT79pjNIh0TPWlio0rP6p93Ch1zgldfGVew511m2E9unMxrKFzLT9t+haBYxa/U5sVwEg3tV+iQZ5sRmaKzMjS1fbsLO+K69Q/4nuymxd09UWnJr/fKfgtPea26QVThKnItJHA3xGYop4QRlsohsIITG0Ooz8rCV5SS960p+jj7G69wGjD79Ua6Q5XDJ0I9TwKKMg8ECLqkIbt1ltHEA5hXNi08Mx3XowpYIcBpyfSuUOAUXMaLL3+edxsPQsD4Q+D7coz7Gzq8HtjXM/0TL6sjX/XMcpo83aZ69QMg==~-1~-1~1758627219~AASAAAAE%2f%2f%2f%2f%2f1cdoQen2s4n8ESYqKCGsKANI1Dj77dFVr9foXkF2r8DuQcI+Yl0Mo7y3PYUmDX7e2og4Yiv~-1; ak_bmsc=63EB145D658CCD2337BA15E4F8C6624C~000000000000000000000000000000~YAAQUozQF6I4DqOaAQAA6aWzAx7LpcA78X2l2B9ELoxSOS8gLNN8AhYac2IrBv9Ltf3ohDH2YdYbKaJz0Vvno6oHuwa0vfBZBMT3CqEVHoF5kHHVdvcw8llptEKMlWMQz7HHEjhdpdfbKvrW5Q1+sLSbnamvRBqzum3JnxZMDotwSPNU4SXTlZL/dvGwmeBolijnVQqH73bLgEWh2uJkGfN1hgtAv/Kn2ei04+slsr2TCmvOmPv882crr3D1m3j2O290V4xvx05Gsx+KMb2PzH9TGC1o890PDKTKnJlDE+/5SntMmtSU9swYt50Ip0wqANQvk4zcMgScHHqxMsqj1/jiV8ofn/uz66XvCZA1f+oVHyagRWHxS3dybz5DKpesTVd3dziy0Mzp2gBlvs1x4GJIeHWfa9LyKjeT4zvigV0=; bm_sz=7C8CE9EC9F630F3CA4CE3F77A2721E24~YAAQUozQF6M4DqOaAQAA6aWzAx72Gkr4yMbtRTHSlU4QqgDBHcvKz8vIM6kjHiT1xQOJhZGsrE1ZiShfYUXEYozH4YmHOc862ixk4AT8g85oy5GnMrtHquSkYYgnOIHMDT31qWHPtEi7SIuq7qjrsnNtJBZdQ6FJoVI6wyufFtIFhO2EnQiPHvW9rJNa6Wzuvq5vDsFlIMQv24kh/ScKBu61gezXvj3pyxwj8W+mTDQ3OdpeeSsRuq9xNWB4XfAKctxs4Ivw3Impks00EF80o4t3TIy8XcAGc31i+y3ZrZm+DSRaXoUuYMG0yI+c43kp5IMvrY13RmZ4oUsqKSWgjARZrMuJx5zlbIQY9ZE2uxS5JUaSe8Wwo7ljmFJYs8Fl7OVDgyscjNBihjKg~4473910~3159346; _ga_F433FYMYX9=GS2.1.s1758623618$o1$g1$t1758623620$j58$l0$h0; _fbp=fb.1.1758623618568.22689390473729608; _ga=GA1.2.169979920.1756910999; _gcl_au=1.1.1263730701.1758623619; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_KY7X120D0N=GS2.1.s1756922043$o1$g0$t1756922043$j60$l0$h0; _ga_6XHS1RXTBF=GS2.1.s1756922026$o1$g1$t1756922034$j52$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1756921934$o1$g0$t1756921934$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0"
}

# =========================================================
# AUTO-INCREMENT DESCRIPTION
# =========================================================

def make_description(i: int) -> str:
    return f"हर घर स्वदेशी, घर घर स्वदेशी - आत्मनिर्भर भारत #1ee101{i}"

# =========================================================
# MULTIPART BODY BUILDER
# =========================================================

def build_body(description_value: str) -> str:
    return (
        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="description"\r\n\r\n'
        f"{description_value}\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="navigationtag"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="referral_jsondata"\r\n\r\n'
        "[]\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="addressid"\r\n\r\n'
        "aec0af1223de648f21f391fbe12cf28e30735e4afec9fcb4a417daff4eede6ae\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="title"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="action"\r\n\r\n'
        "createuserposttask\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="X-Access-Token"\r\n\r\n'
        "dd363609a277ba3e3226cc7c44dbf205b64c87028a58bd21397036ce84ffa740646bec23da4e3815fa4d6b1a7e7fe8bbc428e092e80a5f8e61d80c511020b945eb0a23707ab81c4f87c2830c57afa7956b56c11141f91a4bccba76b00e9d2a823b34519053c181a152f2c1de2e4644b39a16b96b50718c3896c09744a2ab6b593ada38aa9624be1ebdd5cc77f8f1f05cf95fef48a14e5e2af4bc7ff3cfbdadd983be30ce4d972bf444ce7da4db3dace5b78356f4f21cabfd2a4d089d4551356c8acf1e2de7d11a7160a201d21f872f1b4f8abc9394dc63ee424fe870a6d7787d96f0c9115a7ed654b0756c8875d76c97\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="apiversion"\r\n\r\n'
        "2\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="deviceid"\r\n\r\n'
        "8455FFF3-8E05-4F50-8087-D71D37FB4F2C\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="groupid"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="x-app-version"\r\n\r\n'
        "7.8\r\n"

        f"--{BOUNDARY}--\r\n"
    )

# =========================================================
# SEND REQUEST
# =========================================================

async def send_request(session, index: int):
    global stop_flag

    if stop_flag:
        return

    description = make_description(index)
    body = build_body(description)

    headers = HEADERS.copy()
    headers["Content-Type"] = f"multipart/form-data; boundary={BOUNDARY}"

    for attempt in range(1, MAX_RETRIES + 1):
        if stop_flag:
            return

        try:
            async with session.post(
                URL,
                headers=headers,
                data=body,
                timeout=5
            ) as response:

                text = await response.text()
                print(f"[{index}] Sent {description} | Status {response.status}")

                # If the server responds with 403 Forbidden, the token likely expired or you are blocked.
                if response.status == 403:
                    print("❌ 403 detected — stopping all tasks")
                    stop_flag = True
                    return

                if response.status == 200:
                    return

        except Exception as e:
            print(f"[{index}] Error (attempt {attempt}): {e}")
            await asyncio.sleep(5)

# =========================================================
# MAIN EXECUTOR
# =========================================================

async def main():
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:

        async def runner(i):
            async with semaphore:
                await send_request(session, i)

        tasks = []

        for i in range(1, TOTAL_REQUESTS + 1):
            if stop_flag:
                break

            tasks.append(asyncio.create_task(runner(i)))

            if i % 50 == 0:
                await asyncio.sleep(5)

        await asyncio.gather(*tasks, return_exceptions=True)

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
