# Data Partitioning :

## Overview

This session isolates the concept of data partitioning. Rather than bundle it with Hive or other systems, we’ll treat partitioning as a fundamental data modeling and storage optimization technique. Expect five deep questions that cover motivation, strategies, pruning, bucketing, and real-world considerations.

**The focus is on understanding why and how data is partitioned across storage systems.**

## Goals

- Learn what partitioning means in the context of databases and data lakes.
- Explore different partitioning strategies and their trade-offs.
- Examine how partitioning interacts with query optimization and maintenance.

:warning: **Note:**

- This day is strictly theoretical; no specific software or engines are required.
- Discuss unclear points with your mentor.

### ⏳ Timeline

Estimated Duration: 0.5 Days

- Day 1: Learn what partitioning is and the core concepts; spend half a day.
  - Have a Q&A session the same day

## Core Questions

1. **Motivation & Definitions:** What problems does partitioning solve? Distinguish between horizontal and vertical partitioning, and between logical and physical partitions.

החלוקה לpartitions באה לעזור מבחינת ביצועים של שאילתות, כלומר ניתן לבצע שאילתות רק על החלקים הרלוונטים מהמידע. ובאופן כללי זה מאפשר ניהול של המידע ברמה יותר ספציפית כלומר במקום לנהל מידע של טבלאות ענקיות ביחד, אפשר לפרק ולנהל partitions.

בhorizontal partitioning מחלקים לפי שורות כלומר כל שורה תשמר בpartition אחר בהתאם לערך עליו עושים את הpartition.
לעומת זאת, בverical partitioning מחלקים את הטבלה לכמה טבלאות כשבכל אחת רק חלק מהעמודות.

בעצם ההבדל הוא בין הkey שאנחנו מגדירים שלפיו תתבצע הlogical partition לבין החלוקה על הדיסק של הDB עצמו כלומר physical partitioning.

2. **Strategies:** Describe common partitioning techniques (range, list, hash, composite) and when each is appropriate. Include considerations for time-series data.

range - המידע מחולק לפי range של ערכים בעמודה מסויימת למשל תאריכים או ערכים נומרים.
שימושי כאשר המידע עולה עם הזמן באופן יחסית אחיד

list - חילוק שורות לפי ערכים ספציפים למשל מדינה או סטטוס שימושי בקרדינליות נמוכה כאשר המכנה המשותף הזה חשוב לנו.

hash - הפעלת פונקצית hash על אחת מכמה עמודות וחילוק לפיה. שימושי כאשר חשוב לנו התפלגות אחידה בין החלקים ובשביל load balancing במערכות מבוזרות.

בקשר לtime series data, רוב הזמן המידע העדכני יותר חשוב ולכן הגיוני לבצע partitions לפי הזמן ולהעביר מידע ישן לcold storage.

3. **Pruning & Optimization:** Explain how partition pruning works and why it’s critical for performance. How do query planners determine which partitions to scan?

הpartition pruning הוא בעצם טקטיקה לסריקת פחות partitions ובכך לחסוך פעולות I/O יקרות.
זה עובד בשתי תצורות, static וdynamic.

בstatic זה קורה בזמן קומפילציה כלומר כבר ברמת הטבלה ששולפים עליה ניתן לקבוע את הpartition.
בdynamic, הפילטור קורה בזמן ריצה למשל כאשר השאילתה תלויה בעוד טבלאות ולכן לא ניתן לקבוע את הpartition בזמן קומפילציה.
בדרך כלל query planners יודעים לבצע partition pruning לפי החלק של הWhere.

4. **Maintenance & Evolution:** What challenges arise when partitions grow or have inconsistent metadata? Discuss operations like adding, dropping, or merging partitions.

כשpartitions גדלים יותר מדי, מאבדים הרבה מהיתרונות שלהם, נצטרך עדיין לסרוק כמויות גדולות של מידע ואז אולי כדאי לחשוב על איזשהו sub partiton או bucketing.
או לקחת partitions יותר קטנים.
כשמאבדים metadata על partitions או אם הmetadata לא מדויק זה יכול לגרום למנוע עיבוד לדלג על partitions רלוונטים לפספס מידע ועוד שאר ירקות.

בשביל להוסיף partitions זה קצת תלוי מימוש, בדרך כלל בrange, ניתן להוסיף partitions מהקצוות.
בlist אפשר להוסיף כל עוד זה לא קיים.
ובhash ניתן להוסיף אבל מידע יכול לזוז בין partitions ולכן זה יכול לקחת זמן.
בdropping פשוט מוחקים את הpartition
כלומר את המידע ממש.
לגבי merging, בrange, ניתן לחבר רק בין partitions סמוכים ובlist ניתן בין כל 2 ערכים והpartition יהיה כמצופה בשניהם.
בדרך כלל לא ניתן לעשות merge בין hash partitions.

5. **Bucketing & Data Layout:** What is bucketing, and how does it differ from partitioning? When is bucketing useful (e.g., joins, load balancing, reducing shuffle)? How can bucketing complement partitioning in large datasets?

ההבדל הוא שקובעים partitions לפי משמעות לוגית שתעזור לחלק את המידע ולעזור לתשאולים למשל לחלק משתמשים לפי ארצות מוצא. לעומת זאת בbucketing המטרה היא לחלק את המידע יותר באופן שווה כלומר סוג של load balancing, אבל המושגים די משלימים זה את זה.
על מנת למנוע מעבר של מידע ברשת, כלומר bucketing, בשביל join או כל פעולה אחרת שדורשת סוג של סיווג של המידע כמו groupBy. מומלץ להשתמש בbucketing כך למשל אם אנחנו יודעים ששתי טבלאות משתמשות בbucketing על עמודה שעושים עליה join בעצם אנחנו חוסכים את הshuffle הזה.

## Wrapping Up :trophy:

Review your answers with your mentor and identify scenarios where partitioning could dramatically improve or hurt a workload.

## Action Items

- Identify storage systems you want to try partitioning in (e.g., Hive, Iceberg, PostgreSQL).
- Prepare questions for the next mentor Q&A.
