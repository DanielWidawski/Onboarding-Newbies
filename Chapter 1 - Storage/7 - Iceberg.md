# Apache Iceberg

Now that you are familiar with the concepts of catalogs and the metastore,
and understand the critical separation between how data is stored versus how it is logically organized,
it is time to move from theory to the practice of the modern data world.

Meet Apache Iceberg – the table format we use as the storage layer in our lakehouse.
designed to solve the consistency and performance "pains" of legacy directory-based systems.

###⏳ Timeline
Estimated Duration: 2 Days
- Day 1: Independent research and deep dive into the foundations of Iceberg.
- Day 2:
  - (Morning): First Q&A.
  - (End of Day): Question Answering & Final Q&A.

### 📚 Resources
Use the resources listed below and practice searching the internet for questions not answered by the provided documentation.
- [Apache Iceberg Official Docs](https://iceberg.apache.org/docs/latest/#documentation)
- [Apache Iceberg Definitive Guide](http://103.203.175.90:81/fdScript/RootOfEBooks/E%20Book%20collection%20-%202024%20-%20F/CSE%20%20IT%20AIDS%20ML/Apache%20Iceberg%20(2024).pdf)
- [Meap Book - Apache Iceberg](./asstes/Architecting_an_Apache_Iceberg_Lakehouse_v3_MEAP.pdf)

### Guide Questions❓
Please use these questions as a guide for your research, dive in, and deepen your understanding of all concepts.
1. What is Apache Iceberg? 
   Explain the problems it solves compared to Hive tables (schema evolution, partitioning, consistency, performance).

זה בעצם table format שבשונה מהייב, מסדר את המידע במבנה שטוח יותר, עם "עץ" של metadata שמתאר אותו.
בהייב schema evolution קורה רק ברמת הmetadata והתמיכה בו מוגבלת.
כנ"ל לגבי partitions, בהייב אי אפשר לפרטש לפי ערכים שונים מעבר לכתיבת כל הטבלה.
בiceberg, המידע המפורטש נשמר ברמת הmetadata ולכן מעבר מpartition לפי חודשים ללפי ימים לא דורש שכתוב של המידע.
בעצם iceberg משתמש בsnapshots כדי להבטיח isolation בין כותבים, והמידע משתנה בפועל בmetadata רק כשהובטח שהכתיבה הצליחה המבנה השטוח והגישה של optimistic concurrency משפרות ביצועים ותמיכה בACID כלומר כל כותב חושב שהוא חי לבד וswaps בין הsnapshots קורים בצורה אטומית.
בנוסף המבנה השטוח של הקבצים ללא חלוקה לתיקיות מונע קריאות RPC וlisting בכל מיני תיקיות וbuckets.

2. Describe the Apache Iceberg table architecture. 
   Explain metadata files, manifest files, data files, and snapshots and how they relate to each other.

אסביר מלמטה למעלה:

data files - אלה הקבצים ששומרים את המידע עצמו iceberg אגנוסטי לפורמט שלהם, אבל הפורמט בשימוש הגבוה ביותר הוא parquet ויש לו בגדול תמיכה בכל מנוע וכלי מודרני.

manifest file - אלה סוג של קבצי metadata שמטרתם לעקוב אחרי הdatafiles (deletefiles) והם מחזיקים סטטיסטיקות על כל קובץ, למשל מינימום ומקסימום של עמודות.
הם מכילים בנוסף גם מידע על שייכות לpartitions.
הם בפורמט Avro.

manifest list - אלו קבצים שמייצגים snapshots.
הם בעצם מכילים רשימה של כל הmanifest files המיקומים שלהם והpartitions שלהם וסטטיסטיקות ברמה קצת יותר כללית מmanifest files של הpartitions.
גם הם נכתבים בפורמט Avro.

metadata file - זאת הישות שעוקבת אחרי manifest list הם בעצם מחזיקים מידע על טבלת iceberg בנקודת זמן כלשהי.
כלומר, הם מכילים מידע על הסכימה, הpartitions, הsnapshots ואיזה snapshot הכי עדכני.


3. What is an Iceberg catalog, and what is its role? 
   Explain what a catalog manages (table namespace, metadata pointers, commits), why it’s required, and how it differs from a metastore. 
   Mention common catalog implementations.

בדומה לקטלוגים רגילים גם כאן המטרה שלו היא לספק מידע לגבי איפה טבלאות נמצאות בפועל כדי לאפשר גישה אליהן.
זו בעצם נקודת הגישה הראשונה שלנו למציאת טבלה ולהתמצאות בdata lake.
הקטלוג מנהל גם namespaces ומחזיק פוינטר לsnapshot העדכני ביותר כלומר לmetadata file העדכני ביותר.
כשמתבצע שינוי בטבלה מתבצע commit בצורת atomic swap.
בעצם בלי קטלוגים נאבד את הקישוריות לטבלאות כלומר לא נדע איך לקרוא את הtable format בiceberg זה אפילו יותר קיצוני מהייב כיוון שאין לנו מבנה היררכי פיזי של תיקיות.
אין ממש הבדל לפחות לדעתי, ניתן להשתמש בmetastore כקטלוג לiceberg פשוט יש לו כמה חסרונות, העיקרי הוא חוסר תמיכה בטרנזקציות על כמה טבלאות.
הiceberg table format מאוד פתוח לקטלוגים ובעצם יש ממשק די בסיסי שצריך לממש כדי להיות קטלוג.
בין הקטלוגים יש את Hive, AWS Glue, Nessie, REST (שהוא עוד סוג של הפשטה שממשים אותה למשל gravitino, Tabular, polaris).

4. How does Iceberg handle concurrent reads and writes? 
  Explain snapshot isolation, atomic commits, optimistic concurrency control, and conflict detection.

בכתיבה, דבר ראשון פונים לקטלוג כדי לקבוע את המיקום העדכני של הטבלה כלומר הmetadata file
בעצם אנחנו צריכים את הmetadata file כדי לקרוא את הסכימה של הטבלה והpartitions.
לאחר מכן רושמים את הקבצים עצמם.
רושמים את הרשומות בקובץ (הדיפולטיבי הוא parquet) לפי הpartitions.
לאחר מכן נוצר manifest file עם המידע על הנתיב של הdatafile וסטטיסטיקות שמחושבות עוד בכתיבה עצמה.
לאחר מכן נוצר manifest list שרשומים בו כל הmanifest files שקשורים לsnapshot הזה.
לבסוף יוצרים metadata file חדש מעודכן תוך כדי שמירת הsnapshot הקודם, ומחליפים בצורה אטומית את ההצבעה של הקטלוג לmetadata file החדש.

בעצם בצורה הזאת, ניתן לאפשר למספר כותבים לכתוב במקביל ורק הראשון שיסיים יצליח לעדכן את הקטלוג בסוג של test&set אטומי.
וזו בעצם הגישה של OCC.

5. What maintenance operations does Iceberg require, and why? 
   Discuss compaction, snapshot expiration, orphan file cleanup, and metadata cleanup.

צריך לבצע הרבה פעולות תחזוקה כדי לשמור על ביצועים טובים בiceberg.

compaction - איחוד של מספר קבצים לקובץ אחד.
זה חשוב בעיקר כי data lakes לא אוהבים קבצים קטנים. הם דורשים יותר I/O ושומרים יותר מקום עם metadata.
ולכן כדאי לאחד קבצים קטנים לקובץ יחיד.
ניתן לתזמן תהליכי spark שיעשו זאת.

snapshot expiration -  כדאי למחוק snapshots אחרי הזמן שכבר לא צריך אותם ובכך לחסוך במקום.
אין לי הרבה מה להגיד על זה, אפשר לתזמן תהליכי spark בדומה שיעשו את זה.

orphan file cleanup - כתיבות שנכשלו אבל עדיין יצרו קבצים, צריכים להתנקות כלומר להמחק.
אלו בעצם קבצים שיושבים ב"תיקייה" של הטבלה אבל אין שום metadata שמצביע עליהם ולכן אין סיבה לשמור אותם.
כדאי להריץ פרוצדורה שתמחק אותם.

metadata cleanup - אחרי כל שינוי בטבלה נוצר metadata file חדש אבל הקודם לא נמחק אלא הקובץ metadata file הנוכחי עוקב אחריו בmetadata-log.
לאחר כמה זמן אין צורך בהם וכדאי לנקות אותם.
יש קונפיגורציה לכמה לשמור והאם למחוק אותם או לתת להם להיות orphan files.

### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Iceberg and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Add real life usecase 
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.
