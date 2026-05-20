# Introduction to Trino 🐰

## Overview

Today’s session introduces Trino, a distributed SQL query engine designed for high-performance analytics across multiple data sources. Unlike traditional databases, Trino does not store data itself. Instead, it queries data where it already resides, enabling fast interactive analysis across large and diverse datasets.

**The emphasis is on Trino’s architecture, distributed execution model, and how it integrates with modern data platforms.**

## Goals

- Understand what Trino is and where it fits in a modern data architecture.
- Learn how Trino executes distributed queries across workers.
- Explore how Trino connects to multiple data sources and federates queries.
- Improve your ability to research distributed data systems independently.

:warning: **Note:**

- This is a self-study day; independence and time management are crucial.
- If you can’t explain a concept clearly, you probably need to revisit it.
- Ask your mentor if you’re unsure what to research.

### ⏳ Timeline

Estimated Duration: 3 Days

- Day 1: Learn the fundamentals of distributed SQL engines and Trino’s role in the data ecosystem.
- Day 2: Dive deeper into Trino architecture, connectors, and query execution.
- Day 3: Review performance optimization and operational concepts, followed by a Q&A session.

---

## Core Concepts

### Part 1: Distributed SQL Engines (General Concepts)

Answer these questions to understand the broader category of distributed query engines before focusing on Trino specifically.

1. **Role in the Data Architecture:**  
   What is a distributed SQL query engine, and where does it sit in a modern data architecture? How does it differ from storage systems such as data lakes or databases?

2. **Motivation & Use Cases:**  
   Why do organizations use distributed SQL engines? In what scenarios are they preferred (for example: interactive analytics on large datasets, federated queries across multiple systems, or querying data lakes)?

3. **Distributed Query Processing:**  
   How do distributed query engines typically execute queries across multiple nodes? Explain concepts such as parallel processing, data shuffling, and shared-nothing architectures.

---

### Part 2: Trino (Implementation & Operations)

Answer these questions to cover Trino’s major architectural and operational concepts.

1. **Purpose & Position in the Data Stack:**  
   What is Trino, and where does it sit in the data architecture? Explain its role as a distributed MPP SQL engine, how it differs from storage systems, and when it should be used instead of other query engines.

2. **Architecture & Query Execution:**  
   How is Trino architected, and how does it execute queries in a distributed environment? Discuss the roles of the Coordinator and Workers, stages and tasks, data exchanges, and the execution model.

3. **Connectors & Catalogs:**  
   How does Trino integrate with external systems through connectors and catalogs? Explain what connectors are responsible for, how catalogs are configured, and how Trino can federate queries across multiple data sources.

4. **Governance & Workload Management:**  
   How does Trino handle governance and workload management? Discuss resource groups, concurrency control, memory limits, access control (RBAC), and multi-tenant isolation.

5. **Query Optimization & Performance:**  
   How does Trino optimize query performance? Explain cost-based optimization, statistics usage, join strategies, predicate pushdown, partition pruning, spilling, and caching behavior.

6. **High Availability & Multi-Cluster Routing:**  
   How does Trino Gateway enable high availability and workload isolation across multiple Trino clusters? Explain how it provides a single entry point, performs rule-based query routing and load balancing, monitors cluster health, and enables failover and multi-cluster isolation beyond what a single Trino coordinator can support.

---

## Q&A

1. איך אפשר לכפות על trino להיות DB ?

ניתן להשמש בconnector שנקרא memory ואז מידע נשמר על הnodes עצמם.

2. מה ההבדל בין spooling ל spill to disk ?

בspooling מאחסנים תוצאות בobject storage ואז ניתן לרשום באופן מקבילי ואין bottle neck בcoordinator.
בspill to disk זה כמו swapping על המידע, כלומר במידה ואין מספיק זכרון, תוצאות ביניים יורדות לlocal disk של הworker.
הם בכלל לא עובדים אותו דבר ולאותה מטרה

3. איך פונים לtrino cluster מעבר לREST וjdbc ?

דרך הCLI.

4. איך superset מתקשר עם trino ?

בREST

5. איך משפיע המימוש של RPC Queue מול HTTP בtrino ?

לאחר שמתקבלים מספיק בקשות http, trino דוחה את הבקשות ומחזיר שגיאה.
לעומת RPC queue שיש לו יותר מקום לבקשות, לפחות בhdfs...

6. כשלקוח פונה לtrino איך נקראת הבקשה ?

הבקשה נקראת SQL statement.

7. מה הסוג Plan הראשון שיש ?

הסוג הראשון הוא query plan ומקבלים אותו אחרי ריצת הplanner

8. מתי קורה שלב האופטימייזר ?

כחלק משלב הplanner

9. כמה סוגי plan יש ?

יש את הquery plan הרגיל, ולאחר ריצת הscheduler מקבלים distributed query plan שהוא בעצם חילוק של העבודה ליחידות שיכולות לרוץ במקביל

