#MadeBy Baaviz

import os
import time
import random
import logging
from datetime import datetime
from instagrapi import Client
from typing import List
from PIL import Image
import requests
from io import BytesIO
import glob

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('notebot.log'),
        logging.StreamHandler()
    ]
)

# Instagram credentials
USERNAME = "#" 
PASSWORD = "#"

# Configuration
CONFIG = {
    'min_interval': 300,  # Minimum 5 minutes between posts
    'max_interval': 900,  # Maximum 15 minutes between posts
    'photo_interval': 10, # 10 seconds between photo posts
    'retry_delay': 60,    # Delay between retries on error
    'max_retries': 3,     # Maximum number of retries per post
    'photos_directory': 'islamic_photos'  # Directory containing Islamic photos
}

# Islamic Remembrances
REMEMBRANCES = [
        # Quranic Verses (Ayat)
            "وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ ۚ عَلَيْهِ تَوَكَّلْتُ وَإِلَيْهِ أُنِيبُ",  # Hud 11:88

    "قُلْ هُوَ اللَّهُ أَحَدٌ ﴿١﴾ اللَّهُ الصَّمَدُ ﴿٢﴾ لَمْ يَلِدْ وَلَمْ يُولَدْ ﴿٣﴾ وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ ﴿٤﴾",  # Surat Al-Ikhlas
    "وَإِلَٰهُكُمْ إِلَٰهٌ وَاحِدٌ ۖ لَّا إِلَٰهَ إِلَّا هُوَ الرَّحْمَٰنُ الرَّحِيمُ",  # Al-Baqarah 2:163
    "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ",  # Ayat Al-Kursi (part)
    "إِنَّ مَعَ الْعُسْرِ يُسْرًا",  # Ash-Sharh 94:6
    "وَقُل رَّبِّ زِدْنِي عِلْمًا",  # Taha 20:114
    "فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي وَلَا تَكْفُرُونِ",  # Al-Baqarah 2:152
    "وَإِذَا سَأَلَكَ عِبَادِي عَنِّي فَإِنِّي قَرِيبٌ",  # Al-Baqarah 2:186
    "رَبَّنَا لَا تُؤَاخِذْنَا إِن نَّسِينَا أَوْ أَخْطَأْنَا",  # Al-Baqarah 2:286
    "حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ",  # Al-Imran 3:173
    # Original remembrances
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
    "اللهم ارحمهما كما ربياني صغيرًا",  # Allahumma irham waliday kama rabbayani saghiran
    "يا الله، اجعلني من عبادك الصالحين",  # Ya Allah, aj'alni min 'ibadika as-salihin
    "اللهم اجعلني من الذين يحبون الخير للناس",  # Allahumma aj'alni min al-ladhina yuhibbuna al-khayr lil-nas
    "اللهم إني أعوذ بك من الفقر",  # Allahumma inni a'udhu bika min al-faqr
    "الحمد لله على كل النعم",  # Alhamdulillah 'ala kulli an-na'am
    "اللهم اجعلني ممن يتبعون الصراط المستقيم",  # Allahumma aj'alni mimman yattabi'una al-sirat al-mustaqim
    "يا الله، ارحم ضعفي",  # Ya Allah, irham da'fi
    "اللهم إني أسألك حسن الخاتمة",  # Allahumma inni as'aluka husn al-khatimah
    "أستغفر الله، وأتوب إليه",  # Astaghfirullah, wa atubu ilayh
    "إن الله لا يغير ما بقوم حتى يغيروا ما بأنفسهم",  # Inna Allah la yughayiru ma bi-qawmin hatta yughayiru ma bi-anfusihim
    "يا الله، اجعلني من الذين يعبدونك حق عبادتك",  # Ya Allah, aj'alni min al-ladhina ya'budunak haqqa 'ibadatika
    "اللهم اجعلني من أوليائك",  # Allahumma aj'alni min awliya'ika
    "اللهم اجعلني من الذين يسيرون على صراطك المستقيم",  # Allahumma aj'alni min al-ladhina yasiruna 'ala siratika al-mustaqim
    "سبحان الله، ما أعظمك",  # SubhanAllah, ma a'zamuk
    "سبحان الله",  # Subhanallah
    "بسم الله الرحمن الرحيم",  # Bismillah ir-Rahman ir-Raheem
    "اللهم اني أسألك الجنة",  # Allahumma inni as'aluka al-jannah
    "رب اشرح لي صدري",  # Rabbi ishrah li sadri
    "حسبي الله ونعم الوكيل",  # Hasbunallahu wa ni'mal wakeel
    "اللهم إني أسألك العفو والعافية",  # Allahumma inni as'alukal 'afwa wal 'afiyah
    "رب اغفر وارحم وأنت خير الراحمين",  # Rabbighfir warham wa anta khair ur-rahimeen
    "اللهم أعني على ذكرك وشكرك وحسن عبادتك",  # Allahumma a'inni 'ala dhikrika wa shukrika wa husni 'ibadatik
    "سبحان الله والحمد لله ولا إله إلا الله والله أكبر",  # Subhanallah wal hamdulillah wa la ilaha illallah wallahu akbar
    "اللهم صل على محمد وعلى آل محمد",  # Allahumma salli 'ala Muhammad wa 'ala aali Muhammad


]

