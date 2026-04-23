# File Systems Fundamentals :
## Overview
This session introduces the basic ideas that apply to most file systems, whether they run on a single machine or across a cluster. The goal is to understand how data is organized, managed, and accessed so you can speak intelligently about storage technologies.

**We will focus on general concepts such as hierarchy, metadata, block allocation, and performance trade-offs.**

## Goals
- Develop a foundational understanding of how file systems work.
- Learn the common components and terminology used by most file systems.
- Practice planning a self-study day and estimating time for learning.

:warning: **Note:**
- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- Review the [Exercise](#exercise) before diving in so you know what to focus on.
- When in doubt about what you need to learn, ask your mentor.

### ⏳ Timeline
Estimated Duration: 0.5 Day
- Day 1: Spent no more than hlaf a day on file systems;
    - Have a Q&A session right after


### Core Concepts

Think through the following questions; by answering them you’ll touch every major topic listed above:

1. **Hierarchy, Metadata & Lookup:**  Describe how a file system organizes files in a namespace, how it separates metadata from content (e.g. using inodes), and explain the steps taken to resolve a path like `/home/user/docs/report.txt` to the underlying data.

רוב מערכות הקבצים מארגנות את הקבצים בצורה היררכית - תיקיות.
כל תיקייה או קובץ (תיקייה היא גם קובץ...) יושב תחת תיקייה אחרת עד ה root directory.
מכיוון שתיקייה היא גם קובץ, אמנם קובץ מיוחד אבל עדיין קובץ, היא מכילה מיפוי של שמות של קבצים וה Inodes שלהם.
כלומר כשניגשים לקובץ, בעצם ניגשים לתיקייה שהקובץ נמצא בו ומשם ל inode שלו.

כשמדברים על כתובת אבסולטית מתחילים מה root directory.
לאחר מכן מתבצעת טוקניזציה לפי '/' ומתבצע חיפוש איטרטיבי.
אתעלם באלגנטיות ממקרים כמו "." או ".."
מחפשים את השם בתיקייה כדי למצוא את ה inode וממשיכים איטרטיבית.
שוב אתעלם באלגנטיות ממקרים בהם מדובר ב symlink או במקרים בהם אחת התיקיות בדרך היא mount
למשל במקרה המבוקש מתחילים ב root ומחפשים home.
אם זאת אכן תיקייה, ממשיך לחפש בה עד שנגיע לסוף ונחזיר את ה indoe של report.txt.

2. **Storage & Allocation:**  Explain block allocation strategies (contiguous, linked, indexed, extent‑based), discuss what internal and external fragmentation are, and outline how performance is impacted by file size and access patterns (small vs. large files, sequential vs. random).

יש כמה סוגי אסטרטגיות עיקריות לגבי איך שומרים קבצים על הדיסק. כל דיסק מחולק לבלוקים והאסטרטגיות האלה קובעות איך הקובץ נשמר על הבלוקים.

לפני האסטרטגיות, אסביר על פרגמנטציות:
פרגמנטציה חיצונית - יש מקום על הדיסק כדי למלא בקשה כלשהי, אבל הוא מפוזר בין המון חלקים קטנים ואין איך לנצל את כולם ביחד.
פרגמנטציה פנימית - אם הוקצה זיכרון אבל אין שימוש בכולו, למשל אם הוקצה בלוק שלם לקובץ אבל הוא משתמש רק בחצי ממנו.

contiguous - לפי האסטרטגיה הזאת, לכל קובץ מוקצים בלוקים רציפים על הדיסק בהתאם לגודל של הקובץ ולכן צריך לדעת את הגודל של הקובץ מראש.
היתרונות הם שהשיטה הזאת מאוד מהירה כי המידע נשמר בצורה רציפה ואין צורך בקפיצות וחיפושים, ויש גישה ישירה לכל בלוק של הקובץ.
החסרונות הם פרגמנטציה חיצונית ופנימית. וקשה להגדיל קובץ.

linked - כל בלוק שומר מצביע לבלוק הבא.
היתרון או החיסרון הוא שאין צורך ברציפות ומכאן אין בעיה להגדיל קובץ ואין בעיה של פרגמנטציה חיצונית. מצד שני, צריך חיפוש סדרתי כדי להגיע לבלוק ספציפי ולכן השיטה יותר איטית.

indexed - לכל קובץ יש בלוק אינדקסים ששומר את האינדקסים של כל הבלוקים שמוקצים לקובץ.
היתרון הוא שאין פרגמנטציה חיצונית ויש גישה (כמעט) ישירה לכל הבלוקים שמוקצים לקובץ ולכן מאפשר גישה מהירה אליהם.
החיסרונות הם שיש יותר overhead של פוינטרים מאשר ב linked allocation. וכאשר יש קבצים קטנים, צריך לשמור בלוק שלם בשביל כמות קטנה של פוינטרים לעומת linked ששומרים בה פוינטר לכל בלוק וזהו.

extent-based - זאת שיטה חדשה יחסית שרוצה לשלב את היתרונות של contiguous ביחד עם הגמישות של שאר השיטות.
בעצם במקום להקצות בלוקים אחד אחד, מקצים בלוקים בגודל של ה extent . זה נותן לקבצים קצת יותר מרחב גדילה מבלי לגרום לפרמנטציה חיצונית. עדיין יש סיכוי לפרגמנטציה פנימית אם מדובר בקבצים קטנים או שלא מתחלק טוב ביחס לגודל של ה extent. השיטה הזאת היא בעצם ה"אמצע" של השיטות האחרות והיא מאוד טובה בהתמודדות עם קבצים גדולים. 


3. **Directories, Indexing & Permissions:**  Compare different directory indexing methods (linear lists, hash tables, B‑trees) and why efficient lookup matters. Then describe common permission models such as UNIX mode bits and ACLs, and how access control integrates with directory lookup.

כל המטרה של אינדקסים היא בשביל לייעל את החיפושים. חיפוש לא יעיל יכול לעלות בזמן יקר בסדרי גודל ולגרום פוטנציאלית לגישות מיותרות לדיסק ובכך להאט את המערכת.

linear lists - זה בסך הכל קובץ שמכיל רצף של key value ממוינים לפי ה key. היתרונות הם גישה נוחה ויש random access וחיפוש יעיל. החסרונות הם עידכונים לא יעילים כי זה הכנסה לסוג של מערך ממוין ואז צרית להזיז הכל.

hash tables - שימוש בפונקציות האש בשביל לאנדקס. יתרונות חיפוש מאוד מהיר עבור שוויונים - ערך ספציפי.
חסרון משמעותי הוא שאין אפשרות לשאילתות range כמו ב B-trees. ובאופן כללי זה פתרון מאוד טוב למקרה הספציפי הזה.

B-trees - המידע נשמר במבנה נתונים של B-tree. לא ארחיב עליו יותר מידי אבל היתרונות שלו הם חיפוש\הכנסה\מחיקה כמו עץ מאוזן כלומר O(log(n)) כי הוא תמיד נשאר מאוזן, וכיוון שהוא שומר על ערכים קרובים, קרוב יחסית בניגוד להאש ואפשר להשיג איתם מינימום אחוז של node שיהיה מלא, כלומר לחסוך מקום ולאפטם על כמות בלוקים שמביאים מהדיסק.

בUNIX יש 3 סוגים של קבוצות ו3 סוגים של הרשאות.
הקבוצות הן user, group, everyone והסוגים הם read, write, execute.
כל קבוצה מקבלת 3 ביטים שמייצגים את ההרשאות שלה למשל 110 אומר הרשאות קריאה וכתיבה אבל ללא הרצה.
בפועל זה נראה משהו כזה -rwxr-xr-x כאשר התווים מייצגים הרשאות. משנים הרשאות באמצעות פקודת chmod.

ACL - Access Control Lists - בעצם מאפשרים לנו לתת הרשאות יותר ספציפיות למשל אם נרצה ש group מסוים יוכל לקרוא רק משהו ספציפי ששייך ל group אחר אבל לא הכל. בעצם ACL מאפשר לנו לתת את ההרשאות האלו מבלי לשנות את הרשאות הבסיס
משנים זאת עם פקודת setfacl

בעצם כשיהיה lookup נצטרך לקחת בחשבון את ההרשאות של היוזר ולראות האם הוא באמת יכול לחפש בתיקייה המבוקשת, כלומר לקרוא אותה.



4. **Consistency, Journaling & Caching:**  Why do file systems employ journaling or copy‑on‑write logs? What problems do these techniques address, and how do caching and write buffering interact with crash recovery and power‑failure scenarios?

מערכות קבצים משתמשות בזה כדי לשמור על נכונות של המערכת, לפני שמשהו נכתב לקובץ או מתבצעת איזהשהי פעולה במערכת הקבצים, הפעולה נרשמת ב journal שהוא על הדיסק, ורק אחרי שהכל נרשם ל journal כמו שצריך, השינויים קורים בפועל במערכת.
וכך במקרה שהמערכת קורסת באמצע ניתן להשתמש ב journal בשביל לשחזר את הפעולה.

החיסרון העיקרי ב journaling הוא כתיבה כפולה לדיסק, ולכן משתמשים בזה רק בעיקר בשביל המטא דאטא, אחרת האוברהד יכול להכביד מדי על המערכת. ולכן יכולות להיות שגיאות וחוסר עקביות במידע עצמו, אבל הוא לא יפגע בשאר המערכת.

ב copy-on-write logs, הרעיון הכללי הוא שכל עוד לא יתבצע שינוי במידע, ניתן לספק פוינטרים למידע המקורי, ובמידה ויש שינוי יוצרים העתק של המידע ומפנים אליו. יתרון מהותי של copy-on-write הוא היכולת לקחת snapshots. 
בהקשר של מערכות קבצים, מידע או פעולה שקורית לא מתבצעת נשמרת ישירות על המערכת, אלא נרשמת במקום פנוי בדיסק ורק לאחר שהמידע הצליח להשמר, מעדכנים את המטא דאטא. העובדה שהמידע הישן לא נמחק מאפשר לנו לקחת snapshots.
חסרון הוא שהעתקות כאלה של המידע יכולות לגרום לפרגמנטציה.

5. **Performance Trade‑offs & Distributed Extensions:**  Discuss the key trade‑offs between throughput, latency, and reliability in file systems. Finally, briefly explain how additional concepts like replication, failover, and namespace servers extend these ideas in distributed systems (HDFS, Ceph) without re‑inventing the core principles.

lataency - זה הדיליי בין בקשה לתשובה
throughput - מספר הבקשות פר יחידת זמן שהמערכת יכולה להתמודד איתה
reliability - כמה המערכת שומרת על מידע עקבי, רלוונטי בעיקר במקרי קצה.
יש tradeoff בסיסי בין המושגים האלה, לאו דווקא רק בהקשר של מערכות קבצים, הדוגמה הפשוטה היא מערכות batch שיש להם throughput גבוה על חשבון latency גבוה.
או במקרה ההפוך, מערכות שהן יותר בזמן אמת מתעדפות latency נמוך על חשבון throughput גבוה
באופן דומה, בשביל מערכת אמינה ועקבית לפעמים צריך להוסיף רכיבים שפוגעים ב latency, למשל journaling.




### Real-World Context
Rather than focusing on one technology, think about how these ideas show up in common operating systems (ext4, NTFS, APFS), networked storage (NFS, SMB), and cloud offerings (S3, Azure Blob). Your task is to recognize the underlying principles across implementations.

## Wrapping Up :trophy:
Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later study specific systems such as HDFS.

## Additional Topics from Review
- The I/O path: what happens when an application calls `read()` or `write()`? Understand the kernel I/O path, page cache, and block layer.
- Mounting & abstraction layers: what “mounting a filesystem” means, and the separation between filesystem, block device, partition, volume manager. These ideas are essential later for containers, cloud disks, distributed storage, RAID/LVM.

## Action Items
- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world file systems you’d like to examine in future chapters.
- Prepare questions for the upcoming mentor Q&A session.
- Continue the Day 01 challenge by mapping these ideas to future chapters.

