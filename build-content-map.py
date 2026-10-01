# -*- coding: utf-8 -*-
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PURPLE = "4A3463"; CREAM = "FBF8F2"; GOLD = "C9A86A"; GREY = "8A8A8A"

# date, platform, topic, format, reach, nonfollow, shares, saves, comments, visits, follows, leads, learned, link
IG = "אינסטגרם"
R = "ריל"; C = "קרוסלה"; P = "תמונה"

ten = [
 ("17.09", IG, "מצלמות סרטונים לסושיאל, מאחורי הקלעים", R, 79, None, 2, 1, 0, None, None, None,
  "הריל היחיד מתוך העשרה שמישהי שלחה הלאה, וגם החשיפה הגבוהה ביותר. תוכן שמראה אותך עובדת מייצר שיתוף, לא רק צפייה.",
  "https://www.instagram.com/reel/DdZfL-QxMVx/"),
 ("16.09", IG, "מבחן הצ׳ק, מילים שאפשר לפרוע", R, 25, None, 0, 1, 0, None, None, None,
  "אותו רעיון בדיוק כמו הקרוסלה של אותו יום. הריל הביא פי שלושה חשיפה מהקרוסלה.",
  "https://www.instagram.com/reel/DdWW35_sx8R/"),
 ("16.09", IG, "מבחן הצ׳ק, מילים שאפשר לפרוע", C, 8, None, None, 0, 0, None, 0, None,
  "יצאה באותו יום עם הריל, התחלקה איתו בקהל וכמעט לא נראתה. לא להוציא את אותו רעיון בשני פורמטים באותו יום.",
  "https://www.instagram.com/p/DdW2l1YDIgH/"),
 ("15.09", IG, "חתימת קול, שלוש שאלות", R, 7, None, 0, 1, 0, None, None, None,
  "חשיפה נמוכה מאוד אבל שמירה אחת מתוך שבע. הרעיון עובד, ההפצה לא.",
  "https://www.instagram.com/reel/DdUT8Plxke_/"),
 ("15.09", IG, "חתימת קול, שלוש שאלות", C, 7, None, None, 2, 0, None, 0, None,
  "שתי שמירות מתוך שבע. אחוז השמירה הגבוה ביותר בעשרה אחרי ה-10.09. תוכן של שאלות ותרגילים נשמר.",
  "https://www.instagram.com/p/DdURzeEDExY/"),
 ("14.09", IG, "היי יקרה או בואי נדבר תכלס", P, 11, None, None, 2, 0, None, 0, None,
  "תמונה בודדת עם שאלה ישירה. שתי שמירות ואפס תגובות, למרות שהשאלה נשאלה בגוף הפוסט.",
  "https://www.instagram.com/p/DdRZ2Y0M3qe/"),
 ("10.09", IG, "הצבעים של החגים, ברכת שנה טובה", R, 22, None, 0, 2, 1, None, None, None,
  "התגובה היחידה בכל העשרה. נושא רגשי וחגיגי, זה מה שהוציא מישהי מהגלילה.",
  "https://www.instagram.com/reel/DdHZmE2x8-K/"),
 ("10.09", IG, "הצבעים של החגים, ברכת שנה טובה", C, 4, None, None, 1, 1, None, 0, None,
  "ארבע חשיפות בלבד. אחוז החיבור של 50% הוא אדם אחד, אל תסיקי ממנו כלום.",
  "https://www.instagram.com/p/DdHbA5wkUsR/"),
 ("09.09", IG, "מה לא עובר איתך לשנה הבאה", R, 13, None, 0, 1, 0, None, None, None,
  "ריל ראש השנה. שמירה אחת, אפס שיתופים, אפס תגובות.",
  "https://www.instagram.com/reel/DdErJQMs5mk/"),
 ("08.09", IG, "לוגוטייפ בשתי דקות", R, 13, None, 0, 0, 0, None, None, None,
  "הנושא הכי מעשי בעשרה, עם קריאה לפעולה ישירה, והכי פחות הניע. אפס שמירות ואפס תגובות.",
  "https://www.instagram.com/reel/DdCOiRoxA65/"),
]

