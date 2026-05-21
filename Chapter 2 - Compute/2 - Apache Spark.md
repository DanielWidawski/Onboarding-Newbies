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

3. **Spark Shuffle & Joins:** Compare the different kind of joins, and when will spark use each? how can we tell spark to prefer one over the other? what is join reordering? and why is "broadcasting" considered a high-risk, high-reward optimization? What is a _Narrow_ transformation, and _Wide_ transformation? Why do some operations require shuffle? what exactly is written in shuffle?

4. **Tungsten & Resources in Spark:** What is an RDD? Why did Spark move away from RDDs in favor of DataFrames/Datasets? Explain how Tungsten uses off-heap memory to avoid Garbage Collection pauses. Why is it a bad idea to give one executor a lot of resources (the "Fat Executor" problem)? What is the difference between Execution/Storage memory and the overhead memory? What happens when a task exceeds its allotted execution memory?

5. **Spark Skew, Partitioning & Caching:** What is data skew? how can it be solved? what is the difference between `repartition(n)` and `coalesce(n)`? What are the spark `StorageLevel`s? what is the difference between `cache` and `persist`? why are udf's (expecially in python) bad? how does spark solve the serde bottleneck with udf's?


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
