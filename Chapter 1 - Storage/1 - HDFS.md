# Hadoop Distributed File System (HDFS) :elephant:

## Overview

This session focuses on the core concepts of HDFS, the distributed storage layer of the Hadoop ecosystem. Understanding its architecture will help you appreciate how big data clusters store and manage massive datasets across many machines.

**Study the key components, design decisions, and how they work together to provide fault-tolerant, scalable storage.**

## Goals

- Learn the architecture and roles of HDFS components (NameNode, DataNode, etc.).
- Understand how HDFS handles storage, replication, and availability.
- Practice planning a self-study day and managing your time.

:warning: **Note:**

- This is a self-study day; independence and time management matter.
- Focus on grasping the full picture of each concept; if you can’t explain it, you haven’t learned it.
- When in doubt, consult your mentor about what to study.

### ⏳ Timeline

Estimated Duration: 3 Days

- Day 1-3: Learn the concepts of HDFS; spent time on what is it? on fault tolernce, on failover process and on how reads and writes are being done?
  - Have a Q&A session at the third day and in between sessions each day

## Core Concepts

Consider the following five questions to cover the major HDFS topics:

1. **Architecture & Roles:** Describe HDFS’s overall architecture, including NameNode(s), DataNodes, blocks, and how the namespace and metadata are managed. Don’t forget the role of ZooKeeper in coordinating HA and keeping track of leases.

עובד לפי ארכיטקטורת master-slave.

NameNode - בעצם מנהל את כל הnamespace ואת המיפוי של בלוקים לdatanodes בעצם המאסטר בארכיטקטורה

DataNode - הישות ששומרת את הבלוקים של המידע בפועל. קריאות וכתיבות מתבצעות דרכה. כשהnode עולה, הוא מנסה להתחבר לnamenode, ומוודא שהnamespace והגרסה שלו תואמים לזה של הNameNode.

Blocks - כל קובץ בhdfs מחולק לבלוקים, כל בלוק הוא בגודל 128MB וכל בלוק נשמר פוטנציאלית במקומות שונים
בcluster

משתמשים בZK בשביל HA על ידי זה שכל NameNode פוטנציאלי מחזיק session פתוח בצורת ephemeral ובמידה והוא נסגר אז מתבצע leader election בשביל active namenode.

הhdfs מנהל leases שהם בעצם מנעולים (רק על כותבים) שמנוהלים גם הם על ידי הNN

2. **Storage & Fault Tolerance:** Explain how HDFS divides files into blocks, uses replication (default factor three), and how it detects and recovers from node failures.

כל קובץ מחולק לבלוקים בגודל 128MB. כל בלוק נשמר בDN ויש לו עוד 2 רפליקות (דיפולטית) המידע על המיפוי של קובץ-בלוקים כלומר לכל קובץ, איפה הבלוקים שלו נמצאים מופיע בNN. בתוך DN, כל בלוק מיוצג באמצעות 2 קבצים, הדאטא עצמו ומטא דאטא.
כדי לזהות בעיות, כל DN שולח לNN block report על כל הבלוקים שברשותו כל שעה, ושולח heartbeat לNN כל כמה שניות. אם לא התקבל heartbeat במשך 10 דקות, הNN מחשיב את הDN הזה כמת, ומשכתב את הרפליקות שלו לDN אחר.
בheartbeats מגיע גם מידע על השרת כמו מקום פנוי, אחוז ניצולת והמידע שעובר כרגע.
הNN משתמש בזה לLoad Balancing

3. **Topology Awareness & Performance:** What is rack awareness and why does HDFS replicate across racks? Discuss how block placement, snapshots, and checksums contribute to performance and data integrity.

כל rack זה בעצם קבוצת שרתים שמחוברת לאותה רשת ולכן תקשורת בה יותר מהירה. משתמשים בrack awareness בשביל HA, כלומר מחלקים את הרפליקות בין racks כדי שבמידה וrack נופל למשל הnetwork switch שלו, המידע עדיין יהיה נגיש.
בנוסף, ככל שהמידע מחולק בצורה יותר רחבה, הוא יהיה נגיש ביעילות ממקומות שונים ברשת ולא בהכרח מrack ספציפי.
מצד שני יש את הטרייד אוף עם הכתיבה, כתיבה לDNים שונים יותר איטית אבל יש פחות עמידות.

