import requests
import time
import signal
import sys
import concurrent.futures
import socket
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Force IPv4 - Fix for AWS EC2 where IPv6 is unreachable
original_getaddrinfo = socket.getaddrinfo

def forced_ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = forced_ipv4_getaddrinfo

# --- Configuration ---
START_POST_ID = 150690
END_POST_ID = 100000000
CONCURRENT_WORKERS = 10
DELAY_PER_REQUEST = 0.1
PAUSE_INTERVAL = 100
PAUSE_DURATION = 2
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# Credentials
X_ACCESS_TOKEN = "4947cc41372a23e93cc7eea9eefc937dfe1088984dca182bf079b228f7c8ce573842323bd005a181e6b18cdfe0ebe90168b8c3525f60e2898fa7ddf3bf74e6dff5535f5ae7c9035db00f7e8e07559cf42d770ecdd9d80e6dd301e50966143063485ac90ad1de207bbdf4f755cf1de9c0b528685d14e11d9b9db007a4d4fa53498c2dca6e170d1f6020b77c7a8bbfbd17632259f03bef332747345987e5e5f0c47de77864330e52b316dcb38732c759e60a702b5120ba1d351d176f0001bfccf49c7a25dc00b4955f6dccf00136efffb39b8bd3414d01af305e73a1b7617868f0d018627e22fdb069fea62363e01c77da"
ADDRESS_ID = "4973ead8a91b974b2af3ce356ddd8134ebb496e4d070a26c58cd5e08e9040720"
DEVICE_ID = "b7e10055-66bb-2012-9e3c-d690e0f34f8c"
TOKEN = "pOMW+oq2p5Thkecatjd5bINTCYADHxix1cSpvaJLVpbie6j/S8C3f16o+7U5GU0g"

url = "https://api.narendramodi.in/apiv1"

headers_template = {
    "Host": "api.narendramodi.in",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-site",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "cors",
    "Origin": "https://www.narendramodi.in",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Referer": "https://www.narendramodi.in/",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty"
}

# Graceful shutdown flag
shutdown_requested = False

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global shutdown_requested
    print("\n⚠️  Shutdown requested. Completing current tasks...")
    shutdown_requested = True

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def send_request_with_retry(post_id):
    """Send request with retry logic and exponential backoff"""
    global shutdown_requested
    
    if shutdown_requested:
        return False
    
    for attempt in range(1, MAX_RETRIES + 1):
        if shutdown_requested:
            return False
            
        try:
            fields = {
                "image": "",
                "comment": "Jai Bjp",
                "type": "news-updates",
                "postid": str(post_id),
                "title": "",
                "subcomment": "No",
                "action": "postcomment",
                "X-Access-Token": X_ACCESS_TOKEN,
                "addressid": ADDRESS_ID,
                "deviceid": DEVICE_ID,
                "apiversion": "2",
                "version": "3",
                "token": TOKEN,
                "request_source": "pwa",
                "lang": "en",
                "platform": "iOS"
            }

            m = MultipartEncoder(fields=fields)
            current_headers = headers_template.copy()
            current_headers["Content-Type"] = m.content_type

            response = requests.post(
                url, 
                data=m, 
                headers=current_headers, 
                timeout=REQUEST_TIMEOUT
            )
            
            # Validate response
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    status = json_response.get("status", "unknown")
                    message = json_response.get("message", "")
                    print(f"✅ PostID: {post_id} | Status: {response.status_code} | Response: {status} - {message}")
                except:
                    print(f"✅ PostID: {post_id} | Status: {response.status_code}")
                return True
                
            elif response.status_code == 429:
                # Rate limited - wait longer before retry
                wait_time = (2 ** attempt) * 2
                print(f"⏳ PostID: {post_id} | Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                continue
                
            elif response.status_code >= 500:
                # Server error - retry with backoff
                wait_time = 2 ** attempt
                print(f"🔄 PostID: {post_id} | Server error {response.status_code}. Retry {attempt}/{MAX_RETRIES} in {wait_time}s...")
                time.sleep(wait_time)
                continue
                
            else:
                print(f"❌ PostID: {post_id} | Failed with status: {response.status_code}")
                return False
            
        except requests.exceptions.Timeout:
            wait_time = 2 ** attempt
            print(f"⏱️  PostID: {post_id} | Timeout. Retry {attempt}/{MAX_RETRIES} in {wait_time}s...")
            time.sleep(wait_time)
            
        except requests.exceptions.ConnectionError as e:
            wait_time = 2 ** attempt
            print(f"🔌 PostID: {post_id} | Connection error. Retry {attempt}/{MAX_RETRIES} in {wait_time}s...")
            time.sleep(wait_time)
            
        except Exception as e:
            print(f"❌ PostID: {post_id} | Error: {e}")
            return False
    
    print(f"❌ PostID: {post_id} | Failed after {MAX_RETRIES} retries")
    return False

def main():
    global shutdown_requested
    
    print(f"🚀 Starting process from {START_POST_ID} to {END_POST_ID}...")
    print(f"📊 Config: {CONCURRENT_WORKERS} workers, {DELAY_PER_REQUEST}s delay, pause every {PAUSE_INTERVAL} requests")
    print(f"🔄 Max retries: {MAX_RETRIES}, Timeout: {REQUEST_TIMEOUT}s")
    print("-" * 60)
    
    total_processed = 0
    successful = 0
    failed = 0
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
            futures = {}
            
            for post_id in range(START_POST_ID, END_POST_ID + 1):
                if shutdown_requested:
                    break
                
                # Submit task
                future = executor.submit(send_request_with_retry, post_id)
                futures[future] = post_id
                
                # Limit pending futures to prevent memory issues
                if len(futures) >= CONCURRENT_WORKERS * 2:
                    # Wait for at least one to complete
                    done, _ = concurrent.futures.wait(
                        futures, 
                        return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    for completed_future in done:
                        try:
                            if completed_future.result():
                                successful += 1
                            else:
                                failed += 1
                        except Exception as e:
                            failed += 1
                        del futures[completed_future]
                        total_processed += 1
                
                # Pause Logic
                if total_processed > 0 and total_processed % PAUSE_INTERVAL == 0:
                    print(f"\n--- 📊 Progress: {total_processed} processed ({successful} ✅, {failed} ❌). Pausing for {PAUSE_DURATION}s... ---\n")
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
                except Exception as e:
                    failed += 1
                total_processed += 1
                
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Final Summary:")
    print(f"   Total Processed: {total_processed}")
    print(f"   Successful: {successful} ✅")
    print(f"   Failed: {failed} ❌")
    print("=" * 60)
    
    if shutdown_requested:
        print("🛑 Process was stopped by user.")

if __name__ == "__main__":
    main()
