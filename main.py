import asyncio
import aiohttp

URL = "https://api.narendramodi.in/apiv2"

stop_flag = False   # GLOBAL FLAG

HEADERS = {
    "Host": "api.narendramodi.in",
    "User-Agent": "Narendra Modi App/7.8 (iOS 18.5; iPhone Build/Narendra Modi App)",
    "Accept": "*/*",
    "Requestfrom": "ios",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",

    # keep your real cookie here
    "Cookie": "NSC_10.10.24.75_443=ffffffff0902060845525d5f4f58455e445a4a423660; _abck=E921128DDAE2823E0112175943B9E330~-1~YAAQtnBWuAj9vAWbAQAAtDnNIQ+1sSwvmMEurgeMPZlyFMhr8UC0fDqH15GcvNsg6fBv2PTQ/EmwoB7QerVhVJ8VNr4rJxGrPbvhlf46sFTdfmEkATnRfQSoqhoAWTcfgLjHw87AkrNk5yha4liZZVPPbdglM+g64E6Iw9wJeX+wRUFtMIW8EKelAOtgzekSaZRSjPOiqxqHTA31lv3ZDbRb7jeOph4HdAeyV+z5hwZa0n+qH7xMTU5D2tZEOp5AR3cYzJvaeyM/i0LTIQmqIgM8JkSmb/bfyIeZs2fIcxbrGlab6hRIzDuXFXYQb8f1JvFfo8atqyCVEZm/9lBenk9GpePBXkw0OIiRSLp+b6Hkh+fVmxX1HOwiQTiZYov5pI9aXiuYA3210zwtzSqTrkgrZalQ6rtwAUZtGVOPzHGL6sP/HzEjX/Ywo6lkPWSIDTe18d74sjUJeJ/orwNu2CpoPLCYv48IlG6VuZ8IWRJcUvd/GVb+TNmq09Sn4TigVFoI+bzN6spwj2k+siGa73u+TUITitILn+ddLtw2dY4juTjJYAYAdYWYfZeEDGIeiIL+Uok9wo6UeUJTaAC/H/fzeatlG809ciminb8a4uddXKFvoeF4Ww==~-1~-1~1765797788~AAQAAAAE%2f%2f%2f%2f%2fwOJKdRT3+WJ6Sk1Eh1WJWXAzeY6zEjhFBFlH5fSGdBZrSASyqIsQ71anGN5wnpdln0Wt6+wA4CVfT6BDYd5Z8DpKCYtwiT1Zuic~-1; ak_bmsc=48117DBC293D64BA93DE2D5F80969B84~000000000000000000000000000000~YAAQOUw5F1dCrAubAQAAkXDKIR70dvZHJN4DPPUVBlvLzoOdRwfb/fi6wVmOw4T1UUq4lsyqywk37FgagA0icBDKVkJ4q7Ry+PL1E8qAo9PmDfOeMz/hARcVvgsAx37qPJyIvgqWjInLuUCG9H0TH02namSfONgleBCYVgnJ4aKntZV4cFbPGGaObEPbZzYfQHVjMXo10obKsJo6Alm/+oqQsb/vyWTON7MfchYFHQrKWxPCO5hBZDu5WSt2/nAePbJLuq3+LQr0Le7QNTcBi9jNuJXlQbHuwLe43ahK9g5p5/+H5z/RXZ5BjxALMHgQ5rs4nP91pV+fYI/OR2s230RnD21vG8zt9i1dKosFsgrvoIXEO1+tukwlxEhT487bdq1vatOEPL9SxKfvIdHbkoCqI7dPbJIESpVWTdMY3n4=; _ga_VFNMV2T18E=GS2.1.s1765794488$o1$g0$t1765794490$j58$l0$h0; _ga=GA1.1.169979920.1756910999; bm_sv=54CC06178CFD142AED36CC862615900E~YAAQzKTUF5nX1QybAQAAxNGKIR450mdVhcBloot54LuTKXEQARF6dJx3zVrydN65Z/tXoNhdC3b9MPFDBb4qAiLP6ElKK1GWK2DORNYDhTBfHZpFyYUjPkX11dva/TjbXlspc2aMxQmLkWDw58BR36qoTJyQD5e3jD0cdFWfHrCKJC0sW3TkrRPp6D7UKZM15BTbHxm1EUgjLnx7HOb3y+PFUmMU9vFxY484D884/fo87jBwipfGAhpDmnliF1wYATsxgNA=~1; bm_sz=F4DB22EAC810C73E1D8143F42B298E23~YAAQzKTUF6TA1AybAQAAjQyJIR7uG+B1yWBl6PlcKeRocWAwPR618uI4GByYSonwGpUdlNn8BJ+dHAkxz5GqebUq8EAaG38ep9Vgq8Z+NuuRLKn67cNtT/SpEkZyy90VXchKo6L+PsB0jU9gWSyIZwDDmzBR2NL7saSva0VZ1KPkmCEudE3H2rQvnNnHHBtlfXaInfLuEKcXGXBa2QMd2T/w480kmNrKgLHd5WNkFb1BIiGiRsbvxrLCoEBHh8d2VM+m0mdyv+a/3Ow85l8e+rOQm8Kl/a7nlXaxHEz8x2Quo1ih6GxtC0DztvtbxiF9yNpzIJL+pgJCeh8MukzdiuLxmzNdfIhgbu7LBw0I/n/hZRB7ufKsewmZ7109gL4Pbat5Q1Xw5l93kHaPg1wAn36PbDFsqzGR0H3FuZXgddowujhniN8=~4405556~3225651; _ga_F433FYMYX9=GS2.1.s1758623618$o1$g1$t1758623620$j58$l0$h0; _fbp=fb.1.1758623618568.22689390473729608; _gcl_au=1.1.1263730701.1758623619; _ga_977P7XNV6X=GS2.2.s1758550394$o3$g0$t1758550394$j60$l0$h0; _ga_KY7X120D0N=GS2.1.s1756922043$o1$g0$t1756922043$j60$l0$h0; _ga_6XHS1RXTBF=GS2.1.s1756922026$o1$g1$t1756922034$j52$l0$h0; _ga_KE0FR5JBNB=GS2.1.s1756921934$o1$g0$t1756921934$j60$l0$h0; _ga_HQGP5S5CDY=GS2.1.s1756910998$o1$g0$t1756910999$j59$l0$h0"
}


