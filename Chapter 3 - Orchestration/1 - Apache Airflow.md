# Orchestration Fundamentals:

## Overview

This section will go over the fundamentals of _Apache Airflow_, consisting of the client side, and the backend.

**We will focus on general concepts of airflow, the flow of the tasks and how does client code look like.**

## Goals

- Develop a foundational understanding of how scheduling is done.
- Learn the common terminology used by most schedulers.
- Practice planning a self-study day and estimating time for learning.

:warning: **Note:**

- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- When in doubt about what you need to learn, ask your mentor.

### Core Concepts

Think through the following questions; by answering them you’ll touch every major topic listed above:

1. **Airflow User API & Concepts:** Explain the difference between a DAG and a DagRun? How do tasks share small metadata versus global configuration? What is Jinja Templating, and why would you use {{ ds }} instead of Python's datetime.now()? Contrast the TaskFlow SDK with Classic Operators. How does the TaskFlow SDK handle XComs differently than the old xcom_pull method? What are Assets? What types of Operators exist? Why is it not recommended to run any time consuming code in top level dag code? How does this affect the DAG Processor's performance? What is a Hook? what is the connection between Hooks, Connections and Operators?

2. **Airflow Backend & Architecture:** What are the different components in the airflow architecture? Define the roles of each component. Why is the Executor considered a mechanism/logic rather than a standalone service? Explain the Deferrable Operator. Which component makes these possible, and how do they save money/resources in a Big Data stack? What are Airflow Providers?

3. **Airflow Workflow Synchronization:** How were DAGs typically synchronized to the Scheduler and Workers in Airflow 2? What where the risks with the approach? How was this solved in Airfloe 3? How did it solve the main issue with the Airflow 2 approach? What are the other advantages DagBundles give us?

4. **Airflow Task Lifecycle:** What is the full flow of a dag from being written to being run? What happens when the DAG Processor encounters your file? How is Jinja parsing different in dag processing than execution time? At which state does the Scheduler stop managing the task and hand it over to the Executor? What is the flow when a task gets to a worker? when does it become running?

5. **Airflow Critical Sections:** What is the "Critical Section" of the Scheduler? Describe the three primary "loops" or critical sections (DagRun Creation, Task Instance Creation, Task Scheduling).

## Q&A

1. אלטרנטיבות לairflow והבדלים עיקריים.

Luigi - פרוייקט open source שפותח על ידי spotify.
הוא עובד מאוד דומה לairflow.
אין הרבה מה להרחיב, יש לו קהילה הרבה פחות פעילה ולכן פחות מומלץ.

Prefect - אלטרנטיבה יותר חדשה ומודרנית לairflow.
יצירה של DAGS היא הרבה יותר native לפייתון.
ובאופן כללי יש פיצ'רים יותר מתקדמים וניתן לממש פיצ'רים קיימים (מairflow) בפשטות יותר.
מצד שני perfect יכול להסתבך יותר עם DAGs יותר מורכבים בגלל שאין parsing אלא זה עובד בruntime.

Dagster - טכנולוגיה לאורקסטרציה שיותר מתמקדת במידע עצמו, בעצם מתייחסים למידע כחלק מהDAG.
אין רק tasks, אלא הdata עצמו הוא asset שלוקחים בחשבון.

2. למה צריך את הקוד של הDAG בmetadata database ?

כדי לייעל את הגישה של הwebserver לקוד, גישה לDB יותר מהירה מאשר לעשות import מהקבצים.
כלומר יוצרים decoupling בין פרסור DAGs על ידי הwebserver להצגתו, ובכך מאפשרים לשמור עליו יותר קל וסקיילביליות קלה יותר.

3. celery over k8s (CeleryKubernetes)

זאת בעצם הרצה של CeleryExecutor וKubernetesExecutor במקביל.
מיפוי של tasks קורה לפי queues שונים.

4. מה היחס בין Task ל Operator

operator הוא בעצם תבנית ליצירת Task
בעצם Task הוא המעטפת.
קונספטואלית, operator הוא class וtask הוא instance.

5. מה הusecase לbash operator