# all content Aug 25 to Sep 17
allc = [
 ("17.09", R, "מצלמות סרטונים לסושיאל", 79, 2, 1, 0, 96, 12.1, 34.9, "https://www.instagram.com/reel/DdZfL-QxMVx/"),
 ("16.09", R, "מבחן הצ׳ק", 25, 0, 1, 0, 28, 11.2, 50.0, "https://www.instagram.com/reel/DdWW35_sx8R/"),
 ("16.09", C, "מבחן הצ׳ק", 8, None, 0, 0, 20, None, None, "https://www.instagram.com/p/DdW2l1YDIgH/"),
 ("15.09", R, "חתימת קול", 7, 0, 1, 0, 13, 20.2, 60.0, "https://www.instagram.com/reel/DdUT8Plxke_/"),
 ("15.09", C, "חתימת קול, שלוש שאלות", 7, None, 2, 0, 22, None, None, "https://www.instagram.com/p/DdURzeEDExY/"),
 ("14.09", P, "היי יקרה או תכלס", 11, None, 2, 0, 17, None, None, "https://www.instagram.com/p/DdRZ2Y0M3qe/"),
 ("10.09", R, "הצבעים של החגים", 22, 0, 2, 1, 27, 15.7, 65.2, "https://www.instagram.com/reel/DdHZmE2x8-K/"),
 ("10.09", C, "הצבעים של החגים", 4, None, 1, 1, 10, None, None, "https://www.instagram.com/p/DdHbA5wkUsR/"),
 ("09.09", R, "מה לא עובר לשנה הבאה", 13, 0, 1, 0, 17, 9.9, 33.3, "https://www.instagram.com/reel/DdErJQMs5mk/"),
 ("08.09", R, "לוגוטייפ בשתי דקות", 13, 0, 0, 0, 16, 14.3, 53.8, "https://www.instagram.com/reel/DdCOiRoxA65/"),
 ("07.09", R, "מספר אחד שקובע, שני פונטים", 17, 0, 1, 0, 19, 9.9, 46.7, "https://www.instagram.com/reel/Dc_qjY-RnlV/"),
 ("06.09", R, "שניים, זה כל מה שצריך", 14, 0, 0, 0, 18, 11.4, 28.6, "https://www.instagram.com/reel/Dc9MbIZxtJu/"),
 ("06.09", C, "פונטים, איך בוחרים את השניים", 16, None, 2, 0, 31, None, None, "https://www.instagram.com/p/Dc9GC-GkQWz/"),
 ("03.09", R, "ללא תיאור בקובץ", 16, 0, 0, 0, 26, 7.1, 44.4, "https://www.instagram.com/reel/Dc1I0t8RSh3/"),
 ("02.09", R, "מטר אחורה מהמסך", 65, 0, 1, 0, 84, 8.0, 44.9, "https://www.instagram.com/reel/Dcy4_lvRnil/"),
 ("01.09", R, "60/30/10 גרסה קצרה", 9, 0, 0, 0, 16, 12.6, 66.7, "https://www.instagram.com/reel/DcwO0R_N79j/"),
 ("01.09", R, "ללא תיאור בקובץ", 11, 0, 0, 0, 19, 7.0, 50.0, "https://www.instagram.com/reel/DcwOSuGxsMB/"),
 ("01.09", R, "60/30/10 לצבעים", 68, 0, 1, 0, 85, 9.7, 20.5, "https://www.instagram.com/reel/DcwOQksRpDY/"),
 ("31.08", R, "אף אחד לא יגיד לך את זה בפנים", 25, 0, 1, 1, 40, 34.3, 72.0, "https://www.instagram.com/reel/Dctoqz_RZ1t/"),
 ("30.08", R, "זה לא הלוגו", 9, 0, 1, 0, 16, 19.5, 50.0, "https://www.instagram.com/reel/DcrD2kZMvdT/"),
 ("27.08", R, "מיתוג זה לא רק לוגו", 20, 0, 1, 0, 43, 9.1, 62.5, "https://www.instagram.com/reel/DciZyAtR68L/"),
 ("27.08", C, "ללא תיאור בקובץ", 22, None, 1, 1, 42, None, None, "https://www.instagram.com/p/DcjXsLFEaC6/"),
 ("26.08", C, "ללא תיאור בקובץ", 0, None, 0, 0, 0, None, None, "https://www.instagram.com/p/DchLlrMkQk0/"),
 ("25.08", R, "ריל ההיכרות, שעות על עיצוב אחד", 131, 1, 1, 4, 187, 13.8, 49.7, "https://www.instagram.com/reel/DceW21bxJUA/"),
 ("25.08", R, "ללא תיאור בקובץ", 27, 0, 1, 0, 35, 17.1, 40.9, "https://www.instagram.com/reel/DceWDwgRUYH/"),
 ("25.08", R, "ללא תיאור בקובץ", 9, 0, 1, 0, 14, 28.3, 44.4, "https://www.instagram.com/reel/DceRtlRxv6n/"),
 ("25.08", R, "ללא תיאור בקובץ", 115, 0, 0, 0, 126, 7.4, 17.9, "https://www.instagram.com/reel/Dcd_K_YM4lR/"),
]

