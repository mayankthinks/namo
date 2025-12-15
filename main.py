import asyncio
import aiohttp

URL = "https://api.narendramodi.in/mlapiv1"
# Updated Boundary from your new request
BOUNDARY = "Boundary+2C2F2A3AAB987201"

stop_flag = False   # GLOBAL FLAG

# -----------------------------
# HEADERS with updated Cookie
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
    # Updated Cookie field
    "Cookie": "ADRUM_BT=R%3A0%7Cg%3Af0deca6d-538f-4c8a-8340-8d4bc6ea4fcc822%7Cn%3Atmp_bjp_fb49d1de-d391-478a-ab5f-c84d7b25602e%7Ci%3A37734%7Ch%3Ae%7Ce%3A84; NSC_10.10.24.75_443=ffffffff0902064045525d5f4f58455e445a4a423660; _abck=E921128DDAE2823E0112175943B9E330~-1~YAAQTnIsMRW/CQqbAQAAB3VgIQ8MgnhUdT3mGLwEOF8TWN3jjgYSOIYHo+saARDdeGa2U0hJ67RIlp5IWLHO5M5oyr18wkSuOFon0NpYRSxmbZnS3vWEEkKLCHyC4Z62/hNw3Aq2tYO7tpPWsWfEHpAAsJamFY1RaOimKP8fh/kLW4C+5LfGtOnAxNzaYhexkIRXNwo8dg0+LCfxXl9S0TTBX8kT1YdbvPWqZ0VbaY9gmuxjHFGGwjmDSNgnwjgYSSOT95DslB8sAHkd5UmaEMCteoGhThXaIeG0w6lUSgaqz8sMc/TraW7D6pODt4aTu5IEnZQwRDqc0JByOA3+YVX2wwpoJOSri8Xvxk/RVQB2mxTnDWTN4JaHwdPwkclqfjph3PTOJbeiyaxN9MTdxhANZMaEw8uKx9WtjkpTQJmtaQnK8ilfxXVw5T+x7rfZ48QMW6bIKKYwcNx/BISL3KhL0ut5dqh7IvYOC1jZ2kNB6b66wRhWcO8LuHZ493h2sE6uw6X/dE3+Tlq34d+zMJjDB7N7Ycr2jzXxQ5eY5tn1wXwsfW7uPXsirlwf/YleuBM=~-1~-1~1758627219~AASAAAAE%2f%2f%2f%2f%2fz08ECwfGzosOTKXmJDU2CVZpsKACckhAegxUWXGp8nS%2fDDoU%2f%2fTatJSuy9yPMtbR92wZ0fu~-1; ak_bmsc=65268E8B1536682D9B520DDE8CC42F26~000000000000000000000000000000~YAAQOUw5F7KgmwubAQAAVnZYIR4aDeNVfU/Wf96tMP56ST42gE81Jx+OtreV/ygEM7iTPkMGYV85B5vhxcpgUNHI60C5GTlMI3l6LpdAsOwr2hufS1tlNtqEMmx/ACzERevoFHmhGohnJC4kzJUCq1FnP19N1axl06NqdDHCTf6dSHVS8S0PDLxs8lp5F4r8+X0vTpdQVZcamo3An7qKCoqqteguV/cQBbpWL3V/QBVEvU6XTAqtU2DOnbZkkdRYM4lv6jdllkMazQlRcp3Nb/QHZ7pyZKP54bSHe4pnbfWQPkMgoy1+ZzF50E1dSYMGi9NZcfKctc6hFrvEpb0rY9vZGnyW5NKjsqAzM2fgqpGloLwV7+Vblbuw6kb9NMhWHVa+1v7ovEUgHPS83DzWGM1lkoeGSVQqYRQg70kcraY=; bm_sz=F4DB22EAC810C73E1D8143F42B298E23~YAAQIUw5F0XgbxCbAQAAga8xIR6ae4qR1Zd2f6tmcMeD5iT8zoK87yfAjit1yWWBWc+emeXFvDeADc9WKG6IqUH83DWka/Cr0RYsSRevtXZ9yy5cMlKb1PBv0rXDYoFsdflo59vBSiAkKpj/8bgM1epAMC6H8oqm+Dp8QVpPRfyS6/tfuJgdPmiAyC+BTHb92LTaEVqkz9ezB/PSyh55EQmFh7y8AiU+tmn+f4h9YPw/8uWb3z5r+4zaL6OBSEK1bnTyE8AVjJrW/GAF1oUhBExHEyb1yNJ2oMRbFCo/wGuAr7GROMb7u4NHtjQPpeO0G4kwvFehN2I6hUAOy0ZHtb62cHa1BWfdSxrArFJ98Kv6M9au71HheNoW2dix7UYCXoqwwPZX9zPkHhiPrZzMPS5fANoy9VkMKV3zBvcYVkdfRWgU~4405556~3225651; _ga_F433FYMYX9=GS2.1.s1758623618$o1$g1$t1758623620$j58$l0$h0; _fbp=fb.1.1758623618568.22689390473729608; _ga=GA1.2.169979920.1756910999; _gcl_au=1.1.1263730701.1758623619; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_KY7X120D0N=GS2.1.s1756922043$o1$g0$t1756922043$j60$l0$h0; _ga_6XHS1RXTBF=GS2.1.s1756922026$o1$g1$t1756922034$j52$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1756921934$o1$g0$t1756921934$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0"

# -----------------------------
# Build the multipart/form-data body
# -----------------------------
def build_body(comment):
    return (
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"taskid\"\r\n\r\n"
        "5d8521be2c675f3816bf56eb\r\n"
        f"--{BOUNDARY}\r\n"
        "Content-Disposition: form-data; name=\"X-Access-Token\"\r\n\r\n"
        "fa4d7d63ee643db59e1bc0d943b1be037a831955527ebe82d203e0c2f2df65fbbc31e94d778b9b5457851ecf1ffc33cfb3b50b4d73dd503e811329e2f1d25d83d96ddaaa4a1fadb40b133fe9d26b96954ffdaaec8d2ca2e7c7451a50f34b0795b77858fc24739d25a9d8d8a97ed7c7155f69ca9321288aeeebae48bd271b954002f619fc1f68df0b5561183deddf1d5f612a90296ba2ed4e73af9715afe865b8d3aca137f318cb0cf674684dbc006a03630beb52bb031168eedec4ae25d855b132e37ac198aa9672ab87192b4e4b83dd33b78fddc1e15d1f0a92a52003367d89d3eb5880465630cb6d1dc9178eea58f0\r\n"
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
        "5e6d8b312636f2a3be74d4ea6646602ccfc20c7b80840364649d32f4075006a0\r\n"
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
            async with session.post(URL, headers=headers, data=body, timeout=2) as response:
                print(f"Sent: {comment} | Status: {response.status}")

                if response.status == 403:
                    print("\n🔥🔥 403 detected — STOPPING all tasks immediately!\n")
                    stop_flag = True
                    return

                if response.status == 200:
                    return

        except Exception as e:
            print(f"Error sending {comment}: {e}, retry {attempt+1}")
            await asyncio.sleep(3)


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

        for i in range(1, 50000000):
            if stop_flag:
                break

            comment = f"patt bjp 1 {i}"
            tasks.append(asyncio.create_task(sem_task(comment)))

            if i % 50 == 0:
                await asyncio.sleep(5)

        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())
