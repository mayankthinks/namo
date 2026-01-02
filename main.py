import asyncio
import aiohttp
import os

# =========================================================
# CONFIGURATION
# =========================================================

URL = "https://api.narendramodi.in/mlapiv1"
CONCURRENCY = 1        # Number of simultaneous requests
TOTAL_REQUESTS = 500000    # Total requests to send
MAX_RETRIES = 3        # Retries if a request fails

# The image file to upload. 
# ⚠️ THIS FILE MUST EXIST IN THE SAME FOLDER ⚠️
IMAGE_FILENAME = "rb.jpeg"

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
    "User-Agent": "Narendra Modi App/7.8 (iOS 18.5; iPhone Build/Narendra Modi App)",
    "Connection": "keep-alive",
    # Cookie from your latest dump
    "Cookie": "NSC_10.10.24.75_443=ffffffff0902067c45525d5f4f58455e445a4a423660; _abck=FDB3220133339F2D910B7F843BED449F~-1~YAAQx6TUFwK6fE6bAQAAPoHefw8OfZKHncdSilg7jKl1VSUfed/V3MhX/IEdKapaihQudd2VCju6WMGB/fd0PVAvGw0mfmw3gBs/6DFi/MPibvAo9/v5f8xEAc5+3vMBx1RDyAeY5rXkEU/8aOCUEfUpJHlkM+PMQlbKFiSjTbMgthhAhZWG59mS6K78CF4b0K6H6YAV5nrjBzKGFXnM7WoQ+LdcJo4Q8cLBZhiEAw5Ljs2ZRDb/3CIexjsGQLcb1sYiioCwuVcxZO3vEq4psVCvrCBt8ZuzpQbByrSM8orVlMPSAbbc9pghMlXFQ4waH/oevit2AOrcaUm1XQaLLNR0uB8sMnrpjFd+jVsxNcrJSo/1T4CDGA==~-1~-1~-1~AASAAAAE%2f%2f%2f%2f%2f5JL6YH8QcuG2P6OJ4vQx3KxCZ8rETDVUlrZJZ5bRoCbQFz4aRKR1BdhVfhwxW7MsghZsV63~-1; bm_sz=D2F8A004D24154DAF2C2A937FC99E84B~YAAQrAzVF+g1zS2bAQAAXBHOfx6jMyr5PdtI59gSD5SiXmbLusDX8rgB3LpBN3qXjN8zgwWh/4D6yZ06asJaL21M+XSVuk4pyGdO7lH2CZeDamMdivpcKYNdL6AcatK8DXElKbsaqu5Rk/Y4ucEUw4gBRIOnQOuGfWzZuW0vFecOoh2/aIYfZbe31kKKOVAlifkKrTeWiZYcbHPv9ywwS/QfmesaQsLFDQKvi8rAA3KvaUajbpMY+0VGBvxqvjPTDuxfTM9u+I0DN2/cMWGjKzybOdEH4YfJXD1mor6jhPH5c3vOXiCxLDJtRkXWZ16QGdAUMsjpS6Bam38T+M2AxUgX+41y7L5RlqrkfN8qKTeDhZ9z3LIHrK9KNIrMtdMSS5lpvyQQXEmWu0ul~4468791~4600886; ak_bmsc=D21A175315101EA25739D481B7337C84~000000000000000000000000000000~YAAQXgkuF2Tb/HKbAQAAFMLKfx7UbZRKuc+dAngJMXlbJXi6tO0ouwIKdOkxCkLtaOzAbhMvFMaUx4NQfxCEQtrKPduN+phQKw8h59rXM0LmeUhlao4dF9ciUO66sKg6gtrIdVZE+Pp/X0NgPltsHGpHEXltOzAmSewjrg/xVTM8fMxLcqpulih6M6yVRN3xT8uYAZKtCUJwHwDmgDxzeGe1/fl48ksN+tTF9erwOyyKXi8rs8ktp+em2WYfZQM83GaAE1ehPKzCs/RqrVn2+I+jVCDtC82zpRP0E0b5bOdKL2SU9wSBPWRhEOKILeix6TMcfpdrhjL55O3BZCH2IEIywwnGwv79CyOcVvaKzCQGQHJhVFwO2aH3gqidT7fUrXlBhLkz7ACnNemovmEy/rq4R9tw3lorW4jHwng6NbTX"
}

# =========================================================
# DATA BUILDER
# =========================================================

