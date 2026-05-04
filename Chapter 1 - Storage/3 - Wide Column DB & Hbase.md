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

   בראי הschema design חשוב לקחת בחשבון במיוחד את ה row key, הוא בעצם האינדקס היחיד שלנו ולכן נרצה שרוב הגישות יקרו דרכו שכן הוא הכי אופטימלי לחיפושים.
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

4. **Fault Tolerance & Coordination:**  
   How does HBase use WAL replay, region reassignment, and coordination via ZooKeeper to handle failures and maintain availability? What happens when a RegionServer crashes?

5. **Scalability & Operations:**  
   Discuss how HBase scales horizontally through region splitting and balancing, how it relies on HDFS for durability, and what administrative actions (snapshots, backups, schema changes, recovery) operators perform in production environments.

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