wb = Workbook()

thin = Side(style="thin", color="DDD5E0")
bord = Border(left=thin, right=thin, top=thin, bottom=thin)

def hdr(ws, row, cols, fill=PURPLE, color="FFFFFF"):
    for i, v in enumerate(cols, start=2):
        c = ws.cell(row=row, column=i, value=v)
        c.font = Font(bold=True, color=color, size=10, name="Arial")
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = bord

# ---------- tab 1 ----------
ws = wb.active
ws.title = "מפת תוכן"
ws.sheet_view.rightToLeft = True

ws["B1"] = "מפת התוכן שלי"
ws["B1"].font = Font(bold=True, size=18, color=PURPLE, name="Arial")
ws["B2"] = "10 התכנים האחרונים, 08.09 עד 17.09. הנתונים נמשכו מ-Metricool ב-21.09.2026."
ws["B2"].font = Font(size=10, color=GREY, name="Arial")
ws["B3"] = "הסיווג גילוי / חיבור / פעולה הוא אינדיקציה יחסית בתוך העשרה, לא אמת מוחלטת. בחשיפה מתחת ל-10 כל אחוז הוא אדם בודד."
ws["B3"].font = Font(size=10, color=GREY, name="Arial")

for i, t in enumerate(["גילוי", "חיבור", "פעולה"]):
    c = ws.cell(row=5, column=15 + i, value=t)
    c.font = Font(bold=True, size=10, color=PURPLE, name="Arial")
    c.fill = PatternFill("solid", fgColor="EFE9F3")
    c.alignment = Alignment(horizontal="center")

cols = ["#", "תאריך", "סוג תוכן", "כותרת / נושא", "פורמט", "Reach", "% לא עוקבים",
        "Sends / Shares", "Saves", "Replies / Comments", "Profile visits", "Follows",
        "DMs / Clicks / Leads", "Send rate", "Connection rate", "Action rate",
        "תפקיד אוטומטי", "מה למדתי", "לינק לפוסט"]
hdr(ws, 6, cols)

def rate(n, d):
    if n is None or not d:
        return None
    return n / d

rows_calc = []
for n, r in enumerate(ten, start=1):
    date, plat, topic, fmt, reach, nonf, sh, sv, cm, pv, fo, lead, learned, link = r
    send = rate(sh, reach)
    conn = rate((sv or 0) + (cm or 0), reach)
    rows_calc.append((send, conn, reach))

best_send = max((s for s, c, rc in rows_calc if s), default=0)
conns = sorted((c for s, c, rc in rows_calc if c is not None), reverse=True)
conn_cut = conns[4] if len(conns) > 5 else 0