def build_form_data(index: int):
    # Using aiohttp.FormData handles the Boundary automatically.
    data = aiohttp.FormData()
    
    # 1. Description (Hindi + Tag + Index to avoid duplicates)
    data.add_field("description", f"सशक्त नारी, विकसित भारत!\n\n#WomenEmpowerment11 - {index}")
    
    # 2. Dates
    data.add_field("enddate", "2026-01-03 23:33:00")
    data.add_field("startdate", "2026-01-02 23:33:00")
    
    # 3. Links & IDs
    data.add_field("youtubelink", "")
    data.add_field("event_cat_id", "0")
    data.add_field("referral_jsondata", "[]")
    
    # 4. Location
    data.add_field("longitude", "86.975656")
    data.add_field("latitude", "25.253978")
    
    # 5. Title (Hindi + Tag)
    data.add_field("title", f"सशक्त नारी, विकसित भारत!\n\n#WomenEmpowerment1 - {index}")
    
    # 6. Action & Flag
    data.add_field("action", "createeventtask")
    data.add_field("flag", "volunteer")
    
    # 7. Access Token (From your dump)
    data.add_field("X-Access-Token", "19385891a626ce735e693ce89e96480ee06f0ad34cf2f7085b316b830259af704ce5b641c38fdb61eaaee03dfd3661c00768c516a8f9f36997ad1405eeb62821ae57db9f02a2b9fae69a21f554e003adcfee34f7e1e4dcf5d085d1877bd3e31748a74fe2606e81f976dd87b56909935e65df51587ea5e093893b2fd9090d3f06f2879cfeabf90c15279d96cf8996ce00537fc3b9c64b960a57f46d5dea34af84b2fa660d23b885a8d1702bdaed7818edbc5c5d956931337e802ad64288ad73cce00dcbc777d94f4ddedff7b1539c56c52b22b8a5ccac3559b4184c5cb0d5ec437a6804ea297f29babf18572a377147e6")
    
    # 8. Device & Venue Info
    data.add_field("deviceid", "8455FFF3-8E05-4F50-8087-D71D37FB4F2C")
    data.add_field("venue", "16, Deep Nagar , Bhagalpur, 812001 , Bihar , India")
    data.add_field("addressid", "1ee9f0cc08de502c70e706f6fd7289c9ae51c122e04ba3fd9fac14ff6234d5e9")
    
    # 9. Versions
    data.add_field("x-app-version", "7.8")
    data.add_field("apiversion", "2")
    data.add_field("navigationtag", "")
    
    # 10. IMAGE UPLOAD
    # This block handles the binary part (ÿØÿà...) automatically
    if os.path.exists(IMAGE_FILENAME):
        data.add_field("image1", 
                       open(IMAGE_FILENAME, "rb"), 
                       filename=IMAGE_FILENAME, 
                       content_type="image/jpeg")
    else:
        raise FileNotFoundError(f"File {IMAGE_FILENAME} not found.")

    return data

# =========================================================
# WORKER FUNCTION
# =========================================================

async def send_request(session, index: int):
    global stop_flag
    
    if stop_flag: return

    try:
        data = build_form_data(index)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        stop_flag = True
        return

    # No manual Content-Type header; aiohttp handles the boundary
    request_headers = HEADERS.copy()

    for attempt in range(1, MAX_RETRIES + 1):
        if stop_flag: return

        try:
            # Increased timeout to 20s for image upload
            async with session.post(URL, headers=request_headers, data=data, timeout=20) as response:
                
                print(f"[{index}] Status: {response.status}")

                if response.status == 403:
                    print(f"❌ 403 Forbidden at index {index}. Stopping.")
                    stop_flag = True
                    return
                
                if response.status == 200:
                    return

        except Exception as e:
            print(f"[{index}] Error (Attempt {attempt}): {e}")
            await asyncio.sleep(2)

# =========================================================
# MAIN EXECUTION
# =========================================================

async def main():
    if not os.path.exists(IMAGE_FILENAME):
        print(f"❌ ERROR: '{IMAGE_FILENAME}' not found in this folder.")
        print("Please ensure 'photo.jpg' is present.")
        return

    print(f"🚀 Starting {TOTAL_REQUESTS} requests...")
    
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:
        
        async def runner(i):
            async with semaphore:
                await send_request(session, i)

        tasks = []
        for i in range(1, TOTAL_REQUESTS + 1):
            if stop_flag:
                break
            
            task = asyncio.create_task(runner(i))
            tasks.append(task)
            
            if i % 100 == 0:
                await asyncio.sleep(10)

        await asyncio.gather(*tasks, return_exceptions=True)
        print("✅ Finished.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