# Utility Functions
def generate_cookie(username: str, password: str) -> None:
    """Generate and save Instagram session cookies."""
    try:
        cl = Client()
        cl.login(username, password)
        cl.dump_settings(f"{username}.json")
        logging.info("Successfully generated new cookies")
    except Exception as e:
        logging.error(f"Failed to generate cookies: {str(e)}")
        raise

def get_random_remembrance(remembrances: List[str]) -> str:
    """Select a random remembrance with timestamp."""
    remembrance = random.choice(remembrances)
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"{remembrance}\n\n⏰ Posted at: {current_time}"

def send_remembrance(remembrance_text: str, retries: int = 0) -> bool:
    """Send a remembrance to Instagram with error handling and retries."""
    try:
        cl = Client()
        cl.load_settings(f"{USERNAME}.json")
        cl.login(USERNAME, PASSWORD)
        
        logging.info(f"Sending: {remembrance_text}")
        cl.create_note(remembrance_text, 0)
        logging.info(f"Successfully posted remembrance")
        return True
        
    except Exception as e:
        logging.error(f"Error posting remembrance: {str(e)}")
        if retries < CONFIG['max_retries']:
            logging.info(f"Retrying in {CONFIG['retry_delay']} seconds... (Attempt {retries + 1}/{CONFIG['max_retries']})")
            time.sleep(CONFIG['retry_delay'])
            return send_remembrance(remembrance_text, retries + 1)
        return False

def get_post_statistics() -> dict:
    """Track posting statistics."""
    return {
        'total_posts': 0,
        'successful_posts': 0,
        'failed_posts': 0,
        'start_time': datetime.now()
    }

def get_random_photo() -> str:
    """Get a random photo from the photos directory."""
    photos = glob.glob(f"{CONFIG['photos_directory']}/*.[jJ][pP][gG]") + \
             glob.glob(f"{CONFIG['photos_directory']}/*.[pP][nN][gG]")
    if not photos:
        raise FileNotFoundError("No photos found in photos directory")
    return random.choice(photos)

def post_photo(photo_path: str, caption: str = "", retries: int = 0) -> bool:
    """Post a photo to Instagram with error handling and retries."""
    try:
        cl = Client()
        cl.load_settings(f"{USERNAME}.json")
        cl.login(USERNAME, PASSWORD)
        
        logging.info(f"Posting photo: {photo_path}")
        cl.photo_upload(photo_path, caption)
        logging.info("Successfully posted photo")
        return True
        
    except Exception as e:
        logging.error(f"Error posting photo: {str(e)}")
        if retries < CONFIG['max_retries']:
            logging.info(f"Retrying in {CONFIG['retry_delay']} seconds... (Attempt {retries + 1}/{CONFIG['max_retries']})")
            time.sleep(CONFIG['retry_delay'])
            return post_photo(photo_path, caption, retries + 1)
        return False

# Main Script
def main():
    # Initialize statistics
    stats = {
        'total_posts': 0,
        'successful_posts': 0,
        'failed_posts': 0,
        'total_photos': 0,
        'successful_photos': 0,
        'failed_photos': 0,
        'start_time': datetime.now()
    }
    
    # Create photos directory if it doesn't exist
    os.makedirs(CONFIG['photos_directory'], exist_ok=True)
    
    # Check/generate cookies
    cookie_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{USERNAME}.json")
    if os.path.exists(cookie_path):
        logging.info("Using existing cookies")
    else:
        generate_cookie(USERNAME, PASSWORD)
        logging.info("New cookies generated")

    logging.info("Starting NoteBot...")
    
    last_photo_time = 0
    
    while True:
        try:
            current_time = time.time()
            
            # Check if it's time to post a photo
            if current_time - last_photo_time >= CONFIG['photo_interval']:
                try:
                    photo_path = get_random_photo()
                    caption = random.choice(REMEMBRANCES)  # Use a random remembrance as caption
                    
                    stats['total_photos'] += 1
                    if post_photo(photo_path, caption):
                        stats['successful_photos'] += 1
                    else:
                        stats['failed_photos'] += 1
                    
                    last_photo_time = current_time
                except FileNotFoundError as e:
                    logging.warning(f"Photo posting skipped: {str(e)}")
            
            # Regular remembrance posting
            remembrance = get_random_remembrance(REMEMBRANCES)
            stats['total_posts'] += 1
            
            if send_remembrance(remembrance):
                stats['successful_posts'] += 1
            else:
                stats['failed_posts'] += 1
            
            # Log statistics
            logging.info(
                f"Statistics:\n"
                f"Text Posts: Total={stats['total_posts']}, Success={stats['successful_posts']}, Failed={stats['failed_posts']}\n"
                f"Photo Posts: Total={stats['total_photos']}, Success={stats['successful_photos']}, Failed={stats['failed_photos']}"
            )
            
            # Random interval between posts
            interval = random.randint(CONFIG['min_interval'], CONFIG['max_interval'])
            logging.info(f"Waiting {interval} seconds until next post...")
            time.sleep(interval)
            
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            time.sleep(CONFIG['retry_delay'])

if __name__ == "__main__":
    main()
