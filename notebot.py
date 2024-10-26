#MadeBy Baaviz

import os
import time
from instagrapi import Client

# Instagram credentials
USERNAME = "Username_here"
PASSWORD = "Password_here"

# Islamic Remembrances
REMEMBRANCES = [
    "الحمد لله",  # Alhamdulillah
    "الله أكبر",  # Allahu Akbar
    "لا إله إلا الله",  # La ilaha illallah
    "أستغفر الله",  # Astaghfirullah
    "لا حول ولاقوة إلا بالله",  # La hawla wa la quwwata illa billah
    "اللهم صل وسلم على نبينا محمد",  # Allahumma salli wa sallim 'ala nabiyyina Muhammad
    "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار",  # Rabbana atina fidunya hasanatan wa fil akhirati hasanatan wa qina 'adhab an-nar
    "إنما المؤمنون إخوة",  # Innamal mu'minuna ikhwah
    "أعوذ بالله من الشيطان الرجيم",  # A'udhu billahi min ash-shaytan ir-rajim
    "سبحان الله وبحمده",  # Subhanallahi wa bihamdi
    "الحمد لله رب العالمين",  # Alhamdulillahi rabbil 'alamin
    "اللهم اغفر لي",  # Allahumma ighfir li
    "اللهم ارحمني",  # Allahumma irhamni
    "اللهم اهدني",  # Allahumma ihdini
    "اللهم انصرني",  # Allahumma ansurni
    "الحمد لله على كل حال",  # Alhamdulillah 'ala kulli hal
    "ربي زدني علمًا",  # Rabbi zidni 'ilma
    "اللهم اجعلني من المتقين",  # Allahumma aj'alni min al-muttaqin
    "اللهم اكتب لي الخير",  # Allahumma uktub li al-khayr
    "لا إله إلا أنت سبحانك إني كنت من الظالمين",  # La ilaha illa anta subhanaka inni kuntu min al-zalimin
    "إن الله مع الصابرين",  # Inna Allah ma'a as-sabirin
    "اللهم اجعلني من الصالحين",  # Allahumma aj'alni min as-salihin
    "اللهم ارزقني الرزق الحلال",  # Allahumma urzuqni al-rizq al-halal
    "اللهم اجعل لي من كل هم فرجًا",  # Allahumma aj'al li min kulli hamin farajan
    "الحمد لله الذي عافاني",  # Alhamdulillah alladhi 'afani
    "أستغفر الله ربي من كل ذنب",  # Astaghfirullah Rabbi min kulli dhamb
    "اللهم اجعلني ممن يستمعون القول فيتبعون أحسنه",  # Allahumma aj'alni min al-ladhina yastami'una al-qawl fa-yattabi'una ahsanahu
    "سبحان الله, ما أكرمك",  # SubhanAllah, ma akramak
    "اللهم اجعلني ممن يطلبون علمك",  # Allahumma aj'alni min al-ladhina yatlubuna 'ilmuka
    "اللهم ارحم والدي كما ربياني صغيرًا",  # Allahumma irham waliday kama rabbayani saghiran
    "يا الله، اجعلني من عبادك الصالحين",  # Ya Allah, aj'alni min 'ibadika as-salihin
    "اللهم اجعلني من الذين يحبون الخير للناس",  # Allahumma aj'alni min al-ladhina yuhibbuna al-khayr lil-nas
    "اللهم إني أعوذ بك من الفقر",  # Allahumma inni a'udhu bika min al-faqr
    "الحمد لله على كل النعم",  # Alhamdulillah 'ala kulli an-na'am
    "اللهم اجعلني ممن يتبعون الصراط المستقيم",  # Allahumma aj'alni mimman yattabi'una al-sirat al-mustaqim
    "يا الله، ارحم ضعفي",  # Ya Allah, irham da'fi
    "اللهم إني أسألك حسن الخاتمة",  # Allahumma inni as'aluka husn al-khatimah
    "أحبك يا رب",  # Uhibbuka ya Rabb
    "أستغفر الله، وأتوب إليه",  # Astaghfirullah, wa atubu ilayh
    "إن الله لا يغير ما بقوم حتى يغيروا ما بأنفسهم",  # Inna Allah la yughayiru ma bi-qawmin hatta yughayiru ma bi-anfusihim
    "يا الله، اجعلني من الذين يعبدونك حق عبادتك",  # Ya Allah, aj'alni min al-ladhina ya'budunak haqqa 'ibadatika
    "اللهم اجعلني من أوليائك",  # Allahumma aj'alni min awliya'ika
    "اللهم اجعلني من الذين يسيرون على صراطك المستقيم",  # Allahumma aj'alni min al-ladhina yasiruna 'ala siratika al-mustaqim
    "سبحان الله، ما أعظمك",  # SubhanAllah, ma a'zamuk
        "سبحان الله",  # Subhanallah

]

# Utility Functions

def generate_cookie(USERNAME, PASSWORD):
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings(f"{USERNAME}.json")

def send_remembrance(remembrance_text):
    cl = Client()
    cl.load_settings(f"{USERNAME}.json")
    cl.login(USERNAME, PASSWORD)
    print(f"Sending: {remembrance_text}")
    cl.create_note(remembrance_text, 0)
    return f"Posted: {remembrance_text}"

# Main Script

if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{USERNAME}.json")):
    print("Using existing cookies")
else:
    generate_cookie(USERNAME, PASSWORD)
    print("Cookies generated")

while True:
    for remembrance in REMEMBRANCES:
        print(send_remembrance(remembrance))
        time.sleep(600)  # Wait for 600 seconds (10 minutes) before sending the next remembrance