for n, r in enumerate(ten, start=1):
    date, plat, topic, fmt, reach, nonf, sh, sv, cm, pv, fo, lead, learned, link = r
    send, conn, _ = rows_calc[n - 1]
    if send and send >= best_send:
        role = "גילוי"
    elif conn and conn >= conn_cut:
        role = "חיבור" if reach >= 10 else "חיבור, אבל על מדגם זעיר"
    elif conn:
        role = "חיבור חלש"
    else:
        role = "לא הניע כלום"
    vals = [n, date, plat, topic, fmt, reach, "אין ב-Metricool", sh if sh is not None else "אין נתון",
            sv, cm, "אין ב-Metricool", fo if fo is not None else "אין נתון",
            lead if lead is not None else 0, send, conn, "אין נתון", role, learned, link]
    row = 6 + n
    for i, v in enumerate(vals, start=2):
        c = ws.cell(row=row, column=i, value=v)
        c.font = Font(size=10, name="Arial")
        c.border = bord
        c.alignment = Alignment(vertical="center", wrap_text=(i in (5, 19)))
        if i in (15, 16, 17):
            c.number_format = "0.0%"
            c.alignment = Alignment(horizontal="center", vertical="center")
        if i in (2, 3, 6, 7, 9, 10, 11, 13):
            c.alignment = Alignment(horizontal="center", vertical="center")
        if v in ("אין ב-Metricool", "אין נתון"):
            c.font = Font(size=10, color="B0A8B8", italic=True, name="Arial")
        if i == 18:
            c.font = Font(size=10, bold=True, name="Arial",
                          color={"גילוי": "1F7A4D", "חיבור": PURPLE, "חיבור, אבל על מדגם זעיר": "8E7AA0"}.get(v, GREY))
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if i == 20:
            c.font = Font(size=9, color="5A6FA8", name="Arial")
    ws.row_dimensions[row].height = 46
    if row % 2 == 1:
        for i in range(2, 21):
            if ws.cell(row=row, column=i).fill.fgColor.rgb in (None, "00000000"):
                ws.cell(row=row, column=i).fill = PatternFill("solid", fgColor=CREAM)

w = {2: 4, 3: 8, 4: 11, 5: 30, 6: 9, 7: 8, 8: 14, 9: 14, 10: 8, 11: 17, 12: 13, 13: 9,
     14: 17, 15: 11, 16: 15, 17: 11, 18: 20, 19: 52, 20: 40}
for k, v in w.items():
    ws.column_dimensions[get_column_letter(k)].width = v
ws.freeze_panes = "C7"

note = 18
ws.cell(row=note, column=2, value="שתי עמודות ריקות ולמה")
ws.cell(row=note, column=2).font = Font(bold=True, size=12, color=PURPLE, name="Arial")
for i, line in enumerate([
    "% לא עוקבים ו-Profile visits לא קיימים ב-Metricool בכלל, לא ברמת הפוסט הבודד.",
    "כדי למלא אותן צריך להיכנס לכל פוסט באינסטגרם, ללחוץ על הצפיות ולקרוא את המספר ידנית.",
    "אפשרות שנייה: Meta Business Suite במחשב, לשונית תוכן, תצוגת טבלה. שם רואים את כל הפוסטים בשורה אחת.",
    "Sends / Shares ריק בכל הקרוסלות והתמונות. Metricool מגיש שיתופים רק בריילס בחשבון הזה.",
], start=1):
    c = ws.cell(row=note + i, column=2, value=line)
    c.font = Font(size=10, name="Arial")

# ---------- tab 2 ----------
ws2 = wb.create_sheet("סיכום")
ws2.sheet_view.rightToLeft = True
ws2["B1"] = "סיכום, מה הנתונים אומרים"
ws2["B1"].font = Font(bold=True, size=18, color=PURPLE, name="Arial")
ws2["B2"] = "מבוסס על 10 התכנים שבלשונית מפת תוכן, ועל כל 27 התכנים שבלשונית כל התוכן."
ws2["B2"].font = Font(size=10, color=GREY, name="Arial")

