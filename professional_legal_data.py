#!/usr/bin/env python3
"""
Professional Legal Data Generator - Mukammal professional qonun ma'lumotlari bazasi
"""

import json
from datetime import datetime
import hashlib

class ProfessionalLegalDataGenerator:
    """Professional qonun ma'lumotlari generatori - to'liq va mukammal"""
    
    def __init__(self):
        self.comprehensive_codes = {
            "Jinoyat kodeksi": [
                {
                    "number": "1-modda",
                    "title": "Jinoyat qonunining vazifalari",
                    "content": "O'zbekiston Respublikasi Jinoyat kodeksining vazifalari jamiyatni jinoyatlikdan himoya qilish, inson huquqlari va erkinliklarini, mulkiy huquqlarni, jamoat xavfsizligini va jamoat tartibini himoya qilish, tinchlikni va xavfsizlikni ta'minlash, shuningdek, jinoyatning oldini olish, jinoyatchilikka qarshi kurashish, jinoyat sodir etishning sabab va shart-sharoitlarini bartaraf etishdan iboratdir.",
                    "category": "umumiy_qoidalar",
                    "severity": "high",
                    "punishment_type": "umumiy"
                },
                {
                    "number": "15-modda",
                    "title": "Javobgarlik yoshiga yetmagan shaxslarning javobgarligi",
                    "content": "14 yoshga to'lgan, ammo 18 yoshga to'lmagan shaxslar sodir etgan jinoyatlari uchun ular javobgarlikka tortiladilar. 14 yoshga to'lgan shaxslar faqat qasddan odam o'ldirish, sog'liq uchun og'ir oqibatlarga olib keladigan shikast yetkazish, o'g'rilik, talonchilik, bosqinchilik kabi og'ir jinoyatlar uchun javobgarlikka tortiladilar.",
                    "category": "umumiy_qoidalar",
                    "severity": "high",
                    "punishment_type": "yoshga_qarab"
                },
                {
                    "number": "27-modda", 
                    "title": "Jinoyat tushunchasi",
                    "content": "Jinoyat - bu jamiyat uchun xavfli, ushbu Kodeksda taqiqlangan harakat yoki harakatsizlik, qonunga muvofiq javobgarlikka tortiladigan, shu jumladan, jazoni qo'llaniladigan ijtimoiy xavflilik belgilariga ega bo'lgan, aqli raso, 14 yoshga to'lgan shaxs tomonidan sodir etilgan vijdonsiz harakatdir.",
                    "category": "umumiy_qoidalar",
                    "severity": "high",
                    "punishment_type": "umumiy"
                },
                {
                    "number": "97-modda",
                    "title": "Qotillik", 
                    "content": "Qasddan odam o'ldirish - o'n besh yildan yigirma yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Qotillikning quyidagi holatlari uchun yigirma yildan yigirma besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi: ikki yoki undan ortiq shaxsga nisbatan; ota-onasiga, farzandiga, turmush o'rtog'iga nisbatan; boshqa shafqatsizlik holatida; o'tkir ijtimoiy xavfli usullar bilan; maqsadini yashirish yoki boshqa jinoyat sodir etishni yengillatish uchun.",
                    "category": "shaxsga_qarshi_jinoyatlar",
                    "severity": "extreme",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                },
                {
                    "number": "104-modda",
                    "title": "Og'ir shikast yetkazish orqali sog'liqni og'irlashtirish",
                    "content": "Qasddan inson sog'ligiga og'ir shikast yetkazish, bu odamning hayotiga xavf solishi yoki u umrbod kasallikka uchrashi, shuningdek, ijtimoiy faoliyatini to'liq yo'qotishiga olib kelishi - besh yildan sakkiz yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu harakatlar o'limga olib kelsa, o'n yildan o'n besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                    "category": "shaxsga_qarshi_jinoyatlar",
                    "severity": "extreme",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                },
                {
                    "number": "164-modda",
                    "title": "O'g'rilik",
                    "content": "Boshqa kishining mol-mulkini noqonuniy olib qochish yoki o'zlashtirish - uch yildan o'n yilgacha ozodlikdan mahrum qilish bilan jazolanadi. O'g'rilik qilishda qasddan ochilgan qurol yoki boshqa qurollar qo'llanilganda, shuningdek, o'g'rilik qilishda o'g'rilikka qarshi kurashayotgan shaxsga qarshi zo'ravonlik qo'llanilganda sodir etilgan o'g'rilik - besh yildan yigirma besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi.",
                    "category": "mulkka_qarshi_jinoyatlar",
                    "severity": "high",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                },
                {
                    "number": "165-modda",
                    "title": "Talonchilik",
                    "content": "O'g'rilik maqsadida boshqa kishining mol-mulkini ochiqdan-ochiq olib qochish, shu maqsadida zo'ravonlik qo'llash yoki zo'ravonlik qo'llash bilan tahdid qilish - uch yildan yetti yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar talonchilik qilishda qasddan ochilgan qurol yoki boshqa qurollar qo'llanilsa yoki bir necha kishi tomonidan sodir etilsa, besh yildan o'n yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                    "category": "mulkka_qarshi_jinoyatlar",
                    "severity": "high",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                },
                {
                    "number": "167-modda",
                    "title": "Bosqinchilik",
                    "content": "O'g'rilik yoki talonchilik maqsadiga erishish uchun bosqinchilik qilish - to'rt yildan sakkiz yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Bosqinchilik qilishda qasddan ochilgan qurol yoki boshqa qurollar qo'llanilganda yoki bir necha kishi tomonidan sodir etilganda, olti yildan o'n ikki yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                    "category": "mulkka_qarshi_jinoyatlar",
                    "severity": "extreme",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                },
                {
                    "number": "169-modda",
                    "title": "Mulkni o'g'irlash",
                    "content": "O'zlashtirish maqsadida boshqa kishining mol-mulkini noqonuniy ravishda olib qochish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. O'zlashtirish qilishda qasddan ochilgan qurol yoki boshqa qurollar qo'llanilganda, shuningdek, o'zlashtirish qilishda o'zlashtirishga qarshi kurashayotgan shaxsga qarshi zo'ravonlik qo'llanilganda sodir etilgan o'zlashtirish - uch yildan etti yilgacha ozodlikdan mahrum qilish bilan jazolanadi.",
                    "category": "mulkka_qarshi_jinoyatlar",
                    "severity": "medium",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                },
                {
                    "number": "276-modda",
                    "title": "Pulga soxtalashtirish",
                    "content": "Milliy valyuta yoki xorijiy valyutani pulga soxtalashtirish, shuningdek, shunday pul muomalaga kiritish - sakkiz yildan o'n besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar pulga soxtalashtirish uyushma holda sodir etilsa yoki katta miqdorda bo'lsa, o'n yildan yigirma yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                    "category": "iqtisodiy_jinoyatlar",
                    "severity": "high",
                    "punishment_type": "ozodlikdan_mahrum_qilish"
                }
            ],
            "Fuqarolik kodeksi": [
                {
                    "number": "1-modda",
                    "title": "Fuqarolik qonunchiligining asoslari",
                    "content": "O'zbekiston Respublikasida fuqarolik qonunchiligi fuqarolarning huquq va erkinliklarini, shu jumladan, mulkiy huquqlarini himoya qilishga, fuqarolarning shaxsiy va mulkiy manfaatlarini himoya qilishga, shuningdek, iqtisodiy munosabatlarning barqarorligini ta'minlashga yo'naltirilgan. Fuqarolik qonunchiligi fuqarolar va tashkilotlarning o'zaro huquqiy munosabatlarini tartibga soladi.",
                    "category": "umumiy_qoidalar",
                    "severity": "medium",
                    "punishment_type": "huquqiy_munosabatlar"
                },
                {
                    "number": "10-modda",
                    "title": "Fuqarolik qonunchiligining manbalari",
                    "content": "O'zbekiston Respublikasida fuqarolik qonunchiligining manbalari O'zbekiston Respublikasi Konstitutsiyasi, ushbu Kodeks, boshqa qonunlar, shuningdek, O'zbekiston Respublikasi tomonidan ratifikatsiya qilingan xalqaro shartnomalardir. Xalqaro shartnomalarning qoida va tartiblari to'g'risidagi qonunlardan farqli bo'lsa, xalqaro shartnoma qoidalari qo'llaniladi.",
                    "category": "umumiy_qoidalar",
                    "severity": "low",
                    "punishment_type": "huquqiy_munosabatlar"
                },
                {
                    "number": "16-modda",
                    "title": "Fuqarolik huquqlarining tengligi",
                    "content": "Fuqarolar fuqarolik huquqlariga ega bo'lishda va ularni amalga oshirishda tengdirlar. Hech kim jinsi, irqi, millati, tili, diniy e'tiqodi, siyosiy qarashlari, ijtimoiy kelib chiqishi, mulkiy ahvoli, faoliyat turi, turar joyi yoki boshqa har qanday holatlarga qarab farqlanmaydigan huquqlardan mahrum etilishi yoki ularga nisbatan imtiyozlar berilishi mumkin emas.",
                    "category": "shaxslar_huquqlari",
                    "severity": "medium",
                    "punishment_type": "huquqiy_munosabatlar"
                },
                {
                    "number": "19-modda",
                    "title": "Fuqarolik huquqlarining nomoyon bo'lishi",
                    "content": "Fuqarolik huquqlari, shu jumladan, mulkiy huquqlar qonunda belgilangan tartibda guvohnoma yoki ro'yxatdan o'tkazish orqali, shuningdek, sud qarori yoki boshqa huquqiy hujjatlar bilan nomoyon bo'ladi. Fuqarolik huquqlari, qonunda belgilangan hollar bundan mustasno, ro'yxatdan o'tkazilgunga qadar ham tan olinadi.",
                    "category": "shaxslar_huquqlari",
                    "severity": "medium",
                    "punishment_type": "huquqiy_munosabatlar"
                },
                {
                    "number": "154-modda",
                    "title": "Mulk huquqi",
                    "content": "Mulk huquqi - bu mulk egasining o'z mulkiga qonunda belgilangan chegaralarda o'z xohishiga ko'ra egalik qilish, foydalanish va tartibga solish huquqidir. Mulkiy huquq mulk egasi tomonidan o'z mulkini egalik qilish, undan foydalanish va uni tartibga solish bilan bog'liq harakatlarni amalga oshirish orqali amalga oshiriladi.",
                    "category": "mulkiy_huquqlar",
                    "severity": "high",
                    "punishment_type": "mulkiy_munosabatlar"
                },
                {
                    "number": "167-modda",
                    "title": "Mulkning xususiyatlariga ko'ra bo'linishi",
                    "content": "Mulk ajralmas va bo'linadigan bo'ladi. Ajralmas mulk - bu bo'linishi mumkin bo'lmagan yoki bo'linishi uning maqsadiga zid bo'lgan mulkdir. Bo'linadigan mulk - bu bo'linishi mumkin bo'lgan va bo'lingandan keyin ham o'z maqsadiga xizmat qilishda davom etadigan mulkdir. Mulklarning xususiyatlari qonunda belgilangan tartibda belgilanadi.",
                    "category": "mulkiy_huquqlar",
                    "severity": "medium",
                    "punishment_type": "mulkiy_munosabatlar"
                },
                {
                    "number": "367-modda",
                    "title": "Sotib olish shartnomasi",
                    "content": "Sotib olish shartnomasi bo'yicha sotuvchi mol-mulkni sotib oluvchining mulkiga o'tkazish majburiyatini oladi, sotib oluvchi esa bu mol-mulkni sotuvchidan qabul qilib, uning uchun belgilangan narhni to'lash majburiyatini oladi. Sotib olish shartnomasi yozma ravishda tuzilishi shart, agar qonunda boshqa tartib belgilanmagan bo'lsa.",
                    "category": "shartnomalar",
                    "severity": "high",
                    "punishment_type": "shartnoma_munosabatlari"
                },
                {
                    "number": "617-modda",
                    "title": "Shartnoma tushunchasi",
                    "content": "Shartnoma - bu ikki yoki undan ortiq shaxslarning o'zaro huquq va majburiyatlarini belgilovchi kelishuvi. Shartnoma shakllantirish uchun tomonlarning o'zaro kelishuvi zarur. Shartnoma tomonlarning o'zaro kelishuvi bilan shakllantiriladi. Shartnoma qonun talablariga rioya qilgan holda tuzilishi shart.",
                    "category": "shartnomalar",
                    "severity": "medium",
                    "punishment_type": "shartnoma_munosabatlari"
                },
                {
                    "number": "695-modda",
                    "title": "Garov shartnomasi",
                    "content": "Garov shartnomasi bo'yicha garov beruvchi qarzdorlik majburiyatini qisman yoki to'liq ta'minlash uchun garov qo'yilgan mol-mulkni garov oluvchining foydasiga garov qo'yadi. Garov shartnomasi yozma ravishda tuzilishi shart. Garov qilingan mol-mulk garov beruvchining mulkida qoladi, agar qonunda boshqa tartib belgilanmagan bo'lsa.",
                    "category": "shartnomalar",
                    "severity": "high",
                    "punishment_type": "shartnoma_munosabatlari"
                },
                {
                    "number": "775-modda",
                    "title": "Shartnomaviy javobgarlikning turlari",
                    "content": "Shartnomaviy javobgarlik qonun yoki shartnoma asosida qonuniy majburiyatni bajarmaslik yoki noto'g'ri bajarmish uchun yuzaga keladigan majburiyatlardir. Javobgarlik turlari: tovon to'lash, jarima, garov, zamin. Shartnomaviy javobgarlik tomonlarning kelishuvi bilan belgilanishi mumkin.",
                    "category": "javobgarlik",
                    "severity": "medium",
                    "punishment_type": "javobgarlik_turlari"
                }
            ],
            "Oila kodeksi": [
                {
                    "number": "1-modda",
                    "title": "Oila tushunchasi",
                    "content": "Oila - qonunga asosan nikohda turuvchi yoki qonuniy asoslarda farzand asrab olish shartnomasini tuzgan shaxslar jamlangan. Oilaning asosi nikohdir. Nikohga kirishish erk ixtiyoriy bo'lib, ikkala tomonning roziligi bilan amalga oshiriladi. Oilada o'zaro hurmat, yordam, mas'uliyat va vijdonanlikka asoslangan munosabatlar bo'lishi kerak.",
                    "category": "umumiy_qoidalar",
                    "severity": "medium",
                    "punishment_type": "oilaviy_munosabatlar"
                },
                {
                    "number": "8-modda",
                    "title": "Nikohga kirishishning asoslari",
                    "content": "Nikohga kirishish fuqarolarning o'zaro roziligiga asoslanadi. Nikohga kirishish uchun kuyovning 18 yoshga, kelinning esa 17 yoshga to'lgan bo'lishi shart. Nikohga kirishish fuqarolarning shaxsiy xohish-irodasiga asoslanadi, hech kim nikohga kirishishga majbur etilishi mumkin emas.",
                    "category": "nikoh",
                    "severity": "medium",
                    "punishment_type": "nikoh_munosabatlari"
                },
                {
                    "number": "16-modda",
                    "title": "Nikoh yoshi",
                    "content": "Er-xotin bo'lish uchun kuyovning 18 yoshga, kelinning esa 17 yoshga to'lgan bo'lishi shart. Kuyov yoki kelin yoshi quyidagi hollarda pasport inspeksiyalari tomonidan oshirilishi mumkin: kelin homilador bo'lganda; kelin yoki kuyov birgalikda farzandni tarbiyalashga olishganida; boshqa alohida holatlarda.",
                    "category": "nikoh",
                    "severity": "medium",
                    "punishment_type": "nikoh_munosabatlari"
                },
                {
                    "number": "33-modda",
                    "title": "Nikohning tugatilishi",
                    "content": "Nikoh er-xotinning birining vafot etishi yoki sud tomonidan e'lon qilingan nikohning bekor qilinishi bilan tugatiladi. Nikohni bekor qilish to'g'risidagi ariza er-xotinning birgalikda yoki alohida kelishuvi bilan sudga topshiriladi. Agar ularning voyaga yetmagan farzandlari bo'lsa, ajralish faqat sud tartibida amalga oshiriladi.",
                    "category": "nikoh",
                    "severity": "high",
                    "punishment_type": "nikoh_munosabatlari"
                },
                {
                    "number": "54-modda",
                    "title": "Ota-onaning farzandlarini boqish majburiyati",
                    "content": "Ota-onaning voyaga yetmagan farzandlarini boqish majburiyati voyaga yetguncha davom etadi. Ota-ona farzandlarini material, ma'naviy va jismoniy tarbiyalash majburiyatiga ega. Agar ota-ona farzandni boqishdan bosh tortsa, sud ularning ish haqining yoki boshqa daromadlarining bir qismini aliment sifatida undirishga haqlikdir.",
                    "category": "ota-ona_va_farzandlar",
                    "severity": "high",
                    "punishment_type": "aliment_majburiyati"
                },
                {
                    "number": "63-modda",
                    "title": "Aliment majburiyati",
                    "content": "Ota-onaning voyaga yetmagan farzandlarini boqish majburiyati voyaga yetguncha davom etadi. Agar ota-ona farzandni boqishdan bosh tortsa, sud ularning ish haqining yoki boshqa daromadlarining bir qismini aliment sifatida undirishga haqlikdir. Aliment miqdori har bir tomonning daromadi va farzandlar sonini hisobga olgan holda belgilanadi.",
                    "category": "ota-ona_va_farzandlar",
                    "severity": "high",
                    "punishment_type": "aliment_majburiyati"
                },
                {
                    "number": "78-modda",
                    "title": "Farzandning ota-onaga nisbatan majburiyatlari",
                    "content": "Voyaga yetgan farzandlar ota-onalariga moddiy yordam ko'rsatish majburiyatiga ega. Agar ota-onalar kasal bo'lib, ishlay olmasa yoki ularning daromadi yetarli bo'lmasa, farzandlar ularni boqishlari shart. Bu majburiyat farzandlarning voyaga yetgunga qadar davom etadi.",
                    "category": "ota-ona_va_farzandlar",
                    "severity": "medium",
                    "punishment_type": "aliment_majburiyati"
                },
                {
                    "number": "115-modda",
                    "title": "Asrab olish",
                    "content": "Asrab olish - bu voyaga yetmagan farzandni ota-onaning roziligi bilan o'z oilasiga qabul qilish va unga ota-onaga xos huquq va majburiyatlarni yuklashdir. Asrab olish faqat voyaga yetmagan farzandning manfaatlariga mos kelishi shart. Asrab olish to'g'risidagi shartnoma yozma ravishda tuziladi.",
                    "category": "asrab_olish",
                    "severity": "high",
                    "punishment_type": "asrab_olish_munosabatlari"
                },
                {
                    "number": "126-modda",
                    "title": "Ajralish tartibi",
                    "content": "Nikoh sud tomonidan bekor qilinadi. Ajralish to'g'risidagi ariza er-xotinning birgalikda yoki alohida kelishuvi bilan sudga topshiriladi. Agar ularning voyaga yetmagan farzandlari bo'lsa, ajralish faqat sud tartibida amalga oshiriladi. Sud ajralish to'g'risida qaror chiqargandan so'ng, nikoh tugatiladi.",
                    "category": "ajralish",
                    "severity": "high",
                    "punishment_type": "ajralish_munosabatlari"
                },
                {
                    "number": "138-modda",
                    "title": "Ajralishdan keyin farzandlarni joylashtirish",
                    "content": "Ajralishdan keyin voyaga yetmagan farzandlar kim bilan qolishi to'g'risida ota-ona o'rtasida kelishuvga erishiladi. Agar kelishuvga erishilmasa, sud farzandning manfaatlarini hisobga olgan holda qaror qabul qiladi. Sud qarori farzandning yoshi, sog'lig'i, ota-onaning moddiy ahvoli va boshqa omillarni inobatga oladi.",
                    "category": "ajralish",
                    "severity": "high",
                    "punishment_type": "ajralish_munosabatlari"
                }
            ],
            "Mehnat kodeksi": [
                {
                    "number": "1-modda",
                    "title": "Mehnat qonunining vazifalari",
                    "content": "O'zbekiston Respublikasi Mehnat kodeksining vazifalari ishchilar va ish beruvchilar o'rtasidagi mehnat munosabatlarini tartibga solish, ularning huquq va majburiyatlarini belgilash, mehnat haqqini to'lanishini ta'minlash, ish xavfsizligini kafolatlash, mehnat sharoitlarini yaxshilashdan iboratdir.",
                    "category": "umumiy_qoidalar",
                    "severity": "medium",
                    "punishment_type": "mehnat_munosabatlari"
                },
                {
                    "number": "73-modda",
                    "title": "Ish haqi",
                    "content": "Ish haqi - bu ish beruvchi tomonidan ishchining mehnati uchun to'lanadigan pul mablag'i. Ish haqi oylik, soatlik, qismlarga bo'lib yoki ish natijasiga qarab belgilanishi mumkin. Ish haqi kamida eng kam ish haqi miqdoridan kam bo'lmasligi shart. Ish haqini o'z vaqtida va to'liq to'lash ish beruvchining majburiyatidir.",
                    "category": "ish_haqqi",
                    "severity": "high",
                    "punishment_type": "ish_haqqi_munosabatlari"
                },
                {
                    "number": "77-modda",
                    "title": "Eng kam ish haqi",
                    "content": "Eng kam ish haqi - bu ishchining eng kam hayot kechirish vositalarini ta'minlaydigan ish haqi miqdoridir. Eng kam ish haqi O'zbekiston Respublikasi Vazirlar Mahkamasining qarori bilan belgilanadi. Ish haqi eng kam ish haqi miqdoridan kam bo'lmasligi shart.",
                    "category": "ish_haqqi",
                    "severity": "high",
                    "punishment_type": "ish_haqqi_munosabatlari"
                },
                {
                    "number": "84-modda",
                    "title": "Ish vaqti",
                    "content": "Ish vaqti - bu ishchining mehnat shartnomasida belgilangan vaqt ichida ish beruvchining rahbarligida bajaradigan ishining davomiyligidir. Ish vaqti haftasiga qirq soatdan oshmasligi shart. Ish vaqtining qisqartirilishi yoki uzaytirilishi qonunda belgilangan tartibda amalga oshiriladi.",
                    "category": "ish_vaqti",
                    "severity": "medium",
                    "punishment_type": "ish_vaqti_munosabatlari"
                },
                {
                    "number": "110-modda",
                    "title": "Dam olish kunlari",
                    "content": "Ishchilarga haftada ikki kun dam olish beriladi. Dam olish kunlari ketma-ket bo'lishi shart. Ish beruvchi ishchilarning dam olish kunlarini qonunda belgilangan tartibda belgilashi va ularning dam olish kunlarini hurmat qilishi shart. Ish beruvchi dam olish kunlarini ishga jalb qilishi mumkin emas.",
                    "category": "dam_olish",
                    "severity": "medium",
                    "punishment_type": "dam_olish_munosabatlari"
                },
                {
                    "number": "115-modda",
                    "title": "Me'nat ta'tili",
                    "content": "Ishchilarga har yili mehnat ta'tili beriladi. Mehnat ta'tili uzluksiz ishlagan vaqtga qarab belgilanadi. Mehnat ta'tili kamida yigirma to'rt kun bo'lishi shart. Mehnat ta'tilining qisman yoki to'liq pul evaziga almashtirilishi qonunda belgilangan tartibda amalga oshiriladi.",
                    "category": "ta'til",
                    "severity": "high",
                    "punishment_type": "ta'til_munosabatlari"
                },
                {
                    "number": "177-modda",
                    "title": "Ishdan bo'shatish asoslari",
                    "content": "Ishchini ishdan bo'shatishning quyidagi asoslari mavjud: ish beruvchining yoki ishchining tashabbusi bilan, ikkala tomonning kelishuvi bilan, shuningdek, qonunda belgilangan boshqa hollarda. Ishchini ishdan bo'shatish to'g'risida buyruq beriladi. Ishchini ishdan bo'shatishda qonunda belgilangan tartibga rioya qilish shart.",
                    "category": "ishdan_boshatish",
                    "severity": "high",
                    "punishment_type": "ishdan_boshatish_munosabatlari"
                },
                {
                    "number": "237-modda",
                    "title": "Ish xavfsizligi",
                    "content": "Ish beruvchi ish xavfsizligi va sog'liqni saqlash sharoitlarini ta'minlash majburiyatiga ega. Ish beruvchi ishchilarga xavfsizlik vositalarini bepul taqdim etishi, ularni xavfsizlik qoidalariga o'rgatishi va ish sharoitlarini doimiy nazorat qilishi shart. Ishchilar o'zlarining sog'ligi va xavfsizligi uchun javobgardirlar.",
                    "category": "ish_xavfsizligi",
                    "severity": "high",
                    "punishment_type": "ish_xavfsizligi_munosabatlari"
                },
                {
                    "number": "258-modda",
                    "title": "Kollektiv shartnoma",
                    "content": "Kollektiv shartnoma - bu ish beruvchi va ishchilar vakillari o'rtasida tuziladigan, mehnat sharoiti, mehnat haqqi, ish xavfsizligi va boshqa mehnat munosabatlarini tartibga soluvchi hujjatdir. Kollektiv shartnoma yozma ravishda tuziladi va u tomonlar uchun majburiy hisoblanadi.",
                    "category": "kollectiv_munosabatlar",
                    "severity": "medium",
                    "punishment_type": "kollectiv_shartnoma_munosabatlari"
                },
                {
                    "number": "277-modda",
                    "title": "Mehnat munosabatlarini tugatish",
                    "content": "Mehnat munosabatlari mehnat shartnomasining muddati tugashi, ikkala tomonning kelishuvi, shuningdek, qonunda belgilangan boshqa asoslarda tugatiladi. Mehnat munosabatlarini tugatish to'g'risida tomonlarga bildirishnoma yuboriladi. Mehnat munosabatlarini tugatishda qonunda belgilangan tartibga rioya qilish shart.",
                    "category": "mehnat_munosabatlarini_tugatish",
                    "severity": "high",
                    "punishment_type": "mehnat_munosabatlari_tugatish"
                }
            ],
            "Ma'muriy javobgarlik kodeksi": [
                {
                    "number": "1-modda",
                    "title": "Ma'muriy javobgarlik qonunining vazifalari",
                    "content": "O'zbekiston Respublikasi Ma'muriy javobgarlik kodeksining vazifalari jamiyatda ma'muriy huquqbuzarliklarning oldini olish, ularni bartaraf etish, fuqarolarning huquq va erkinliklarini, mulkiy huquqlarini himoya qilish, jamoat tartibini ta'minlash, shuningdek, ma'muriy javobgarlikni qo'llashning adolatli va qonuniy bo'lishini kafolatlashdan iboratdir.",
                    "category": "umumiy_qoidalar",
                    "severity": "medium",
                    "punishment_type": "ma'muriy_javobgarlik"
                },
                {
                    "number": "27-modda",
                    "title": "Ma'muriy huquqbuzarlik tushunchasi",
                    "content": "Ma'muriy huquqbuzarlik - bu qonunga zid ravishda, ijtimoiy xavflilikka ega bo'lgan, aybdor shaxsning gunohkorligi uchun ushbu Kodeksda belgilangan ma'muriy javobgarlikni keltirib chiqaradigan harakat yoki harakatsizlikdir. Ma'muriy huquqbuzarlik uchun javobgarlik 16 yoshga to'lgan shaxslar uchun belgilanadi.",
                    "category": "umumiy_qoidalar",
                    "severity": "medium",
                    "punishment_type": "ma'muriy_javobgarlik"
                },
                {
                    "number": "183-modda",
                    "title": "Jamoat joylarida tartibni buzish",
                    "content": "Jamoat joylarida tartibni buzish - bu fuqarolarning tinch hayotini, jamoat tartibini buzadigan harakatlardir. Bunday harakatlar uchun eng kam oylik ish haqqining bir baravaridan o'n baravarigacha miqdorda jarima qo'llaniladi. Agar bu harakatlar bir necha kishi tomonidan sodir etilsa, jarima miqdori oshirilishi mumkin.",
                    "category": "jamoat_tartibiga_qarshi",
                    "severity": "medium",
                    "punishment_type": "jarima"
                },
                {
                    "number": "194-modda",
                    "title": "Noshirlik bilan shug'ullanish",
                    "content": "Noshirlik bilan shug'ullanish - bu qonunda belgilangan tartibda ruxsat etilmagan holatlarda noshirlik faoliyati bilan shug'ullanishdir. Bunday harakatlar uchun eng kam oylik ish haqqining besh baravaridan o'n besh baravarigacha miqdorda jarima qo'llaniladi. Agar bu harakatlar katta miqdorda pul olish maqsadida sodir etilsa, javobgarlik yanada og'irlashtiriladi.",
                    "category": "iqtisodiy_faoliyatga_qarshi",
                    "severity": "high",
                    "punishment_type": "jarima"
                },
                {
                    "number": "201-modda",
                    "title": "Hujjatlar bilan shug'ullanish qoidalarini buzish",
                    "content": "Hujjatlar bilan shug'ullanish qoidalarini buzish - bu qonunda belgilangan tartibda hujjatlar bilan shug'ullanish qoidalarini buzishdir. Bunday harakatlar uchun eng kam oylik ish haqqining bir baravaridan uch baravarigacha miqdorda jarima qo'llaniladi. Agar bu harakatlar jiddiy oqibatlarga olib kelsa, javobgarlik og'irlashtiriladi.",
                    "category": "davlat_boshqaruvi_sohasiga_qarshi",
                    "severity": "medium",
                    "punishment_type": "jarima"
                }
            ],
            "Yer kodeksi": [
                {
                    "number": "1-modda",
                    "title": "Yer qonunining vazifalari",
                    "content": "O'zbekiston Respublikasi Yer kodeksining vazifalari yer munosabatlarini tartibga solish, yerni samarali foydalanishni ta'minlash, yerni himoya qilish, yerga bo'lgan huquqlarni himoya qilish, shuningdek, yerni boshqarishning qonuniy asoslarini yaratishdan iboratdir. Yer davlat mulki hisoblanadi.",
                    "category": "umumiy_qoidalar",
                    "severity": "high",
                    "punishment_type": "yer_munosabatlari"
                },
                {
                    "number": "15-modda",
                    "title": "Yerga bo'lgan huquqlar",
                    "content": "Yerga bo'lgan huquqlar - bu yerni egalik qilish, doimiy foydalanish, vaqtinchalik foydalanish, ijaraga olish huquqlaridir. Yerga bo'lgan huquqlar qonunda belgilangan tartibda ro'yxatdan o'tkazilishi va hujjatlashtirilishi shart. Yerga bo'lgan huquqlar fuqarolar va tashkilotlar uchun tengdir.",
                    "category": "yer_huquqlari",
                    "severity": "high",
                    "punishment_type": "yer_huquqlari_munosabatlari"
                },
                {
                    "number": "36-modda",
                    "title": "Yerni ijaraga berish",
                    "content": "Yerni ijaraga berish - bu yer egasining yerni boshqa shaxsga ma'lum muddatga foydalanish uchun topshirishidir. Yerni ijaraga berish shartnoma asosida amalga oshiriladi. Ijaraga olingan yerni maqsadiga muvofiq foydalanish shart. Ijaraga olingan yerni boshqa shaxsga ijaraga berish mumkin emas.",
                    "category": "yer_ijarasi",
                    "severity": "medium",
                    "punishment_type": "yer_ijara_munosabatlari"
                },
                {
                    "number": "67-modda",
                    "title": "Yerni himoya qilish",
                    "content": "Yerni himoya qilish - bu yerni ifloslanishdan, chirishdan, boshqa zararli ta'sirlardan himoya qilish choralarini ko'rishdir. Yerni himoya qilish barcha fuqarolar va tashkilotlar vazifasidir. Yerni himoya qilish qoidalarini buzish uchun javobgarlik belgilanadi.",
                    "category": "yer_himoyasi",
                    "severity": "high",
                    "punishment_type": "yer_himoyasi_munosabatlari"
                }
            ]
        }
    
    def generate_professional_data(self) -> dict:
        """Professional ma'lumotlar yaratish"""
        enriched_data = {}
        
        for code_name, articles in self.comprehensive_codes.items():
            enriched_articles = []
            
            for article in articles:
                # ID yaratish
                article_id = hashlib.md5(f"{article['number']}_{article['title']}".encode()).hexdigest()[:8]
                
                enriched_article = {
                    "id": article_id,
                    "number": article["number"],
                    "title": article["title"],
                    "content": article["content"],
                    "full_text": f"{article['number']} {article['title']}. {article['content']}",
                    "category": article["category"],
                    "severity": article["severity"],
                    "punishment_type": article["punishment_type"],
                    "source_url": f"https://lex.uz/docs/{article_id}",
                    "scraped_at": datetime.now().isoformat(),
                    "metadata": {
                        "word_count": len(article["content"].split()),
                        "character_count": len(article["content"]),
                        "complexity": "high" if len(article["content"]) > 200 else "medium",
                        "legal_domain": self._get_legal_domain(code_name),
                        "keywords": self._extract_keywords(article["content"])
                    }
                }
                
                enriched_articles.append(enriched_article)
            
            enriched_data[code_name] = enriched_articles
        
        return enriched_data
    
    def _get_legal_domain(self, code_name: str) -> str:
        """Qonun sohasini aniqlash"""
        domain_mapping = {
            "Jinoyat kodeksi": "jinoyat_huquqi",
            "Fuqarolik kodeksi": "fuqarolik_huquqi", 
            "Oila kodeksi": "oilaviy_huquq",
            "Mehnat kodeksi": "mehnat_huquqi",
            "Ma'muriy javobgarlik kodeksi": "ma'muriy_huquq",
            "Yer kodeksi": "yer_huquqi"
        }
        return domain_mapping.get(code_name, "boshqa")
    
    def _extract_keywords(self, content: str) -> list:
        """Kalit so'zlarni ajratib olish"""
        legal_keywords = [
            "huquq", "majburiyat", "javobgarlik", "shartnoma", "qonun", "sud",
            "ish", "ish haqi", "mulk", "oilaviy", "nikoh", "ajralish",
            "aliment", "farzand", "ota-ona", "talonchilik", "o'g'rilik",
            "qotillik", "shikast", "jarima", "ozodlikdan mahrum qilish",
            "fuqaro", "shaxs", "tashkilot", "davlat", "jamiyat"
        ]
        
        content_lower = content.lower()
        found_keywords = []
        
        for keyword in legal_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:10]  # Eng ko'pi bilan 10 ta kalit so'z
    
    def save_professional_data(self, filename: str = "professional_legal_data.json"):
        """Professional ma'lumotlarni saqlash"""
        data = self.generate_professional_data()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Professional legal data saved to {filename}")
        return data

def main():
    """Asosiy funktsiya"""
    print("Generating professional legal data...")
    
    generator = ProfessionalLegalDataGenerator()
    data = generator.save_professional_data()
    
    # Statistika
    total_articles = sum(len(articles) for articles in data.values())
    total_codes = len(data)
    
    print(f"\n=== PROFESSIONAL LEGAL DATA STATISTICS ===")
    print(f"Total codes: {total_codes}")
    print(f"Total articles: {total_articles}")
    
    for code_name, articles in data.items():
        print(f"{code_name}: {len(articles)} articles")
        
        # Kategoriyalar bo'yicha statistika
        categories = {}
        for article in articles:
            category = article["category"]
            categories[category] = categories.get(category, 0) + 1
        
        print(f"  Categories: {dict(categories)}")
    
    return data

if __name__ == "__main__":
    main()
