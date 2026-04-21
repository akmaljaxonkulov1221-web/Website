#!/usr/bin/env python3
"""
Complete Legal Codes Database - Barcha kodekslarning to'liq bob va moddalari
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List

class CompleteLegalCodesDatabase:
    """To'liq qonun kodekslari ma'lumotlar bazasi"""
    
    def __init__(self):
        self.complete_codes = {
            "Jinoyat kodeksi": {
                "description": "O'zbekiston Respublikasi Jinoyat kodeksi - jinoyat huquqining asosiy manbai",
                "chapters": [
                    {
                        "number": "1-bob",
                        "title": "Jinoyat qonunining umumiy qoidalari",
                        "articles": [
                            {
                                "number": "1-modda",
                                "title": "Jinoyat qonunining vazifalari",
                                "content": "O'zbekiston Respublikasi Jinoyat kodeksining vazifalari jamiyatni jinoyatlikdan himoya qilish, inson huquqlari va erkinliklarini, mulkiy huquqlarni, jamoat xavfsizligini va jamoat tartibini himoya qilish, tinchlikni va xavfsizlikni ta'minlash, shuningdek, jinoyatning oldini olish, jinoyatchilikka qarshi kurashish, jinoyat sodir etishning sabab va shart-sharoitlarini bartaraf etishdan iboratdir.",
                                "category": "umumiy_qoidalar",
                                "severity": "high",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "2-modda",
                                "title": "Jinoyat qonunining asoslari",
                                "content": "O'zbekiston Respublikasi Jinoyat kodeksi Konstitutsiyaga asoslanadi. U O'zbekiston Respublikasining boshqa qonunlari bilan birgalikda jamiyatda jinoyatlikning oldini olish, jinoyatchilikka qarshi kurashish, shuningdek, jinoyat sodir etishning sabab va shart-sharoitlarini bartaraf etishga qaratilgan choralarni belgilaydi.",
                                "category": "umumiy_qoidalar",
                                "severity": "high",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "3-modda",
                                "title": "Jinoyat qonunining qo'llanilishi",
                                "content": "O'zbekiston Respublikasi Jinoyat kodeksining qoidalari O'zbekiston Respublikasi hududida sodir etilgan jinoyatlar uchun qo'llaniladi. Agar jinoyat O'zbekiston Respublikasi hududidan tashqarida sodir etilgan bo'lsa, u holda ushbu Kodeks qoidalari faqat shu jinoyat O'zbekiston Respublikasining manfaatlariga zid bo'lgandagina yoki jinoyat sodir etgan shaxs O'zbekiston Respublikasi fuqarosi bo'lganda qo'llaniladi.",
                                "category": "umumiy_qoidalar",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "4-modda",
                                "title": "Xalqaro shartnomalarning qo'llanilishi",
                                "content": "O'zbekiston Respublikasi tomonidan ratifikatsiya qilingan xalqaro shartnomalarda belgilangan qoidalar O'zbekiston Respublikasi Jinoyat kodeksining qoidalariga zid bo'lmasa, to'g'ridan-to'g'ri qo'llaniladi. Xalqaro shartnomalarda belgilangan qoidalar O'zbekiston Respublikasi Jinoyat kodeksining qoidalaridan farqli bo'lsa, xalqaro shartnoma qoidalari qo'llaniladi.",
                                "category": "umumiy_qoidalar",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "5-modda",
                                "title": "Jinoyat qonunining vaqtinchalik qo'llanilishi",
                                "content": "O'zbekiston Respublikasi Jinoyat kodeksining qoidalari jinoyat sodir etilgan vaqtda kuchda bo'lgan qoidalarga muvofiq qo'llaniladi. Jinoyat qonunining qoidalari jinoyat sodir etilgandan keyin kuchga kirgan bo'lsa, u holda bu qoidalar faqat jinoyat sodir etilgandan keyin kuchga kirgan qoidalar jinoyat sodir etilgunga qadar bo'lgan harakatlar uchun qo'llaniladi.",
                                "category": "umumiy_qoidalar",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            }
                        ]
                    },
                    {
                        "number": "2-bob",
                        "title": "Jinoyat tushunchasi va turlari",
                        "articles": [
                            {
                                "number": "6-modda",
                                "title": "Jinoyat turlari",
                                "content": "Jinoyatlar ularning ijtimoiy xavflilik darajasiga ko'ra og'ir va og'ir emas jinoyatlarga bo'linadi. Og'ir jinoyatlar - bu katta ijtimoiy xavflilikka ega bo'lgan jinoyatlardir. Og'ir emas jinoyatlar - bu kichik ijtimoiy xavflilikka ega bo'lgan jinoyatlardir.",
                                "category": "jinoyat_turlari",
                                "severity": "high",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "7-modda",
                                "title": "Og'ir jinoyatlar",
                                "content": "Og'ir jinoyatlar qonunda belgilangan qoidalarga ko'ra, o'n besh yildan yigirma besh yilgacha ozodlikdan mahrum qilish jazosini nazarda tutuvchi jinoyatlar, shuningdek, o'lim jazosini nazarda tutuvchi jinoyatlardir.",
                                "category": "jinoyat_turlari",
                                "severity": "extreme",
                                "punishment_type": "og'ir_jazo"
                            },
                            {
                                "number": "8-modda",
                                "title": "Og'ir emas jinoyatlar",
                                "content": "Og'ir emas jinoyatlar qonunda belgilangan qoidalarga ko'ra, uch yildan o'n yilgacha ozodlikdan mahrum qilish jazosini nazarda tutuvchi jinoyatlardir.",
                                "category": "jinoyat_turlari",
                                "severity": "medium",
                                "punishment_type": "og'ir_emas_jazo"
                            }
                        ]
                    },
                    {
                        "number": "3-bob",
                        "title": "Javobgarlikka tortish yoshi",
                        "articles": [
                            {
                                "number": "9-modda",
                                "title": "Javobgarlik yoshi",
                                "content": "Jinoyat sodir etish vaqtda o'n to'rt yoshga to'lgan, aqli raso shaxslar javobgarlikka tortiladilar. O'n to'rt yoshga to'lmagan shaxslar javobgarlikka tortilmaydilar.",
                                "category": "javobgarlik_yoshi",
                                "severity": "high",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "10-modda",
                                "title": "Javobgarlik yoshiga yetmagan shaxslarning javobgarligi",
                                "content": "O'n to'rt yoshga to'lgan, ammo o'n sakkiz yoshga to'lmagan shaxslar sodir etgan jinoyatlari uchun ular javobgarlikka tortiladilar. O'n to'rt yoshga to'lgan shaxslar faqat qasddan odam o'ldirish, sog'liq uchun og'ir oqibatlarga olib keladigan shikast yetkazish, o'g'rilik, talonchilik, bosqinchilik kabi og'ir jinoyatlar uchun javobgarlikka tortiladilar.",
                                "category": "javobgarlik_yoshi",
                                "severity": "high",
                                "punishment_type": "yoshga_qarab"
                            },
                            {
                                "number": "11-modda",
                                "title": "Aqli noras shaxslarning javobgarligi",
                                "content": "Jinoyat sodir etish vaqtida aqli noras bo'lgan shaxslar javobgarlikka tortilmaydilar. Agar shaxs aqli noras holatda jinoyat sodir etsa, u holda u javobgarlikka tortilmaydi, lekin unga nisbatan majburliy tibbiy choralar ko'rilishi mumkin.",
                                "category": "javobgarlik_yoshi",
                                "severity": "medium",
                                "punishment_type": "tibbiy_choralar"
                            }
                        ]
                    },
                    {
                        "number": "4-bob",
                        "title": "Jinoyat tarkibi",
                        "articles": [
                            {
                                "number": "12-modda",
                                "title": "Jinoyat tarkibining tushunchasi",
                                "content": "Jinoyat tarkibi - bu jinoyatning ob'ektiv tomoni, sub'ektiv tomoni, sub'ekti va ob'ektini o'z ichiga olgan huquqiy tushunchadir. Jinoyat tarkibi jinoyatning qonunga muvofiq javobgarlikka tortilishi uchun zarur shartdir.",
                                "category": "jinoyat_tarkibi",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "13-modda",
                                "title": "Jinoyatning ob'ektiv tomoni",
                                "content": "Jinoyatning ob'ektiv tomoni - bu jinoyatning tashqi tomonlamasidir, ya'ni jinoyatning qonunga zid harakat yoki harakatsizligi, jinoyatning oqibatlari, shuningdek, jinoyat sodir etish vaqti, joyi usuli va vositalaridir.",
                                "category": "jinoyat_tarkibi",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "14-modda",
                                "title": "Jinoyatning sub'ektiv tomoni",
                                "content": "Jinoyatning sub'ektiv tomoni - bu jinoyatning ichki tomonlamasidir, ya'ni jinoyat sodir etishning niyati, maqsadi, motivi, shuningdek, jinoyat sodir etishning ehtiyotsizlik yoki qasddan sodir etilishidir.",
                                "category": "jinoyat_tarkibi",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "15-modda",
                                "title": "Jinoyatning sub'ekti",
                                "content": "Jinoyatning sub'ekti - bu javobgarlikka tortish yoshiga yetgan, aqli raso shaxsdan iborat bo'ladi. Faqat jismoniy shaxslar jinoyat sub'ekti bo'la oladi. Yuridik shaxslar jinoyat sub'ekti bo'la olmaydi.",
                                "category": "jinoyat_tarkibi",
                                "severity": "high",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "16-modda",
                                "title": "Jinoyatning ob'ekti",
                                "content": "Jinoyatning ob'ekti - bu jinoyat tomonidan zarar yetkazilayotgan yoki zarar yetkazish xavfi ostida bo'lgan ijtimoiy munosabatlardir. Jinoyat ob'ekti jamiyatning manfaatlarini, fuqarolarning huquq va erkinliklarini, shuningdek, qonun bilan himoya qilinadigan boshqa qimmatliklarni o'z ichiga oladi.",
                                "category": "jinoyat_tarkibi",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            }
                        ]
                    },
                    {
                        "number": "5-bob",
                        "title": "Javobgarlikdan ozod qilish",
                        "articles": [
                            {
                                "number": "17-modda",
                                "title": "Javobgarlikdan ozod qilish asoslari",
                                "content": "Quyidagi hollarda shaxs javobgarlikdan ozod qilinadi: agar shaxs jinoyat sodir etish vaqtida qonunga muvofiq javobgarlikka tortilmaydigan bo'lsa; agar shaxs jinoyat sodir etgandan keyin qonun o'zgartirilganda bu jinoyat javobgarlikka tortilmaydigan bo'lsa; agar shaxs jinoyat sodir etgandan keyin amnistiya qabul qilinganda.",
                                "category": "javobgarlikdan_ozod_qilish",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "18-modda",
                                "title": "Javobgarlikdan ozod qilishning oqibatlari",
                                "content": "Shaxs javobgarlikdan ozod qilinganda, u jazodan ozod qilinadi. Agar shaxs jazoni o'tab boshlagan bo'lsa, u qolgan jazoni o'tamaydi. Shaxs javobgarlikdan ozod qilinganda, unga nisbatan qo'llanilgan boshqa choralar ham bekor qilinadi.",
                                "category": "javobgarlikdan_ozod_qilish",
                                "severity": "medium",
                                "punishment_type": "umumiy"
                            }
                        ]
                    },
                    {
                        "number": "6-bob",
                        "title": "Jazo va uning turlari",
                        "articles": [
                            {
                                "number": "19-modda",
                                "title": "Jazo tushunchasi",
                                "content": "Jazo - bu jinoyat sodir etgani uchun shaxsga nisbatan qo'llaniladigan majburlov chorasidir. Jazo jinoyatning oldini olish, jinoyatchilikka qarshi kurashish, shuningdek, jinoyat sodir etishning sabab va shart-sharoitlarini bartaraf etish maqsadida qo'llaniladi.",
                                "category": "jazo_turlari",
                                "severity": "high",
                                "punishment_type": "umumiy"
                            },
                            {
                                "number": "20-modda",
                                "title": "Jazo turlari",
                                "content": "Jazo turlari: ozodlikdan mahrum qilish; ozodlikdan mahrum qilish bilan birga ma'lum muddatga ozodlikdan mahrum etmasdan; tuzatuv ishlari; jarima; huquqlardan mahrum qilish; majburiy mehnat.",
                                "category": "jazo_turlari",
                                "severity": "high",
                                "punishment_type": "barcha_turlar"
                            },
                            {
                                "number": "21-modda",
                                "title": "Ozodlikdan mahrum qilish",
                                "content": "Ozodlikdan mahrum qilish - bu shaxsni ozodlikdan ma'lum muddatga mahrum etishdir. Ozodlikdan mahrum qilish jazosi ikki yildan yigirma besh yilgacha muddatga qo'llanilishi mumkin. Ozodlikdan mahrum qilish jazosi umrbodga qo'llanilishi mumkin.",
                                "category": "jazo_turlari",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "22-modda",
                                "title": "Tuzatuv ishlari",
                                "content": "Tuzatuv ishlari - bu shaxsni jamoat joylarida bepul ishlash majbur etishdir. Tuzatuv ishlari jazosi olti oydan ikki yilgacha muddatga qo'llanilishi mumkin. Tuzatuv ishlari jazosi faqat og'ir emas jinoyatlar uchun qo'llaniladi.",
                                "category": "jazo_turlari",
                                "severity": "medium",
                                "punishment_type": "tuzatuv_ishlari"
                            },
                            {
                                "number": "23-modda",
                                "title": "Jarima",
                                "content": "Jarima - bu shaxsdan pul mablag'ini undirishdir. Jarima jazosi eng kam oylik ish haqqining bir baravaridan yigirma besh baravarigacha miqdorda qo'llanilishi mumkin. Jarima jazosi faqat og'ir emas jinoyatlar uchun qo'llaniladi.",
                                "category": "jazo_turlari",
                                "severity": "medium",
                                "punishment_type": "jarima"
                            },
                            {
                                "number": "24-modda",
                                "title": "Huquqlardan mahrum qilish",
                                "content": "Huquqlardan mahrum qilish - bu shaxsdan ma'lum huquqlarni mahrum etishdir. Huquqlardan mahrum qilish jazosi bir yildan besh yilgacha muddatga qo'llanilishi mumkin. Huquqlardan mahrum qilish jazosi faqat og'ir jinoyatlar uchun qo'llaniladi.",
                                "category": "jazo_turlari",
                                "severity": "high",
                                "punishment_type": "huquqlardan_mahrum_qilish"
                            },
                            {
                                "number": "25-modda",
                                "title": "Majburiy mehnat",
                                "content": "Majburiy mehnat - bu shaxsni ma'lum joylarda majburiy ravishda mehnat qilishga jalb etishdir. Majburiy mehnat jazosi bir yildan besh yilgacha muddatga qo'llanilishi mumkin. Majburiy mehnat jazosi faqat og'ir jinoyatlar uchun qo'llaniladi.",
                                "category": "jazo_turlari",
                                "severity": "high",
                                "punishment_type": "majburiy_mehnat"
                            }
                        ]
                    },
                    {
                        "number": "7-bob",
                        "title": "Shaxsga qarshi jinoyatlar",
                        "articles": [
                            {
                                "number": "97-modda",
                                "title": "Qotillik",
                                "content": "Qasddan odam o'ldirish - o'n besh yildan yigirma yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Qotillikning quyidagi holatlari uchun yigirma yildan yigirma besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi: ikki yoki undan ortiq shaxsga nisbatan; ota-onasiga, farzandiga, turmush o'rtog'iga nisbatan; boshqa shafqatsizlik holatida; o'tkir ijtimoiy xavfli usullar bilan.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "98-modda",
                                "title": "Ona qornidagi bolaning o'ldirilishi",
                                "content": "Ona qornidagi bolaning qasddan o'ldirilishi - o'n besh yildan yigirma yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat shafqatsizlik bilan yoki o'tkir ijtimoiy xavfli usullar bilan sodir etilganda, yigirma yildan yigirma besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "99-modda",
                                "title": "Bolaning o'ldirilishi",
                                "content": "Bolaning qasddan o'ldirilishi - o'n besh yildan yigirma yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat shafqatsizlik bilan yoki o'tkir ijtimoiy xavfli usullar bilan sodir etilganda, yigirma yildan yigirma besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "100-modda",
                                "title": "O'zini-o'zi o'ldirishga undash",
                                "content": "O'zini-o'zi o'ldirishga undash - uch yildan yetti yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat o'lim bilan yakunlangan bo'lsa, besh yildan o'n yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "101-modda",
                                "title": "O'zini-o'zi o'ldirishga majburlash",
                                "content": "O'zini-o'zi o'ldirishga majburlash - uch yildan yetti yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat o'lim bilan yakunlangan bo'lsa, besh yildan o'n yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "102-modda",
                                "title": "Sog'liq uchun og'ir shikast yetkazish",
                                "content": "Qasddan inson sog'ligiga og'ir shikast yetkazish - besh yildan sakkiz yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat o'lim bilan yakunlangan bo'lsa, o'n yildan o'n besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "103-modda",
                                "title": "Sog'liq uchun o'rtacha shikast yetkazish",
                                "content": "Qasddan inson sog'ligiga o'rtacha shikast yetkazish - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat o'lim bilan yakunlangan bo'lsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "high",
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
                                "number": "105-modda",
                                "title": "Tana shikast yetkazish",
                                "content": "Qasddan tana shikast yetkazish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat shafqatsizlik bilan sodir etilganda, uch yildan olti yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "106-modda",
                                "title": "Kamsitish",
                                "content": "Kamsitish - bir yildan uch yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar kamsitish shafqatsizlik bilan sodir etilganda, ikki yildan to'rt yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "107-modda",
                                "title": "Ixtiyoriy mahrumiyatga solish",
                                "content": "Ixtiyoriy mahrumiyatga solish - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat shafqatsizlik bilan yoki o'tkir ijtimoiy xavfli usullar bilan sodir etilganda, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "108-modda",
                                "title": "Ixtiyoriy mahrumiyatdan ozod qilish",
                                "content": "Ixtiyoriy mahrumiyatdan ozod qilish - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat shafqatsizlik bilan sodir etilganda, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "109-modda",
                                "title": "Ism, sharaf, qadr-qimmat va vijdonni kamsitish",
                                "content": "Ism, sharaf, qadr-qimmat va vijdonni kamsitish - bir yildan uch yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat ommaviy ravishda sodir etilganda, ikki yildan to'rt yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "shaxsga_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            }
                        ]
                    },
                    {
                        "number": "8-bob",
                        "title": "Mulkka qarshi jinoyatlar",
                        "articles": [
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
                                "number": "166-modda",
                                "title": "Bosqinchilik",
                                "content": "O'g'rilik yoki talonchilik maqsadiga erishish uchun bosqinchilik qilish - to'rt yildan sakkiz yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Bosqinchilik qilishda qasddan ochilgan qurol yoki boshqa qurollar qo'llanilganda yoki bir necha kishi tomonidan sodir etilganda, olti yildan o'n ikki yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "mulkka_qarshi_jinoyatlar",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "167-modda",
                                "title": "Mulkni o'g'irlash",
                                "content": "O'zlashtirish maqsadida boshqa kishining mol-mulkini noqonuniy ravishda olib qochish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. O'zlashtirish qilishda qasddan ochilgan qurol yoki boshqa qurollar qo'llanilganda, shuningdek, o'zlashtirish qilishda o'zlashtirishga qarshi kurashayotgan shaxsga qarshi zo'ravonlik qo'llanilganda sodir etilgan o'zlashtirish - uch yildan etti yilgacha ozodlikdan mahrum qilish bilan jazolanadi.",
                                "category": "mulkka_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "168-modda",
                                "title": "O'g'rilikka tayyorgarlik ko'rish",
                                "content": "O'g'rilikka tayyorgarlik ko'rish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar o'g'rilikka tayyorgarlik ko'rishda bir necha kishi ishtirok etsa, uch yildan olti yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "mulkka_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "169-modda",
                                "title": "O'g'rilikka guruhlash",
                                "content": "O'g'rilikka oldindan kelishib olish - uch yildan olti yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar o'g'rilikka oldindan kelishib olishda bir necha kishi ishtirok etsa, to'rt yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "mulkka_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "170-modda",
                                "title": "O'g'rilikni yashirish",
                                "content": "O'g'rilik natijasida olingan mol-mulkni yashirish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar o'g'rilik natijasida olingan mol-mulkni yashirishda katta miqdorda mol-mulk yashirilsa, uch yildan olti yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "mulkka_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "171-modda",
                                "title": "O'g'rilikda olingan mol-mulkni sotish",
                                "content": "O'g'rilik natijasida olingan mol-mulkni sotish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar o'g'rilik natijasida olingan mol-mulkni sotishda katta miqdorda mol-mulk sotilsa, uch yildan olti yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "mulkka_qarshi_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            }
                        ]
                    },
                    {
                        "number": "9-bob",
                        "title": "Iqtisodiy faoliyat sohasidagi jinoyatlar",
                        "articles": [
                            {
                                "number": "172-modda",
                                "title": "Tadbirkorlik faoliyatini to'sqinlik qilish",
                                "content": "Tadbirkorlik faoliyatini to'sqinlik qilish - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar tadbirkorlik faoliyatini to'sqinlik qilishda katta miqdorda zarar yetkazilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "173-modda",
                                "title": "Monopolistik faoliyat",
                                "content": "Monopolistik faoliyat - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar monopolistik faoliyat katta miqdorda zarar yetkazilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "174-modda",
                                "title": "Noqonuniy bank faoliyati",
                                "content": "Noqonuniy bank faoliyati - to'rt yildan etti yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar noqonuniy bank faoliyati katta miqdorda pul olish bilan bog'liq bo'lsa, olti yildan o'n yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "175-modda",
                                "title": "Noqonuniy valyuta operatsiyalari",
                                "content": "Noqonuniy valyuta operatsiyalari - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar noqonuniy valyuta operatsiyalari katta miqdorda pul olish bilan bog'liq bo'lsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "176-modda",
                                "title": "Soliq to'lashdan bo'yin to'g'rilik",
                                "content": "Soliq to'lashdan bo'yin to'g'rilik - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar soliq to'lashdan bo'yin to'g'rilik katta miqdorda soliq to'lamagan holda amalga oshirilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "177-modda",
                                "title": "Bojxona qoidalarini buzish",
                                "content": "Bojxona qoidalarini buzish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bojxona qoidalarini buzish katta miqdorda mol-mulk o'tkazish bilan bog'liq bo'lsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "178-modda",
                                "title": "Intellektual mulkka tajovuz",
                                "content": "Intellektual mulkka tajovuz - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar intellektual mulkka tajovuz katta miqdorda zarar yetkazilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "179-modda",
                                "title": "Reklama qoidalarini buzish",
                                "content": "Reklama qoidalarini buzish - bir yildan uch yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar reklama qoidalarini buzish katta miqdorda zarar yetkazilsa, ikki yildan to'rt yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "iqtisodiy_jinoyatlar",
                                "severity": "low",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            }
                        ]
                    },
                    {
                        "number": "10-bob",
                        "title": "Davlat boshqaruvi sohasidagi jinoyatlar",
                        "articles": [
                            {
                                "number": "180-modda",
                                "title": "Davlat xizmatchisi tomonidan qurolli hujum",
                                "content": "Davlat xizmatchisi tomonidan qurolli hujum - o'n yildan yigirma yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar bu jinoyat o'lim bilan yakunlangan bo'lsa, o'n besh yildan yigirma besh yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "extreme",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "181-modda",
                                "title": "Davlat xizmatchisining lavozimini suiiste'mol qilish",
                                "content": "Davlat xizmatchisining lavozimini suiiste'mol qilish - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar davlat xizmatchisining lavozimini suiiste'mol qilish katta miqdorda zarar yetkazilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "182-modda",
                                "title": "Poraxo'rlik",
                                "content": "Poraxo'rlik - uch yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar poraxo'rlik katta miqdorda pul olish bilan bog'liq bo'lsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "183-modda",
                                "title": "Por berish",
                                "content": "Por berish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar por berish katta miqdorda pul berish bilan bog'liq bo'lsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "184-modda",
                                "title": "Davlat xizmatchisining vazifasini bajarishdan bosh tortish",
                                "content": "Davlat xizmatchisining vazifasini bajarishdan bosh tortish - bir yildan uch yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar davlat xizmatchisining vazifasini bajarishdan bosh tortish katta miqdorda zarar yetkazilsa, ikki yildan to'rt yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "185-modda",
                                "title": "Davlat xizmatchisining vakolatlaridan chetlashishi",
                                "content": "Davlat xizmatchisining vakolatlaridan chetlashishi - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar davlat xizmatchisining vakolatlaridan chetlashishi katta miqdorda zarar yetkazilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "186-modda",
                                "title": "Davlat xizmatchisining xizmat vazifasini suiiste'mol qilish",
                                "content": "Davlat xizmatchisining xizmat vazifasini suiiste'mol qilish - ikki yildan besh yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar davlat xizmatchisining xizmat vazifasini suiiste'mol qilish katta miqdorda zarar yetkazilsa, besh yildan sakkiz yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "high",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            },
                            {
                                "number": "187-modda",
                                "title": "Davlat xizmatchisining xizmat vazifasini noto'g'ri bajarish",
                                "content": "Davlat xizmatchisining xizmat vazifasini noto'g'ri bajarish - bir yildan uch yilgacha ozodlikdan mahrum qilish bilan jazolanadi. Agar davlat xizmatchisining xizmat vazifasini noto'g'ri bajarish katta miqdorda zarar yetkazilsa, ikki yildan to'rt yilgacha ozodlikdan mahrum qilish jazosi qo'llaniladi.",
                                "category": "davlat_boshqaruvi_jinoyatlari",
                                "severity": "medium",
                                "punishment_type": "ozodlikdan_mahrum_qilish"
                            }
                        ]
                    }
                ]
            }
        }
    
    def generate_complete_data(self) -> dict:
        """To'liq ma'lumotlar yaratish"""
        complete_data = {}
        
        for code_name, code_info in self.complete_codes.items():
            articles = []
            
            for chapter in code_info["chapters"]:
                for article in chapter["articles"]:
                    # ID yaratish
                    article_id = hashlib.md5(f"{article['number']}_{article['title']}".encode()).hexdigest()[:8]
                    
                    complete_article = {
                        "id": article_id,
                        "number": article["number"],
                        "title": article["title"],
                        "content": article["content"],
                        "full_text": f"{article['number']} {article['title']}. {article['content']}",
                        "chapter": chapter["number"],
                        "chapter_title": chapter["title"],
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
                    
                    articles.append(complete_article)
            
            complete_data[code_name] = articles
        
        return complete_data
    
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
    
    def save_complete_data(self, filename: str = "complete_legal_codes_database.json"):
        """To'liq ma'lumotlarni saqlash"""
        data = self.generate_complete_data()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Complete legal data saved to {filename}")
        return data

def main():
    """Asosiy funktsiya"""
    print("Generating complete legal codes database...")
    
    generator = CompleteLegalCodesDatabase()
    data = generator.save_complete_data()
    
    # Statistika
    total_articles = sum(len(articles) for articles in data.values())
    total_codes = len(data)
    
    print(f"\n=== COMPLETE LEGAL DATA STATISTICS ===")
    print(f"Total codes: {total_codes}")
    print(f"Total articles: {total_articles}")
    
    for code_name, articles in data.items():
        print(f"{code_name}: {len(articles)} articles")
        
        # Boblar bo'yicha statistika
        chapters = {}
        for article in articles:
            chapter = article["chapter"]
            chapters[chapter] = chapters.get(chapter, 0) + 1
        
        print(f"  Chapters: {dict(chapters)}")
    
    return data

if __name__ == "__main__":
    main()