# -----------------------------
# Build body (id = Bjp1, Bjp2…)
# -----------------------------
def build_body(i: int):
    return {
        "buzzsectionid": "5416",
        "id": f"Bj2457555ft66f5ppp{i}",                 # 🔥 AUTO INCREMENT
        "buzzid": "5415",
        "relation_type": "sharetweet",
        "share_platform": "Twitter",
        "action": "volunteersharecounts",
        "deviceid": "8455FFF3-8E05-4F50-8087-D71D37FB4F2C",
        "addressid": "5e6d8b312636f2a3be74d4ea6646602ccfc20c7b80840364649d32f4075006a0",
        "x-app-version": "7.8",
        "apiversion": "2",
        "navigationtag": "",

        # keep real token
        "X-Access-Token": "fa4d7d63ee643db59e1bc0d943b1be037a831955527ebe82d203e0c2f2df65fbbc31e94d778b9b5457851ecf1ffc33cfb3b50b4d73dd503e811329e2f1d25d83d96ddaaa4a1fadb40b133fe9d26b96954ffdaaec8d2ca2e7c7451a50f34b0795b77858fc24739d25a9d8d8a97ed7c7155f69ca9321288aeeebae48bd271b954002f619fc1f68df0b5561183deddf1d5f612a90296ba2ed4e73af9715afe865b8d3aca137f318cb0cf674684dbc006a03630beb52bb031168eedec4ae25d855b132e37ac198aa9672ab87192b4e4b83dd33b78fddc1e15d1f0a92a52003367d89d3eb5880465630cb6d1dc9178eea58f0"
    }


# -----------------------------
# Async request sender
# -----------------------------
async def send_request(session, i, retries=3):
    global stop_flag
    if stop_flag:
        return

    body = build_body(i)

    for attempt in range(retries):
        if stop_flag:
            return

        try:
            async with session.post(URL, headers=HEADERS, data=body, timeout=5) as resp:
                print(f"Sent id=Bjp{i} | Status={resp.status}")

                if resp.status == 403:
                    print("\n🔥 403 detected — STOPPING ALL TASKS\n")
                    stop_flag = True
                    return

                if resp.status == 200:
                    return

        except Exception as e:
            print(f"Error id=Bjp{i}: {e} | retry {attempt+1}")
            await asyncio.sleep(5)


# -----------------------------
# Main with concurrency control
# -----------------------------
async def main():
    global stop_flag

    concurrency = 4
    semaphore = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:

        async def sem_task(i):
            if stop_flag:
                return
            async with semaphore:
                await send_request(session, i)

        tasks = []

        for i in range(1, 500000000):   # 🔒 keep limit safe
            if stop_flag:
                break

            tasks.append(asyncio.create_task(sem_task(i)))

            if i % 50 == 0:
                await asyncio.sleep(5)

        await asyncio.gather(*tasks, return_exceptions=True)


asyncio.run(main())
