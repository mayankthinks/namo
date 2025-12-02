import asyncio
import aiohttp

URL = "https://api.narendramodi.in/mlapiv1"
BOUNDARY = "Boundary+2C2F2A3AAB987201"

stop_flag = False   # <- GLOBAL FLAG

# -----------------------------
# HEADERS with full Cookie
# -----------------------------
HEADERS = {
    "Host": "api.narendramodi.in",
    "User-Agent": "Narendra Modi App/7.8 (iOS 18.5; iPhone Build/Narendra Modi App)",
    "Accept": "*/*",
    "Requestfrom": "ios",
    "Upload-Draft-Interop-Version": "6",
    "Upload-Complete": "?1",
    "Accept-Language": "en-IN;q=1, hi-IN;q=0.9, hi-Latn-IN;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": "ADRUM_BT=R%3A0%7Cg%3Af044926a-a4b3-4dab-a077-5a980c0fb3955012%7Cn%3Atmp_bjp_fb49d1de-d391-478a-ab5f-c84d7b25602e%7Ci%3A37735%7Cs%3Af%7Ce%3A77; NSC_10.10.24.75_443=ffffffff0902062045525d5f4f58455e445a4a423660; _abck=E921128DDAE2823E0112175943B9E330~-1~YAAQF7xWaJtpHomaAQAAv9U3oA6o3wetFvfGBBCmt83VQGF7YF75bd0CmUobc9SrRb6Ng0jcVvN04vjdZef2dAklq3cdbT5sKbuwFR9GmdYiregov1vS0Vd0j6KPda+0AIhhnqhhYXv2O1xctGm3zhifcqcd0S02i8Z4xS0pFGUimf2/LWSztW0dLqL4A+rn5Kt6dWsvFkkYLMPmC+ZGyohlPCbnBbBdIlFSovhVfq++Txswjl7zghxXyhap8MfOpy6CPyKGyq0ScWw9keMk2mT+i6SmRLyIIJxXiI6+Yq0IJNL2xAJcA77/xH7/FpJQNX0sydf2jT2hx/tcjdctki6zWaXp/CfyJ8AkMEzlISJgmrkoStJ4uD0d3IyQ3mkHNCXeCZorXLhx02oXQ5xdlLFZIIpQWSjw6trDZir6vf9g4FLLm1+oH9YQFsAmEHSOS1LsZYVLpXum+m/b+AcONKJCeoAg5H+MFIBbWosa6fIVdZPyKKYOCSILl4AWwkfsX2OsvIi3Tj5jRB7C7tgCoPOBgoLnQdzqdhI9b8kcWJJujq1X4yf4LOolEGBBE/ARl3fJFILroklinGm0HDSWdNVVDnzASUzqrm1EpQ==~-1~-1~1758627219~AASAAAAE%2f%2f%2f%2f%2fzV3V65Lkl0N6BwkWFdhg%2fcrS%2ft1ctxLI0ewsj5G+MotAoPmHUuR7t78pjqP2mJXl9bCM0eZ~-1; ak_bmsc=A39206D16F1469D483DBC363D57D6D07~000000000000000000000000000000~YAAQDNgsMYL2N4maAQAASYAeoB3TyGU+ADM/4rV30n+luRSWHRCA4MWTfNCTnCRFKr6ZC4J6akB6KFEHGVWQ8Y4XfE5KYextKbuZLd035OWwQcFhlYTwJQMR9l9gYnXv5OHp2bB5Zrfec7EAmRBvZbk8m7JRtr3KXfXJpf3REc8cfdyBnVvq6tv4NYv5aQ0RqqHRw9rovGXJtwDqEmcHoF028fs82ef11IboYb3CQ9YqDj7x4DO6sOwhMRzloG9TGScd4zDbDUrmiKE0rPgsMapBu3tvO3STsJK2sgUUiCubTtDddkwY0K2boyC8eytDM4Kj++t9QpZocGcXWsPzhoLx47tdg/q70zwcnIrZcFmDY6VD8BErWHnTGzbA1+cxByBDdc0DBsqJvxyfjunnRQRvG3BasX1ZOiF4e3qRrI4=; bm_sz=AB164BE5B8BB02EF1505A1B715394377~YAAQDNgsMYP2N4maAQAASoAeoB1AzcJEMmFjY0ar1u+SmapleP6x7ajp8XUHc/9pfb+hHCpHrCwTRSA2r4M9WfxgYLfxgfad8q+Iw0pGT0yr0cL4f0W4KUcjqkC/o4SSASAg9t6V6eBzyrrR7bkkcLclkpEWFAKAoIKmDGpk6rU0DgzsnPwnBZK6gDShLPlwyCOB0367XmRyAlpx3Yt61LDaKZxwd6EPWPn1SIKa3OsbK3rq+asuAVfVaXxac4rpM9RvZvtCrc5/dXlRv8p1FMnLU0CB+W8/9sLw57skeR4YBqyjVKQuL0hlHDI4wSJotp5h1QkNdvGQvYFiRioOan39A50FA9dYs+N/CSGQVTLXRPeGgtVu2dIxXdA7yJRdU0U+LjbpPXHfrMXZ~4468784~3750195; _ga_F433FYMYX9=GS2.1.s1758623618$o1$g1$t1758623620$j58$l0$h0; _fbp=fb.1.1758623618568.22689390473729608; _ga=GA1.2.169979920.1756910999; _gcl_au=1.1.1263730701.1758623619; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_KY7X120D0N=GS2.1.s1756922043$o1$g0$t1756922043$j60$l0$h0; _ga_6XHS1RXTBF=GS2.1.s1756922026$o1$g1$t1756922034$j52$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1756921934$o1$g0$t1756921934$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0"
}

