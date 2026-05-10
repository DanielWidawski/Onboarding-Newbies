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

3. **Catalog Architecture:** Explain typical components of a catalog service
   (namespace management, table and partition metadata, permissions). What
   backend storage is used? Is the catalog itself just a database, or does it
   also manage pointers to objects in a blob store?

4. **Table Formats Overview:** Define what a table format is in the context of
   a data lake. How do formats like Iceberg, Delta, and Hudi differ from
   simple Hive/Parquet tables? What features do they add ?

5. **Metadata & Transaction Log:** How do modern formats store their own
   metadata? Discuss the concept of a transaction log or manifest file, and
   the distinction between file level metadata (e.g. Iceberg data file footers)
   and catalog entries. When would you even need to think about files if the
   catalog abstracts them away?

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
