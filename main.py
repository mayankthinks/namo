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
    "Cookie": "_abck=E921128DDAE2823E0112175943B9E330~-1~YAAQVXIsMYA13rqaAQAAdAFlKA+eiEuD8CNiiquLMB8/Qxw81kILITC4TItZr46msvbGWp0dau7jua7G2e+MAl/+coU0BGmuF8CL/HT/gFLf0U768ShUjtRvnO1XFyR8/nq/r5Q6BGCr0nZZuAQ1fXHX+AqitrGCN5rgF3UmAauUNxP16LXl1ay1YxherGm1i9sGYLAlF+GWfOMdntS8dxUw/9mS19dU3lhLDui2VOlyo2mhW9RSoSnFZTClUCB9Iq/178b1N7WED3A4Ntdze9NYkX4LOZrO7EgLZRN6Z3pY4c+4obeErUaI32JjsbS3n5H++N2jXi8QZmeEqTcPKhVRbZn6upmrs3RjdNVpVnubcWCU5Kz5fTBfFw0ZfQIfmbF8+VN3D77srFHoevugR8tAPBl5RczxdQOjj5rwerkNIQDdGxM59LSBscx1fKv0HQw+/BTu9jBbXv/nuI/uXZjYteaw2aacqTp03J82X40z3BW730IHkgBadYSAD4j/3maf573jvM40QGPOH7NlilICiZrjVrvt9fg13xbSAc/6RxV3TsQTkwp5O5C+LsFtVcMomRGtzmNNy1n8pouoXviTSAy7YI/UDcH15AlC2G8Ux3J1PE26PthtzYv0E76GGMm56MOFK/m4EZWbv1RCy8Y3~0~-1~1765907225~AAQAAAAE%2f%2f%2f%2f%2f5bp4ZWQnbv2ZPXgy%2fFDn+4kSsKap+JKTi9cHOCzzByc7MmFK1nKIygjAfvjuXf32kuSwPDq4a0m2fhnKwScINwQrPrd5tW%2f7Ype8c5GYCJgMZgOex2Z9JV2Of6JqCQs+d%2fauAM%3d~-1; _ga_F433FYMYX9=GS2.1.s1765908971$o4$g1$t1765908973$j58$l0$h0; _ga_GXKBS9831X=GS2.1.s1765908971$o2$g0$t1765908973$j58$l0$h0; WZRK_S_4RR-W49-K84Z=%7B%22p%22%3A1%2C%22s%22%3A1765908971%2C%22t%22%3A1765908972%7D; _fbp=fb.1.1758623618568.22689390473729608; WZRK_G=0b186018b046466a9c8fabc3a6abc97e; _ga=GA1.1.169979920.1756910999; _gid=GA1.2.2102339053.1765889446; _ga_KY7X120D0N=GS2.1.s1765908967$o3$g0$t1765908967$j60$l0$h0; ak_bmsc=933E2012562B7A7FDB13064DE0C21A71~000000000000000000000000000000~YAAQ9sIRYESpVCWbAQAATf5cKB7oq8sIA+B5Lkud6Quegb0Aov+xF4y6Gi2nyahIbaa4tlHTEodYSOh0cvq6CDBHRXGRN7Y2tWKRJ5uRI0QdSWkp6JmPNAFZwZFMn8gHPW7fdzV7h00jHLQltEu3KOwClkizVAC/bVjswEgVSvKMDyhwYOEBoXg+nrq/Iwzsc5ZdVYVNbgTcUGJbsNZqk4m/iwGRpdE8feJ3LPSFw3EwEBB3itW7Is/seQRC/qozviLdAJfQ3TEYF9dPpXK5sNmugoyN/kNOzdrzVj74+lGuvD/To96g39GhMLrf2gkwRJol5mb/XjQrg98X3rT8/ogM/rffhVMw2DOPq/I26pIKXll9UfgoSmVIfy2a8cnhM49viudSBlPy9ZrA3upa6jq/lOGPsI8lKNtUEfupmB4=; bm_sv=9B62068A4D49F119890A9A7A903B4C91~YAAQVXIsMWfg27qaAQAANX0VKB4HAHxUSB7QcQFiLv9xsoEjPz7Ya5Qwk9z6i2s4DYKW6BVK/CuhXcvT/CJHo9dFKpfUum2Bl9zolcVrHEIUq4xJLRxj486NhSEqJ76ponJlAXeXofrh/TCxCwlrlDhoWf32R/6CO96MjbHIEQk5DWCGGPWLjIO7P1RozCa9kBvhekiuE7UeLK4vnOYNvLkzZQbiuFHrgvyAwFeyvPfDAOmSUgETT0yttKFo2T094u6YnuU=~1; _ga_6XHS1RXTBF=GS2.1.s1765903577$o2$g0$t1765903577$j60$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1765903414$o2$g0$t1765903414$j60$l0$h0; bm_sz=167FB28F1F866C5FA9735CC91914FF82~YAAQVXIsMcSc2bqaAQAAhaEFKB47cQp5HN1FbLbvK/xMaEhgGS8bT7NHH9lNc2mM6Kpx291J3ejkcF7MHlR+AvKv8lTpMveDG9Yioo2COloU5iGVid2FbErfZEMSgp/QCwIpjRsMJ0/m8AJ8vOL6F+7EgajbUiFe7kVxDcusvhIf3NvnziaUvFxIl76Srp1Br84pIoHspVVQSnW8TeR2xUr8HbRoFRSLUS0Ar9dFMUqhWvJx2dPO4HNHe0x05AE+bHoLvnlixkc82SCKqyc5VRaGUudiH0jKKwcBOx2yjRou0Zw1m88fJYFU9ErjHouG2NgtiC+kLfFqvuYaRO9nnoVr7I9T6QvFwUSQ5UPS3oO7oLOT77FwTBiLrWjobFc7YHuLzyGOqgtmX8L14UuBhiufIyCiqceazKQgkXokEnLSBRCQhg==~3289393~3686706; _ga_VFNMV2T18E=GS2.1.s1765902441$o2$g1$t1765902491$j10$l0$h0; _gcl_au=1.1.1263730701.1758623619; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0",
}

