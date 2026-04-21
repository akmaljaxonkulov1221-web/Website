#!/usr/bin/env python3
"""
Professional Lex.uz Scraper - Barcha kodekslarni avtomatik sken qilish
AI-powered scraping system for all Uzbek legal codes
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Logging sozlamalari
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LexUzProfessionalScraper:
    """Professional Lex.uz scraper for all legal codes"""
    
    def __init__(self):
        self.base_url = "https://lex.uz"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'uz-UZ,uz;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Kodekslar manzillari
        self.legal_codes = {
            "Jinoyat kodeksi": "https://lex.uz/docs/111453",
            "Fuqarolik kodeksi": "https://lex.uz/docs/111189", 
            "Mehnat kodeksi": "https://lex.uz/docs/6257288",
            "Oila kodeksi": "https://lex.uz/docs/104720",
            "Ma'muriy javobgarlik kodeksi": "https://lex.uz/docs/97664",
            "Yer kodeksi": "https://lex.uz/docs/149947"
        }
        
        self.scraped_data = []
    
    def get_page_content(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Sahifa mazmunini olish"""
        for attempt in range(retries):
            try:
                logger.info(f"Fetching page: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                response.encoding = 'utf-8'
                
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
                
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
    
    def extract_articles_from_page(self, soup: BeautifulSoup, code_name: str) -> List[Dict]:
        """Sahifadan moddalarni ajratib olish"""
        articles = []
        
        # Moddalarni topish uchun turli patternlar
        article_patterns = [
            # Standart modda formati
            soup.find_all('div', class_='doc-text'),
            soup.find_all('p'),
            soup.find_all('div', class_='document-text'),
            soup.find_all('article'),
            soup.find_all('section'),
        ]
        
        all_text_content = []
        
        # Barcha matnli elementlarni yig'ish
        for pattern in article_patterns:
            for element in pattern:
                text = element.get_text(strip=True)
                if text and len(text) > 50:  # Qisqa matnlarni tashlab yuborish
                    all_text_content.append(text)
        
        # Moddalarni ajratib olish
        current_article = None
        current_number = None
        current_title = None
        current_content = []
        
        for text in all_text_content:
            # Modda raqamini topish
            article_match = re.search(r'(\d+)-modda', text, re.IGNORECASE)
            if article_match:
                # Avvalgi moddani saqlash
                if current_article:
                    articles.append(current_article)
                
                # Yangi modda boshlanishi
                article_number = article_match.group(1)
                
                # Modda sarlavhasini topish
                title_match = re.search(r'(\d+-modda)\s*(.+?)(?=\.|\n|$)', text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(2).strip()
                else:
                    # Sarlavhani keyin qatoridan topish
                    lines = text.split('\n')
                    title = lines[1].strip() if len(lines) > 1 else f"Modda {article_number}"
                
                current_article = {
                    "kodeks": code_name,
                    "modda": article_number,
                    "nomi": title,
                    "matn": text,
                    "tahlil": self._analyze_article(text, code_name)
                }
                
                logger.info(f"Found article: {article_number}-modda - {title}")
                
            elif current_article:
                # Hozirgi modda matnini to'ldirish
                current_article["matn"] += "\n" + text
        
        # Oxirgi moddani saqlash
        if current_article:
            articles.append(current_article)
        
        return articles
    
    def _analyze_article(self, text: str, code_name: str) -> Dict:
        """Modda matnini AI tahlili"""
        analysis = {}
        
        # Kodeksga qarab tahlil
        if "Jinoyat kodeksi" in code_name:
            analysis = self._analyze_criminal_article(text)
        elif "Fuqarolik kodeksi" in code_name:
            analysis = self._analyze_civil_article(text)
        elif "Mehnat kodeksi" in code_name:
            analysis = self._analyze_labor_article(text)
        elif "Oila kodeksi" in code_name:
            analysis = self._analyze_family_article(text)
        elif "Ma'muriy javobgarlik kodeksi" in code_name:
            analysis = self._analyze_administrative_article(text)
        elif "Yer kodeksi" in code_name:
            analysis = self._analyze_land_article(text)
        
        return analysis
    
    def _analyze_criminal_article(self, text: str) -> Dict:
        """Jinoyat kodeksi moddasini tahlil qilish"""
        analysis = {
            "obekt": self._extract_object(text),
            "subekt": "16 yoshga to'lgan, aqli raso shaxs",
            "sanksiya": self._extract_sanction(text),
            "jinoyat_turi": self._determine_crime_type(text),
            "og'irlik_darajasi": self._determine_severity(text)
        }
        return analysis
    
    def _analyze_civil_article(self, text: str) -> Dict:
        """Fuqarolik kodeksi moddasini tahlil qilish"""
        analysis = {
            "mavzu": self._extract_subject(text),
            "tomonlar": self._extract_parties(text),
            "huquq_majburiyatlari": self._extract_rights(text),
            "shartnoma_turi": self._determine_contract_type(text)
        }
        return analysis
    
    def _analyze_labor_article(self, text: str) -> Dict:
        """Mehnat kodeksi moddasini tahlil qilish"""
        analysis = {
            "mehnat_munosabatlari": self._extract_labor_relations(text),
            "tomonlar": "Ish beruvchi va xodim",
            "ish_haqi": self._extract_salary_info(text),
            "ish_vaqti": self._extract_working_hours(text)
        }
        return analysis
    
    def _analyze_family_article(self, text: str) -> Dict:
        """Oila kodeksi moddasini tahlil qilish"""
        analysis = {
            "oilaviy_munosabatlar": self._extract_family_relations(text),
            "nikoh_shartlari": self._extract_marriage_conditions(text),
            "ajralish_tartibi": self._extract_divorce_procedure(text),
            "aliment_mas'alalari": self._extract_alimony_issues(text)
        }
        return analysis
    
    def _analyze_administrative_article(self, text: str) -> Dict:
        """Ma'muriy javobgarlik kodeksi moddasini tahlil qilish"""
        analysis = {
            "ma'muriy_huqbuqarorlik": self._extract_admin_responsibility(text),
            "jarima_miqdori": self._extract_fine_amount(text),
            "majburiy_choralar": self._extract_compulsory_measures(text)
        }
        return analysis
    
    def _analyze_land_article(self, text: str) -> Dict:
        """Yer kodeksi moddasini tahlil qilish"""
        analysis = {
            "yer_huquqi": self._extract_land_rights(text),
            "yer_foydalanish": self._extract_land_use(text),
            "yer_himoyasi": self._extract_land_protection(text),
            "yer_munosabatlari": self._extract_land_relations(text)
        }
        return analysis
    
    # Tahlil yordamchi funksiyalari
    def _extract_object(self, text: str) -> str:
        """Ob'ektni ajratib olish"""
        objects = [
            "o'zganing mulki", "jamiyat xavfsizligi", "inson sog'lig'i", "hayot", 
            "davlat manfaatlari", "huquq tartiblari", "mulkkiy huquqlar"
        ]
        for obj in objects:
            if obj.lower() in text.lower():
                return obj
        return "Jamiyat manfaatlari"
    
    def _extract_sanction(self, text: str) -> str:
        """Sanksiyani ajratib olish"""
        sanctions = [
            "ozodlikdan mahrum qilish", "jarima", "tuzatuv ishlari", 
            "huquqlardan mahrum qilish", "majburiy mehnat"
        ]
        found_sanctions = []
        for sanction in sanctions:
            if sanction.lower() in text.lower():
                found_sanctions.append(sanction)
        return ", ".join(found_sanctions) if found_sanctions else "Jazo"
    
    def _extract_subject(self, text: str) -> str:
        """Mavzuni ajratib olish"""
        subjects = [
            "shartnoma", "mulkiy huquq", "meros", "egalik huquqi", 
            "xizmat", "kafillik", "garov"
        ]
        for subject in subjects:
            if subject.lower() in text.lower():
                return subject
        return "Fuqarolik-huquqiy munosabatlar"
    
    def _extract_parties(self, text: str) -> str:
        """Tomonlarni ajratib olish"""
        if "shartnoma" in text.lower():
            return "Shartnoma tomonlari"
        elif "meros" in text.lower():
            return "Meros qoldiruvchi va vorislar"
        else:
            return "Fuqarolar, yuridik shaxslar"
    
    def _extract_rights(self, text: str) -> str:
        """Huquq va majburiyatlarni ajratib olish"""
        return "Huquq va majburiyatlar"
    
    def _determine_contract_type(self, text: str) -> str:
        """Shartnoma turini aniqlash"""
        contracts = ["sotib olish", "ijara", "qarz", "xizmat", "ish"]
        for contract in contracts:
            if contract in text.lower():
                return f"{contract.capitalize()} shartnomasi"
        return "Shartnoma"
    
    def _determine_crime_type(self, text: str) -> str:
        """Jinoyat turini aniqlash"""
        crimes = [
            "o'g'rilik", "talonchilik", "bosqinchilik", "qotillik", 
            "shikast", "firibgarlik", "poraxo'rlik"
        ]
        for crime in crimes:
            if crime in text.lower():
                return crime.capitalize()
        return "Jinoyat"
    
    def _determine_severity(self, text: str) -> str:
        """Og'irlik darajasini aniqlash"""
        if "o'n besh yildan" in text or "yigirma yil" in text:
            return "Juda og'ir"
        elif "besh yildan" in text or "o'n yil" in text:
            return "Og'ir"
        elif "uch yildan" in text:
            return "O'rta"
        else:
            return "Engil"
    
    def _extract_labor_relations(self, text: str) -> str:
        """Mehnat munosabatlarini ajratib olish"""
        return "Mehnat munosabatlari"
    
    def _extract_salary_info(self, text: str) -> str:
        """Ish haqi ma'lumotlarini ajratib olish"""
        if "ish haqi" in text.lower():
            return "Ish haqi to'lash tartibi"
        return "Ish haqi"
    
    def _extract_working_hours(self, text: str) -> str:
        """Ish vaqtini ajratib olish"""
        if "ish vaqti" in text.lower():
            return "Ish vaqti tartibi"
        return "Ish vaqti"
    
    def _extract_family_relations(self, text: str) -> str:
        """Oilaviy munosabatlarni ajratib olish"""
        return "Oilaviy munosabatlar"
    
    def _extract_marriage_conditions(self, text: str) -> str:
        """Nikoh shartlarini ajratib olish"""
        if "nikoh" in text.lower():
            return "Nikoh shartlari"
        return "Nikoh"
    
    def _extract_divorce_procedure(self, text: str) -> str:
        """Ajralish tartibini ajratib olish"""
        if "ajralish" in text.lower():
            return "Ajralish tartibi"
        return "Ajralish"
    
    def _extract_alimony_issues(self, text: str) -> str:
        """Aliment mas'alarini ajratib olish"""
        if "aliment" in text.lower():
            return "Aliment to'lash"
        return "Aliment"
    
    def _extract_admin_responsibility(self, text: str) -> str:
        """Ma'muriy javobgarlikni ajratib olish"""
        return "Ma'muriy javobgarlik"
    
    def _extract_fine_amount(self, text: str) -> str:
        """Jarima miqdorini ajratib olish"""
        if "jarima" in text.lower():
            return "Jarima"
        return "Jarima belgilanadi"
    
    def _extract_compulsory_measures(self, text: str) -> str:
        """Majburiy choralarini ajratib olish"""
        return "Majburiy choralar"
    
    def _extract_land_rights(self, text: str) -> str:
        """Yer huquqlarini ajratib olish"""
        return "Yer huquqlari"
    
    def _extract_land_use(self, text: str) -> str:
        """Yer foydalanishini ajratib olish"""
        return "Yer foydalanish"
    
    def _extract_land_protection(self, text: str) -> str:
        """Yer himoyasini ajratib olish"""
        return "Yer himoyasi"
    
    def _extract_land_relations(self, text: str) -> str:
        """Yer munosabatlarini ajratib olish"""
        return "Yer munosabatlari"
    
    def scrape_all_codes(self) -> List[Dict]:
        """Barcha kodekslarni sken qilish"""
        logger.info("Starting to scrape all legal codes...")
        
        for code_name, url in self.legal_codes.items():
            logger.info(f"Scraping {code_name} from {url}")
            
            soup = self.get_page_content(url)
            if soup:
                articles = self.extract_articles_from_page(soup, code_name)
                self.scraped_data.extend(articles)
                logger.info(f"Successfully scraped {len(articles)} articles from {code_name}")
            else:
                logger.error(f"Failed to scrape {code_name}")
            
            # Serverni yuklamaslik uchun kutish
            time.sleep(2)
        
        logger.info(f"Total articles scraped: {len(self.scraped_data)}")
        return self.scraped_data
    
    def save_to_json(self, filename: str = "lex_uz_scraped_data.json"):
        """Ma'lumotlarni JSON formatida saqlash"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {filename}")
    
    def save_to_excel(self, filename: str = "lex_uz_scraped_data.xlsx"):
        """Ma'lumotlarni Excel formatida saqlash"""
        if not self.scraped_data:
            logger.warning("No data to save")
            return
        
        # DataFrame yaratish
        df_data = []
        for article in self.scraped_data:
            row = {
                "Kodeks": article["kodeks"],
                "Modda": article["modda"],
                "Nomi": article["nomi"],
                "Matn": article["matn"],
                "Tahlil": json.dumps(article["tahlil"], ensure_ascii=False)
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df.to_excel(filename, index=False, engine='openpyxl')
        logger.info(f"Data saved to {filename}")
    
    def generate_statistics(self) -> Dict:
        """Statistikani generatsiya qilish"""
        stats = {
            "scraping_date": datetime.now().isoformat(),
            "total_codes": len(self.legal_codes),
            "total_articles": len(self.scraped_data),
            "codes_statistics": {}
        }
        
        for code_name in self.legal_codes:
            code_articles = [a for a in self.scraped_data if a["kodeks"] == code_name]
            stats["codes_statistics"][code_name] = {
                "articles_count": len(code_articles),
                "articles": [a["modda"] for a in code_articles]
            }
        
        return stats
    
    def run_complete_scraping(self):
        """To'liq sken qilishni bajarish"""
        print("=== PROFESSIONAL LEX.UZ SCRAPER ===")
        print("Starting complete scraping process...")
        
        # Barcha kodekslarni sken qilish
        data = self.scrape_all_codes()
        
        # Ma'lumotlarni saqlash
        self.save_to_json()
        self.save_to_excel()
        
        # Statistika
        stats = self.generate_statistics()
        
        # Statistikani saqlash
        with open("scraping_statistics.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"\n=== SCRAPING RESULTS ===")
        print(f"Total codes scraped: {stats['total_codes']}")
        print(f"Total articles scraped: {stats['total_articles']}")
        
        for code_name, code_stats in stats["codes_statistics"].items():
            print(f"{code_name}: {code_stats['articles_count']} articles")
        
        print(f"\nFiles created:")
        print(f"- lex_uz_scraped_data.json")
        print(f"- lex_uz_scraped_data.xlsx")
        print(f"- scraping_statistics.json")
        
        return data

def main():
    """Asosiy funktsiya"""
    scraper = LexUzProfessionalScraper()
    return scraper.run_complete_scraping()

if __name__ == "__main__":
    main()
