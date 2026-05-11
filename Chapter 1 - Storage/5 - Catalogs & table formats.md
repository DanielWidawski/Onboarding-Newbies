# Catalogs & Table Formats :

## Overview

This session dives into the metadata layer that sits above raw files in a data
lake or warehouse. Before we talk about individual systems, start by thinking
about the big picture: what is a _data warehouse_ versus a _data lake_ versus a
_lakehouse_, and why do teams care about catalogs and table formats in each
case? (Hint: consistency, governance, and performance are the common threads.)

We’re not going to install or run Spark/Trino/etc. (If you don’t know what those are, no worries you will soon.);
the material stays at themetadata level. That said, good formats enable optimizations such as
partition pruning, predicate push‑down, and efficient file compaction, all of
which have a dramatic impact on execution even though we won’t be executing
anything here.

\*\*We’ll examine why catalogs exist, how they differ from Hive’s metastore
(which is itself just one implementation of a catalog), and the design goals of
modern table formats such as Iceberg, Delta Lake, and Hudi. Examples of
catalog implementations include Hive Metastore, AWS Glue, Databricks Unity
Catalog, and even simple relational databases;

## Goals

- Clarify what catalogs and table formats actually manage and why teams put
  them on top of object storage.
- Sketch the difference between a warehouse, a lake, and the newer lakehouse
  idea so you have context for why metadata matters.
- Learn about emerging formats that implement ACID, schema evolution, time
  travel and other optimizations, and why those features make life easier for
  query engines.
- Build on previous lessons by focusing on interoperability and metadata
  management rather than specific execution engines.

:warning: **Note:**

- Keep the focus on metadata and format, and on optimizations derived from those rather than on query engines or execution.
- Ask your mentor if you're unsure about scope.

### ⏳ Timeline

Estimated Duration: 1 Day

- Day 1: Learn the concepts of catalogs and table formats; spend the day.
  - Have a Q&A session the same day

## Core Concepts

1. **Data warehouse / lake / lakehouse:** What are the defining
   characteristics of each? Why do architects care about a separate metadata
   layer in a lakehouse versus a traditional warehouse?

המאפיינים של Data Warehouse הם בעיקר schema on write, כלומר המידע נבדק ונאכף על ידי הסכימה בכתיבה שלו לwarehouse, זה מאפשר ביצועים מאוד טובים ברמת התשאול ולכן data warehouse מאוד שימושיים לBI.
בדרך כלל יש מנוע תשאול מובנה, כלומר אין הפרדה בין storage ל compute.

המאפיינים העיקריים של data lake הם בעיקר
schema on read כלומר אין פורמט סטנדרטי למידע נכנס אלא סכימה נאכפת כשניגשים למיד.
זה מאפשר יותר גמישות ברמת המידע שניתן לשמור והם יכולים להכניס מידע במהירות גבוהה יותר.
יש הפרדה בין storage ו compute ולכן הם בדרך כלל יותר זולים וסקיילבילים.

מאפיינים של data lakehouse הם בעיקר שילוב של השניים.
מצד אחד מידע יכול להגיע בכל התצורות (סכימה בכתיבה היא אופציונלית).
בדרך כלל יש כלי אנליטיקות שקשורים (integrated) יותר לlakehouse
ותמיכה בACID.
אבל הם גם מפרידים storage ו compute.

מרוויחים הרבה מזה שמוציאים את הmetadata layer מהstorage, בעיקר כי בlakehouse האחסון הוא מאוד זול ובדרך כלל גם איטי, ואם הmetadata מופרדת אז ניתן לתשאל אותה בהרבה יותר יעילות והיא לא תלויה באחסון עצמו.
בwarehouse, שבדרך כלל מגיע כמוצר מוגמר הגישה לmetadata פחות תכופה כי המידע יותר מסודר ויותר יעילה כי זה מותאם ישירות לwarehouse.

2. **The Concept Of Catalog** Describe the purpose of a metadata catalog. How
   does it compare to Hive Metastore (hint: the metastore _is_ a catalog)
   and why might systems introduce separate catalog layers (e.g. AWS Glue,
   Databricks Unity Catalog, in‑house catalog backed by PostgreSQL)?

הקטלוג הוא בעצם רשימה של המידע הקיים במערכת משתמשים בו כדי למצוא ולהבין את המידע בקלות.
הHMS הוא סוג של קטלוג.
בעצם השימוש בו הוא על מנת לסווג את המידע וגישה אליו בצורה מהירה ולדעת מידע עליו בלי לגשת למידע ישירות.
חברות נוהגות להוציא קטלוגים משלהן כדי להפריד תלויות מהדאטא עצמו לקטלוג.
וכל catalog עוזר לדברים קצת יותר ספציפים.
ובגדול כל המטרה של קטלוג הוא לסווג את המידע ללא תלות לאיך הוא נשמר אז אין סיבה שהוא לא יהיה אגנוסטי לפלטפורמת האחסון.

3. **Catalog Architecture:** Explain typical components of a catalog service
   (namespace management, table and partition metadata, permissions). What
   backend storage is used? Is the catalog itself just a database, or does it
   also manage pointers to objects in a blob store?

