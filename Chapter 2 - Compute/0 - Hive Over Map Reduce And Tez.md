# Hive on MapReduce and Tez 🐝

## Overview
Today’s session introduces how Hive queries are executed using distributed compute engines. While Hive defines the table format, schema, and metadata through the Hive Metastore (HMS), the actual query execution is performed by an underlying processing engine.

Historically, Hive executed queries using MapReduce. Later, Apache Tez was introduced to significantly improve performance and efficiency.

**The emphasis is on understanding how Hive queries are translated into distributed execution jobs and how MapReduce and Tez differ as execution engines.**

## Goals
- Understand how Hive queries are executed in a distributed environment.
- Learn the basic execution model of MapReduce.
- Understand how Apache Tez improves Hive query execution.
- Build intuition about how SQL queries translate into distributed jobs.

:warning: **Note:**
- This is a self-study day; independence and time management are crucial.
- Focus on understanding the concepts rather than memorizing implementation details.
- If you cannot explain how a Hive query becomes a distributed job, revisit the material.
- Ask your mentor if something is unclear.

### ⏳ Timeline
Estimated Duration: 1 Day

- Day 1: Learn the basics of Hive query execution and how MapReduce and Tez are used as execution engines.

---

### Guide Questions❓

Answer these five questions to understand how Hive queries are executed using MapReduce and Tez.

1. **Hive as a Query Platform:**  
   Hive provides tables, schemas, and SQL querying on top of distributed storage systems such as HDFS. Explain Hive’s role as a platform layer that sits above storage and relies on external compute engines to execute queries.

הייב בעצם מתרגם שאילתות שדומות בגדול לSQL לתוכנות הרצה מבוזרות כמו mapred או עוד execution engines.
בעצם הייב מאפשר גישה חכמה לdata וחישובים עליו באמצעות מנוע עיבוד, וזאת על ידי הארכיטקטורה המלאה שלו, מmetastore וtable format שמגדירים את המבנה של המידע ועד והרכיבים שמתרגמים את השאילתה או העיבוד מהרמה הלוגית לתכנית בפועל.
את התכנית הרצה הוא מנגיש למנועי עיבוד חיצוניים.

2. **Hive Query Stages and Task Execution:**  
When Hive translates a SQL query into a distributed job, how is the work divided into stages and tasks?  
Explain how Hive breaks a query into execution stages, how tasks are distributed across the cluster, and how intermediate results are passed between stages.

בעצם זה התפקיד של הdriver.
הוא מורכב מ4 חלקים:
הראשון הוא הParser, שתפקידו לבדוק האם הsyntax של השאילתה תקין.
הPlanner שמוודא שהשאילתה מתייחסת לעצמים קיימים למשל עמודות קיימות בטבלה וטיפוסים מתאימים. ולאחר מכן הוא מייצר תכנית הרצה.
הOptimizer שתפקידו לייעל את ה execution plan, בכל מיני דרכים ביניהם predicate pushhdown, partition pruning ועוד.
והExecutor שמטרתו לקחת את הexecution plan המוכנה ולתרגם אותו לאחד המנועים, כמו mapred , tez.
הישות שאחראית על חלוקת העבודה ואוסף של תוצאות ביניים, היא ה App Manager.
זה בעצם ה"מאסטר" בארכיטקטורה של המנועים האלה.

3. **Hive Query Execution Pipeline:**  
   What happens when a user runs a query in Hive? Describe the main stages of execution: SQL parsing, logical planning, physical planning, and submitting jobs to an execution engine such as MapReduce or Tez.

השלב הראשון שקורה הוא parsing כלומר בודקים את הsyntax של השאילתה לאחר מכן בונים AST ותכנית הרצה לוגית.
כלומר בונים את התכנית הרצה בכלליות ללא התחייבות למנוע מסויים.
לאחר מכן מתבצעת אופטימיזציה לשאילתה.
ואז ממירים את התכנית הלוגית למנוע עיבוד מסויים למשל mapred. ומייצרים רצף של תכניות mapred.
את התכנית מגישים לexecution engine ומאחסנים את התוצאה או מציגים אותה.

4. **MapReduce Fundamentals:**  
   What is the MapReduce programming model? Explain the roles of the `map phase`, `shuffle and sort`, and `reduce phase`. Why was MapReduce originally used as Hive’s execution engine?

