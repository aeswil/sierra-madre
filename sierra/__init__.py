import json
from dataclasses import dataclass
from re import compile
from time import sleep as sleep_sync

from httpx import AsyncClient
from pyrogram.client import Client
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import Message
from rich.console import Console
from rich.status import Status

from . import api
from . import captcha

logo = """


███████ ██ ███████ ██████  ██████   █████      ███    ███  █████  ██████  ██████  ███████ 
██      ██ ██      ██   ██ ██   ██ ██   ██     ████  ████ ██   ██ ██   ██ ██   ██ ██      
███████ ██ █████   ██████  ██████  ███████     ██ ████ ██ ███████ ██   ██ ██████  █████   
     ██ ██ ██      ██   ██ ██   ██ ██   ██     ██  ██  ██ ██   ██ ██   ██ ██   ██ ██      
███████ ██ ███████ ██   ██ ██   ██ ██   ██     ██      ██ ██   ██ ██████  ██   ██ ███████ 
                                                                                          
                                                                                          
"""


# -------------------------------------

@dataclass()
class Config:
    accounts: list[tuple[str, str]]
    api_id: str | None
    api_hash: str | None


def load_config(fp: str) -> Config | None:
    try:
        keys = ['accounts', 'api_id', 'api_hash']
        with open(fp) as f:
            config = json.load(f)

        key_not_in_config = [key for key in keys if key not in config]
        if key_not_in_config:
            console.log(
                f'Erro no arquivo de configuração, as configurações: {", ".join(key_not_in_config)} não foram '
                f'encontradas.',
                style='red')
            return

        value_in_config_is_invalid = [key for key in keys if config.get(key) in [None, '', [], ' '] + keys]
        if value_in_config_is_invalid:
            console.log(
                f'Erro no arquivo de configuração, os valores das configurações:'
                f' {", ".join(value_in_config_is_invalid)} são inválidos.',
                style='red')
            return

        config['accounts'] = [account.split(':') for account in config['accounts']]

        return Config(config['accounts'], config['api_id'], config['api_hash'])

    except FileNotFoundError:
        console.log('Erro ao carregar o arquivo de configuração, o arquivo não foi encontrado.', style='red')

    except Exception:
        console.log('Erro ao carregar o arquivo de configuração por razões desconhecidas.', style='red')
        console.print_exception()


REGEX = compile(r'SSSGAME[\w\d]+')
CFG: Config | None

console = Console()
status: Status = Status(status='')
console.clear()


async def auto_redeem(httpx: AsyncClient, username: str, password: str, code: str) -> bool:
    # captcha solver
    res = await api.get_captcha(httpx)
    rjson = res.json().get('data')
    key, image = rjson['key'], rjson['codeUrl']
    result = captcha.solve_from_base64(image)

    res = await api.login(httpx, username, password, key, result)
    rjson = res.json()

    if 'token' in res.text:
        token = rjson['data']['token']
        console.log(f'Login com sucesso com a conta: {username}', style='green')
        rres = await api.redeem(httpx, token, code)
        if 'sucedida' in rres.text:
            console.log(f'O código {code} foi aplicado na conta: {username} com sucesso.', style='green')
            return True
        else:
            console.log(f'Tentativa de aplicar o código {code} em sua conta: {username} não foi possível.', style='red')
            console.print_json(rres.text)
            return True
    elif 'Usuário ou senha incorretos' in res.text:
        console.log(f'Tentativa de login falha, usuário ou senha errada: {username}', style='red')
        return True
    elif 'captcha' in res.text:
        console.log(f'Tentativa de login falha: {username}, captcha errado, iremos tentar denovo.', style='yellow')
    else:
        console.log('Tentativa de login falha, por razões desconhecidas:', style='red')
        console.print_json(res.text)


def defer_status(f):
    async def wrapper(client, message):
        r = await f(client, message)
        status.update('Analisando novas mensagens...')
        return r

    return wrapper


@defer_status
async def handler(_, message: Message):
    global status
    status.update('Analisando mensagem recebida...')
    content = message.text or message.caption
    if not content:
        return

    matchs = REGEX.findall(content)
    if not matchs:
        return

    try:
        matchs.remove('SSSGAMEBRASIL')
    except ValueError:
        pass

    if len(matchs) < 1:
        return

    console.log(f'Foi encontrado x{len(matchs)} código(s): {", ".join(matchs)}')
    code = matchs.pop()

    for account in CFG.accounts:
        user, password = account
        status.update(f'Tentando aplicar código {code} em sua conta: {user}')
        async with AsyncClient(timeout=30) as httpx:
            for _ in range(3):
                ok = await auto_redeem(httpx, user, password, code)
                if ok is not None:
                    break


async def run(config: str = 'config.json'):
    global CFG
    global status

    console.print(logo.strip() + '\n', style='bold #ffd700')

    with console.status("[bold yellow] carregando e validando configurações...") as status:
        sleep_sync(1)

        CFG = load_config(config)
        if CFG is None:
            return

        status.update('Conectando ao telegram')
        async with Client('session', api_id=CFG.api_id, api_hash=CFG.api_hash) as client:
            console.log(f'Bem-vindo {client.me.username or client.me.first_name or client.me.id}')
            status.update('Analisando novas mensagens...')
            client.add_handler(MessageHandler(handler))
            console.log('Sniper iniciado, agora é só aguardar por novos códigos :)')
            await idle()
            status.update('Se desconectando do telegram.')
            console.log('Bye bye')
