/**
 * Google Apps Script - עיצוב גיליון שבת משפחת ליבן
 * גרסה מהירה - מעצבת הכל בפעולה אחת במקום שורה אחר שורה
 *
 * שימוש:
 * 1. פתחו את הגיליון ב-Google Sheets
 * 2. תוספות > Apps Script
 * 3. הדבקו את הקוד הזה ושמרו
 * 4. הריצו את הפונקציה: formatShabbatSheet
 */

function formatShabbatSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();

  sheet.setRightToLeft(true);

  const lastRow = sheet.getLastRow();
  const lastCol = Math.max(sheet.getLastColumn(), 6);
  const allData = sheet.getDataRange().getValues();

  const CATEGORY_COLORS = {
    'זום התנעה':        '#FFF9C4',
    'פילוח משתתפים':   '#E8EAF6',
    'חלוקת תפקידים':   '#E8F5E9',
    'תפילות ושיעורים': '#E3F2FD',
    'פעילויות שישי':   '#FFF3E0',
    'פעילויות שבת':    '#FCE4EC',
    'לוגיסטיקה':       '#E0F2F1',
    'עיצוב ופרסום':    '#F1F8E9',
  };

  const AGE_COLORS = {
    'מבוגרים':              '#C8E6C9',
    'נוער בוגר':            '#DCEDC8',
    'נוער צעיר':            '#F0F4C3',
    'ילדים - גיל יסודי':   '#FFF9C4',
    'ילדי גנים':            '#FFE0B2',
    'תינוקות ופעוטות':     '#FFCCBC',
  };

  // בניית מערכי צבע לכל שורה - פעולה אחת מהירה
  const bgColors   = [];
  const fontColors = [];
  const fontWeights = [];
  const fontSizes  = [];

  let currentSection = '';
  let currentCategoryColor = '#FFFFFF';

  for (let i = 0; i < lastRow; i++) {
    const row = i < allData.length ? allData[i] : [];
    const firstCell = String(row[0] || '');

    // ערכי ברירת מחדל לשורה
    let bg = '#FFFFFF';
    let fc = '#000000';
    let fw = 'normal';
    let fs = 11;

    if (i < 5 && firstCell) {
      bg = i === 0 ? '#1A237E' : '#283593';
      fc = '#FFFFFF';
      fw = 'bold';
      fs = i === 0 ? 14 : 11;

    } else if (!firstCell && !String(row[1] || '')) {
      bg = '#FFFFFF';
      currentCategoryColor = '#FFFFFF';

    } else if (
      firstCell &&
      !String(row[1] || '') &&
      !String(row[2] || '') &&
      !String(row[3] || '') &&
      !String(row[4] || '')
    ) {
      currentSection = firstCell;
      currentCategoryColor = '#FFFFFF';
      bg = '#37474F';
      fc = '#FFFFFF';
      fw = 'bold';
      fs = 12;

    } else if (
      firstCell === 'קטגוריה' ||
      firstCell === 'תפילה' ||
      firstCell === 'קבוצת גיל' ||
      firstCell === 'משפחה'
    ) {
      bg = '#546E7A';
      fc = '#FFFFFF';
      fw = 'bold';

    } else if (currentSection === 'לוח משימות') {
      if (CATEGORY_COLORS[firstCell]) {
        currentCategoryColor = CATEGORY_COLORS[firstCell];
      }
      bg = currentCategoryColor || '#F5F5F5';

    } else if (currentSection === 'לוח תפילות ושיבוץ תפקידים') {
      bg = i % 2 === 0 ? '#EDE7F6' : '#D1C4E9';

    } else if (currentSection === 'פילוח משתתפים לפי גיל') {
      bg = AGE_COLORS[firstCell] ||
        (firstCell.includes('סה') ? '#B2DFDB' : '#F5F5F5');

    } else if (currentSection === 'רשימת משפחות') {
      bg = i % 2 === 0 ? '#E3F2FD' : '#BBDEFB';
    }

    // שורה אחת במערך = עמודות רבות (אותו ערך לכל עמודה)
    const rowBg = Array(lastCol).fill(bg);
    const rowFc = Array(lastCol).fill(fc);
    const rowFw = Array(lastCol).fill(fw);
    const rowFs = Array(lastCol).fill(fs);

    bgColors.push(rowBg);
    fontColors.push(rowFc);
    fontWeights.push(rowFw);
    fontSizes.push(rowFs);
  }

  // הגדרת עיצוב בפעולה אחת מהירה
  const range = sheet.getRange(1, 1, lastRow, lastCol);
  range.setBackgrounds(bgColors);
  range.setFontColors(fontColors);
  range.setFontWeights(fontWeights);
  range.setFontSizes(fontSizes);
  range.setFontFamily('Arial');
  range.setVerticalAlignment('middle');
  range.setHorizontalAlignment('right');

  // רוחב עמודות
  sheet.setColumnWidth(1, 210);
  sheet.setColumnWidth(2, 290);
  sheet.setColumnWidth(3, 150);
  sheet.setColumnWidth(4, 130);
  sheet.setColumnWidth(5, 110);
  sheet.setColumnWidth(6, 210);

  SpreadsheetApp.getUi().alert(
    'עיצוב הושלם!\n\n' +
    'הגיליון מוגדר מימין לשמאל\n' +
    'עם קידוד צבעים לפי קטגוריות וסקציות.'
  );
}
