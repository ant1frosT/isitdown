import argparse
import asyncio
import json

import aiohttp

parser = argparse.ArgumentParser('./check', description="Check domain status with https://www.isitdownrightnow.com/")
parser.add_argument('domains', nargs='*', type=str)
parser.add_argument('-f', '--file', type=str, required=False, help='File with domains: one domain on every row')
parser.add_argument('-j', '--json', type=str, required=False,
                    help='File contains json like: {"ip": "domain", "ip2": "domain2"}')
args = parser.parse_args()


PARALLEL_REQUESTS = 100
check_url_pattern = "https://www.isitdownrightnow.com/check.php?domain={}"
is_down_patter = 'is DOWN'


async def get_domains_from_file(path: str):
    with open(path, 'r') as f:
        content = f.read()
        result = content.splitlines()
        return result


async def get_domains_from_json_file(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
        return list(data.values())

processed = 0


async def gather_with_concurrency(conn, domains, n):
    semaphore = asyncio.Semaphore(n)
    session = aiohttp.ClientSession(connector=conn)

    async def get(url):
        async with semaphore:
            async with session.get(url, ssl=False) as response:
                response_text = await response.text()
                is_down = is_down_patter in response_text
                global processed
                processed += 1
                print("[{processed} of {total}]: {domain} is {status}".format(
                    processed=processed,
                    total=len(domains),
                    domain=url[len(check_url_pattern) - 2:],
                    status='DOWN' if is_down else 'UP'
                ))
    await asyncio.gather(*(get(check_url_pattern.format(domain)) for domain in domains))
    await session.close()


async def get_domains():
    domains = args.domains

    if args.file:
        domains += await get_domains_from_file(args.file)
    if args.json:
        domains += await get_domains_from_json_file(args.json)

    return list(set(domains))


async def main():
    domains = await get_domains()

    conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
    await gather_with_concurrency(conn, domains, PARALLEL_REQUESTS)
    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
