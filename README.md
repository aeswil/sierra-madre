![Screenshot](screenshot.jpg)

---

Explicação do projeto:
sssɢᴀᴍᴇ em seu canal do telegram posta (ou postava) alguns códigos que poderiam ser resgatados por uma recompensa
este simples projeto, "escutava" o canal do telegram da sssɢᴀᴍᴇ, caso fosse detectado um código na mensagem, o projeto logava na conta e resgatava automaticamente.

**AVISO**
Fiz isso faz um tempo, não sei se eles ainda postam códigos, e entrei recentemente no site e vi que o esquema de captcha mudou, por isso este script não funciona mais.

exemplo de config.json:
```json
{
  "accounts": [
    "user:senha",
    "user:senha"
  ],
  "api_id": "telegram_api_id",
  "api_hash": "telegram_api_hash"
}
```

```sh
pip3 install -r requirements.txt
python3 run.py
```