snapshots הם read-only-copy של איזשהו תת עץ בעץ תיקיות.
היתרון שלהם הוא שהם לא צורכים הרבה מקום אבל הם לא באמת שומרים את המידע עצמו אלא רק את המטא דאטא על כל קובץ והבלוק ליסט שלו.

hdfs יוצר לכל בלוק checksum בכתיבה ובודק אותו בקריאה.
זאת טכניקה לאימות המידע כלומר אם הייתה שגיאה אז היא תתגלה אבל לא מה הייתה השגיאה זה חישוב מאוד פשוט ולכן לא משפיע כמעט על הביצועים וזה לא שומר הרבה מקום.

4. **High Availability :** Outline HDFS High Availability (Active/Standby NameNode, JournalNodes). How do these features improve scalability and uptime?

קצת הזכרנו מקודם, כדי להשיג HA משתמשים בכמה NN שמחכים ב standby וכאשר הactive נופל הם מחליפים אותו מהר.
בשביל שההחלפה של הactive תתבצע כמה שיותר מהר משתמשים בJournalNodes.
בעצם הactive NN רושם פעולות שמתבצעות על הcluster לJN.
הstandby NN קוראים כל הזמן מהJN ומבצעים את הפעולות לוקאלית. כדי שפעולה תיחשב חוקית היא צריכה להירשם לרוב של ה JN.
בנוסף כל DN חייב לשלוח block reports גם לstandby כדי שתהיה להם גם תמונה נכונה של הקבצים במערכת.
באופן הזה אם הactive נפל, אחד הstandby יכול לתפוס את המקום שלו במהירות כמעט בלי צורך להסתנכרן

5. **Protocol & Operations:** Describe how clients read and write data to HDFS via RPC, how they locate NameNodes and DataNodes, how DataNodes send block reports, and why these mechanisms matter for everyday operations. Cover the runtime behaviour of leases and pipeline formation.

הלקוח לא מאתר ישירות את הNN, הוא פונה לnameservice, והוא מפנה אותו לactive. הnameservice עובד בעצם כמו סוג של proxy לNN.

בקריאה, הלקוח פונה לNN באמצעות RPC כדי לקבל את המיקומים של הבלוקים הראשונים של הקובץ. הNN מחזיר את הכתובות של הDN שיש להם רפליקה של הבלוקים האלה.
מוחזר אובייקט סטרים שעליו מופעל read() שמזרים מידע חזרה ללקוח כשמסיימים לקרוא את הבלוק, נסגר החיבור לDN והDFSInputStream מחזיר את הDN שמחזיק את הבלוק הבא.
כשמסיימים לקרוא סוגרים את הFSInputStream שעוטף את הDFSInputStream.

בצורה דומה, כתיבה מתחילה גם כן בשליחת RPC לNN עם בקשת create כדי ליצור קובץ חדש בלי בלוקים שקשורים אליו כרגע.
הNN מבצע בדיקות כדי לוודא כל מיני דברים, למשל הרשאות ושהקובץ לא קיים כבר. אם הכל עובר הNN יוצר רשומה עם הקובץ החדש. ואז מוחזר FSDataOutputStream שהלקוח יכול לרשום אליו מידע. כמו בקריאה זה עוטף את DFSOutputStream שמנהל את התקשורת בין הDN לNN.
המידע שנכתב מחולק לpackets שנרשמים לאיזה תור פנימי שנקרא data queue המידע נצרך באמצעות DataStreamer שאחראי לבקש מהNN להקצות בלוקים חדשים ולבחור רשימה של DNים שישמשו כרפליקות.
הרפליקות מהוות פייפליין כלומר הDataStreamer מזרים את הפקטות לDN הראשון והוא מזרים אותן הלאה לאחר שכל הDNים כתבו את המידע הם מחזירים ack.
לבסוף לאחר פקודת close הNN כבר יודע את המיקומים של הבלוקים והוא רק מחכה שכולם יחזירו לו ack.