המודל של mapreduce מורכב משלושה חלקים עיקריים. map, shuffle and sort, reduce.
המודל מאפשר יכולות עיבוד גבוהות על גבי cluster של מחשבים, כלומר באופן מבוזר.
הוא מאוד פשוט להבנה וסקיילבילי ולכן נבחר לexecution engine המקורי 
אבל אני לא יודע בכלל אם השאלה מנוסחת כמו שצריך כי הייב לא "בחר" בmapreduce, זאת פשוט הייתה הפלטפורמה הקיימת, והייב נוצר בשביל לתת framework יותר קל לעבודה איתו כלומר בפורמט דומה לSQL.

map phase - פונקציה שמופעלת על כל רשומה כלומר מקבלת רשומה ומוציאה כפלט טרנספורמציה שלהם כזוג של kv.
דוגמה למשל, העלאת מערך שלם בריבוע.

shuffle and sort - קיבוץ חלקים רלוונטים בשביל הreduce כדי למנוע מעבר של מידע בשלב הreduce.
זה בעצם סוג של groupby.

reduce phase - חישוב אגרגטיבי מקבץ על התוצאות משלב הmap, כמובן לאחר shuffle and sort.
למשל סכימה של מערך.

5. **Introduction to Apache Tez:**  
   What is Apache Tez, and how does it improve Hive query execution? Explain how Tez replaces chains of MapReduce jobs with a Directed Acyclic Graph (DAG) of tasks, reducing unnecessary disk I/O and improving query performance.

## Q&A

1. מה זה msck repair ומתי נקבל fileNotFound ?

הפקודה msck repair מעדכנת את הmetastore עם המצב העדכני במערכת הקבצים.
חיוני כאשר מוחקים מוסיפים partitions ישירות דרך הFS.
אחרת נקבל שגיאת FileNotFound בתשאול.

2. איך הApplication Master מחליט לכמה containers לחלק את התהליך ?

דיפולטית מוגדר map לכל block של hdfs
ויותר ספציפית, לגודל של input split.
יש קונפיגורציה אבל היא יותר בגדר Hint.

3. למה צריך sort ?

זה עוזר לreducers להבין מאיפה ועד לאן הם צריכים לקרוא לפי המפתח - עד שהוא משתנה.
היה אפשר להשתמש בhashmap, אבל הוא צורך יותר מידי memory.

4. Hive MapRed vs Hive Tez

הייב משתמש בארכיטקטורה קבועה ולא ניתנת לשינוי של map ואז reduce (כמובן שגם כל השלבים באמצע כמו shuffle וsort). Tez לעומת זאת, מאפשר יותר גמישות על ידי הגדרה יותר פתוחה של הDAG כלומר ניתן לוותר על שלבים מיותרים.
ולכן חוסכים הרבה גישות I/O מיותרות וoptimizers יכולים באמת לייעל את התכנית בנוסף Tez שומר intermediate results בזיכרון או על הדיסק לוקאלי (לא על הhdfs) מה שמוריד גם כן I/O או overhead של רפליקציות. 

5. איך Tez מטפל בכשלים - Fault tolerant ?



6. מתי נשתמש בTez ומתי בMapRed ?
7. מתי Tez לא מספיק טוב ?



---

### 🔄 Alternatives
Assignment: Briefly research another distributed processing framework used for large-scale data processing.

- Deliverable: A written summary (1–2 sentences).
- Add a simple real-life use case.
- Focus: What problem does this framework solve compared to MapReduce or Tez?

---

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipelin

## Wrapping Up :trophy:
Review your answers with your mentor and make sure you can clearly explain how a simple Hive query becomes a distributed computation job. This knowledge will help you understand later query engines and compute systems used in the data platform.

---

## Action Items
- Identify parts of Hive query execution you want to explore further.
- Look at example Hive query plans to see how jobs are structured.
- Prepare questions for the next mentor Q&A session.

---

### 📚 Resources
Use the resources listed below and practice searching the internet for questions not answered by the provided documentation.
- [Hive Documentation](https://hive.apache.org/docs/latest/)
- [Hadoop: The Definitive Guide (O'Reilly)](https://piazza-resources.s3.amazonaws.com/ist3pwd6k8p5t/iu5gqbsh8re6mj/OReilly.Hadoop.The.Definitive.Guide.4th.Edition.2015.pdf)
- [Apache Tez Documentation](https://tez.apache.org/)
- [Apache MapReduce Docs](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)
