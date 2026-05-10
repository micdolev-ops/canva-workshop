/**
 * Google Apps Script - עיצוב גיליון שבת משפחת ליבן
 *
 * שימוש:
 * 1. פתחו את הגיליון ב-Google Sheets
 * 2. כלים (Extensions) > Apps Script
 * 3. הדבקו את הקוד הזה ושמרו
 * 4. הריצו את הפונקציה: formatShabbatSheet
 *
 * הסקריפט מגדיר:
 * - כיוון ימין לשמאל (RTL)
 * - קידוד צבעים לפי קטגוריות וסקציות
 * - רוחב עמודות מותאם
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

  sheet.getRange(1, 1, lastRow, lastCol)
    .setBackground('#FFFFFF')
    .setFontColor('#000000')
    .setFontWeight('normal')
    .setFontSize(11)
    .setFontFamily('Arial')
    .setVerticalAlignment('middle')
    .setHorizontalAlignment('right');

  let currentSection = '';
  let currentCategoryColor = '#FFFFFF';

  for (let i = 0; i < allData.length; i++) {
    const row = allData[i];
    const rowNum = i + 1;
    const rowRange = sheet.getRange(rowNum, 1, 1, lastCol);
    const firstCell = String(row[0] || '');

    if (rowNum <= 5 && firstCell) {
      rowRange
        .setBackground(rowNum === 1 ? '#1A237E' : '#283593')
        .setFontColor('#FFFFFF')
        .setFontWeight('bold')
        .setFontSize(rowNum === 1 ? 14 : 11);
      continue;
    }

    if (!firstCell && !String(row[1] || '')) {
      rowRange.setBackground('#FFFFFF');
      currentCategoryColor = '#FFFFFF';
      continue;
    }

    const isSectionHeader =
      firstCell &&
      !String(row[1] || '') &&
      !String(row[2] || '') &&
      !String(row[3] || '') &&
      !String(row[4] || '');

    if (isSectionHeader) {
      currentSection = firstCell;
      currentCategoryColor = '#FFFFFF';
      rowRange
        .setBackground('#37474F')
        .setFontColor('#FFFFFF')
        .setFontWeight('bold')
        .setFontSize(12);
      continue;
    }

    const isColumnHeader =
      firstCell === 'קטגוריה' ||
      firstCell === 'תפילה' ||
      firstCell === 'קבוצת גיל' ||
      firstCell === 'משפחה';

    if (isColumnHeader) {
      rowRange
        .setBackground('#546E7A')
        .setFontColor('#FFFFFF')
        .setFontWeight('bold');
      continue;
    }

    if (currentSection === 'לוח משימות') {
      if (CATEGORY_COLORS[firstCell]) {
        currentCategoryColor = CATEGORY_COLORS[firstCell];
      }
      rowRange.setBackground(currentCategoryColor || '#F5F5F5');

    } else if (currentSection === 'לוח תפילות ושיבוץ תפקידים') {
      rowRange.setBackground(i % 2 === 0 ? '#EDE7F6' : '#D1C4E9');

    } else if (currentSection === 'פילוח משתתפים לפי גיל') {
      const bg = AGE_COLORS[firstCell] ||
        (firstCell.includes('סה') ? '#B2DFDB' : '#F5F5F5');
      rowRange.setBackground(bg);

    } else if (currentSection === 'רשימת משפחות') {
      rowRange.setBackground(i % 2 === 0 ? '#E3F2FD' : '#BBDEFB');
    }
  }

  try {
    sheet.setColumnWidth(1, 210);
    sheet.setColumnWidth(2, 290);
    sheet.setColumnWidth(3, 150);
    sheet.setColumnWidth(4, 130);
    sheet.setColumnWidth(5, 110);
    sheet.setColumnWidth(6, 210);
  } catch (e) {}

  sheet.getRange(1, 1, lastRow, lastCol)
    .setBorder(
      null, null, null, null, true, true,
      '#E0E0E0',
      SpreadsheetApp.BorderStyle.SOLID
    );

  SpreadsheetApp.getUi().alert(
    'עיצוב הושלם!\n\n' +
    'הגיליון מוגדר מימין לשמאל\n' +
    'עם קידוד צבעים לפי קטגוריות וסקציות.'
  );
}