10. האם תמיד קורים כל הסוגים של plan ?

למיטב הבנתי כן, שכן הquery plan הוא רק plan לוגי,
ואילו הdistributed plan שהוא ממש חילוק לstages ומראה ממש את העברת המידע בין workers.

11. מה היחידה הקטנה ביותר בהקשר של Task ?

בהקשר של task כלומר חילוק עבודה על מידע בפועל, היחידה הקטנה ביותר ברמת המידע היא split ואילו ברמת העיבוד היא operator.

12. מה זה driver ומה זה operator ?

הdriver פועל על המידע ומאחד כמה אופרטורים כדי להחזיר output לtask שעליו הוא קיים
כאשר operator הוא החלק עיבוד הקטן ביותר והספציפי ביותר
בעצם driver הוא thread יחיד שחי בתוך task והוא בעצם pipeline של כמה operators.

13. איך מגדירים בSQL מאיפה לשלוף ?

טבלה בנויה מ3 חלקים:
הטבלה עצמה, הסכימה של הטבלה שזה פשוט אוסף של טבלאות - מקביל לDB, הקטלוג של הסכימה.
הקטלוג בעצם מגדיר את הdata source על ידי הconnector שמוגדר לו

14. איך operator וdriver מתקשרים לSPI ומה זה ?

הspi הוא בעצם interface שמגדיר לנו איך plugin צריך להיראות.
למשל איך connector צריך להיראות ואיזה פונקציונליות הוא צריך לממש.
פעולות על הדאטא תלויות במימוש של ה SPI כלומר drivers ובפרט operators עושים פעולות שונות בהתאם לconnector.
למשל הhive connector מתאר splits כpath לקובץ עם offset ואורך

15. מה הקשר בין קטלוג לconnector ?

הconnector מוכל בתוך קטלוג.

16. מהם 4 הרכיבים של coordinator ?
    - parser/analyzer - השלב הראשון שמטרתו להפוך statement לשאילתה תקנית על אובייקטים קיימים.

    - planner/optimizer - בונה query plan לאחר האפטום.

    - scheduler - אחראי על חילוק העבודה על הworkers.

    - discovery service - תהליך שרץ על הcoordinator וworkers נרשמים דרכו לcluster.
      הcoordinator מנהל את הworkers על ידי זה שהם שולחים לו heartbeats.

## 2nd Q&A

1. איך retry polucy מסוג task מחליף spill to disk ?

אם task נכשל בגלל כי עקף את כמות הזיכרון, מריצים את הtask מחדש עם בקשה לקבל את כל הnode לבד לביצוע של הtask.

2. האם worker יכול להתחבר לכמה coordinators ?

לא, כל worker נרשם לcoordinator יחיד ויש coordinator יחיד בcluster.

3. איפה קורה כל אחד משלבי ה pushdown ?

בpushdown דוחפים את התנאי (לפחות במקרים של predicate, projection) לdata source עצמו, ואז כך חוסכים מעבר של הרבה מידע מיותר ברשת.

4. איזה משאבים ניתן להגביל בresource group ואילו סוגי הגבלות ?

ניתן להגביל cpu שזה בעצם cpu time בתווך זמן מסוים,memory, כמות שאילתות שרצות במקביל, הגודל של הqueue של הqueries.

5. מה זה system catalog ואיך מוסיפים קטלוג ?

ניתן להוסיף קטלוג ישירות דרך trino עם SQL syntax כלומר פשוט על ידי פקודת CREATE CATALOG
catalog_name
USING connector_name

הsystem הוא connector שמחזיק מידע על הcluster trino שרץ.
והוא נגיש מהקטלוג בשם system.

6. הגבלת גישה בtrino

ניתן להגדיר access control למשל file access control
כלומר ניתן להגדיר בקובץ JSON את ההרשאות למידע למשל גישה לקטלוגים, סכימות וטבלאות, כאשר ניתן לקנפג רק אופציות מסויימות למשל עבור DROP בדרך כלל צריך הרשאת all.
או למשל הרשאות של הרצת queries ממש.

7. כמה אחוז מהmemory מומלץ להקצות לJVM ?

בין 70 ל85 אחוז מכמות הזיכרון.

8. למה trino gateway צריך DB ?

הוא שומר שם בגדול גם את הqueries האחרונים
וגם את המידע על כל הrouting groups שיש לנו.

9. איך מוסיפים חוקים לgateway ?

אפשר או באמצעות קובץ YAML ולהגדיר בו את החוקים, או באמצעות בקשת REST לgateway.
אלו הדרכים הנאיביות, אם משתמשים בexternal routing service, ניתן להגדיר לוגיקות יותר מסובכות למשל שמירת states.

10. איזה דרכים יש לעשות load balancing מעבר לRR וstochastic ?