facts = [
 ("סך החשיפה של עשרת האחרונים", "189", "ממוצע 19 חשיפות לתוכן"),
 ("סך החשיפה של ארבעת התכנים של 25.08", "282", "יום אחד הביא יותר מעשרה ימי תוכן"),
 ("שיתופים בעשרה האחרונים", "2", "כולם מריל אחד, 17.09"),
 ("תגובות בעשרה האחרונים", "2", "שתיהן על תוכן החגים של 10.09"),
 ("עוקבות חדשות שיוחסו לתוכן", "0", "Metricool מייחס עוקבת אחת בלבד בכל התקופה, לריל ההיכרות של 25.08"),
 ("שמירות בעשרה האחרונים", "11", "שיעור שמירה כולל של 5.8% מהחשיפה, זה מספר טוב"),
 ("ריל מול קרוסלה, אותו רעיון באותו יום", "25 מול 8", "16.09. הריל הביא פי שלושה"),
 ("ממוצע צפייה הגבוה ביותר", "34.3 שניות", "31.08, הריל של חוק 60/30/10"),
 ("אחוז צפייה הגבוה ביותר", "72%", "גם הוא 31.08"),
]
hdr(ws2, 4, ["מה נמדד", "מספר", "מה זה אומר"])
for n, (a, b, c_) in enumerate(facts, start=5):
    for i, v in enumerate([a, b, c_], start=2):
        cell = ws2.cell(row=n, column=i, value=v)
        cell.font = Font(size=10, bold=(i == 3), name="Arial")
        cell.border = bord
        cell.alignment = Alignment(vertical="center", wrap_text=True,
                                   horizontal="center" if i == 3 else "right")
        if n % 2 == 1:
            cell.fill = PatternFill("solid", fgColor=CREAM)
    ws2.row_dimensions[n].height = 30

ws2["B16"] = "שלוש מסקנות"
ws2["B16"].font = Font(bold=True, size=14, color=PURPLE, name="Arial")
concl = [
 "1. החשיפה יורדת, לא עולה. ארבעת התכנים של 25.08 הביאו 282 חשיפות. עשרת התכנים של ספטמבר הביאו 189. יותר תוכן, פחות אנשים. הבעיה אינה כמות.",
 "2. מי שכן רואה, כן שומר. 11 שמירות על 189 חשיפות זה 5.8%, שיעור גבוה. התוכן עצמו עובד. ההפצה היא שלא עובדת.",
 "3. רק דבר אחד ייצר שיתוף, וזה היה תוכן שרואים בו אותך. הריל של 17.09, מאחורי הקלעים של הצילומים, הוא היחיד שנשלח הלאה וגם בעל החשיפה הגבוהה ביותר בעשרה. גם ריל ההיכרות של 25.08, עם 131 חשיפות ו-4 תגובות, הוא מאותו סוג.",
]
for n, t in enumerate(concl, start=17):
    c = ws2.cell(row=n, column=2, value=t)
    c.font = Font(size=11, name="Arial")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws2.merge_cells(start_row=n, start_column=2, end_row=n, end_column=4)
    ws2.row_dimensions[n].height = 46

ws2["B21"] = "מה לעשות עם זה"
ws2["B21"].font = Font(bold=True, size=14, color=PURPLE, name="Arial")
todo = [
 "להוסיף ריל אחד בשבוע שרואים בו אותך מדברת או עובדת. זה הפורמט היחיד שייצר שיתוף.",
 "להפסיק להוציא את אותו רעיון בריל ובקרוסלה באותו יום. לפצל ליומיים.",
 "המספר שכדאי לעקוב אחריו הוא שיתופים חלקי חשיפה. הוא היחיד שמביא קהל חדש.",
]
for n, t in enumerate(todo, start=22):
    c = ws2.cell(row=n, column=2, value=t)
    c.font = Font(size=11, name="Arial")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws2.merge_cells(start_row=n, start_column=2, end_row=n, end_column=4)
    ws2.row_dimensions[n].height = 26

for k, v in {2: 42, 3: 14, 4: 60}.items():
    ws2.column_dimensions[get_column_letter(k)].width = v

# ---------- tab 3 ----------
ws3 = wb.create_sheet("כל התוכן")
ws3.sheet_view.rightToLeft = True
ws3["B1"] = "כל התוכן, 25.08 עד 17.09"
ws3["B1"].font = Font(bold=True, size=18, color=PURPLE, name="Arial")
ws3["B2"] = "27 פריטים. Reach, Shares, Saves ו-Comments מ-Metricool. ממוצע צפייה ואחוז צפייה קיימים רק בריילס."
ws3["B2"].font = Font(size=10, color=GREY, name="Arial")