# -----------------------------
# Build the multipart/form-data body
# -----------------------------
def build_body(comment):
    return (
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"taskid\"\r\n\r\n"
        "63256e933f99b3468b3cac26\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"X-Access-Token\"\r\n\r\n"
        "5cb77f2c39ef108d90c093e6148997be11a195b1f559071d680516970359de6429a4a736aa68ba6b2d1f568e9af9421f6ced70d11281c6764a144807e3b1aa0a52d18527695cca6f021c7488e902073ec39ad2d637256003538fe0e7ffaf9b840aa0cbe8693234834b6f7bfa8b61e8368d8578bfdab5efd13e7f090713ccb3a45fcd5b4d768ae260a50371cd7a7db5bea999c02620885622fac7bb5490ee6384c34a8395dcfd5fdbab75fb321eb31ac1a87ecfe5a7dc637e493f8c74ef1c3fa9e17c7598fcb47690e8413c1dbffb2b692dd501e4288fc43a28c50ebf18454e9a130d54e0f8cd3114b6f7aab07e780f85\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"deviceid\"\r\n\r\n"
        "8455FFF3-8E05-4F50-8087-D71D37FB4F2C\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"action\"\r\n\r\n"
        "postcomment\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"navigationtag\"\r\n\r\n\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"commenttext\"\r\n\r\n"
        f"{comment}\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"apiversion\"\r\n\r\n"
        "2\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"x-app-version\"\r\n\r\n"
        "7.8\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"addressid\"\r\n\r\n"
        "b44502f02d80be505b3573c2ef251f04d5680fe29cf84be414876c9273311b8b\r\n"
        f"--{BOUNDARY}--\r\n"
    )

# -----------------------------
# Async send_comment with retries
# -----------------------------
async def send_comment(session, comment, retries=3):
    global stop_flag
    if stop_flag:
        return

    body = build_body(comment)
    headers = HEADERS.copy()
    headers["Content-Type"] = f"multipart/form-data; boundary={BOUNDARY}"

    for attempt in range(retries):
        if stop_flag:
            return

        try:
            async with session.post(URL, headers=headers, data=body, timeout=5) as response:
                print(f"Sent: {comment} | Status: {response.status}")

                if response.status == 403:
                    print("\n🔥🔥 403 detected — STOPPING all tasks immediately!\n")
                    stop_flag = True
                    return

                if response.status == 200:
                    return

        except Exception as e:
            print(f"Error sending {comment}: {e}, retry {attempt+1}")
            await asyncio.sleep(5)


async def main():
    global stop_flag
    concurrency = 3
    semaphore = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:

        async def sem_task(comment):
            global stop_flag
            if stop_flag:
                return
            async with semaphore:
                await send_comment(session, comment)

        tasks = []

        for i in range(1, 500000):
            if stop_flag:
                break

            comment = f"Ytededwdyr14713196 Bjp {i}"
            tasks.append(asyncio.create_task(sem_task(comment)))

            if i % 50 == 0:
                await asyncio.sleep(5)

        await asyncio.gather(*tasks, return_exceptions=True)


asyncio.run(main())
