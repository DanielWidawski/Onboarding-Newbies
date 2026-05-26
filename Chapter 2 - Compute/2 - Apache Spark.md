# Spark Fundamentals:

## Overview

This section will go over the fundamentals of _apache spark_.

**We will focus on general concepts such as the spark architecture, optimizations, caching and data geometry.**

## Goals

- Develop a foundational understanding of how scheduling is done.
- Learn the common terminology used by most schedulers.
- Practice planning a self-study day and estimating time for learning.

:warning: **Note:**

- This is a self-study day. Independence and time management are essential.
- Many newcomers struggle with self-study; take a moment to plan your day and stick to it.
- Understand the **big picture** of each concept. If you can't explain it, you probably haven't learned it.
- Be prepared to describe how concepts relate to one another and to real-world scenarios.
- Review the [Exercise](#exercise) before diving in so you know what to focus on.
- When in doubt about what you need to learn, ask your mentor.

### Core Concepts

Think through the following questions; by answering them you’ll touch every major topic listed above:

1. **Spark Architecture & Execution:** what are the main components of spark? what is the role of each component? what are their roles? what is the difference between a transformation and an action? how does spark achieve fault tolerance? what is lazy execution in spark? go over [this](assets/where_do_i_run.py) and for each line, comment where it runs.

יש כמה רכיבים עיקריים בארכיטקטורה של spark:

Driver - התהליך שמריץ את הmain ויוצר את הspark context כאשר הspark context מקביל לsession.

Cluster manager - ישות חיצונית (כמו YARK או K8S) שמטרתה להקצות משאבים על הcluster.

Worker node - כל שרת שיכול להריץ את הקוד של האפליקציה בcluster.

Executor - התהליך שרץ על worker node ומריץ בפועל את האפליקציה.

Task - יחידת עבודה שנשלחת לexecutor

Job - יחידה של כמה Tasks שמרכיבים פעולת Spark למשל save, collect

Stage - מקביל לstage בTrino, כל Job מחולק לכמה stages שכל אחד מכיל כמה Tasks.

RDD - Resilient Distributed Dataset - זה אוסף ללא סדר של של אובייקטי scala/java שמבוזרים על גבי הcluster. כל הפעולות שמתבצעות על זה הן פעולות JVM.
יש אכיפת טיפוסים חזקה.
יכולות לקרות הרבה בעיות, במיוחד אם spark לא יודע לעשות על המחלקות והפונקציות של הJVM, SerDes.

Dataframe - בא אחרי RDD ושונה ממנו בכך שמתייחסים למידע כטבלה כך שפעולות כמו למשל פונקציות SQL יכולות להיות מופעלות עליו. אין טיפוסים בכלל מה שיכול לגרום לבעיות ושגיאות בזמן ריצה.
היתרונות העיקריים הם הפורמט הטבלאי והעובדה שלא צריך לעשות SerDes לשורה שלמה אם הפורמט שהמידע נשמר בו הוא columnar אז אפשר לקחת רק שורות ספציפיות.

Dataset - שיפור של Dataframe שמביא קצת אכיפת טיפוסים אלו בעצם Dataframes שמשוייך להם סוג של אובייקט encoder שמקושר למחלקת Java ואז spark יכול לבדוק את הסכימה לפני שהוא מריץ את הקוד
בפועל אין אכיפת טיפוסים ממש חזקה וברוב הפעולות נתעלם מהטיפוס אבל זה עדיין שיפור כי נכשל כאשר נפרש את הDAG ולא בזמן העיבוד עצמו.
באופן כללי זה הטיפוס שיש עליו הכי הרבה אופטימציות

Transformation - פעולות שמתבצעות על אובייקטים של Spark. ויוצרים אובייקט חדש מהקיים למשל Map.
הtranformations קורות בצורה lazy כלומר לא קורות בפועל עד שנקראת פעולת action.

Action - פעולת spark על אובייקט שמחזירה ערך (די מקביל לreduce)
בעצם זה מה שמטריג את כל התכנית.

Lazy evaluation - בעצם החישוב לא קורה ושום דבר לא נטען לזיכרון עד שקורא action כלומר שצריך את המידע בפועל, ואז ניתן לאפטם את כל הpipeline של המידע.

Fault tolerance - spark יודע להשתמש בDAG כך שאם פעולה או executor נכשל הוא ידע להפעיל מחדש את הDAG רק על החלק הספציפי שאבד
ניתן בנוסף לשמור את הRDD באחסון פרסיסטנטי.

2. **Spark Planning & Optimization:** Logical vs Physical Planning: Walk through the transition from Logical Plan to Physical Plan; What is the fundamental difference between Rule-Based (RBO) and Cost-Based Optimization (CBO), what are the common kinds of optimizations used? What is the AQE? Why is running ANALYZE TABLE recommended for performant CBO? and what is whole-stage code generation?

ההבדל בין logical לphysical plan, מאוד מזכיר את ההבדל בtrino.
בlogical plan רק בונים את האבסטרקציה של כל הפעולות שאמורות להתבצע ואין הקשר של driver ו executors.
לעומת זאת, הphysical plan מסבירה איך התכנית הלוגית תתבצע בפועל על הרכיבית הפיזים בcluster.

בבחירת הlogical plan מתבצע הRBO כלומר מתבצעות מניפולציות על העץ של הפעולות על מנת לייעל אותן בצורה לוגית, כלומר ללא הקשר לסטטיסטיקות למשל predicate pushdown.

בבחירת הphysical plan מתבצע הCBO.
כלומר משתמשים בסטטיסטיקות כדי לקבוע אופטימיזציות שהן לא בהכרח דטרמיניסטיות למשל join reordering או אסטרטגיית join.

הAQE הוא אופטימיזציה שקורית בזמן ריצה, כלומר לפי סטטיסטיקות והמידע בפועל.
למשל החלפת אסטרטגיית join לbroadcast join.
או איחוד של partitions קטנים כדי למנוע יותר מדי shuffles.

הרצה של ANALYZE TABLE מעדכנת סטטיסטקות של טבלה, ולכן מייעלת את הCBO.

הcatalyst עושה code generation כלומר הופך שאילתת SQL לJava Byte Code
כדי למנוע overhead של interpretation.
ובעצם לחסוך המון קריאות לפונקציות של הPipeline ולעשות הכל בפונקציה אחת ובכך גם לשפר אופטימיזציות של הJVM JIT.

3. **Spark Shuffle & Joins:** Compare the different kind of joins, and when will spark use each? how can we tell spark to prefer one over the other? what is join reordering? and why is "broadcasting" considered a high-risk, high-reward optimization? What is a _Narrow_ transformation, and _Wide_ transformation? Why do some operations require shuffle? what exactly is written in shuffle?

יש תמיכה ב5 אלגוריתמי join בspark.
לא ארחיב יותר מדי על כל אחד כי הם מאוד דומים לאלגוריתמים בtrino.

- broadcast hash join - עושים broadcast ל dataset הקטן יותר ואז hash.
  ניתן להשתמש רק עבור שוויון.
  אם הdataset שעושים לו broadcast גדול מדי, נצרוך המון זכרון ונוכל לגרום לשגיאות OOM.

- shuffle hash join - מאוד דומה לקודם, רק עושים shuffle במקום broadcast.
  שימושי בעיקר כאשר dataset גדול מכדי לעשות לו broadcast אבל צד אחד של הpartition מספיק קטן כדי לעשות hash.

- Shuffle Sort Merge Join - כמו הקודם, רק כאשר ממיינים את אחד הdatasets במקום לעשות hash.
  שימושי כאשר הdatasets גדולים מכדי לשמור את הhash בזכרון.

- Broadcast Nested Loop Join - כמו broadcast, אבל עם nested loop שמאפשר Join שהוא לא שוויון.

- Cartesian Product Join - מאוד דומה לקודם, רק במקום broadcast, כל partition מרופלק לשאר הpartitions מהdataset השני בשביל join של לולאה כפולה.
  זה האלגוריתם join הכי יקר.
  ועדיף לא להשתמש בו, כי בעצם אין שום אופטימיזציה.

ניתן להשתמש בjoin hints כדי להגיד לspark להשתמש בjoin strategy ספציפי.
spark לא בהכרח ישתמש בjoin הזה כי הוא לא בהכרח נתמך.

האסטרטגיה של broadcasting נחשבת high risk higs reward כיוון שבהנחה ויש מספיק זכרון, זהו הjoin הכי מהיר שכן כל הטבלה תמצא בmemory.
מצד שני, אם הטבלה שעושים לה broadcast גדולה מדי, נקבל המון שגיאות OOM.

Narrow Transformation - פעולות בהן כל partition של output dataframe תלוי לכל היותר בpartition אחד של input dataframe.
למשל map למיניהם.

Wide Transformation - פעולות בהן partition של הoutput יכול להיות תלוי בכמה partitions של הinput.
ולכן יש צורך בshuffling כי הפעולה צריכה מידע מכמה partitions למשל groupby, joins.

בפועל בshuffle, המדיע שזז הוא רשומות על מנת לגרום לpartition חדש.

4. **Tungsten & Resources in Spark:** What is an RDD? Why did Spark move away from RDDs in favor of DataFrames/Datasets? Explain how Tungsten uses off-heap memory to avoid Garbage Collection pauses. Why is it a bad idea to give one executor a lot of resources (the "Fat Executor" problem)? What is the difference between Execution/Storage memory and the overhead memory? What happens when a task exceeds its allotted execution memory?

המבנים RDD, dataframe, dataset וההבדלים ביניהם הוסברו בפירוט בשאלה הראשונה.
בקשר לTungsten, הזכרון מוקצה באופן ידני

5. **Spark Skew, Partitioning & Caching:** What is data skew? how can it be solved? what is the difference between `repartition(n)` and `coalesce(n)`? What are the spark `StorageLevel`s? what is the difference between `cache` and `persist`? why are udf's (expecially in python) bad? how does spark solve the serde bottleneck with udf's?

## Q&A

1. 3 diffs, spark vs pandas

spark מבוזר לעומת pandas שקורה במכונה אחת.
pandas הוא single threaded ולכן הרבה יותר קשה לעשות scale
spark משתמש בlazy evaluation לעומת pandas, שלא.

2. \*\* polars
3. usecase of spark/pandas/polars

pandas - רלוונטי למשימות קטנות לוקאלית כאשר מעדיפים נוחות

4. spark submit

פקודת CLI שדרכה מריצים תהליכי spark.
כלומר נותנים בפקודה את כל הפרמטרים הדרושים, למשל הכתובת של ה Resource Manager, השם של האפליקציה, הjars של האפליקציה, הdeploy mode, resources של הרכיבים ועוד.

5. \* definity.ai
6. 3 transformers, 3 actions

transformations

- map - מפעיל פונקציה על כל איבר בdataset ומחזיר RDD חדש אחרי הפעלת הפונקציה על כל איבר.
- filter - מחזיר RDD חדש מפולטר כלומר רק עם הערכים שהוחזר עליהם True מהפרדיקט.
- repartition - עושה shuffle לדאטא רנדומלית על מנת ליצור את מספר הpartitions הנתון.

actions

- collect - מחזיר מערך של האיברים בdataset
- count - מחזיר את כמות הערכים בdataset (כמות שורות בdataframe וכמות ערכים בRDD)
- first - מחזיר את האיבר הראשון מהdatset.

7. RDD, Dataframe, Dataset

RDD הוא האבסטרקציה הבסיסית ביותר בSpark והוא בעצם אוסף immutable וpartitioned של איברים שניתן לבצע עליהם פעולות במקביל.

Dataframe הוא דו מימדי כלומר המידע מסודר בתוך עמודות עם שמות.
בפועל זה בתוך אובייקט שנקרא Row
אין type safety בכלל.
יש אופטימציות של הcatalyst.

Dataset הוא סוג של הרחבה של Dataframe אם יותר type safety כלומר יש encoder שמטרתו לעשות Serdes, כלומר ניתן להשתמש בcustom types למשל מחלקות java.

8. lifecycle of spark proccess

הלקוח שולח את הקוד לcluster באמצעות spark submit.
לאחר שהCluster Manager קיבל את הבקשה, הוא יוצר driver (תלוי deploy mode) הdriver מתחיל לבצע את הקוד שלנו.
יוצרים spark session, שמטרתו להיות אחראי על איתחול הSpark Cluster.
בנוסף הוא אחראי על תקשורת עם הcluster manager על מנת ליצור executors.
עוד על spark session בהמשך.
כעת האפליקציה רצה על הקלאסטר כלומר כל executor מבצע חלק מהקוד ומדווח לdriver וכו'.
לאחר שהתהליך הסתיים, הdriver מבצע exit ולאחר מכן, הcluster manager סוגר את ה executors.

9. האם transformation הוא interface ?

לא, הוא לא interface.

10. מה הכלל אצבע בחלוקה לstages ?

אוסף של transformations עד שצריך shuffle.

11. מתי stages יכולים לרוץ במקביל ?

כל עוד אין להם תלויות אחד בשני.

12. מה זה Task ?

פעולת העיבוד שקורית בפועל.
task היא פעולה שקורית בפועל על המידע, למשל טרנספורמציות למיניהן או count וקריאת מידע.

13. מה זה repartition ומה האלטרנטיבה ?

זאת פקודה לחילוק מחדש של הdataset, למספר partitions כנתון בפקודה, גורם לshuffling בין כל הpartitions על מנת להביא לגודל partitions אחיד.
ניתן להשתמש בcoalesce רק על מנת להוריד את מספר הpartitions.
הוא מאחד partitions ביחד ולכן זז בפועל פחות מידע, ואילו הpartitions החדשים יהיו כנראה פחות מאוזנים, אם הpartitions המקוריים לא מאוזנים.

14. spark session vs spark context

15. \* fault tolerance
    - מה קורה אם driver נופל
    - מה קורה אם executor נופל
16. מה ההבדל בפועל בין spark לtrino ?

יש כמה הבדלים, לא מאוד מהותיים מבחינת ארכיטקטורה.
spark מאופטם לשאילתות יותר custom כיוון שאין coupling לSQL אלא ניתן לרשום פונקציות אחרות ולהשתמש ביותר פונקציונליות.
ולכן יותר מאופטם לעיבודים גדולים בדרך כלל יש יותר
cluster spark מותאם ליוזר אחד מה שמאפטם על שאילתות יותר ארוכות וbatch כיוון שהoverhead של עלייה של cluster יכול להיות לא שווה את זה עבור שאילתות פשוטות.
ולכן עבור שאלות פשוטות שדורשות תשובה יחסית מהירה - adhoc עדיף להשתמש בtrino.

17. \* shuffle services
18. spark web ui

זה UI של spark שרץ ומציג מידע על האפליקציית spark.
יש כמה חלוניות.
בחלונית של הjobs ניתן לראות מידע על ה jobs שרצים, למשל מתי התחילו מי הריץ timeline של events שקשורים להוספה והורדה של executors.
ויזואליזציה של DAG, רשימה של stages ועוד.
בדומה יש חלונית של stages עם מידע על הstage, ויזאוליזציה DAG של הstage,
מידע על כל הtasks שרצים עם מטריקות עליהן
ניתן לראות את הקונפיגורציות בEnvironment Tab.
מידע על Executors, משאבים ניצולת מידע על shuffling וזמן GC.

## 2nd Q&A

1. איך polars הוא multithreaded אם יש נעילה על כמות הthreads בpython ?

polars משתמש בספרייה multiproccessing על מנת לגרום למקביליות בpython

2. איך קוד pyspark מתורגם לscala ?

משתמשים בסיפריית py4j על מנת לדבר עם הJVM ובפרט לדבר ב"python" עם הJVM.

3. מה זה apache arrow

זה data format קולומנרי שנשמר בmemory,
ומשתמשים בו בspark על מנת להעביר מידע בין תהליכי python לתהליכי spark.

4. בspark-submit עם local deploy mode, איך הdriver רץ ? בקונטיינר ? בJVM שונה ?

רץ בתהליך JVM לא בקונטיינר.

5. מצב שלישי של deploy mode (הייעוד העיקרי שלו הוא לtests)

המצב השלישי אם אפשר לקרוא לו כזה, הוא stand alone
כלומר הרצה לבד של כל הworkers כלומר הexecutors והmaster כלומר הdriver ללא YARN או K8S.

6. ארגומנטים לshow ?

דבר ראשון, show היא פקודה רק על dataframe/dataset.

n: integer - כמות האיברים להראות מהdataframe

trancate: bool or int - עם יש ערך מספרי, חותך מחרוזות עם ערכים גדולים מהמספר.
default הוא 20 אם יש true.

vertical: bool - אם true, מציג את הdataframe בצורה אנכית.

7. מה קורה בterminal כשמריצים spark-submit

8. מה זה predicate pushdown

אופטימיזציה ש"דוחפת" את הפילטר לdatasource על מנת לשלוף לspark כמה שפחות מידע.

9. האם spark יזיז repartition להתחלה ?

לא, אין אופטימיזציה שתזיז פקודה של repartition

10. האם עושים decleration לtype של RDD בJava/scala ?

בjava כן, בscala לא.

11. למה בpython אין Dataset ?

כיוון שpython היא לא typed ואילו dataset הוא כן,
אין סיבה שיהיה dataset אם אין typing, מאחורי הקלעים, dataframe הוא dataset של Rows.

12. למה צריך dataframe

13. האם ניתן לחלק מידע ספציפי לexecutor ספציפי ?

כן זה אפשרי בscala לפחות. ניתן להגדיר RDD עם preferred location למשל בעזרת הפעולה makeRDD.
זה אפשרי גם בpython אבל לא בצורה native אלא על ידי גישה לJVM.
ולאובייקטים של scala.

14. תהליך pyspark, שליטה בexecutors באמצעות conf

בגדול אפשר לקנפג את הגודל של הexecutors באמצעות הconf.
(מינימום memory הוא 471859200 בתים)

15. איך spark יודע כמה executors להקים ?
    האם ניתן להגדיר ? אם spark בוחר אז איך הוא יודע כמה צריך ?

ניתן או לקנפג ישירות באמצעות spark.executor.instances
או להשתמש בdynamicAllocation כלומר לקנפג spark.dynamicAllocation.enabled
ואז spark יתאים את מספר הexecutors בהתאם לworkload בזמן ריצה.

16. האם spark מקים מחדש executor שקיבל OOM/נפל ?
    ואם אקטיבית הורדתי אותו האם spark יחזיר אותו ?

17. איך spark מתנהל עם שגיאת הרשאות בזמן ריצה ?
18. מה היחידת מידה של מעבד בspark ?
19. כמה executors יופיעו בspark UI עבור כמות מבוקשת כלשהי ?

### Real-World Context

Rather than focusing on one technology, think about how these ideas show up in distributed processing frameworks, how they are used by other procerssing frameworks and what are the core concepts of processing.

## 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between Spark and an industry alternative.

    Deliverable: A written summary (minimum 1 or 2 sentences).
    Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
    Goal: You must be able to justify why the department uses this tool for our specific environment.

## 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

    Deliverable: A written summary example/story (two sentences approx.).
    Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.

## Wrapping Up :trophy:

Discuss your answers and any areas of confusion with your mentor. Reflect on how these general concepts will help when you later write code and help clients.

## Additional Topics from Review

- A deep dive into spark internals: what are other optimizations that are implemented in spark? what is java off-heap memory? how does spark's memory allocation work?
- What are other well known processing frameworks? what are the use cases spark meets? when should I NOT use spark?

## Action Items

- Review your notes and identify topics you want to explore deeper.
- Collect a list of real-world use cases for apache spark.
- Prepare questions for the upcoming mentor Q&A session.

## Recommemded Resources

- [Apache Spark Documentation](https://spark.apache.org/documentation.html)