# =========================================================
# AUTO-INCREMENT DESCRIPTION
# =========================================================

def make_description(i: int) -> str:
    return f"हर घर स्वदेशी, घर घर स्वदेशी - आत्मनिर्भर भारत #101{i}"

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
        "22c38c89fee584e187569a6d8491cb9424ff834d6b8346c1554d0b9c87961dbc\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="title"\r\n\r\n\r\n'

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="action"\r\n\r\n'
        "createuserposttask\r\n"

        f"--{BOUNDARY}\r\n"
        'Content-Disposition: form-data; name="X-Access-Token"\r\n\r\n'
        "fa4d7d63ee643db59e1bc0d943b1be037a831955527ebe82d203e0c2f2df65fbbc31e94d778b9b5457851ecf1ffc33cfb3b50b4d73dd503e811329e2f1d25d83d96ddaaa4a1fadb40b133fe9d26b96954ffdaaec8d2ca2e7c7451a50f34b0795b77858fc24739d25a9d8d8a97ed7c7155f69ca9321288aeeebae48bd271b954002f619fc1f68df0b5561183deddf1d5f612a90296ba2ed4e73af9715afe865b8d3aca137f318cb0cf674684dbc006a03630beb52bb031168eedec4ae25d855b132e37ac198aa9672ab87192b4e4b83dd33b78fddc1e15d1f0a92a52003367d89d3eb5880465630cb6d1dc9178eea58f0\r\n"

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
                await asyncio.sleep(2)

        await asyncio.gather(*tasks, return_exceptions=True)

# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped by user")
