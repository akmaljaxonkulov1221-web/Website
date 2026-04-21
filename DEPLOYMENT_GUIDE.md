# Deploy Qo'llanmas

## 🚀 Variant 1: Birlashtirilgan Tizim

Professional Legal System ichiga Case-Law Interactive qo'shilgan.

**Imkoniyatlari:**
- ✅ Bitta saytda ikkala tizim
- ✅ Port 5005 da Professional Legal System
- ✅ Port 5006 da Case-Law Interactive
- ✅ Umumiy ma'lumotlar almashinadi

**Ishga tushirish:**
1. Professional Legal System ni ishga tushirish:
   ```bash
   python professional_legal_app.py
   ```

2. Case-Law Interactive ga kirish:
   - Professional Legal System asosiy sahifasida
   - `/case_law` tugmasi orqali

## 🚀 Variant 2: Alohida Deploy

Ikkala tizimni alohida deploy qilish.

**Imkoniyatlari:**
- ✅ Har bir tizim alohida ishlaydi
- ✅ Mustahil resurslardan foydalanish
- ✅ Mustahil scaling imkoniyati

**Deploy qilish:**
1. **Professional Legal System** uchun:
   - Render.com da mavjud service'ni yangilash
   - Manual Deploy qilish

2. **Case-Law Interactive** uchun:
   - Render.com da yangi service yaratish
   - `render_case_law.yaml` faylini ishlatish

## 🎯 Tavsiya

**Birlashtirilgan tizim** tavsiya etiladi, chunki:
- Bitta saytda ikkala funksiyani boshqarish osonroq
- Umumiy ma'lumotlar almashinadi
- Foydalanuvchilar bir tizimdan ikkinchasiga o'tishi mumkin

## 📋 Deploy Qadamlari

### Professional Legal System
1. Render.com ga kiring
2. Legal Service'ingizni oching
3. **"Manual Deploy"** → **"Deploy latest commit"** deb bosing

### Case-Law Interactive
1. Render.com da **"New +"** tugmasini bosing
2. **"Web Service"** tanlang
3. **Name:** `case-law-interactive`
4. **Branch:** `main`
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `python case_law_interactive.py`
7. **Environment Variables:**
   - `FLASK_ENV`: `production`
   - `PORT`: `5006`

## 🔍 Tekshirish

### Professional Legal System
- URL: http://localhost:5005
- Route: `/case_law` - Case-Law Interactive ga kirish

### Case-Law Interactive
- URL: http://localhost:5006
- Barcha funksiyalar ishlashi kerak

---

**Tanlangan variantni qo'llab qiling:** 🎯
