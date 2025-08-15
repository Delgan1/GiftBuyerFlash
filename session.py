from pyrogram import Client


# Если данные значения не работают, то вы можете сами создать API отсюда https://my.telegram.org/auth
api_id = 28405970
api_hash = "078481a5bf79e1deb7cca2bc63792164"

# Имя аккаунта для входа, оно сохранится в .session файле, и вы его можете прописать в config.py
name_session = input("Введите имя сессии: ")

app = Client(
    name_session,
    api_id=api_id,
    api_hash=api_hash,
    device_model="iPhone 14 Pro",
    system_version="iOS 17.5.1",
    app_version="10.14.1 (30141)",
    lang_pack="ios",
    lang_code="en",
    sleep_threshold=30,
    skip_updates=False
)

with app:
    print("Session Created")