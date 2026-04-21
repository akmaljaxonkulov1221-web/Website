#!/usr/bin/env python3
"""
Advanced AI Analyzer - Professional qonun matnlarini chuqur tahlil qilish
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedAIAnalyzer:
    """Advanced AI-powered legal text analyzer"""
    
    def __init__(self):
        # Chuqur AI tahlili uchun patternlar
        self.legal_patterns = {
            # Ob'ekt elementlari - kengaytirilgan
            "object": {
                "primary_patterns": [
                    r"(hayot|salomatlik| sog'liq|tibbiy yordam)",
                    r"(mol-mulk|mulkiy huquq|tana|pul|valyuta|aktivlar|investitsiya)",
                    r"(huquq|erkinlik|konstitutsiyaviy huquq|fuqarolik huquqi)",
                    r"(tartib|xavfsizlik|jamoa xavfsizligi|davlat xavfsizligi)",
                    r"(inson|fuqaro|shaxs|tashkilot|korxona|muassasa)",
                    r"(ijtimoiy aloqalar|oilaviy munosabatlar|nikoh|ajralish)",
                    r"(atrof-muhit|tabiat|suv|yer|havo|resurslar)",
                    r"(ism|sharaf|qadr-qimmat|vijdon|shaxsiyat huquqi)",
                    r"(meros|vorislik|testament|vasiyatnoma)",
                    r"(intellektual mulk|avtorlik huquqi|patent|tovar belgisi)"
                ],
                "secondary_patterns": [
                    r"(uy|avtomobil|telefon|komp'yuter|texnika)",
                    r"(hujjat|shartnoma|guvohnoma|litsenziya|ruxsatnoma)",
                    r"(bank hisobraqami|karta|pul o'tkazmalari)",
                    r"(biznes|korxona|do'kon|fabrika|ishlab chiqarish)",
                    r"(o'qish|ta'lim|ilmiy daraja|diploma|sertifikat)"
                ],
                "context_keywords": [
                    "zarar", "talon-taroj", "buzish", "o'g'irlash", "o'ldirish", 
                    "parchalash", "musbat", "manfiy", "kaltaklash", "kamsitish"
                ]
            },
            
            # Sub'ekt elementlari - kengaytirilgan
            "subject": {
                "primary_patterns": [
                    r"(shaxs|fuqaro|fuqarolik|jamoat a'zosi)",
                    r"(mansabdor|davlat xizmatchisi|rasmiy shaxs)",
                    r"(tadbirkor|biznesmen|ishlab chiqaruvchi|importyor|eksportyor)",
                    r"(ishchi|xodim|hizmatchi|mutaxassis|rahbar|direktor)",
                    r"(o'qituvchi|o'quvchi|talaba|magistr|bakalavr)",
                    r"(sotuvchi|sotib oluvchi|xaridor|yetkazib beruvchi)",
                    r"(ota-ona|farzand|o'g'il|qiz|aka|uka|opa|singil|turmush o'rtog'i)",
                    r"(prokuror|sudya|tergovchi|advokat|huquqshunos)",
                    r"(shifokor|tibbiyot xodimi|sog'liqni saqlash xodimi)",
                    r"(bankir|moliyachi|buxgalter|auditor)"
                ],
                "secondary_patterns": [
                    r"(ijrochi|boshqaruvchi|administrator|moderator)",
                    r"(haydovchi|transport xizmatchi|pilot|kapitan)",
                    r"(quruvchi|muhandis|arxitektor|dizayner)",
                    r"(dehqon|fermer|chorvador|bog'bon)",
                    r"(olim|tadqiqotchi|professor|ilmiy xodim)"
                ],
                "context_keywords": [
                    "sodir etdi", "bajaradi", "qiladi", "amalga oshiradi",
                    "ayblanadi", "javobgar", "sub'ekt", "ishtirok etdi"
                ]
            },
            
            # Ob'ektiv tomon - kengaytirilgan
            "objective_side": {
                "primary_patterns": [
                    r"(o'ldirish|qotillik|parchalash|jarohat yetkazish)",
                    r"(o'g'rilash|talonchilik|bosqinchilik|mulkni o'g'irlash)",
                    r"(olish|berish|topshirish|qabul qilish|yetkazish)",
                    r"(buzish|bajarmaslik|e'tiborsizlik|qoidabuzarlik)",
                    r"(to'lash|talon to'lash|jarima to'lash|kompensatsiya)",
                    r"(sodir etish|amalga oshirish|qilish|yaratish|ochish)",
                    r"(aldash|soxtalashtirish|g'ayritabiiy usulda qilish)",
                    r"(qo'rqitish|tahdid qilish|bosim o'tkazish)",
                    r"(kiritish|chiqarish|import|eksport)",
                    r"(ishlatish|foydalanish|sotish|almashtirish)"
                ],
                "secondary_patterns": [
                    r"(yopish|ochiq qoldirish|to'sish|to'siq qo'yish)",
                    r"(o'zgartirish|o'chirish|yo'q qilish|buzish)",
                    r"(ko'chirish|joylashtirish|joylashtirilgan)",
                    r"(ro'yxatdan o'tkazish|registratsiya qilish|rasmiylashtirish)",
                    r"(tekshirish|nazorat qilish|taftish qilish)"
                ],
                "context_keywords": [
                    "usulda", "yo'l bilan", "tarzda", "usulida", "orqali",
                    "yordamida", "bilan", "tufayli", "sabab", "asosida"
                ]
            },
            
            # Sub'ektiv tomon - kengaytirilgan
            "subjective_side": {
                "primary_patterns": [
                    r"(qasddan|niyat bilan|rejalashtirilgan|maqsadli)",
                    r"(ehtiyotsizlikdan|xatolik bilan|bilmagan holda)",
                    r"(bilib|bilmasdan|ongli ravishda|ongasiz ravishda)",
                    r"(zo'ravonlik bilan|shafqatsizlik bilan|nafrat bilan)",
                    r"(manfaat uchun|moddiy foyda uchun|shaxsiy manfaat)",
                    r"(g'azab bilan|hasad bilan|qasos olish maqsadida)",
                    r"(iqdrosizlikdan|bexosorlikdan|e'tiborsizlikdan)",
                    r"(majburlash|tazyiq ostida|majburan)",
                    r"(aldash orqali|hiyla nayrang bilan|noqonuniy usulda)",
                    r"(o'z xohishi bilan|ixtiyoriy ravishda|roziligiz bilan)"
                ],
                "secondary_patterns": [
                    r"(tasodifiy|to'satdan|kutilmagan holda)",
                    r"(umumiy xavf|umumiy xavflilik|ijtimoiy xavflilik)",
                    r"(shaxsiy dushmanlik|do'stlik munosabatlari|oilaviy nizolar)",
                    r"(kasbiy majburiyat|rasmiy vazifa|xizmat vazifasi)",
                    r"(ijtimoiy talab|jamoa talabi|guruh talabi)"
                ],
                "context_keywords": [
                    "niyat", "maqsad", "reja", "xatolik", "ehtiyotsizlik",
                    "g'oya", "fikr", "qaror", "ixtiyor", "iyyoq"
                ]
            },
            
            # Jazo turlari - yangi
            "punishment": {
                "primary_patterns": [
                    r"(ozodlikdan mahrum qilish|qamoq|asirlikda saqlash)",
                    r"(jarima|pul jazosi|moliyaviy jazo)",
                    r"(tuzatuv ishlari|jamoat ishlari|majburiy mehnat)",
                    r"(majburiy mehnat|mehnatga jalb qilish)",
                    r"(huquqlardan mahrum qilish|huquqni cheklash)",
                    r"(musodara qilish|mulkni musodara qilish)",
                    r"(ruhsatnomadan mahrum qilish|litsenziyadan mahrum qilish)",
                    r"(oqqa o'tqazish|o'q jarimasi|og'ir jarima)"
                ],
                "secondary_patterns": [
                    r"(ogohlantirish|ogohlantiruv chora|ogohlantirish berish)",
                    r"(shartli ravishda jazolanmaslik|shartli ozodlik)",
                    r"(sinov muddati|sinov muddatiga qo'yish)",
                    r"(jamoat joyida ishlash|jamoat ishlari)",
                    r"(ma'muriy javobgarlik|intizomiy jazo)"
                ],
                "context_keywords": [
                    "yil", "oy", "kun", "so'm", "ming", "million", "baravar",
                    "jazo", "javobgarlik", "jazolanadi", "tortiladi"
                ]
            }
        }
        
        # Qonun sohalarini aniqlash uchun patterns
        self.legal_domains = {
            "jinoyat_huquqi": [
                r"(jinoyat|qotillik|o'g'rilik|talonchilik|bosqinchilik)",
                r"(qamoq|ozodlikdan mahrum qilish|jazo|javobgarlik)",
                r"(prokuror|sudya|tergov|surishtiruv)"
            ],
            "fuqarolik_huquqi": [
                r"(fuqaro|fuqarolik|shartnoma|mulkiy huquq)",
                r"(tovan|kompensatsiya|shartnoma|kelishuv)",
                r"(tashkilot|korxona|yuridik shaxs)"
            ],
            "mehnat_huquqi": [
                r"(ish|ishchi|ish beruvchi|mehnat|ish haqi)",
                r"(ta'til|dam olish|ish vaqti|ishdan bo'shatish)",
                r"(kollektiv shartnoma|ish xavfsizligi)"
            ],
            "oilaviy_huquq": [
                r"(nikoh|oilaviy|ajralish|aliment)",
                r"(ota-ona|farzand|asrab olish|voyaga yetmagan)",
                r"(turmush o'rtog'i|kelin|kuyov)"
            ],
            "ma'muriy_huquq": [
                r"(ma'muriy|jarima|ogohlantirish|intizomiy)",
                r"(davlat organi|rasmiy shaxs|mansabdor)",
                r"(qoidabuzarlik|huquqbuzarlik)"
            ],
            "yer_huquqi": [
                r"(yer|zamin|tuproq|agroler|shahar yerlari)",
                r"(ijara|doimiy foydalanish|mulkiy huquq)",
                r"(yer kadastr|yer reformasi|yer taqsimoti)"
            ]
        }
    
    def analyze_text_element(self, text: str, element_config: Dict) -> List[str]:
        """Matndan ma'lum bir elementni chuqur tahlil qilish"""
        text_lower = text.lower()
        found_elements = []
        
        # Primary patterns bo'yicha qidirish
        for pattern in element_config.get("primary_patterns", []):
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            found_elements.extend(matches)
        
        # Secondary patterns bo'yicha qidirish
        for pattern in element_config.get("secondary_patterns", []):
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            found_elements.extend(matches)
        
        # Context keywords atrofidan so'zlarni olish
        for keyword in element_config.get("context_keywords", []):
            # Kalit so'z atrofidagi gaplarni olish
            context_patterns = [
                rf"([^.\n]*{keyword}[^.\n]*)",
                rf"({keyword}[^.\n]*)",
                rf"([^.\n]*{keyword})"
            ]
            
            for pattern in context_patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    # Gapdan muhim so'zlarni ajratib olish
                    words = re.findall(r'\b\w+\b', match)
                    for word in words:
                        if (len(word) > 3 and 
                            word not in keyword and 
                            word not in ["va", "ham", "bilan", "uchun", "tufayli"]):
                            found_elements.append(word)
        
        # Takrorlarni olib tashlash va tozalash
        unique_elements = []
        seen = set()
        
        for element in found_elements:
            element_clean = element.strip()
            if (element_clean and 
                len(element_clean) > 2 and 
                element_clean not in seen and
                not element_clean.isdigit()):
                unique_elements.append(element_clean)
                seen.add(element_clean)
        
        # Eng muhim elementlarni tanlash (birinchi 10 ta)
        return unique_elements[:10]
    
    def determine_legal_domain(self, text: str) -> str:
        """Matn tegishli bo'lgan qonun sohasini aniqlash"""
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, patterns in self.legal_domains.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches
            domain_scores[domain] = score
        
        # Eng yuqori ballga ega sohani qaytarish
        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            if domain_scores[best_domain] > 0:
                return best_domain
        
        return "umumiy"
    
    def analyze_article_complexity(self, article: Dict) -> Dict:
        """Moddaning murakkabligini tahlil qilish"""
        content = article.get("content", "")
        title = article.get("title", "")
        
        word_count = len(content.split())
        sentence_count = len(re.findall(r'[.!?]+', content))
        
        # Murakkablik darajasi
        if word_count > 200:
            complexity = "high"
        elif word_count > 100:
            complexity = "medium"
        else:
            complexity = "low"
        
        # Huquqiy tushunchalar soni
        legal_terms = len(re.findall(
            r'(huquq|javobgarlik|shartnoma|qonun|sud|jazo|majburiyat)',
            content.lower()
        ))
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "complexity": complexity,
            "legal_terms_count": legal_terms,
            "avg_sentence_length": word_count / max(sentence_count, 1)
        }
    
    def analyze_article(self, article: Dict) -> Dict:
        """Moddani chuqur AI tahlili"""
        content = article.get("content", "") + " " + article.get("title", "")
        
        analysis = {}
        
        # Asosiy elementlarni tahlil qilish
        for element_name, element_config in self.legal_patterns.items():
            found_elements = self.analyze_text_element(content, element_config)
            analysis[element_name] = found_elements
        
        # Qonun sohasini aniqlash
        analysis["legal_domain"] = self.determine_legal_domain(content)
        
        # Murakkablik tahlili
        analysis["complexity_analysis"] = self.analyze_article_complexity(article)
        
        # Jazo tafsilotlari
        analysis["punishment_details"] = self.extract_punishment_details(content)
        
        # Huquqiy aloqalar
        analysis["legal_relations"] = self.extract_legal_relations(content)
        
        # Xulosa
        analysis["summary"] = self.generate_advanced_summary(analysis, article)
        
        # Ishonch darajasi
        analysis["confidence_score"] = self.calculate_confidence_score(analysis)
        
        return analysis
    
    def extract_punishment_details(self, text: str) -> Dict:
        """Jazo tafsilotlarini ajratib olish"""
        text_lower = text.lower()
        
        # Jazo miqdorini olish
        amount_patterns = [
            r'(\d+)\s*(yil|oy|kun)',
            r'(\d+)\s*(so\'m|ming|million)',
            r'(\d+)\s*baravar',
            r'eng kam oylik ish haqqining\s*(\d+)\s*baravar'
        ]
        
        amounts = []
        for pattern in amount_patterns:
            matches = re.findall(pattern, text_lower)
            amounts.extend([f"{match[0]} {match[1]}" for match in matches])
        
        # Jazo turi
        punishment_types = []
        if "ozodlikdan mahrum qilish" in text_lower:
            punishment_types.append("ozodlikdan mahrum qilish")
        if "jarima" in text_lower:
            punishment_types.append("jarima")
        if "tuzatuv ishlari" in text_lower:
            punishment_types.append("tuzatuv ishlari")
        if "majburiy mehnat" in text_lower:
            punishment_types.append("majburiy mehnat")
        
        return {
            "amounts": amounts[:5],  # Eng ko'pi bilan 5 ta miqdor
            "types": punishment_types,
            "severity": self.determine_punishment_severity(text_lower)
        }
    
    def extract_legal_relations(self, text: str) -> List[str]:
        """Huquqiy munosabatlarni ajratib olish"""
        text_lower = text.lower()
        
        relations = []
        
        relation_patterns = [
            r"(ota-ona.*farzand|farzand.*ota-ona)",
            r"(ish beruvchi.*ishchi|ishchi.*ish beruvchi)",
            r"(sotuvchi.*sotib oluvchi|sotib oluvchi.*sotuvchi)",
            r"(turmush o\'rtog\'i.*turmush o\'rtog\'i)",
            r"(davlat.*fuqaro|fuqaro.*davlat)",
            r"(tashkilot.*shaxs|shaxs.*tashkilot)"
        ]
        
        for pattern in relation_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            relations.extend(matches)
        
        return list(set(relations))[:5]  # Eng ko'pi bilan 5 ta munosabat
    
    def determine_punishment_severity(self, text: str) -> str:
        """Jazo og'irligini aniqlash"""
        if any(word in text for word in ["yigirma besh", "yigirma", "o'n besh", "o'n"]):
            return "extreme"
        elif any(word in text for word in ["yetti", "olti", "besh", "to'rt"]):
            return "high"
        elif any(word in text for word in ["uch", "ikki", "bir"]):
            return "medium"
        else:
            return "low"
    
    def generate_advanced_summary(self, analysis: Dict, article: Dict) -> str:
        """Chuqur xulosa yaratish"""
        summary_parts = []
        
        # Sub'ekt
        if analysis.get("subject"):
            summary_parts.append(f"Sub'ekt: {', '.join(analysis['subject'][:3])}")
        
        # Ob'ekt
        if analysis.get("object"):
            summary_parts.append(f"Ob'ekt: {', '.join(analysis['object'][:3])}")
        
        # Harakat
        if analysis.get("objective_side"):
            summary_parts.append(f"Harakat: {', '.join(analysis['objective_side'][:3])}")
        
        # Niyat
        if analysis.get("subjective_side"):
            summary_parts.append(f"Niyat: {', '.join(analysis['subjective_side'][:2])}")
        
        # Jazo
        punishment_details = analysis.get("punishment_details", {})
        if punishment_details.get("types"):
            summary_parts.append(f"Jazo: {', '.join(punishment_details['types'])}")
        
        # Qonun sohasi
        domain = analysis.get("legal_domain", "")
        if domain:
            summary_parts.append(f"Soha: {domain}")
        
        return " | ".join(summary_parts)
    
    def calculate_confidence_score(self, analysis: Dict) -> float:
        """Tahlil ishonch darajasini hisoblash"""
        score = 0.0
        max_score = 100.0
        
        # Elementlar soni bo'yicha ball
        for element in ["subject", "object", "objective_side", "subjective_side"]:
            elements_count = len(analysis.get(element, []))
            if elements_count > 0:
                score += min(elements_count * 10, 25)  # Har bir element uchun max 25 ball
        
        # Jazo tafsilotlari uchun ball
        punishment_details = analysis.get("punishment_details", {})
        if punishment_details.get("amounts") or punishment_details.get("types"):
            score += 15
        
        # Huquqiy munosabatlar uchun ball
        if analysis.get("legal_relations"):
            score += 10
        
        # Qonun sohasi aniqlangan bo'lsa
        if analysis.get("legal_domain") != "umumiy":
            score += 10
        
        return min(score, max_score)
    
    def analyze_all_articles(self, articles_data: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """Barcha moddalarni chuqur tahlil qilish"""
        logger.info("Starting advanced AI analysis...")
        
        analyzed_data = {}
        
        for code_name, articles in articles_data.items():
            analyzed_articles = []
            
            for article in articles:
                logger.info(f"Analyzing {article.get('number', 'unknown')} from {code_name}")
                
                analyzed_article = article.copy()
                analyzed_article["advanced_ai_analysis"] = self.analyze_article(article)
                analyzed_articles.append(analyzed_article)
            
            analyzed_data[code_name] = analyzed_articles
            logger.info(f"Advanced analysis completed for {len(analyzed_articles)} articles in {code_name}")
        
        return analyzed_data
    
    def generate_analysis_report(self, analyzed_data: Dict[str, List[Dict]]) -> Dict:
        """Tahlil hisobotini yaratish"""
        report = {
            "total_codes": len(analyzed_data),
            "total_articles": sum(len(articles) for articles in analyzed_data.values()),
            "analysis_timestamp": datetime.now().isoformat(),
            "domain_distribution": {},
            "complexity_distribution": {"high": 0, "medium": 0, "low": 0},
            "average_confidence_score": 0.0,
            "most_common_elements": {},
            "punishment_severity_distribution": {"extreme": 0, "high": 0, "medium": 0, "low": 0}
        }
        
        total_confidence = 0
        all_elements = {"subject": [], "object": [], "objective_side": [], "subjective_side": []}
        
        for code_name, articles in analyzed_data.items():
            for article in articles:
                analysis = article.get("advanced_ai_analysis", {})
                
                # Qonun sohalari
                domain = analysis.get("legal_domain", "umumiy")
                report["domain_distribution"][domain] = report["domain_distribution"].get(domain, 0) + 1
                
                # Murakkablik
                complexity = analysis.get("complexity_analysis", {}).get("complexity", "low")
                report["complexity_distribution"][complexity] += 1
                
                # Ishonch darajasi
                confidence = analysis.get("confidence_score", 0)
                total_confidence += confidence
                
                # Elementlar
                for element_type in all_elements:
                    elements = analysis.get(element_type, [])
                    all_elements[element_type].extend(elements)
                
                # Jazo og'irligi
                punishment_severity = analysis.get("punishment_details", {}).get("severity", "low")
                report["punishment_severity_distribution"][punishment_severity] += 1
        
        # O'rtacha ishonch darajasi
        total_articles = report["total_articles"]
        if total_articles > 0:
            report["average_confidence_score"] = total_confidence / total_articles
        
        # Eng ko'p uchraydigan elementlar
        for element_type, elements in all_elements.items():
            from collections import Counter
            counter = Counter(elements)
            report["most_common_elements"][element_type] = counter.most_common(5)
        
        return report

def main():
    """Asosiy funktsiya"""
    logger.info("Starting Advanced AI Analysis System...")
    
    # Professional ma'lumotlarni yuklash
    try:
        with open('professional_legal_data.json', 'r', encoding='utf-8') as f:
            professional_data = json.load(f)
    except FileNotFoundError:
        logger.error("professional_legal_data.json not found. Please run professional_legal_data.py first.")
        return
    
    # Advanced AI analyzer
    analyzer = AdvancedAIAnalyzer()
    
    # Tahlil qilish
    analyzed_data = analyzer.analyze_all_articles(professional_data)
    
    # Natijalarni saqlash
    with open('advanced_analyzed_legal_data.json', 'w', encoding='utf-8') as f:
        json.dump(analyzed_data, f, ensure_ascii=False, indent=2)
    
    # Hisobotni yaratish
    report = analyzer.generate_analysis_report(analyzed_data)
    
    with open('analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info("=== ADVANCED AI ANALYSIS COMPLETED ===")
    logger.info(f"Total codes analyzed: {report['total_codes']}")
    logger.info(f"Total articles analyzed: {report['total_articles']}")
    logger.info(f"Average confidence score: {report['average_confidence_score']:.2f}")
    
    logger.info("=== DOMAIN DISTRIBUTION ===")
    for domain, count in report['domain_distribution'].items():
        logger.info(f"{domain}: {count} articles")
    
    logger.info("=== COMPLEXITY DISTRIBUTION ===")
    for complexity, count in report['complexity_distribution'].items():
        logger.info(f"{complexity}: {count} articles")
    
    logger.info("=== PUNISHMENT SEVERITY ===")
    for severity, count in report['punishment_severity_distribution'].items():
        logger.info(f"{severity}: {count} articles")
    
    logger.info("Analysis results saved to advanced_analyzed_legal_data.json")
    logger.info("Analysis report saved to analysis_report.json")

if __name__ == "__main__":
    main()