הרצת סקריפטים בשפות תכנות שהן לא פייתון, בפרט bash.

6. השוואה בין אופרטורים של spark

SparkSubmitOperator - מבצע spark-submit דרך הDAG עם האופציות של הקונפיגורציה של spark-submit, זה סוג של wrapper.

SparkSqlOperator - מאפשר להריץ SQL ישירות, בעצם מפשט עוד יותר את השימוש בspark שכן רושמים ממש סטרינג SQLי.

SparkPipelinesOperator - משתמש במקום בspark submit, בspark-pipelines כלומר מריץ spark declerative pipeline.

PySparkOperator - מריץ אפליקציית pyspark במצב standalone או עם spark connect.

SparkJDBCOperator - משתמש ב SparkSubmitOperator על מנת לקרוא או לכתוב מידע מDB שהם חלק מהJDBC, ובעצם מקל על הקונפיגורציה.

7. למה spark צריך כזה הרבה אופרטורים ?

כי spark היא טכנולוגיה מסובכת שדורשת הרבה קונפיגורציות ומאוד ורסאטילית וכל oprator מקל על חלק יותר ספציפי בspark ומאפשר להריץ אותו בצורה נוחה ואינטואטיבית יותר.

8. למה airflow צריך psycopg2 ?

כי זה dependency של sqlalchemy.

9. האם יש מקבילה של PythonOperator לGO ולעוד שפות ?

לא, אין.

10. מה זה worker וכמה כאלה יש ?

זה בעצם רכיב שמריץ את הtasks.
אין הגבלה על כמות הworkers.
למשל בcelery ניתן להגדיר את כמות הworkers.

11. כמה workers יש לapi server איפה הם רצים ולמה צריך כמה מהם ?

זה workers של gunicorn. הם לא באמת מריצים tasks.
הם רצים כprocesses בwebserver.
ההבדל העקרי בין uvicorn לgunicorn הוא הקונספט של מקביליות מול concurrency, uvicorn משתמש בconcurrency לעומת gunicorn שמשתמש בparallelism אמיתי ויוצר processes של workers.
(ניתן להשתמש בשניהם עבור אותה אפליקציה, כלומר כל worker של gunicorn יריץ uvicorn).

12. מה ההגבלה של xcom וממה היא נובעת ?

המגבלה היא לפי הmetadata database.
בpostgress 1Gb
בSQlite 2Gb
בMySQL 64kb.

13. באיזה רמה מוגדר xcom על s3 (task, dag,...)

מוגדר ברמת כל הcluster.

14. מה מצפים לראות בלוגים של של airflow ?

נצפה לראות למשל שכל הדרישות (dependencies) מסופקות
איזה מספר הרצה, לוגים מאופרטורים built in, שהtask הסתיים.

15. אין לוגים לTask, מה יכולים להיות הגורמים ?

לא מסתכלים על level נכון.
קריאת לוגים מתיקייה לא נכונה או כתיבה למשל לאיזשהו local file system לא נגיש של קונטיינר.

16. מה זה state missmatch

כאשר מצב של task instance משתנה לא דרך הairflow למשל אם הורגים את התהליך.
ובכך יוצרים אי התאמה בין המצב בDB למצב בפועל.

17. מה זה SQLite

זה RDBMS שהקטע שלו הוא שפשוט להקים אותו והוא embedded.
כלומר הוא חי על אותה מכונה באותה אפליקציה דרך סיפרייה.
המידע נשמר בקובץ אחד עם סיומת .db או .sqlite
ואין צורך בקונפיגורציות בכלל מה שמאוד מקל את ה"פריסה" שלו ומאוד שימושי בשביל embedded database.

18. מה ההיתרונות והחסרונות של airflow over SQLite ?

היתרון נובע מהקלות של ההרמה של sqlite והעובדה שהוא מאוד קל לשימוש.
החסרון נובע מאותה סיבה, הוא מאוד פשוט והוא embedded ולכן לא סקיילבילי ולא ריאלי בסביבות גדולות או עם כמה schedulers.
והתמיכה במקביליות שלו הרבה יותר חלשה.

