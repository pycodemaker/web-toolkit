import requests
import optparse
import httpx
import asyncio

subdomains: list = []
paths: list = []

def get_args() -> optparse.Values:
    """"
    :return: options provided by the user.
    """

    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest='url', help='set the target url')
    (options, arguments) = parser.parse_args()
    if not options.url:
        parser.error('[-] Please specify a destination url, use --help for more info.')
    return options

async def request(url: str) -> int:
    """
    :return: status code of the requested url
    """
    try:
        async with httpx.AsyncClient() as client:
            return await client.get(f'http://{url}')
    except Exception:
        pass

def export_csv(filename, items):
    with open(f'result/{filename}.txt', 'w') as f:
        for items in items:
            f.writelines(items+'\n')
    
async def main():
    options = get_args()

    with open('subdomain.txt') as wordlist:
        for subdomain in wordlist:
            test_url = subdomain.strip() + '.' + options.url
            resp = await request(test_url)
            try:
                if resp.status_code == 200:
                    found = f'[+] Discovered subdomain --> {test_url}'
                    print(found)
                    subdomains.append(test_url)
            except:
                pass 
    
    if len(subdomains) != 0:
        print(f'{"-"*15} Phase 2 {"-"*15}')
        with open('web-common.txt') as dirs:
            for subdomain in subdomains:
                for dir in dirs:
                    test_url = f'http://{subdomain}/{dir}'.strip()
                    if test_url[0] == '/':
                        test_url = test_url[1:]
                    resp = await request(test_url)
                    try:
                        if resp.status_code == 200:
                            found = f'[+] Discovered path --> {test_url}'
                            print(found)
                            paths.append(test_url)
                    except:
                        pass

    export_csv(f'{options.url}.paths', paths)
    export_csv(f'{options.url}.subdomains', subdomains)

    
if __name__ == '__main__':
    asyncio.run(main())