import requests
import time
import signal
import sys
import concurrent.futures
import os
import random

# --- Configuration ---
def get_config(key, default):
    return os.getenv(key, default)

START_POST_ID = int(get_config("START_POST_ID", "50000"))
END_POST_ID = int(get_config("END_POST_ID", "1000000000000000000"))
CONCURRENT_WORKERS = int(get_config("CONCURRENT_WORKERS", "1"))
DELAY_PER_REQUEST = float(get_config("DELAY_PER_REQUEST", "1"))
PAUSE_INTERVAL = int(get_config("PAUSE_INTERVAL", "50"))
PAUSE_DURATION = float(get_config("PAUSE_DURATION", "1"))
REQUEST_TIMEOUT = int(get_config("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(get_config("MAX_RETRIES", "3"))

# --- Proxy Configuration ---
USE_PROXY = get_config("USE_PROXY", "False").lower() == "true"
PROXY_URL = get_config("PROXY_URL", "http://IP:PORT")

# --- Credentials ---
X_ACCESS_TOKEN = get_config("X_ACCESS_TOKEN",
    "a46fbf7fec8281f252cb75c96bb7e8e074eb95f9dfa4a9e771929734f65cd037a60"
    "bf830825f31675fb26dbee34161a3cfafda6ace8b0a9efa76b94142167f6052f90"
    "12b6ec7734c4e43523dab807dffa745a17e5eefe4db35fda436df2e365fd10aec0b"
    "bf973a6f369f08a85c1b9e720b5076cb35b2053e88aed2d974a8a73c678e929fb65"
    "41d273a747a5da61d4b33936441b48f796c821436a5376fa4b5a31dd18498aab9f"
    "adc5249c29aa631084b2f52b3c0f8d99064a93348d76311eed5b1a6f9f3a3b623cd0"
    "0c9b90f310ef37a9905bf1d5fc4be227f4c7f4e01883a75bcecba4d3da1e8d70f7"
    "3b08c3e535568"
)

ADDRESS_ID = get_config("ADDRESS_ID", "0228a3439c5d0108711a7ee829c60b8e09f9ce168844e125d211f0bf05b7956f")
DEVICE_ID = get_config("DEVICE_ID", "8455FFF3-8E05-4F50-8087-D71D37FB4F2C")

# --- Sensor & Cookie Data ---
X_ACF_SENSOR_DATA = get_config("X_ACF_SENSOR_DATA",
    "4,i,oKaBIsIWpVocxqq18CbaPiy1yqM7GyXKB/8zjL5D8Vy1PQ8b06VlgMIiDi/s9DU7mpLXELXe4PEEQhtgUZ/Szhz9ZbF7uw5k5j+9ZFiq4riGr86A8JDvQ/mLw4pPXMoC31GGkYhXF6BvZAT7ETlqZ6nNNI4E8o6pNksA1vm78c4=,VFRSAygDR0ml21S0/gAki5C7FJaJz6pTu9JjcScg4evsU33+CfeBWHkzijyyydJ1n4nY+fsc7l2OYad1iV2QzcCY0ItnlQlHtOJ8iNGDZ2T6PGf04GHxrCGXvMoaGSZMvZTZEVQ/oj11zhNYePptXEJtFL1D01CL08MB3FtSZEY=$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$15,10,57$$$AAQAAAAG%2f%2f%2f%2f%2f6w12nf0j0t7AZEnrpm6qREwRI0OFbAwCv6VRm4Dxj%2fbyWx56x423MbT01hogTeFLIlVTLwIK1CNCr6TD9AthqP7l4tWiX2Kx3vCTWfthC%2fhVGU5jz5vWZ4rA27WOcosuHCRkZaoybnIffOVYg0SKwwtuzLIsAVGq7PXuGEdNvBHb+zQWMPaZZBVfO9ws59PkFLY2+QT6viFis653PaOn20iwXfGEzB8YxT6iWEJ%2fM0YPoXEnq2DeBjtM61RTb6v6ocsZmqldCqeGOJBBrWrVkuWq2XdibUBrx%2fuy3Tcw5oBZZgDw8D7hlBwemxKGCsZC1PCQbimuntAiMgkKGGvlbw%3d"
)

COOKIE = get_config("COOKIE",
    "_abck=FAE3E3D938D02209ECBA22E43979144B~-1~YAAQtsEzuFcZMOyfAQAAkpCXJBBux/pqCB6b3NMehXrOdFmEmVIho1jVL+T7ggC2vGIaTtxTxzIwAHkAmCztiHi5m8plj/dm172WNgmcTO3YNwLxPVNHPbLtq3PRJv6QIsttNenflkPiqxpmtN5fjR6Z56xPMvg/w6LhcbY7u58scCFgQcCzaeSbHit/07vYT0Lj1EDHMhkl8amMGxjsgnDsdnR8FPX4QL7EMWglCB/j/dMnJKAHb5g0NWAa71LW4lj0GVhhLlLLMq3auFC9M4nz9NAjRVRA2sWZ0Lyxm078wG+dUd8kz2OaU80p2a8TBcdpzrN74ucP1lM4ptc0dTmIiZ3j3+sejYEmKF48X42IeHXYTmqEt2mINhG6UpGIa0d1SvxmJOj6P1fTX0/R1vvK1tq8sBTHe6FXZQcuELlwA46SfMI/1VlggjAWA1qURh6uq+Kr4WIQ90M1kEODsLwC8tT1fF2cBWbh40Ll8n3gHW1424D/OMf6JFN9ESkRtiKJXwXH6PQLxDgqf3Nt/NbtR73g83QV4TDfb5Npqz7ZWNnInxzpi0o8hv14lxkYkN55G8326wQgztY5IN2nyrKk0rktdtPvY86imKtAh76X0iW9QOmcFuDAACKfhRyQagtsjd+EwTWfu5wSCWRATqWEvrSyRYCDOB7F2xqph827Uq6pYA==~-1~-1~1787322191~AAQAAAAG%2f%2f%2f%2f%2f8Ulr3TB7htCa1Y95KdDle7jLmdMrCtZWGwsahR0vAX17oyh6t14H3jBI1px8AUsO96k%2fKV2wybtIhkqQ1C+uQa4S%2fgZ2bWoNN4s~-1; "
    "ak_bmsc=6C173AB8D753C2362D8FE5DB16C691F6~000000000000000000000000000000~YAAQx8EzuJQeC/WfAQAATh2AJAClWYqsXnUoW5Qc+6nkzAEauZFN/b0QxabJB39pzSvh7bOhMIwxEJW/hr1dR2mTmngBHBQOacyf74Xp96hmmz1JZf4/lVeUUWg1ewEKdP8G3nQoEpULCJ2UHfidO1ue7B0G/mE02/Hbw4EjpJmJLtiThUAgBQEVh4lNmfHFM8WcgBxbQtrxMpNWgR8DnR8Xu8RGI9qYwTL/LV87he+qqbLmHst1MSQt9xocZYbwo6oNAEKRYdRTTd4pKmumPEjiroFWLAlEL2eEuqFdJFLtv4hlJwF6DC1cPJOxkfM8H9R6ICAE69+f4HkyYaV9tEv3+dMBJJEpNc0uqy4EyZQ5fb+f63v06lrPs3pX6LGdVaIZxsxjAGuaHjnGxqYnEukL8VoNyxoeafCOyv72ZeXnTGrsJSiRFeXw1SMWZ+iYprJEybKeUV6SSADKUkR4sFvnn4NNxQYqezPB3DIqMDjqJZViGahtki5a65DPQAfLlnplwROq2z52Pxa97aLWvqrcEREMd/UZlaGaI3MjLwEABkOb2Ks=; "
    "_ga_6XHS1RXTBF=GS2.1.s1787318723$o1$g1$t1787318724$j59$l0$h0; "
    "_ga_VFNMV2T18E=GS2.1.s1787318640$o1$g0$t1787318643$j57$l0$h0; "
    "bm_mi=E616A45095D2AEE0A0070D737827D17A~YAAQLGvJF5eHI+yfAQAA6ld9JABacUyrM0ntq96EJuAzy/CdJ1H7yHmnvpB/lEEF+jv8iJeT9PTvEooJuv5O6uXdsFBy6mZifDWXKRbZznZmbKZh5bMlAveHw3KXam22Qs6lQRrQdkNX4VWftDvbo5Fzw/34UMJB+u6O0vulfXEWAD/jNfv+a58FbfZIvU9dm+/3OZWDGpDdaSDm/Pqcidk2pNxtMXPsify0KWJyoLtHa6ZSZHR1Qvs0vq8eigFPus5FCZjl67bnl7xg/RJ5G5BkbJOqoNtIRcVkHi+/6XCAr1MXsT6iXYkfPZvLlTfKu1DCMoW4/muvKpWEke4uil/1LA==~1; "
    "bm_sv=75A027D1E600195E452F4ED8E98661E4~YAAQLGvJF5iHI+yfAQAA6ld9JAAhJHq5xcHwIWqkJJPz9VRttQjDvM0a4nTGCkyyY9mDct2b0Gur1vRLlFI29IMmRfVmODUDigdfephGTTGrECn66ucskgUSb8TT7Cyh6KVonRozWBqVs4LmwUJ0WSWcIET8pUvtDesii3nJniSL/JSlbrb+S+95D2wPxuu0dAItNf9JoVsfL31JlsO+6cmaGxc1b4b94YcxnghPo0oAuwYVG8UEy8CCwToaumN0JGVPXWw=~1; "
    "bm_sz=785EA17CBD681B4A5D4F748E2A0C2BD5~YAAQLGvJF5mHI+yfAQAA6ld9JAAbPvIKUbfjlypWPAGBT4eeMG4K4e4x5aPcZPfwHAtE5uqq0anRNjtq5Lk8qeJ3m42hwSmMG3VVXrFeYRK560J3sar/FZyxoioupqjjTqs7DHDn32DwXdMZL3bHoo8mBUQlojAWTUQufeF+x9so//tiJ84k/cFH8La7MNHIVuwK02DxZp/rbpB2CwCQbgj/6eKdifzHKvM5D06XvOFKoQewP2MNmfknvmIjV6ZDgdujvAOQf1IjjJQ9P329nGVVDJJir3+CgCaPl8upgghK+R8pw8af9XJliVdkP8pBlFLG/d134jLl62nwmpcrHcj/EdylYni3FIr4FP7k6uFv2kRAsSzqXSmcSLNiznJkp4civk9pi3CPoDvH4PKgvYbs2E2mM1sWLlzJ+c5eC0hL+Q==~4469045~3359302; "
    "aopopuwtjtssi=RS_10_10_24_81_BJP_80; "
    "_ga_HQGP5S5CDY=GS2.1.s1786947916$o1$g0$t1786947916$j60$l0$h0; "
    "_ga_D18QMBPWTR=GS2.1.s1787320424$o1$g0$t1787320431$j53$l0$h0; "
    "_ga=GA1.1.1634634630.1786947916; "
    "_ga_W68WP061GD=GS2.1.s1787320342$o1$g1$t1787320387$j15$l0$h0"
)

# --- URL ---
API_URL = get_config("API_URL", "https://api.narendramodi.in/apiv1")

# --- Headers Template ---
headers_template = {
    "Host": "api.narendramodi.in",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "User-Agent": "Narendra Modi App/7.9 (iOS 18.5; iPhone Build/Narendra Modi App)",
    "requestFrom": "ios",
    "Accept-Language": "en-IN,en;q=0.9",
    "Connection": "keep-alive", # Changed from close to keep-alive to support concurrent requests efficiently
}

# --- Graceful Shutdown ---
shutdown_requested = False

def signal_handler(sig, frame):
    """Handle Ctrl+C / SIGTERM gracefully"""
    global shutdown_requested
    print("\n⚠️  Shutdown requested. Completing current tasks...")
    shutdown_requested = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def send_request_with_retry(post_id):
    """Send a like request for a given postid with retry logic and exponential backoff"""
    global shutdown_requested

    if shutdown_requested:
        return False

    for attempt in range(1, MAX_RETRIES + 1):
        if shutdown_requested:
            return False

        try:
            # --- Build form body ---
            payload = {
                "postid": str(post_id),
                "actionon": "nmreels",
                "type": "nmreels",
                "flag": "1",
                "action": "postlikedislike",
                "deviceid": DEVICE_ID,
                "X-Access-Token": X_ACCESS_TOKEN,
                "addressid": ADDRESS_ID,
                "x-app-version": "7.9",
                "apiversion": "2",
                "navigationtag": "",
            }

            # --- Build headers ---
            current_headers = headers_template.copy()
            current_headers["X-acf-sensor-data"] = X_ACF_SENSOR_DATA
            current_headers["Cookie"] = COOKIE

            # --- Proxy ---
            proxies = None
            if USE_PROXY:
                proxies = {"http": PROXY_URL, "https": PROXY_URL}

            # --- Send ---
            response = requests.post(
                API_URL,
                data=payload,
                headers=current_headers,
                timeout=REQUEST_TIMEOUT,
                proxies=proxies,
            )

            # --- Handle response ---
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    status = json_response.get("status", "unknown")
                    message = json_response.get("message", "")
                    print(f"✅ PostID: {post_id} | Status: {response.status_code} | Response: {status} - {message}")
                except Exception:
                    print(f"✅ PostID: {post_id} | Status: {response.status_code} | Raw: {response.text[:120]}")
                return True

            elif response.status_code == 429:
                wait_time = (2 ** attempt) * 2 + random.uniform(0, 1)
                print(f"⏳ PostID: {post_id} | Rate limited (429). Waiting {wait_time:.1f}s before retry {attempt}/{MAX_RETRIES}...")
                time.sleep(wait_time)
                continue

            elif response.status_code >= 500:
                wait_time = 2 ** attempt + random.uniform(0, 1)
                print(f"🔄 PostID: {post_id} | Server error {response.status_code}. Retry {attempt}/{MAX_RETRIES} in {wait_time:.1f}s...")
                time.sleep(wait_time)
                continue

            else:
                print(f"❌ PostID: {post_id} | Failed with status: {response.status_code} | {response.text[:120]}")
                return False

        except requests.exceptions.Timeout:
            wait_time = 2 ** attempt
            print(f"⏱️  PostID: {post_id} | Timeout. Retry {attempt}/{MAX_RETRIES} in {wait_time}s...")
            time.sleep(wait_time)

        except requests.exceptions.ConnectionError:
            wait_time = 2 ** attempt + random.uniform(0, 2)
            print(f"🔌 PostID: {post_id} | Connection error. Retry {attempt}/{MAX_RETRIES} in {wait_time:.1f}s...")
            time.sleep(wait_time)

        except Exception as e:
            print(f"❌ PostID: {post_id} | Unexpected error: {e}")
            return False

    print(f"❌ PostID: {post_id} | Failed after {MAX_RETRIES} retries")
    return False


def main():
    global shutdown_requested

    print("=" * 65)
    print("🚀 NaMo Auto Like Reels Script")
    print("=" * 65)
    print(f"📌 API URL     : {API_URL}")
    print(f"📌 Post Range  : {START_POST_ID} → {END_POST_ID}")
    print(f"📌 Workers     : {CONCURRENT_WORKERS}")
    print(f"📌 Delay/Req   : {DELAY_PER_REQUEST}s")
    print(f"📌 Pause Every : {PAUSE_INTERVAL} requests for {PAUSE_DURATION}s")
    print(f"📌 Max Retries : {MAX_RETRIES} | Timeout: {REQUEST_TIMEOUT}s")
    print(f"📌 Proxy       : {'ON → ' + PROXY_URL if USE_PROXY else 'OFF'}")
    print("=" * 65)
    print()

    total_processed = 0
    successful = 0
    failed = 0
    start_time = time.time()

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
            futures = {}

            for post_id in range(START_POST_ID, END_POST_ID + 1):
                if shutdown_requested:
                    break

                # Submit task
                future = executor.submit(send_request_with_retry, post_id)
                futures[future] = post_id

                # Limit pending futures to prevent memory blowup
                if len(futures) >= CONCURRENT_WORKERS * 2:
                    done, _ = concurrent.futures.wait(
                        futures,
                        return_when=concurrent.futures.FIRST_COMPLETED,
                    )
                    for completed_future in done:
                        try:
                            if completed_future.result():
                                successful += 1
                            else:
                                failed += 1
                        except Exception:
                            failed += 1
                        del futures[completed_future]
                        total_processed += 1

                # Pause logic — every PAUSE_INTERVAL requests
                if total_processed > 0 and total_processed % PAUSE_INTERVAL == 0:
                    elapsed = time.time() - start_time
                    rate = total_processed / elapsed if elapsed > 0 else 0
                    print(
                        f"\n{'─' * 65}\n"
                        f"📊 Progress: {total_processed} processed "
                        f"({successful} ✅ | {failed} ❌) "
                        f"| Speed: {rate:.1f} req/s\n"
                        f"⏸️  Pausing for {PAUSE_DURATION}s...\n"
                        f"{'─' * 65}\n"
                    )
                    time.sleep(PAUSE_DURATION)

                # Small delay between submissions
                time.sleep(DELAY_PER_REQUEST)

            # Wait for remaining futures
            for future in concurrent.futures.as_completed(futures):
                if shutdown_requested:
                    break
                try:
                    if future.result():
                        successful += 1
                    else:
                        failed += 1
                except Exception:
                    failed += 1
                total_processed += 1

    except Exception as e:
        print(f"\n❌ Unexpected fatal error: {e}")

    elapsed = time.time() - start_time

    print()
    print("=" * 65)
    print("📊 FINAL SUMMARY")
    print("=" * 65)
    print(f"   Total Processed : {total_processed}")
    print(f"   Successful      : {successful} ✅")
    print(f"   Failed          : {failed} ❌")
    print(f"   Time Elapsed    : {elapsed:.1f}s")
    print(f"   Avg Speed       : {total_processed / elapsed:.1f} req/s" if elapsed > 0 else "")
    print("=" * 65)

    if shutdown_requested:
        print("🛑 Process was stopped by user/system signal.")


if __name__ == "__main__":
    main()