הNN משתמש במידע מheartbeats גם כדי לדעת את המצב של הDN אבל גם להרבה דברים אחרים למשל כדי לרשום בלוק חדש לcluster, לדווח על מקום פנוי אחוז ניצולת.
הNN משתמש במידע הזה כדי לבזר עומסים בצורה טובה יותר ולתפעל את הcluster יותר ביעילות.

הblock reports חשובים כדי שהNN יוכל לדעת איפה נמצא כל בלוק כדי לדעת להפנות לשם במידת הצורך

על pipeline formation הסברתי בחלק של הכתיבה.
לגבי leases, מכיוון שאנחנו עובדים במערכת מבוזרת, אי אפשר לאפשר לשני כותבים לכתוב לאותו קובץ במקביל, lease הוא בעצם סוג של lock עם timeout.

חשוב לשים לב שניהול של heartbeats, block reports, leases כולם overhead של ניהול הcluster שיושב על הNN.

## Extra Questions

1. מה זה native api ?

זה בסהך הכל api רגיל או בעצם אינטגרציות שנוצרו על ידי אותו ארגון של האפליקציות עצמן למשל אינטגרציה בין Google meet ל Google cloud.

2. מה זה thrift ומה מיוחד בו ?

זה בעצם "מערכת" שדרכה ניתן לממש RPC.
הוא מאפשר Cross-Language Service, כלומר מאפשר להנגיש שירותים שרשומים בשפות שונות ובכך לאפשר אינטגרציה פשוטה יותר בין מערכות.

3. מה ההבדל העיקרי בין שרת rest סטנדרטי לבין שרת rpc ?

ההבדל העיקרי הוא שREST יותר מכוון לבצע מניפולציות על עצמים בשרת למשל להפעיל אותם או לצרוך אותם לעומת RPC שנועד להפעיל פונקציונליות מסויימת על שרת מרוחק ולהתייחס לזה כאילו זה הופעל לוקאלית.
ובנוסף, REST הוא stateless לעומת RPC שיכול להיות statefull

4. מה ההבדלים העיקריים בין HDFS 1 ל 2 ?

ההבדל העיקרי הוא הפיצ'ר של HA
YARN שנותן עוד dameons כמו resource manager, Node manager, app master ועוד
ויש את האופציה של פדרציה וכך כמה NN יכולים לשמור מידע באותו DN בלי שאחד יוכל לגשת למידע של השני.
נוסף גם rolling update.

5. למה נוצר HDFS ?

hdfs נוצר כדי לאפשר dfs על חומרה זולה, ועדיין להיות fault tolerant ועדיין להיות סקיילבילי מאוד וגם תומך בstreaming של מידע. נוצר לראשונה בשביל מנוע חיפוש Nutch

6. מה כלי הCLI המומלצים ביותר לפניה לHDFS ?

המומלץ ביותר הוא בעזרת ה native כלומר הhdfs cli.

7. האם קריאה של קובץ בHDFS היא לינארית או מקבילית ?

כן, קריאה של קובץ בhdfs היא מקבילית.

8. איך הגבלות על משתמש בhdfs ?

ניתן להגביל אחסון בנתיב מסויים על ידי quotas. כלומר האדמין יכול להגדיר space quota ובכל להגביל את הגודל של תיקייה ובפרט למנוע ממשתמש מסויים לפוצץ את הנתיב.

9. האם פניות לcluster חייבות להתבצע דרך ה active NN

כן, כל הפניות מופנות לactive NN כי הוא הישות הפעילה היחידה שמחזיקה את המטא דאטא על העץ תיקיות והמיקומים של בלוקים וקבצים ולכן אין דרך לבצע פעולות על הcluster שאינן עוברות דרכו.

10. Audit and Edit Logs ?

Audit - לעומת לוגים רגילים שבאים לתאר אירועים במערכת ובעיקר לזהות שגיאות, audit logs משמשים לתחקור יותר ספציפי, בעיקר כלפי משתמש, ומשמשים סוג של ראיה כלפי פעולות שמשתמש ספציפי ביצע לעומת flow כללי של המערכת.
Edit Logs - כשלקוח מבצע פעולת כתיבה, הטרנזקציה הזאת נרשמת דבר ראשון לedit logs ורק אחרי שזה נרשם הNN מעדכן את הפעולה בזיכרון שלו. בעזרת שילוב של fsimage ו edit logs ניתן לשחזר את המטא דאטא.

