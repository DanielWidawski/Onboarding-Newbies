# Introduction to HBase :elephant:

> **Note:** this document was renamed earlier to `Wide Column DB & Hbase` to reflect the broader category; the title remains centered on HBase for now.

## Overview

Today’s session dives deeper into column‑oriented databases with a focus on Apache HBase, the Hadoop ecosystem’s wide‑column store. (The filename has been updated to “Wide Column DB & Hbase” per reviewer suggestion.) Understanding HBase will help you see how low‑latency random access is provided over massive data sets.

**The emphasis is on HBase’s architecture, core components, and operational model.**

## Goals

- Grasp the columnar database model and why HBase exists.
- Learn the responsibilities of key HBase components (RegionServer, ZooKeeper, HFile, etc.).
- Improve your ability to plan and self‑direct learning.

:warning: **Note:**

- This is a self‑study day; independence and time management are crucial.
- If you can’t explain a concept clearly, you probably need to revaisit it.
- Read the [Exercise](#exercise) before starting so you know what to emphasize.
- Ask your mentor if you’re unsure what to research.

### ⏳ Timeline

Estimated Duration: 3 Days

- Day 1: Learn the concepts of wide column DB and HBASE spesficly; spend the day.
- Day 2-3: Get deep into HBASE spesficly
  - Have a Q&A session at the third day and in between sessions each day

## Core Concepts

## Part 1: Wide Column Databases (General Concepts)

Answer these questions to understand the fundamentals of wide-column databases before focusing on HBase:

1. **Data Model & Structure:**  
   What is a wide-column database, and how does its data model work? Explain the concepts of rows, column families, and flexible schemas. How does this model differ from traditional relational databases and key-value stores?

זה סוג של NoSQL DB כאשר השמות והפורמטים של העמודות יכולים להשתנות בין רשומות אפילו תחת אותה טבלה.
המודל Row-Oriented כלומר המידע נשמר בשורות.
עמודות מצורפות ביחד תחת column family שמאוחסנות בנפרד אבל לא בהכרח מאחסנות כל עמודה בנפרד בדיסק.

column families - זה בסך הכל אוסף של עמודות, כשכדאי שיהיו קשורות לוגית כדי לייעל שליפות

flexible schema - ניתן להוסיף עמודות חדשות בלי להשפיע על רשומות קיימות

לעומת RDBMS שאם שורה מסויימת צריכה שינוי בעמודות, צריך לשנות את כל המבנה של הטבלה, בwide column ניתן פשוט להוסיף column family לשורה מסויימת. זה מאשפר גם סקיילביליות יותר גבוהה כי לא צריך לשמור את כל העמודות ביחד. מצד שני בwide column הjoin עובד הרבה פחות טוב.

לגבי KV, אין סכימה בכלל מה שמונע כתיבה חלקית או חיפושים לפי ערך. מצד שני בwide column התמיכה בעדכונים לא ממש טובה, כי צריך לטעון column families ממקומות שונים בדיסק

2. **Use Cases & Motivation:**  
   Why do wide-column databases exist? In what scenarios are they most useful (for example: large-scale datasets, time-series data, sparse data, or systems requiring high write throughput)?

בגדול wide-column databases באים כדי לשלב באיזשהו אופן בין KV לRDBMS כלומר להרוויח סקיילביליות וסכימה גמישה על חשבון join ולייעל כתיבות על גבי קריאות.

הם שימושיים בעיקר למקרים הבאים:
הרבה יותר פעולות כתיבה על קריאה
כמעט ואין עדכונים במידע
הגישה למידע ידועה באמצעות הPK
אין צורך בjoin ואגרגציות.

בעצם הjoin בא על חשבון הסקיילביליות ולכן הם שימושיים מאוד לlarge scale database. וכיוון שמידע time series לא דורש כמעט עריכות ויש PK ידוע, הוא יהיה מאוד שימושי גם למקרה הזה.
בדומה, כיוון שאין סכימה אחידה, wide column db יהיה שימושי למידע דליל כלומר כשיש הרבה עמודות ריקות כי פשוט לא נשמור את העמודות האלו בכלל ביחס לשורה הספציפית.
ובגלל שאין סכימה קבועה, כתיבות מתבצעות בהרבה יותר קלות וכמעט בלי overhead.

3. **Distributed Design:**  
   How do wide-column databases distribute data across clusters? Explain concepts such as partitioning, replication, and horizontal scalability.

בגדול המידע מחולק בcluster לפי partitions כלומר חלוקה לוגית של הDB לפי מפתח ואז מתבצע חיפוש יותר יעיל בcluster. בנוסף, העובדה שלא כל העמודות נשמרות ביחד נותן לנו עוד חופשיות בפיזור שלהן על גבי הcluster. העובדה שמידע מקושר תחת מפתחות אבל הaccess pattern פחות נוגע לגבי קריאה אלא יותר כתיבות, מאפשר לנו בקלות להוסיף עוד שרתים - horizontal scaling, כי כמעט אין מגבלות על דאטא שצריך לשבת ביחד באותו מקום.

---

### Part 2: Apache HBase (Implementation & Operations)

Answer these five questions to cover HBase’s major areas:

1. **Architecture & Data Model:**  
   Describe the overall architecture of Apache HBase, including tables, rows keyed by row key, column families, regions, and the storage format (HFile). How do these elements differ from a traditional relational database, and why is schema design driven by access patterns?

   בHBase, מידע נשמר בטבלאות כל טבלה מורכבת משורות וכל שורה מורכבת מrow key וכמות עמודות שקשורה אליה.
   השורות מסודרות באופן אלפביתי לפי הrow key, ולכן כדי שמידע דומה ישמר קרוב - באותו partition, נדאג שהrow keys שלהם יהיו דומים.
   כל column family מגדיר פיזית מקום לעמודות וערכים שלהם על הדיסק. לכל column family יש תכונות שמגדירות איך האחסון נשמר בפועל כמו האם לשמור ערכים בmemory או איך לקודד מפתחות ועוד.
   כל טבלה לאחר שהיא עוברת threshold מסויים מחולקת לregions כל region מכיל חלק משורות בטבלה.
   המידע בפועל נשמר בפורמט HFile בפורמט הזה נשמרים המפתחות והערכים באופן ממויין לפי המפתחות כאשר שניהם נשמרים כמערך של בתים.
   בRDBMS רגילים יש סכימה מאוד קשיחה וכמעט אין גמישות והעובדה שהמטרה של הDB היא שהוא יהיה רלציוני פוגעת קשות בסקיילביליות.
   כאן, הקונספט של column families מונע את הבעיות האלה ומאפשר גם גמישות וגם אפשרות לשמור ערכים ריקים. ואנחנו מתפשרים על קשרים בין טבלאות על מנת לאפשר סקיילביליות גבוהה.

   בראי הschema design חשוב לקחת בחשבון במיוחד את ה row key, הוא בעצם ממוין ולכן נרצה שרוב הגישות יקרו דרכו שכן הוא הכי אופטימלי לחיפושים.
   ובנוסף ננסה להמנע מhot spot כלומר range ספציפי של ערכים שרושמים אליו באופן תדיר מדי.
   בנוסף על ידי זה ששמים עמודות דומות באותה משפחה, נקבל בפעולות read את המידע שצריך אבל לא יותר מה שמייעל על חיפושים מורכבים.

2. **Components & Storage Flow:**  
   Explain the roles of RegionServers, MemStore, HFiles, block cache, and the Write-Ahead Log (WAL). How does data flow from a client write to durable storage, and how are reads served from memory and disk structures?

RegionServer - המטרה של RegionServers היא להנגיש ולנהל regions בסביבה מבוזרת, הRegionServer יושב על DataNode.

MemStore - הmemstore הוא סוג של write buffer שיושב בmemory. כשלקוח רושם מידע לטבלה בhbase, השינוי נרשם קודם כל בmemstore מה שמאפשר פעולות מאוד מהירות על המידע הזה.

HFile - זה פורמט הקובץ בו hbase משתמש כדי לאחסן מידע מעל ה hdfs. הוא מכיל אינדקס שמאפשר לhbase לחפש בו מידע בלי לעבור על כל הקובץ.

block cache - זה פשוט cache של בלוקים שיישבו בזיכרון כדי לאפטם פעולות מולם ולחסוך בפעולות I\O מול הדיסק.

WAL - Write Ahead Log - כל פעולה כתיבה נכתבת לWAL שהוא קובץ שאינו נדיף וכך, אם RegionServer נפל לפני שהוא הספיק לעשות flush לmemstore שלו, המידע לא ייאבד.

הflow של כתיבה נראה ככה :
לקוח שולח בקשה לRegionServer.
הRegionServer רושם את הבקשה לWAL.
המידע נרשם בmemstore.
לאחר שהmemstore מתמלא נעשה flush לדיסק כקובץ HFile.

בקריאה דבר ראשון מחפשים בblock cache לאחר מכן מחפשים בmemstore אם עדיין לא נמצא נשתמש בbloom filter וblock cache כדי לטעון את המידע מהhfile.

3. **Performance & Maintenance:**  
   What are minor and major compactions, MOB storage, Bloom filters, and caching? How do they affect read/write latency, storage efficiency, and amplification? Discuss the importance of row-key design and hotspot avoidance.

compaction - hbase משתמש בcompaction כדי לנצל מקום בצורה יותר טובה ולהוריד את הכמות של חיפושים בדיסק בשביל קריאה. בעצם התהליך בוחר hfiles מregion ומאחד אותם
minor compaction - הסוג הזה רץ כל הזמן, בעצם מאחד קבצים קטנים שנכתבו לאחרונה כדי לשמור על כמות קבצים סבירה ולהמנע מבעיות של קבצים קטנים (תשתית hdfs)

major compaction - רץ בתדירות הרבה יותר נמוכה (פעם בשבוע דיפולטית) זאת פעולה כבידה יותר שמשכתבת את המידע בפועל בקובץ ולכן יכולה בפועל למחוק רשומות

MOB storage - MOB אלו אובייקטים בגודל בינוני בין 100KB ל10MB.
משתמשים בפיצ'ר הזה כדי לאפטם גישות לדיסק עבור אובייקטים שהם גדולים מה threshold הדיפולטי (100KB) בעצם רושמים בנוסף לhfile הרגיל, MOB hfile מיוחד ויש הפניה אליהם בhfile הרגיל.
זה בא כדי למנוע splits, merges וcompactions.

bloom filter - זה מבנה נתונים שמטרתו לנחש האם אובייקט מסויים נמצא בקבוצה. אם הוא מחזיר לא, אז בהכרח האובייקט לא נמצא אבל אם הוא מחזיר כן, זה לא וודאי. במקרה של hbase, כל קובץ מחזיק bloon filter על הערכים של המפתחות בתוכו. אם הbloom filter אומר שמפתח מסויים לא קיים, מדלגים על קריאת הקובץ.

דיברנו קצת על caching מקודם זה בא לשמור בזכרון מידע שנגיש הרבה אם משתמשים בLRU אז זה בא על עקרון time locality. וכך מידע שניגשו אליו לאחרונה יהיה בזכרון ונגיש מהר יותר בהמשך.
גם bloom filter וגם caching באים לייעל קריאות.
bloom filters בא על חשבון אחסון, שכן שומרים מבנה נתונים בנוסף למידע עצמו מה שגם מעלה את הlatency בכתיבה, אבל קריאות יעבדו הרבה יותר מהר
caching בא לעזור בקריאה של בלוקים גם כן, על חשבון מקום בזיכרון, כלומר מונע גישות לדיסק.

hotspotting היא תופעה שנובעת מdesign לא נכון של row key. כיוון שהמפתחות ממויינים בסדר מילוני, אפשר לשמור מפתחות קשורים או כאלה שרוצים שייקראו ביחד קרוב. Hotspotting היא התופעה בא כמות בקשות מגיעה לאותו רצף מפתחות כלומר לאותה קבוצה ספציפית של RS מה שיכול לגרום לבעיות בביצועים או קריסה של הRS.

4. **Fault Tolerance & Coordination:**  
   How does HBase use WAL replay, region reassignment, and coordination via ZooKeeper to handle failures and maintain availability? What happens when a RegionServer crashes?

5. **Scalability & Operations:**  
   Discuss how HBase scales horizontally through region splitting and balancing, how it relies on HDFS for durability, and what administrative actions (snapshots, backups, schema changes, recovery) operators perform in production environments.

## Q&A

1. מה הגודל האופטימלי של resion בRS ?

הגודל האופטימלי הוא בין 5-10 GB
כאשר המקסימום המומלץ הוא בין 10-20 GB

2. מה כמות הregions המקסימלית והאופטימלית בcluster ובRS?

בגדול כמות הregions האופטימלית בRS היא בסביבות ה100
כמות הregions המקסימלית בRS נקבעת בעיקר מהגודל שמוקצה לmemstore. לא נרצה לעקוף את הגודל הזה ולכן נרצה שגודל memstore size \* (# of cf) לא יעבור את הגודל שמוקצה בכולל לmemstore בRS.

בנוגע לcluster השיקולים נובעים בעיקר מהמאסטר.

3. מה הם טיפוסי הנתונים בhbase ואיך זה נוגע לRK ?

אין בhbase טיפוסי נתונים וניתן להכניס כל מה שאפשר להמיר ולקרוא כמערך של בתים.
ההשלכות על הrow key נובעות מזה שגם המיון הלקסיקוגרפי מתבצע על המערך של הבתים ולכן חשוב לשים לב לפורמט בו מכניסים את הrow key.

4. מה המאפיינים של schema on read ו schema on write ב hbase ?
5. האם ניתן לאכוף עמודות מסויימות בתוך CF ?

לא, אבל רק כי בדקתי בקוד עצמו ויכול להיות שפספסתי משהו.

6. האם יש אובייקט לוגי שנמצא מעל טבלאות בhbase ?

כן, יש namespace והוא משמש לניהול quota למשל כמות regions וטבלאות שיכולים להיות מקושרים לnamespace
לאפשר עוד אופציות אדמיניסטרטיביות של ניהול גישה.
וכדי להכיל namespace על קבוצה מסויימת של RS.

7. האם ניתן להרים hbase על סוגי storage שונים מhdfs ?

כשמריצים standalone כלומר לוקאלית, הוא משתמש במערכת קבצים המקומית.
אבל כשמריצים גרסה מבוזרת חייב hdfs.

8. מה זה ROOT ולמה הוא לא קיים יותר ?

זאת הייתה טבלה שהייתה מפנה לטבלת META.
במאמרים של bigtable המטרה של טבלת ROOT הייתה כדי לאתר regions שונים בMETA אבל (לפחות בגרסה ההיא) טבלת META מוחזקת ב region אחד ולכן אין סיבה להגיע דרך ROOT ואפשר לגשת ישירות מהZK.

9. האם טבלת META יכולה להיות על גבי RS שונים ומה ההשלכות של זה ?

טבלת META לא יכולה להתפצל למספר regions שונים.
זה מאוד מגביל את הregions בcluster כי הMETA נשמרת בזכרון.
לעומת זאת אם מאפשרים פיצול של הMETA, צריך לאפשר טבלת ROOT או לתת לZK יותר אחריות של ניהול regions של טבלת הMETA.

10. \* איך יודעים לאן לפנות בקריאה מZK ?
11. האם hbase תומך בjoin ואם כן אז איך זה ממומש ?

hbase לא תומך בjoin באופן ישיר
בגדול המשתמש צריך לממש את זה בעצמו למשל בעזרת mapreduce.

12. מה זה skip list ?

מבנה נתונים הסתברותי שיש לו סיבוכיות הכנסה חיפוש והסרה בO(logn) בממוצע, והייתרון שלו על עצים מאוזנים, הוא שהוא לא צריך לנעול הרבה nodes בפעולות שלו אלא הוא עובד על ה nodes הסמוכים.

13. לכל איזה אובייקט לוגי מוצמד memstore ?

מוצמד memstore לכל CF.

14. איך memstore שומר את המידע - באיזה מבנ"ת ?

שומר את המידע בskip list

15. האם ניתן לבצע updates ומחיקות ברמת הcell ?

בעקרון hbase לא תומך בupdate ישירות אלא updates עובדים דרך פעולות put.
וכך בעצם ניתן לערוך cell.
ואכן ניתן לבצע מחיקות ברמת הcell/column.

16. איפה tombstone נשמר\נכתב ?

נשמר בhfile גם אם יש את השורה כבר בmemstore כדי שאם השורה כבר קיימת באחד הhfiles אז היא אכן תמחק ויהיה תיעוד שהיא נמחקה.

17. איך RK בנוי ואיך מעצבים אותו אידיאלית - מה הדגשים ?

בסוף זה מערך של בתים ולכן השיקולים הם ב access pattern כלומר נרצה לאפטם על קריאות ולמנוע hotspotting בשרתים כלומר אם נבחר להכניס מידע שתלוי בזמן עם timestamp כkey, נקבל רק הכנסות רציפות כלומר רוב העבודה תתבצע באותו RS מה שפוגע בload balancing.

18. איך TTL עובד בhbase ?

ניתן להגדיר TTL על CF ואז כאשר הtimestamp עובר את הזמן של הTTL השורה מסומנת כנמחקה.
ניתן באופן דומה להגדיר TTL על column qualifier ספציפי כלומר על versions של cell.

19. האם hfile יכול להכיל מספר cfים ? הקשר בין הdatamodel לשכבה הפיזית.

כל hfile מתאים לCF אבל לכל CF יכולים להיות כמה hfiles.

20. \* LSM tree in hbase
21. מה זה store בhbase ?

אוסף שמחזיק CF בregion, זה בעצם הmemstore של הCF והhfiles שמשוייכים לCF הזה.

## Extra Q&A

1. HBCK and HBCK 2 ?

כלי שבודק עקביות ונכונות של טבלאות בHBase.
hbck1 לא עובד בגרסאות hbase 2 ומעלה ועלול לעשות נזק.

2. async WAL Replication ?

זהו מכניזם להעברת כתיבות מרפליקה ראשית למשניים.
בעצם עובד על ידי Push של שינויים לsecondaries.

3. Region Replication (HA) ?

כדי לשמור על avilability סביר, במקום לשמור על region ב RS יחיד, נשמור רפליקות שלו בRS שונים.
כל הכתיבות תמיד מתבצעות דרך הprimary replica.
נותן יתרון בזמינות של קריאות אבל הן לא בהכרח יהיו עקביות.

4. HDFS vs HBase replication ?
   HDFS replication - רפליקציות של הקבצים עצמם בין DN בHDFS cluster.

Hbase replication - רפליקציה של region או cluster בשביל HA יותר גבוהה.

5. דרכי התחברות לHBase (native API, thrift) ?

הדרך הnative היא באמצעות חבילות java.
כלומר הלקוח שולח בעצם בקשות RPC לclient דרך הjava.
ניתן גם לפנות בבקשות RPC תחת thrift שהיא טכנולוגיה שמממשת RPC.

6. procedures ו remote procedures ב HBase ?

פרוצדורה זו פעולה שמשנה ישות בhbase למשל regions וtables.
בגדול בhbase פרוצדורות ממשיכות לנסות להתבצע עד שהן מסיימות או נכשלות.
remote procedures הן בסך הכל פרוצדורות שרצות על שרתי region server "מרוחקים" למשל פרוצדורות שפותחות וסוגרות regions הן remote procedures.

7. RIT - Region In Transition in HBase ?

מצבים חולפים של regions בhbase למשל closing, opening.
regions במצבים האלה אינם זמינים עד שהם online.

8. Region States ?

לregion יכולים להיות מספר מצבים (states) המצבים נשמרים בטבלת הMETA.
המצבים החשובים הם
offline - הregion לא במצב נגיש ולא הולך להיפתח
open - הregion פתוח והRS עדכן את המאסטר.
closed - הRS סגר את הregion ויידע את המאסטר.
failed close - הRS לא הצליח לסגור את הregion
splitting - כאשר RS מודיע למאסטר שregion מסויים עובר ספליט
ועוד...

9. Connection Registry \*סוגים ואבולוציה ?

10. אלו אובייקטים נשמרים כMOB ?

ניתן להגדיר MOB על גבי cf עם threshold כך שאובייקטים מעליו ישמרו כMOB. hbase לא עושה את זה דיפולטית.

11. Bulk Load ?

זה פיצ'ר שמשתמש בmapred כדי לפרסר מידע טבלאי בפורמט של Hbase כלומר hfiles
ואז להעלות אותו ביעילות לcluster בצורת batch.

12. Short Circuit ?

short circuit זאת אופציה קונפיגורבילית לאפשר ל hbase לקרוא קבצים ישירות מהדיסק המקומי במקום לפתוח socket לDN ולתקשר עם הFS דרכו

13. האם HBase מחייב Data Locality והאם ניתן לשפר או מי אחראי על זה ?

hbase לא כן צריך את הhfiles של הregion שלו קרוב או יותר נכון באותו RS כדי לעבוד באופן מהיר יותר.
באופן כללי major compactions מנסים להזיז את כל הhfiles שקשורים לregion ספציפי לאותו RS.

14. האם region זמין לקריאה וכתיבה במהלך region split ?

לא, region במהלך split לא זמין לא לקריאה ולא לכתיבה.

15. Reference Files ?

אלו קבצים שנוצרים כחלק מתהליך הregion split ומטרתם להחזיק מצביע (כמו symlink) על 2 החצאים בregion המקורי.

16. תיקיית archive ומה היא מכילה ?

אם נלקח snapshot על טבלה מסויימת, נרצה שהמידע המקורי יישמר ולכן נעביר את הקבצים לתיקיית archive כדי שלא יושפעו מcompactions וmerges למיניהם.
וsnapshots יחזיקו הפני אליהם.

17. תיקיית oldwals ?

תיקייה שמכילה קבצי WAL ישנים שעדיין שימושיים לרפליקציות או שהTTL שלהן עדיין לא עבר (דיפולטית 10 דקות).

18. \* אינדקסים בHFile ?
19. מתי הRK מרופלק בתוך HFile - use case ?

כיוון שהRK נמצא עם כל עמודה הוא "מרופלק" דיפולטית

20. RPC בHBase ?

---

### 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between Hbase and an industry alternative.

- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

## Wrapping Up :trophy:

Go over your answers with your mentor and clarify any uncertainties. Relate HBase concepts back to the broader data platform.

## Action Items

- Identify HBase topics you want to delve into further.
- Collect a list of real‑world HBase deployments or related technologies.
- Prepare questions for the next mentor Q&A session.

## Recommended Resources

- [Official HBase Reference Guide](https://hbase.apache.org/book.html) – the definitive documentation.
- _Hadoop: The Definitive Guide_ (O'Reilly) – chapters on HBase.