namespace management זה בעצם איחוד לוגי של כמה טבלאות תחת אובייקט אחד שהוא הnamespace.
(יכול להיות שהכוונה הייתה יותר לסכימה ואכיפה של שמות כדי למנוע קומפליקטים)
בקטלוגים מודרנים, הmetadata מנוהל גם כן על ידי הקטלוג כלומר מיקומים ושמות של טבלאות וחלוקה שלהם לpartitions.
בגדול הרשאות די סטנדרטיות, יש איזשהו read שמאפשר לקרוא מידע, write שמאפשר לבצע פעולות על המידע ולהוסיף מידע חדש ואיזשהו admin שיכול לנהל את הגישות ולערוך את הקטלוג עצמו.

בדרך כלל קטלוגים משתמשים בRDBMS כדי לאחסן את המידע שלהם. כלומר מידע של הקטלוג עצמו וmetadata.

אני הייתי חושב על קטלוג כDB של metadata.
בדרך כלל הוא ממומש על ידי DB כלשהו אבל המידע ששמור בו לא קשור ישירות למה שמחפשים אלא רק מקשר לוגית בין המידע הקיים
קטלוגים יכולים להחזיק פוינטרים למידע חיצוני כלומר למיקום של המידע בstorage וכך גם לאובייקטים בblob storage.

4. **Table Formats Overview:** Define what a table format is in the context of
   a data lake. How do formats like Iceberg, Delta, and Hudi differ from
   simple Hive/Parquet tables? What features do they add ?

table formats הם פורמטים לאיגוד מידע גולמי תחת טבלה אחידה עם ניהול metadata, schema, ACID.
הם מאוד שימושיים בdata lakes כי בdata lakes אין פורמט קבוע למידע שיכול להכנס מה שיכול לגרום להמון מידע לשבת בdata lake בלי יכולת לחפש בו משהו ספציפי - swamp.

דבר ראשון parquet הוא לא table format, אני לא מבין מה אפשר להשוות אליו, זה האובייקט הפיזי וtable format הוא יותר קונספט אבסטרקטי.

בנוגע להייב, יש פחות תמיכה בtransactions לפחות בצורה הפשוטה (זה אפשרי עם transactional tables).
ובנוסף, המבנה ההיררכי גורם לנעילות ומקשה על טרנזקציות.
הוא לא תומך בtime travel והתמיכה בו דועכת עם השנים.
לעומת table formats עדכניים יותר כמו Iceberg, Delta, Hudi.
בגדול hive היה הפורמט הבסיסי וכל פורמט הרחיב לuse case יותר ספציפי,
כך למשל Hudi תומך ביותר פעולות יותר realtime ו Delta שם דגש על reliability וACID.

5. **Metadata & Transaction Log:** How do modern formats store their own
   metadata? Discuss the concept of a transaction log or manifest file, and
   the distinction between file level metadata (e.g. Iceberg data file footers)
   and catalog entries. When would you even need to think about files if the
   catalog abstracts them away?

בפורמטים טבלאיים מודרנים, המטא דאטא על טבלה נשמר בdata lake סמוך לטבלה ולכן ניתן למצוא אותו בקלות מאוד דרך הקטלוג.

manifest files בעצם שומר metadata על כמות של קבצים בין היתר partitions וסטטיסטיקות וכך בעצם מאפשר דילוג על מספר קבצים על ידי קריאת קובץ אחד וחוסך טעינת המון קבצים גם אם קוראים רק את ה footer שלהם.
העיקרון של transaction log הוא די דומה לכל העקרונות של edit logs וWAL והם באים כדי לאפשר transactions.

המידע ששמור בקטלוג הוא חילוק לוגי של הקבצים לטבלאות והמיקומים שלהם. לעומת זאת הmetadata של קבצים הוא מה שמאפשר לנו לקרוא אותם. אי אפשר לקרוא קובץ באופן יעיל ולפעמים בכלל בלי המטא דאטא שלו, נניח ולא היינו יודעים איפה מתחילים ונגמרים row groups ב

6. **Interoperability & Ecosystem:** Describe how catalogs and formats enable
   multiple compute engines to work on the same data (Spark, Trino, Flink).
   Why is standardization important? What role do open specifications
   (e.g. Apache Iceberg spec) play?

## Wrapping Up :trophy:

Review your answers with your mentor, focusing on how catalogs and formats enable a consistent data platform across tools.

## Action Items

- Identify catalogs or formats you’d like to try in practice.
- Prepare questions for the mentor Q&A session.
- Link these ideas back to the [intro chapter](../Chapter%200%20-%20Intro/1%20-%20Big%20Data%20Core%20Concepts.md).

### 📚 Resources

Use the resources listed below and practice searching the internet for questions not answered by the provided documentation.

- [Apache Iceberg Definitive Guide](<http://103.203.175.90:81/fdScript/RootOfEBooks/E%20Book%20collection%20-%202024%20-%20F/CSE%20%20IT%20AIDS%20ML/Apache%20Iceberg%20(2024).pdf>) Use this resource only for warehouse vs lake vs lakehouse (Iceberg will be learned on a different day)
