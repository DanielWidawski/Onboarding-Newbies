# Hive Metastore & Table Format :

## Overview
Today’s session zeroes in on two foundational pieces of Hive: the metastore that holds metadata and the table formats that define how data is structured on disk. We will avoid any discussion of Hive’s execution engines (MapReduce, Tez, etc.) or query processing. The goal is to understand the storage and metadata layers that other tools in the ecosystem rely on.

**Focus only on metadata management and table/format semantics.**

## Goals
- Understand what the Hive Metastore is and why it exists.
- Learn how Hive tables are defined and how formats describe their physical layout.
- Practice self-directed study and time management.

:warning: **Note:**
- Independence is essential; plan your study day accordingly.
- If you can’t explain a concept clearly, revisit the documentation.
- Review the [Exercise](#exercise) before diving into research.
- Ask your mentor for clarification on scope if needed.

### ⏳ Timeline
Estimated Duration: 1 Day
- Day 1: Learn the concepts of Hive both metastore and table format; spend the day.
    - Have a Q&A session the same day

## Hive Metastore

Answer the following questions to explore the metastore:

1. **Purpose & Function:**  What is the Hive Metastore and what types of metadata does it store (databases, tables, columns, partitions, locations, statistics)? Why is a centralized metadata service necessary in a distributed data platform?

ההייב metastore מורכב משני חלקים.
הservice שרץ ודרכו שולחים בקשות ופונים לmetastore.
והDB עצמו שבו המידע שמור בפועל.
הmetastore מכיל בתוכו metadata בגדול על כל מה שמוזכר 

הmetastore היא בעצם שכבת אבסטרקציה בין השכבה הפיזית ללוגית.
כלומר מקביל שמות של טבלאות למיקומים פיזים, מחזיק סכמות של טבלאות data types ואוכף סדר
פורמטים של קבצים ואלגוריתם הכיווץ שלהם
וpartitions.

2. **Architecture & Backend:**  Describe how the metastore is implemented as a standalone service backed by a relational database. What are common backend databases, and how does the service scale and handle concurrent clients?

הHMS בנוי משני חלקים, הservice שהוא בעצם הgateway למידע, והוא ניגש לmetastore בפועל.
ניתן להרים כמה instances שלו תחת איזשהו loadbalancer 
ובאופן הזה לנהל מספר משתמשים במקביל.
המידע בפועל נשמר בRDBMS שהוא חלק מהJDBC והאופי שלו כDB רלציוני מאפשר ACID ובכך גישות ממספר משתמשים.
הDBים הנפוצים הם postgress או MySQL.

3. **Schema & Tables:**  What are the key tables in the metastore schema (e.g. DBS, TBLS, SDS, PARTITIONS)? How do they relate to Hive objects?

די אינטואיטיבי, DBS היא טבלה שמחזיקה מידע על הDBים שיצרנו בהייב למשל הURI והOWNER.
TBLS היא טבלה שמחזיקה מידע על הטבלאות שלנו כמו שם הטבלה זמן גישה אחרון והיא מקושרת להמון טבלאות אחרות שמשלימות את המידע עליה כמו סטטיסטיקות הרשאות וpartition keys.
טבלת partition מכילה מידע על הpartitions 
וSDS מכיל מידע על המיקום הפיזי של טבלאות ועמודות

4. **Extensibility & Clients:**  How do external engines such as Apache Spark, Trino, and other tools interact with the metastore? What APIs and protocols are used?

ניתן לגשת לmetastore דרך api של JDBC או באמצעות thrift api.
הפורט הדיפולטי הוא 9083 thrift הוא 
כל המנועים האלה מדברים עם הHMS (ויותר ספציפית הload balancer) דרך thrift בפורט הנ"ל. 

5. **Administration:**  What are common administrative tasks (backup, schema upgrades, migration, repair)? What happens if the metastore becomes unavailable, and why is it considered a critical dependency in data platforms?

ניתן לעשות backup לmetastore באמצעות פקודות dump למיניהן על הDB.
בשביל שינויים בschema ניתן להשתמש בפקודה schematool בשביל אדמיניסטרציה שקשורה לסכימה.
ניתן לעשות מיגרציות באמצעות פקודת mirror
בשביל תיקונים של טבלאות ספציפית partitions, ניתן להשתמש בפקודה msck.

## Hive Table Formats

Answer the following questions to understand table formats:

1. **Definition & Role:**  What does a “table format” mean in Hive? How does it differ from table metadata stored in the metastore? Explain the relationship between logical schema and physical file layout.

table format זו דרך לאגד מספר קבצי מידע ולהציג אותם תחת טבלה אחת אחידה.
בהייב, הtable format הוא כל הקבצים תחת נתיב מסויים (או לפי prefix בobject storage).
בעצם בHMS שמורים הpaths והמידע הפרקטי שנותן לנו לקרוא את המערכת קבצים בצורה טבלאית ואילו הtabke format הוא בסך הכל איך טבלה מוגדרת על גבי המערכת קבצים בעצם כל מה שתחת תיקייה מסויימת הוא בטבלה, כאשר תתי תיקיות הם partitions.

2. **Common Formats:**  Describe popular formats such as Text/CSV, Parquet, ORC, Avro. How do they differ in encoding, compression, columnar storage, and query performance?

אפשר לחלק את הפורמטים של הקבצים ל3 קבוצות עיקריות.
structured, semistructured, unstructured.
בתוך structured ניתן לחלק ל2 סוגים, row oriented, column oriented.
את הדוגמאות ניתן לחלק באופן הבא:

text הוא unstructured כלומר ניתן לרשום בקלות לסוף אבל אין שום דרך לחפש מידע ביעילות. הוא מקודד כtext כלומר ASCII או UNICODE ולכן קריא לבני אדם.

CSV הוא structured row oriented.
הוא גם כן פורמט טקסטואלי ולכן קריא לבני אדם.
היתרונות שלו הם שהוא מאוד פשוט ונגיש, מצד שני, הוא לא יכול לאכוף סכימה, יש בעיות עם תווים מיוחדים וההבדל בין Null לתא ריק. 
בפורמט מכווץ הוא יכול להקרא רק כstream רציף ולכן לא יעיל.

parquet הוא structured column oriented.
הוא מכיל בתוכו גם סכימה של המידע וגם metadata מה שמייעל קריאות.
הוא לא טקסטואלי ולכן לא ניתן לקרוא את המידע עם איזשהו text editor.
הוא מאוד יעיל בתפיסת המקום שלו ושאילתות רצות פי 30 יותר מהר ביחס לCSV.
הוא תומך בהרבה אלגוריתמי כיווץ ביניהם Snappy, GZIP, Brotli.
ויש לו תמיכה בכמה אופציות קידוד Dictionary, RLE, DELTA.
הצורה בא הוא בנוי מאפשרת לשאילתות לפי עמודות לרוץ מאוד מהר כי הם שמורות קרוב.
מעצם העובדה שהוא columnar, ומשתמש בדחיסה וקידוד לפי עמודות מה שמאוד מקשה על כתיבות.
ובנוסף, עבור כמות מידע יחסית קטנה, כיוון שהיתרונות של הפורמט לא באים לידי ביטוי אלא מהווים overhead.
כנ"ל בקריאה של קצת מידע.

ORC הוא גם כן פורמט structured column oriented.
הוא מכיל בתוכו אינדקס, מה שמאפשר קריאה מאוד מהירה של מידע.
הוא מחולק לstripes, מקביל לRow Group של parquet, מכיל סטטיסטיקות על כל stripe שמאפשר דילוג על כאלה מסויימים בהתאם לסטטיסטיקות.
הפורמט מאוד מאופטם לכיווצים גם כן בדומה לparquet.
הפורמט משתמש בdelta encoding.
כרגע, זה הפורמט היחיד שתומך בACID בהייב, הפיצ'ר בנוי כך שכל פורמט שיש לו ROW Id בצורה כלשהי אבל כרגע האינטגרציה היא רק לORC.

Avro הוא פורמט row oriented (אני נזהר להגיד structured למרות שלדעתי הוא כזה).
הוא משמש בעיקר לSerDes על ידי זה שהוא שומר את הסכימה של המידע בפורמט JSON ביחד עם המידע עצמו.
הוא מאוד יעיל לכתיבות בקצב גבוה ולכן אופטימלי לstreaming ומשתמשים בו בkafka
הוא שומר את המידע בצורה בינארית שיותר יעיל בשליחה ברשת אבל זה לא קריא.
חיפושים גם כן יהיו לא יעילים כי לא שומרים איזשהו מבנ"ת שעוזר לזה.

3. **Schema & Tables:**  Explain the difference between managed and external tables, including ownership, lifecycle, and storage location semantics. How does the metastore map logical tables to physical data in storage systems like HDFS or object storage?

ההבדל הוא בניהול של המידע עצמו.
בmanaged table, הייב מנהל גם את המטא דאטא וגם את המידע עצמו. 
כך למשל הייב בוחר איפה לרשום את הטבלה ויש לו שליטה מלאה על הטבלה, בנוסף פקודה כמו DROP TABLE תמחק גם את המידע עצמו וגם את הmetadata.
לעומת זאת, בexternal table, רק הmetadata מנוהל על ידי הייב ואילו המידע עצמו לא, מה שמאפשר לעוד שירותים לגשת למידע, מצד שני המידע לא מנוהל על ידי הייב מה שאומר שצריך לעשות רפליקציות backup ועוד צעדים לdata integrity ידנית.
בmanaged, הטבלה נשמרת תחת תיקיית warehouse לעומת external שיכול להשמר במקומות חיצוניים לגמרי למשל cluster שונה.
בexternal הייב אפילו לא מוודא שהטבלה או הנתיב קיים.
הוא פשוט מקבל את הlocation (אם צויין) כמו שהוא.

4. **Integration with Storage:**  How do table formats map to physical storage (directories, files)? What conventions does Hive use for partitions, buckets, and file naming?

המיפוי של טבלה בהייב לפי הtable format הוא כך שטבלה מיוצגת באמצעות תיקייה וpartitions הם תתי תיקיות.
עבור object storage משתמשים בprefix.
buckets מיוצגים כקבצים תחת partition וממוספרים בסדר עולה.

### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Hive table format and HMS and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.


## Wrapping Up :trophy:
Review your answers with your mentor and make sure you can articulate how the metastore and formats enable interoperability across Hadoop tools.

## Action Items
- Identify areas of metadata or format behavior you want to explore further.
- Prepare questions for the mentor Q&A session.
- Continue linking these ideas to other chapters as part of the Day 01 challenge.

## Recommended Resources
- [Hive Metastore Documentation](https://cwiki.apache.org/confluence/display/Hive/Metastore+Overview)
- [Hive Language Manual – Table Formats](https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL)