cols3 = ["#", "תאריך", "פורמט", "נושא", "Reach", "Shares", "Saves", "Comments", "Views",
         "ממוצע צפייה (שנ׳)", "אחוז צפייה", "Send rate", "Connection rate", "לינק"]
hdr(ws3, 4, cols3)
for n, r in enumerate(allc, start=1):
    date, fmt, topic, reach, sh, sv, cm, views, aw, vr, link = r
    send = rate(sh, reach); conn = rate((sv or 0) + (cm or 0), reach)
    vals = [n, date, fmt, topic, reach, sh if sh is not None else "אין נתון", sv, cm, views,
            aw if aw is not None else "", vr / 100 if vr is not None else "", send, conn, link]
    row = 4 + n
    for i, v in enumerate(vals, start=2):
        c = ws3.cell(row=row, column=i, value=v)
        c.font = Font(size=10, name="Arial")
        c.border = bord
        c.alignment = Alignment(horizontal="center" if i != 5 else "right", vertical="center")
        if i in (12, 13, 14):
            c.number_format = "0.0%"
        if i == 15:
            c.font = Font(size=9, color="5A6FA8", name="Arial")
        if v == "אין נתון":
            c.font = Font(size=10, color="B0A8B8", italic=True, name="Arial")
        if row % 2 == 1:
            c.fill = PatternFill("solid", fgColor=CREAM)
for k, v in {2: 4, 3: 8, 4: 9, 5: 32, 6: 9, 7: 9, 8: 8, 9: 11, 10: 8, 11: 16, 12: 12,
             13: 11, 14: 15, 15: 42}.items():
    ws3.column_dimensions[get_column_letter(k)].width = v
ws3.freeze_panes = "C5"

# ---------- tab 4 ----------
ws4 = wb.create_sheet("איך משתמשים")
ws4.sheet_view.rightToLeft = True
ws4["B1"] = "איך ממלאים את זה בפעם הבאה"
ws4["B1"].font = Font(bold=True, size=18, color=PURPLE, name="Arial")
steps = [
 ("מה נמשך אוטומטית", "Reach, Saves, Shares, Comments, Views, ממוצע צפייה ואחוז צפייה. אלה נמשכים מ-Metricool ואני יכול לרענן אותם בכל רגע, רק תבקשי."),
 ("מה לא קיים אוטומטית", "% לא עוקבים ו-Profile visits לפוסט. Metricool לא מחזיק אותם."),
 ("איך משיגים את השניים האלה", "1. באינסטגרם: כניסה לפוסט, לחיצה על הצפיות, קריאת אחוז הלא עוקבים וביקורי הפרופיל. 2. במחשב: Meta Business Suite, לשונית תוכן, מעבר לתצוגת טבלה. שם הכל בטבלה אחת ואפשר לשלוח לי צילום מסך."),
 ("כל כמה זמן", "פעם בשבועיים. לא יותר. בחשבון בגודל הזה שבוע בודד הוא רעש."),
 ("מה מסתכלים עליו", "שיעורים, לא מספרים. שיתופים חלקי חשיפה מראה מה מביא קהל חדש. שמירות ותגובות חלקי חשיפה מראה מה מחזק קשר."),
 ("מתי לא להסיק כלום", "כשהחשיפה מתחת ל-10. שם אחוז אחד הוא אדם אחד."),
]
hdr(ws4, 3, ["נושא", "הסבר"])
for n, (a, b) in enumerate(steps, start=4):
    for i, v in enumerate([a, b], start=2):
        c = ws4.cell(row=n, column=i, value=v)
        c.font = Font(size=11, bold=(i == 2), name="Arial")
        c.border = bord
        c.alignment = Alignment(wrap_text=True, vertical="center")
        if n % 2 == 0:
            c.fill = PatternFill("solid", fgColor=CREAM)
    ws4.row_dimensions[n].height = 58
ws4.column_dimensions["B"].width = 28
ws4.column_dimensions["C"].width = 95

out = "/home/user/canva-workshop/מפת-התוכן-שלי-מלא.xlsx"
wb.save(out)
print("saved", out)
