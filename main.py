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
    "Cookie": "_abck=E921128DDAE2823E0112175943B9E330~-1~YAAQhnEsMTtADKyaAQAAyr1nHQ+JBI8rTNn5LiJUgiSsVpV6p3Njvbs0za9dLSRoTF+nDljH+IhYtOSd+mSm+Ob2LA03dwGaQYgTHje7pyme8UQpgIxzlEAUvpfDP/xe967KUVz4J6NBdWL9q49nEXd3KuidyTuH/Qvv5lUZaaCKeoL+oTtRCAOOboq28f1TvoxxI6TjivWHU7TT9QclVU0RUhFdf0SXK3rPJKE32wyJdSbPJqiu8TSsOJcTB6kG4FObZ967b/ih3R8Fy9pdQrYuTWKCQ1fzfEtmXx19Xh+c180PGM5138+KnUSNAY2eeM0ltDM1qLE8HbEI3mz4PhGABbZWzX4nIrkxWYvZ8v+EDdXDrY158gG/9cdP+hMYF1S6V6u8GRsnnKJGKpHib+bzXtsUII7173HIk4wRxfLJyI7BGLW6Erms6FWBxCJ5IFRymNQ9C2m3WqCwUPHgXbyr084115f1AUyote9JSBbJTWcdex/aMq69U+rLhtUuPpviSyNJducjb6YkjWX1SX7r2BpB5Io2NzyX5yuz/JcNqA3aU3sn/D/bKc3qF/xrELt12pmffIHWKgfXIV1Cx2+1uBHybLMwtm559A==~-1~-1~1758627219~AASAAAAE%2f%2f%2f%2f%2f1Ae3cIwNj6NrJAKv++UWcWJfSL1%2fCuQU0f8fv4JDVzn3D58YfBaT%2fjbMZepR7H8occ0gs4u~-1; ak_bmsc=A211193282EE06799053875E4F393CD7~000000000000000000000000000000~YAAQUozQF7iuywWbAQAA1/lcHR5XOtk3m69P1IFz9OSk4nRVa6mCINouRiYvDxbKMCUBf8N/GjURfm1MD8ETNjZ4SVXBGSrqF+sTy+nQB8IrPKEF9GfWZPmKUipTtoLjhqeO/kehMO2WcI6vsJKGDo7Sh/H3uJAs1MkjhcQa2Xo9P4Sj6VzLKC56X8YtdawvWtxwVrW2wTg/c2229If3yqomB4MfVruLIomo6oodB0obB0JiKtYHDmFZsU6JSFzKvkERvBv286yQejrXFHopzArLAlMWfyZPRlXwhmygAQrQYjrdll46BIuf8rl3y52w2BqB1dKcJr7TD/AVxf1CkwMkaUZ2ct032yiMr6s3SQjkX1mJTIQPtC7qxqZIyBS59MNVhoh9+FIq7Q/rB5QYZDFNt7LHVEWJQOQvB8B+VxM=; bm_sz=9790F2C9C54F76DFC089CEDA3A83AD64~YAAQ9sIRYNRNCgqbAQAAH+nHHB6SBAPoctF99TCdQ2fxi85ZTX/aKzqSeqUWp3RqJI+S8TYgeYbqw1AjoupSXCo8OdQ3pi5EJrU+8qioY6bq1KAbgzv/Mw5L9diGGxo5PmYkUuXmKVaITg4U7USFMj6uhf4R+NcfEJU9y8myPzIdsK1k+PKcizZdPI8PDkXXMJ4DWe0z1wMd762WK3HcqeAFdsbQ7pk7x34VpsF40yySRufUDT1cFWoghoRQVncMKqpicnEf8M7Dvjy9UOWxKeA47KMPtuyqSck5K9ugWIAbauorGsczbyNKM02ngzkBvRiYNoYYfL00pJYOVqrVZgJ7K7fnT93v0pAmAnPLqfuOWys/lkSHtdKaqpWcgOPpo+HaYhNVF9mF7XZZ~4339509~3160116; _ga_F433FYMYX9=GS2.1.s1758623618$o1$g1$t1758623620$j58$l0$h0; _fbp=fb.1.1758623618568.22689390473729608; _ga=GA1.2.169979920.1756910999; _gcl_au=1.1.1263730701.1758623619; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_KY7X120D0N=GS2.1.s1756922043$o1$g0$t1756922043$j60$l0$h0; _ga_6XHS1RXTBF=GS2.1.s1756922026$o1$g1$t1756922034$j52$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1756921934$o1$g0$t1756921934$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0"
}

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
    concurrency = 1
    semaphore = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:

        async def sem_task(comment):
            global stop_flag
            if stop_flag:
                return
            async with semaphore:
                await send_comment(session, comment)

        tasks = []

        for i in range(1, 500000000):
            if stop_flag:
                break

            comment = f"15122 Bjp {i}"
            tasks.append(asyncio.create_task(sem_task(comment)))

            if i % 50 == 0:
                await asyncio.sleep(5)

        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())