אפשר לעשות באמצעות adaptive כלומר לשלוח בקשות לcluster הכי פחות עמוס מה שמגביר את הסיכוי שהשאילתה תצליח

11. מה זה hash join, broadcast join, join hints

hash join - לוקחים את אחת הטבלאות, בדרך כלל הקטנה יותר ומחשבים לה hash, על העמודה לפיה עושים את הJoin.
חשוב שהjoin יהיה על equality.
לאחר מכן מכניסים כל שורה מהטבלה הקטנה לhash table.
מחשבים hash על כל מפתח מהטבלה השניה, ואם הוא מופיע בhash table משאירים אותו.

broadcast join - כשיש טבלה מספיק קטנה כך שהיא יכולה להיות מוכלת כולה בזיכרון של כל worker ואז הjoin מתבצע הרבה יותר מהר.

join hints - זה סוג של דגל שנותנים לsession שמשפיע על join strategy.
כלומר איך לממש את הjoin.

12. באיזה סוגי caching, hive connector משתמש ?

מאחסן בהייב בנוסף, listing של טבלאות מסויימות.

13. מה מספר הworkers האידיאלי ?

המינימום בשביל שיעבוד בצורה סבירה ולאפשר שרידות מסויימת הוא 2.
מעבר ל10 כבר יש overhead שמאט את הcoordinator יותר מידי

14. מה עדיף worker חזק או coordinator חזק ?

עדיף coordinator חזק לפחות במקרה של memory, כי הוא מאחסן גם את הstates של הworkers וגם את התוצאות במידה ואין spooling.

15. איזה משאב coodinator צריך יותר, memory או cpu ?

כנראה שיותר memory, כיוון שהוא מקבל המון הודעות למשל heartbeats ובקשות, אבל אין לו חישובים מאוד אינטנסיביים מדי למרות שהוא עדיין מחשב דברים למשל plan
אבל עדיין לדעתי, המשאב העיקרי שצריך הוא memory.

16. הרבה workers מול workers חזקים

תלוי בכמות הworkers, אם זה cluster קטן שגדל לאט, עדיף לבחור כמה workers חזקים כדי למנוע overhead של תחזוק כמות גדולה של שרתים.
לעומת זאת עם זה cluster גדול, שגדל בקצב גבוה, עדיף לבחור הרבה workers כדי לאפשר מקביליות גבוהה יותר ועמידות גבוהה יותר.

17. איזה מידע וכלים trino ui מספק ?

ניתן לראות בUI הרבה מידע על הqueries למשל query id, השאילתה עצמה, כמה אחוז הסתיים כבר, מי ומה יצר את השאילתה.
ביחד עם הquery stateועם עוד שאילתות שהסתיימו לאחרונה.

18. איך היית מציע ללקוח לתחקר שאילתה שנתקעה ?

למשל להשתמש בexplain או explain analyze בשביל לראות מה קרה לא בסדר בשאילתה ולנסות להבין מהexecution plan
ולבדוק האם המידע מחולק באמת בצורה טובה ברמת הdata source
למשל מפורטש נכון ובפורמט קבצים מהיר למשל parquet ולא csv.

19. Explain, Explain Analyze, analyze

Explain - פונקציה שמחזירה את הexecution plan של השאילתה

Explain Analyze - הוא גם מבצע את השאילתה וגם מחזיר את הdistributed execution plan
עם הזמנים שלקחו בפועל

Analyze - מחזיר סטטיסטיקות על טבלאות ועמודות בשביל טבלה מסויימת.

20. אילו יתרונות/חסרונות הJVM מאפשר לtrino ?

הJMV נותן את היתרון של הרצה ללא תלות במערכת הפעלה וחומרה. לעומת זאת התפעול שלו יכול לגרום לoverhead למשל דליפות זיכרון וgarbage collection

### 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between Trino and an industry alternative.

- Deliverable: A written summary (minimum 1–2 paragraphs).
- Add a real-life use case.
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competing technologies.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

---

### 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

---

## Wrapping Up :trophy:

Go over your answers with your mentor and clarify any uncertainties. Relate Trino concepts back to the broader data platform and how distributed query engines interact with storage systems and processing frameworks.

---

## Action Items

- Identify Trino topics you want to explore further.
- Search examples of industray usage of Trino.
- **Bonus** - what is the rabbit's name?
- Prepare questions for the next mentor Q&A session.

---

## Recommended Resources

- [Official Trino Documentation](https://trino.io/docs/current/) – the primary reference guide.
- [Trino: The Definitive Guide (O'Reilly)](https://dokumen.pub/trino-the-definitive-guide-sql-at-any-scale-on-any-storage-in-any-environment-2nbsped-109813723x-9781098137236.html)
- [Official Trino Gateway Documentation](https://trinodb.github.io/trino-gateway/)
