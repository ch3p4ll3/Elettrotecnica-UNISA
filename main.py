from scraper import Scraper
from db import Subscriptions
from pony.orm import db_session
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from os import getenv


load_dotenv()


api_id = getenv("API_ID")
api_hash = getenv("API_HASH")


if getenv("IS_DOCKER", False):
    app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=getenv("BOT_TOKEN"), workdir = "/app/config/")
else:
    app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=getenv("BOT_TOKEN"))

async def job():
    scraper = Scraper()
    new_elements = scraper.scrape()


    with db_session:
        if new_elements:
            for sub in Subscriptions.select():
                for i in new_elements:
                    await app.send_document(sub.telegram_id, i.url, caption=i.id)

@app.on_message(filters.command("start"))
async def on_start(client: Client, message: Message):
    await message.reply_text("""Benvenuto sul Bot Elettrotecnica UNISA! ⚡

Il tuo assistente per rimanere aggiornato sulle novità della bacheca degli esami di Elettrotecnica!

**Comandi:**

/start - Avvia il bot e mostra le informazioni generali.
/subscribe - Attiva gli aggiornamenti automatici sulle novità della bacheca.
/unsubscribe - Disattiva gli aggiornamenti automatici.
/help - Mostra questa guida ai comandi.

**Perché l'ho creato?**

Anche io ero stanco di controllare continuamente la bacheca!  Per questo ho creato questo bot, per aiutare tutti gli studenti di Elettrotecnica a rimanere aggiornati sugli esami in modo semplice e automatico.

**Come restare aggiornati sugli esami di Elettrotecnica?**

Il Bot Elettrotecnica UNISA funziona in modo semplice:

1. **Ogni 10 minuti**: il bot controlla [automaticamente](https://it.wikipedia.org/wiki/Web_scraping) la pagina web della [bacheca esami di Elettrotecnica](https://www.elettrotecnica.unisa.it/didattica/did_etbachecaesami).
2. **Aggiornamenti in tempo reale**: se trova nuovi aggiornamenti, il bot scarica il file PDF aggiornato.
3. **Notifiche immediate**: il bot invia automaticamente il nuovo file PDF a tutti gli utenti che hanno attivato la sottoscrizione.

Il codice sorgente del Bot Elettrotecnica UNISA è completamente open source e disponibile su [GitHub](https://github.com/ch3p4ll3/Elettrotecnica-UNISA).

**Stai riscontrando problemi con il Bot Elettrotecnica UNISA?**

Nessun problema! Puoi contattarmi [qui](https://t.me/ch3p4ll3) per aiutarti a risolvere qualsiasi inconveniente.
""")


@app.on_message(filters.command("help"))
async def on_help(client: Client, message: Message):
    await message.reply_text("""Benvenuto sul Bot Elettrotecnica UNISA! ⚡

Il tuo assistente per rimanere aggiornato sulle novità della bacheca degli esami di Elettrotecnica!

**Comandi:**

/start - Avvia il bot e mostra le informazioni generali.
/subscribe - Attiva gli aggiornamenti automatici sulle novità della bacheca.
/unsubscribe - Disattiva gli aggiornamenti automatici.
/help - Mostra questa guida ai comandi.

**Stai riscontrando problemi con il Bot Elettrotecnica UNISA?**

Nessun problema! Puoi contattarmi [qui](https://t.me/ch3p4ll3) per aiutarti a risolvere qualsiasi inconveniente.""")


@app.on_message(filters.command("subscribe"))
async def on_subscribe(client: Client, message: Message):
    with db_session:
        sub = Subscriptions.get(telegram_id=message.chat.id)

        if sub is None:
            sub = Subscriptions(telegram_id=message.chat.id)
            await message.reply_text("""**Sottoscrizione Attivata!**

Hai attivato con successo gli aggiornamenti automatici per la bacheca esami di Elettrotecnica!

Ora riceverai comodamente il file PDF con le novità direttamente sul tuo Telegram.""")
        else:
            await message.reply_text("""**Sottoscrizione Già Attiva!**

Non è necessario attivarla nuovamente.""")


@app.on_message(filters.command("unsubscribe"))
async def on_subscribe(client: Client, message: Message):
    with db_session:
        sub = Subscriptions.get(telegram_id=message.chat.id)

        if sub is not None:
            sub.delete()
            await message.reply_text("""**Disiscrizione Confermata!**

Hai disattivato con successo gli aggiornamenti automatici per la bacheca esami di Elettrotecnica.

Non riceverai più notifiche PDF.""")

        else:
            await message.reply_text("""**La tua sottoscrizione agli aggiornamenti è già disattivata.

Non riceverai più notifiche PDF con le novità della bacheca esami di Elettrotecnica.

Se in futuro desideri ricevere nuovamente gli aggiornamenti, potrai sempre riattivare la sottoscrizione in qualsiasi momento.""")


scheduler = AsyncIOScheduler()
scheduler.add_job(job, "interval", minutes=10)

scheduler.start()
app.run()
