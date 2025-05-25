import discord
from discord.ext import commands
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from datetime import datetime, timedelta
import random
import os
import pytz

token = os.environ['TOKENBOTDISCORD']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def creer_recu_pdf(date_heure):
    valid_until = date_heure + timedelta(hours=1)
    num_ticket = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    nom_fichier = f"recu_{date_heure.strftime('%Y-%m-%d-%H-%M-%S')}.pdf"

    c = canvas.Canvas(nom_fichier, pagesize=A4)
    width, height = A4

    # ← Utilise directement le fichier PNG local ici
    logo_image = ImageReader("logo.pnj.png")
    c.drawImage(logo_image, 25 * mm, height - 55 * mm, width=35 * mm, preserveAspectRatio=True, mask='auto')

    # Texte à droite du logo
    c.setFont("Helvetica", 11)
    text = c.beginText(65 * mm, height - 30 * mm)
    text.textLine("SOLEA Saeml")
    text.textLine("CA Mulhouse Alsace Aglomération")
    text.textLine("97 rue de la Mertzau")
    text.textLine("68100 MULHOUSE")
    text.textLine("Recettes encaissées par Soléa au")
    text.textLine("nom et pour le compte de CA m2A")
    c.drawText(text)

    # Détails d'achat
    text = c.beginText(25 * mm, height - 90 * mm)
    text.setFont("Helvetica-Bold", 11)
    text.textLine("Reçu d'achat - PAIEMENT PAR SMS")
    text.setFont("Helvetica", 10)
    text.textLine(f"Le {date_heure.strftime('%d/%m/%Y à %H:%M:%S')}")
    text.textLine(f"N° Ticket = {num_ticket}")
    text.textLine(f"Valable du {date_heure.strftime('%d/%m/%Y %H:%M:%S')} au")
    text.textLine(f"{valid_until.strftime('%d/%m/%Y %H:%M:%S')}")

    # Informations tarifaires à droite
    text2 = c.beginText(110 * mm, height - 90 * mm)
    text2.setFont("Helvetica-Bold", 11)
    text2.textLine("JUSTIFICATIF A CONSERVER")
    text2.setFont("Helvetica", 10)
    text2.textLine("1 voyage")
    text2.textLine("Montant HT : 1.45 €")
    text2.textLine("TVA (10%) : 0.15 €")
    text2.textLine("Montant TTC : 1.60 €")

    # Pied de page
    text3 = c.beginText(25 * mm, height - 150 * mm)
    text3.setFont("Helvetica", 10)
    text3.textLine("Non remboursable")
    text3.textLine("")
    text3.textLine("Conditions générales sur www.solea.info ou envoyez AIDE au 93068 (SMS non surtaxé)")

    c.drawText(text)
    c.drawText(text2)
    c.drawText(text3)
    c.showPage()
    c.save()

    return nom_fichier

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.strip().upper() == "SOLÉA**":
        maintenant = datetime.now(pytz.timezone('Europe/Paris'))
        fichier_pdf = creer_recu_pdf(maintenant)
        await message.channel.send("Voici votre reçu PDF :", file=discord.File(fichier_pdf))


bot.run(token)

