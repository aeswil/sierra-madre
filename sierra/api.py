from httpx import AsyncClient
from datetime import datetime


async def get_captcha(client: AsyncClient):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=utf-8',
        'language': 'pt',
        'device': 'Pc',
        'Origin': 'https://www.sssgame.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.sssgame.com/activity',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    timestamp = int(datetime.now().timestamp())

    return await client.get(f'https://www.sssgame.com/api/member/getCaptcha?type=login&timestamp={timestamp}',
                            headers=headers)


async def login(client: AsyncClient, username: str, password: str, captcha_key: str, captcha_code: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'language': 'pt',
        'device': 'Pc',
        'Origin': 'https://www.sssgame.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.sssgame.com/activity',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    data = {
        'username': username,
        'password': password,
        'verificationCode': captcha_key,
        'verifyCode': captcha_code,
        'Randstr': '',
        'Ticket': '',
        'timestamp': int(datetime.now().timestamp())

    }

    return await client.post('https://www.sssgame.com/api/member/login', headers=headers, json=data)


async def redeem(client: AsyncClient, token: str, code: str):
    cookies = {
        'language': '"pt"',
        'token': f'"{token}"'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': f'Bearer {token}',
        'language': 'pt',
        'device': 'Pc',
        'Origin': 'https://www.sssgame.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.sssgame.com/activity',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    timestamp = int(datetime.now().timestamp())

    data = {
        'preferentialActivityId': 47,
        'activityId': 247,
        'promoCode': code,
        'timestamp': timestamp,
    }

    return await client.post(
        'https://www.sssgame.com/api/preferential/preferentialActivity/apply',
        cookies=cookies,
        headers=headers,
        json=data,
    )