11. Under replicated and Missing blocks.

Under Replicated - הבלוק לא רופלק מספיק פעמים כמו שמוגדר בreplication factor.
Missing Blocks - הבלוק לא נגיש בcluster.

לעומת Unde replicated block שהמידע עדיין נגיש, בmissing block אין דרך לגשת למידע.
זה יכול לקרות למשל כשDN נופל או כשיש החלפה של active NN והתקשורת עם הJournal node אינה תקינה או שאפילו הfsimage והמטא דאטא לא מעודכנים.

12. מה זה RPC Queue ?

כל בקשות RPC נכנסות לתור. מהתור יש handlers שמוציאים את הבקשות מהתור ומטפלים בהן.
כאשר התור עמוס או מלא - הhandlers לא עומדים בקצב, בקשות יכולות לא להתבצע ובאופן כללי המצב של הcluster ובפרט הNN לא בריא.

## Q&A

1. האם יכולים להיות 2 active NN בכל דרך כלשהי ?

לא, תמיד יש active NN אחד, משתמשים בשיטות fencing כדי למנוע מצב של split brain. בhdfs משתמשים בZK אבל תיאורטית אם אין fencing, יכול להיות מצב של split brain.

2. איך עובדות הרפליקציות בrack awereness ?

מאפשר שרידות על ידי זה ששמים רפליקה מכל בלוק בrack אחר.

3. איך משתמשים יכולים לפנות לhdfs ?

יש כמה דרכים, או באמצעות הjava api או באמצעות הWebHDFS או באמצעות הCLI אם הורדנו hadoop client.
בכל המקרים צריך עותק של הקונפיגורציות כדי לדעת את הכתובת של הnodes בcluster.

4. \* איך אפשר לאחד קבצים ?
5. האם אפשר לעשות truncate ב hdfs ?

כן, זה אפשרי. במקרה של snapshots, hdfs יוצר בלוק חדש עם המידע לאחר הtruncate.

6. מה זה sequential reads ?

זו דרך גישה לדיסק, בה מידע רציף נקרא ביחד ה access pattern הזה נפוץ בעיקר עם קבצים גדולים.

7. מה זה checkpointing ב hdfs ?

זה בעצם התהליך של לקיחת fsimage קיים ואת הedit logs ולבנות בעזרתם fsimage חדש ועדכני.
checkpoint קורה כאשר עבר מספיק זמן מאז האחרון או שהתבצעו כמות מסויימת של שינויים.
את הcheckpoint יכול לעשות הstandby ואז לשלוח את הfsimage החדש לactive.

8. איפה snapshot נשמר ? איך הוא נראה ? מה קורה כשרוצים לשחזר ממנו ? איך הוא משפיע על ה quota ?

צריך להפוך את התיקייה ל snapshotable ואז ניתן לקחת snapshot של התיקייה. הוא בעצם סוג של hardlink לקובץ, הוא נשמר תחת התיקייה עצמה בhidden directory שנקראת .snapshot.
משחזרים על ידי העתקה של הקובץ מהתיקייה הזאת.

9. מה זה nameQuota ?

כמות הקבצים שמשתמש מסויים יכול ליצור תחת התיקיית root שלו.

10. האם Quota כולל רפליקציות ?

כן, כל רפליקה של הבלוק נחשבת בquota

11. מה ניתן לעשות בsafe mode ?

בעקרון בsafe mode רק פעולות read only מול המטא דאטא מובטחות לעבוד.
קריאת קבצים תעבוד רק כאשר הבלוקים נגישים על הDN שכרגע בcluster.

12. מה זה epoch numbers ב JN ?

זאת שיטת fencing כדי למנוע split brain.
כשNN נהיה active, הוא מקבל epoch number עולה. מספר כזה הוא ייחודי אי אפשר שלשני NN יהיה אותו epoch number.
כשNN שולח הודעה לJN הוא מצרף את המספר הזה והJN בודק אם המספר הזה הוא לפחות כמו מה ששמור אצלו לוקאלית. אם הוא יותר גדול הוא מאשר את ההודעה ומעדכן את המספר אצלו. אם זה קטן יותר, הוא דוחה. כיוון שצריך רוב, רוב של JN חייב להסכים על NN יחיד כחדש יותר.