19. באילו מצבים נבחר בairflow over SQLite ?

כשנרצה לבצע בדיקות, הוא דורש מינימום התעסקות וללא קונפיגורציה וserver נפרד.

20. מה קורה כאשר ה executor נופל, ומה קורה עם נפיל אותו ?

משימות שרצות כרגע, ימשיכו לרוץ. ויעדכנו את הערך שלהם בDB.
לעומת זאת לא נוכל להקצות משימות חדשות ולשנות את המצב של DAG בDB כלומר הDAG יתקע במצב RUNNING.

הערה: הנחתי שהכוונה היא על scheduler, כיוון שexecutor הוא לא רכיב נפרד אלא חי בתוך הprocess של הscheduler.

21. מה זה Fernet key ?

זאת סכימת הצפנה סימטרית, משתמשים בה בairflow על מנת להצפין את הconnections והvariables.

22. מה ההבדל בין Variable ל Connection

במימוש אין הרבה בהבדל, בusecase, hooks מתממשקים ישירות עם connections ויש להם סכימה יותר ברורה ולכן מתאימים יותר ספציפית למקרים של שמירת credentials למקורות חיצוניים.
לעומת זאת, variables משומשים יותר לשמירת משתנים שמשתמשים בהם לקונפיגורציה. ויותר קל לערוך אותם, הם קצת יותר פשוטים כלומר המידע נשמר בתצורת KV ולכן קצת יותר גמישים.

23. מה זה Secret Backend ?

מערכת חיצונית שairflow מתממשק איתה על מנת לאחסן "סודות" שהם בעצם connections וvariables.
בצורה בטוחה וריכוזית.
בדרך כלל הם מאפשרים הרבה פיצ'רים של אבטחה למשל הצפנה וaudit trails.

24. מה הדרישות לDB בairflow

בפועל airflow תומך בpostgress, mysql, sqlite.
אבל תיאורטית יכול לתמוך בכל מה שנתמך על ידי הספרייה SQLAlchemy.

25. למה צריך Redis בairflow ?

זה לא קריטי לairflow נאטיבית, אלא לcelery executor.

26. מה ההבדל בין hook לoperator ?

בפרקטיקה, אפשר לממש hook עם operator, אבל hook מכמס את ההתחברות למקור החיצוני ומפשט את כל  הפיסטונים והופך את הקוד ליותר קריא.

27. מה זה subdag ?

זה DAG שהוא embedded בDAG אחר כלומר מופיע כtask בDAG החיצוני אבל בפועל זה אובייקט DAG עם tasks משלו, schedule משלו ולוגיקה משלו.
זה גרם להרבה בעיות במקרים בהם התזמון של הsubdag לא היה אחיד עם הDAG המקורי, והביא התנהגות לא צפויה.

28. מה ההבדל בין zombie task ל undead task ?

הם הפכים,
במקרה של zombie, הtask אמור לרוץ אבל הפרוסס מת למשל כלומר בפועל הtask לא רץ.
המקרה של undead הוא הפוך, כלומר tasks שלא אמורים לרוץ אבל רצים בפועל.

29. מה זה cluster policies ?

כמו תנאים שאפשר להלביש על cluster כך שכל DAG או Task יהיו חייבים לעמוד בהם.

### Real-World Context

Rather than focusing on one technology, think about how data workflows are shceduled, and think about when running and ocrhestrating data workflows.

## 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between Airflow and an industry alternative.

    Deliverable: A written summary (minimum 1 or 2 sentences).
    Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
    Goal: You must be able to justify why the department uses this tool for our specific environment.

## 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

    Deliverable: A written summary example/story (two sentences approx.).
    Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
    Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

## Wrapping Up :trophy:

Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later when using scheduled jobs.

## Additional Topics from Review

- A deep dive into the Airlfow database and the inner workings of Airflow.
- A deep dive into bugs solved and unsolved inside Airflow.

## Action Items

- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world schedulers and their algorithms.
- Prepare questions for the upcoming mentor Q&A session.

## Recommemded Resources

- [Airflow Docs](https://airflow.apache.org/docs/)