13. אם למשתמש יש הרשאות כתיבה לקובץ אבל לא הרשאות execute לתיקייה אב שלו, האם הוא יכול לערוך אותו ?

לא, הוא לא יכול לערוך אותו.

14. הרשאות default ?

כשמגדירים הרשאות default על תיקייה, כל קובץ שנוצר מאותו רגע בתיקייה, יקבל את אותן הרשאות defaults.

15. sticky bit בלינוקס ו hdfs

ביט ששמים על תיקייה שמאפשר רק לבעלים של התיקייה לבעלים של הקובץ ולroot לערוך את הקבצים האלה או למחוק אותם. בלי sticky bit בהנחה ויש הרשאות write על התיקייה, משתמשים היו יכולים למחוק קבצים של משתמשים אחרים או להזיז אותם ולשנות את השם שלהם.
בhdfs משתמשים בפקודה
hdfs dfs -chmod +t /tmp

16. local user ב hdfs ?

זה המשתמש הלינוקסי שמחובר לשרת. דיפולטית הוא לא חלק מהמשתמשים הרשומים ב hdfs אבל ניתן לרשום אותו אם מתחברים לסופריוזר ויוצרים לו משתמש תחת /users ונותנים לו owner על התיקייה.

17. מה זה cloudera ?

חברה שמספקת מוצרים על גבי hadoop.

18. קבצי core-site, hdfs-site

core-site - משמש להגדרת הרכיבים בcluster כמו כתובות של nodes כמות הזיכרון המקסימלית לdaemons או כמות הthreads המקסימלית לdaemons.

hdfs-site - יותר קשור לניהול של הhdfs עצמו כמו גודל של בלוק, מיקומים של תיקיות ובגדול קונפיגורציות ברמת התוכנה.

19. האם quotas הם רקורסיבים ?

כן, quotas משפיעים על כל מה שמתחת לתיקייה שעליה מוגדרת הquota.

20. האם snapshots נחשבים כחלק מה nameQuotas ?

כן הם נחשבים חלק.

21. הרשאות רקורסיביות בhdfs - default.

ניתן להגדיר הרשאות default על תיקייה בhdfs ואז כל הקבצים שיווצרו מאותו רגע יקבלו את אותן הרשאות ACL.

22. hdfs dfs vs hadoop fs

hadoop fs - יכול לעבוד על כל מערכת קבצים ומקבל בארגומנטים שלו את הURI

hdfs dfs - הוא ספציפי לhdfs ולא דורש URI מלא.

23. האם משתמשי לינוקס לוקאליים יכולים לבצע פעולות בhdfs ?

כן, זה אפשרי.

24. מה המגבלה על כמות ACL שניתן להוסיף ?

ניתן להוסיף עד 32 כניסות.

25. האם ניתן להגדיר quota על נתיב חורג, ואם כן, מה המגבלות ?

כן, ניתן להגדיר quota על נתיב חורג, ואז לא נוכל להמשיך לחרוג אבל המידע שיש כרגע ישמר.

26. לאן קובץ הולך כשמוחקים אותו ?

כל קובץ שמשתמשים מוחקים, הולך לתיקייה .Trash תחת הhome directory שלהם.
בפועל זה כמו snapshot רק שנמחק לגמרי אחרי פרק זמן מוגדר וקונפיגורבילי.

### 🔄 Alternatives

Assignment: You are required to research and write a comparative analysis between HDFS and an industry alternative.

- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario

Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.

- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

## Wrapping Up :trophy:

Review your answers with your mentor and discuss any unclear points. Relate these concepts back to real-world usage scenarios you might encounter.

## Action Items

- Note topics you want to investigate further.
- Prepare questions for the mentor Q&A session.
- Continue the Day 01 challenge by linking these HDFS concepts to other chapters.

## Recommended Resources

- [Official HDFS User Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html)
- [Hadoop: The Definitive Guide (O'Reilly)](https://piazza-resources.s3.amazonaws.com/ist3pwd6k8p5t/iu5gqbsh8re6mj/OReilly.Hadoop.The.Definitive.Guide.4th.Edition.2015.pdf)
