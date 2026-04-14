# Zookeeper, Kerberos & LDAP :lock:

## Overview
This session focuses on the components that provide coordination and authentication in distributed systems.  Zookeeper acts as the lightweight coordination service, while Kerberos and LDAP handle secure identities and directory information.  These technologies are commonly paired in Hadoop and other big‑data ecosystems.

**Study the key components, design decisions, and how they work together to enable secure, reliable clusters.**

## Goals
- Learn Zookeeper’s architecture and core features.
- Understand the Kerberos authentication flow and the purpose of LDAP directories.
- See how these systems integrate with each other and with Hadoop.
- Practice organizing a self‑study day and managing your time.
- Prepare to discuss your findings with your mentor.

:warning: **Note:**
- This is a self‑study session; independence and time management are critical.
- Focus on grasping the full picture of each concept – if you can’t explain it, you haven’t learned it.
- When in doubt, ask your mentor which topics deserve deeper attention.

### ⏳ Timeline
Estimated Duration: 1 Day
- Day 1: Spent no more than third a day on each of the following: LDAP, ZOOKEEPER,Kerberos, Hint read a bit about Active Directory As well;
    - Have a Q&A session right after

## Core Concepts

### Zookeeper – five guiding questions
1. **Architecture & Data Model:**  Describe a Zookeeper ensemble, the role of the leader and followers, the znode hierarchy, and how znodes store data and metadata.

אנסמבל זה אוסף של שרתי זוקיפר בתוך כל אנסמבל כזה יש leader אחד וכל השאר הם followers. 
תפקיד ה followers  הוא להחזיק את המידע בפועל ולאפשר קריאות מהירות ללא צורך בסנכרון.
לעומת זאת בשביל כתיבות, שיש בהן צורך בתזמון, בשביל זה יש את ה leader שהוא מנהל את זה ומונע מקרים של corruption.
הznodes שומרים את המידע בצורה שמזכירה מערכת קבצים כאשר כל תיקייה היא גם קובץ ששומר מידע.
המידע נשמר גם לוקאלית על הזיכרון וגם נכתב לדיסק כלוגים.

2. **Consistency & Watches:**  How does Zookeeper guarantee sequential consistency?  Explain watches, one‑time triggers, and how clients use them for cache invalidation.

זוקיפר משתמש בפרוטוקול ZAB כלומר הפעולה נקלטת רק אם רוב השרתים הסכימו וקיבלו אותה בצורה אטומית ולכן מובטח עקביות בסדר של הפעולות בגלל האטומיות כלומר ברגע שהפעולה תתחיל היא תסתיים לפני שהפעולה הבאה תתחיל
watch זה כמו התראה כאשר node משתנה באיזשהי דרך ואז ניתן לטרגר פעולות בהתאם
כאשר עקביות היא קריטית צריך לעשות invalidate cache מיד כאשר מקור המידע משתנה ואז ניתן להשתמש ב trigger כדי לעשות את זה

3. **Sessions & Failure Handling:**  What is a Zookeeper session, how are heartbeats maintained, and what happens when the session expires?  Discuss how ephemeral and sequential nodes relate to this.

session - זה חיבור של לקוח לאנסמבל של זוקיפר
כדי לשמור על חיבור פעיל הלקוח צריך לשלוח heartbeat לשרת ואם לא נשלח לאורך זמן החיבור מתנתק
יש כמה סוגים של znodes:
ephemeral - קיים כל עוד החיבור פעיל וכאשר הוא מתנתק הוא נמחק אי אפשר ליצור בנים
sequential - נוצר עם מספר עולה מהאב אין מגבלות, כל znode יכול להיות sequential.

4. **Common Patterns:**  Explain how leader election, distributed locks, and configuration storage are implemented on top of Zookeeper primitives.

ניתן לממש leader election באופן הבא: יוצרים znode עם path "ELECTION". כל Node רושם את עצמו לבן של ה znode עם מספר sequence מי שהכי נמוך נבחר להיות ה leader

ניתן לבצע distributed locks באופן די דומה, כל אחד ירשום ephemeral sequential znode ל znode אחר תחת LOCK והנמוך ביותר מחזיק את המנעול. השחרור הוא במחיקת ה znode ובנוסף אם node קורס המנעול ישתחרר אוטומטית.

אפשרי להשתמש בשומר גן החיות כדי לממש אחסון לקונפיגורציה כאשר כמה תהליכים רוצים להשתמש ולגשת לאותם קבצים ונרצה לערוך אותם ולשמור על עקביות עם כל הסרוויסים שקוראים מהקונפיגורציהץ

5. **Operational Concerns:**  Outline how to deploy an ensemble, handle scaling, manage snapshots and transaction logs, and troubleshoot typical issues (e.g., split‑brain, latency).

דבר ראשון צריך להוריד java JDK כי zookeeper כתוב בשפה הנ"ל. מקנפגים את הגודל של ההיפ כדי למנוע כמות swaps. יוצרים קובץ קונפיגורציה ל zookeeper. יוצרים קובץ בשם myid שמכיל את ה id של המכונה 
יוצרים קובץ ריק בשם Initialize שמטרתו להודיע שהשרת לא מחזיק שום מידע, כשהוא קיים נוצר דאטא בייס ריק והקובץ נמחק, אם הוא לא קיים סימן שהתיקיית מידע ריקה ולא יהיו לו זכויות הצבעה 
ואז ניתן להריץ עם פקודת הרצה 
java -cp zookeeper.jar:lib/*:conf org.apache.zookeeper.server.quorum.QuorumPeerMain zoo.conf

ניתן לעשות scaling באמצעות פקודת reconfig עם add server והפרטים שלו.
או אם זה פרוס בקוברנטיס אז ניתן פשוט להעלות את המספר של הפודים ב zookeeperStatefulSet 

zookeeper יוצר snapshots של המערכת כאשר הגודל של הקובץ לוגים של הטרנזקציות גדל מדי ואז נוצר קובץ חדש. כאשר מתבצע snapshot עדיין snapshot 
המידע נכתב למערכת קבצים בדרך כלל חיצונית אבל עדיין יכולים להתבצע שינויים במקביל, שירשמו לקובץ לוגים אבל לא ל snapshot ולכן הסיומת של כל snapshot היא ה id של הטרנזקציה האחרונה שבוצעה, וניתן לשחזר את השאר דרך הקובץ לוגים.

zookeeper פותר את בעיית הsplit brain על ידי בחירת leader על ידי רוב זאת עוד סיבה שלפיה בוחרים מספר אי זוגי של שרתים, כך תמיד יש רוב בnetwork partition.

zookeeper מתמודד עם latency של nodes מאותה סיבה של quorum - לא צריך שכל ה nodes יסיימו לכתוב, מספיק רק רוב. עוד משהו שיכול לגרום לlatency הוא ה garbage collector ולכן כדאי לבדוק קונפיגורציות שונות שלו או להגדיל את ה heap.

### Kerberos – five guiding questions
1. **Protocol Flow:**  Walk through the Kerberos authentication flow from initial login (kinit) to obtaining service tickets.  Include AS, TGS, and ticket caches.

kerberos זה פרוטוקול אוטנטיקציה בין של שרתים ובין  של לקוחות על הרשת שלא שולח מידע כמו סיסמאות על גבי הרשת ולכן בטוח מפני ניסיונות התחזות.

החוזק העיקרי של kerberos הוא ב single sign on כלומר מזדהים פעם אחת ויש גישה לכל השירותים הרשומים.


תחילה מבקשים מה KDC כרטיס TGT, זאת באמצעות פקודת kinit, מקבלים בנוסף גם session ticket.
בעצם הTGT שקיבלנו הוא כמו certificate שמאשר אותנו.
כעת, צריך לבקש ST זה בעצם כרטיס שמבקש גישה לשירות המבוקש, שולחים ל KDC את הפרטים של השרת המבוקש ביחד עם ה TGT והפרטים של הלקוח (מוצפנים באמצעות הST) את כל זה מצפינים עם המפתח של הלקוח. ה KDC מאמת ושולח בחזרה ST מוצפן עם המפתח של השירות.
ולבסוף פונים לשירות עם ה ST והפרטים של הלקוח כאשר הפרטים מוצפנים באמצעות הsession ticket והשירות מאמת. (בתוך הST מופיע גם הsession ticket).

2. **Key Concepts:**  Define principals, realms, KDC components, tickets (TGT vs service ticket), and how encryption keys are derived and used.

principals - צד שאותו צריך לאמת (אפשר לבקש לאמת גם את השרת ולא רק את הלקוח).

realms - רשת לוגית בדומה לדומיין שמכילה את כל השירותים והלקוחות שרשומים בה.

הKDC מורכב מכמה רכיבים:

Authentication Server: זאת הישות שמאמתת את המשתמשים בפועל מול המאגר הרשום ומחלקת את ה TGT אם אכן המשתמש אושר.

TGS - Ticket-Granting Service - זאת הישות שמשלימה את ה AS על ידי אימות לשירות ספציפי, לאחר שיש TGT ניתן לשלוח אותו עם בקשה לשירות ספציפי, וה TGS מאמת את ה TGT ואם הוא נכון, שולח service ticket.

די מפורט למעלה ההבדל בין TGT ל service ticket

מפתחות ההצפנה הם פרטיים ולכן צריכים להיות רשומים מראש ב KDC, השימוש בהם מפורט לעיל.



3. **Security Properties:**  Why is Kerberos considered secure?  Discuss mutual authentication, replay protection, time sensitivity, and the role of the ticket lifetime.

kerberos נחשב בטוח מכמה סיבות.
אין מפתחות שעוברים בין הצדדים אלא כל האימותים עוברים דרך ה KDC שהוא אמור להיות צד שלישי אמין.
יש mutual authentication כלומר המשתמש יכול לבקש מהשרת לאמת את עצמו ולא רק השרת מהמשתמש.

אמנם הודעה יכולה להיקלט אצל גורם עוין ולהשלח שוב ועל ידי זה להשיג גישה. במקרה שלנו, תוקף יכול להשיג את התעבורה בין משתמש ל AS ולנסות להשיג את ה TGT ולאחר מכן להתחזות למשתמש.
הפתרון של kerberos הוא להוסיף להודעות timestamp או לא לאשר הודעות שהגיעו כבר. ויש הצפנה לפי ה session key שאמור לספק עוד שכבת הגנה, שכן אף אחד מלבד הצדדים המתקשרים לא אמור לדעת אותו
מהסיבה הזאת חשוב מאוד שהשעונים של הלקוחות ה AS וה TGS יהיו מתוזמנים.
ה ticket lifetime הוא בעצם התוקף של הכרטיס.
יש שני סוגים:
ticket lifetime - הזמן שיש לכרטיס הנוכחי
renewable lifetime - הזמן שאפשר לחדש כרטיס לפני שצריך להוציא אחד חדש לגמרי.

4. **Administration & Tools:**  What are common Kerberos administration tasks?  Describe commands like `kadmin`, `kinit`, `klist`, `kdestroy`, and how to add principals or change passwords.



5. **Integration & Troubleshooting:**  How do services (Hadoop, HTTP, SSH) integrate with Kerberos?  What are typical issues (clock skew, wrong realm, keytab problems) and how do you diagnose them?

### LDAP – five guiding questions
1. **Directory Structure:**  Explain how LDAP organizes information in a hierarchical tree (DN, RDN), common object classes, and attributes for users and services.
2. **Protocols & Operations:**  Describe basic LDAP operations – bind, search, modify, add, delete – and the difference between simple and SASL binds.
3. **Schema & Extensibility:**  What is an LDAP schema?  How do object classes, attribute types, and syntax rules define what data can be stored?  Mention extending schemas.
4. **Authentication & Authorization:**  How is LDAP used for authentication and authorization?  Cover binding with credentials, password policies, and group lookups.
5. **Deployment & Security:**  Outline how to install/configure an LDAP server (e.g., OpenLDAP), secure it with TLS, replicate data, and troubleshoot common errors (referral loops, access controls).

### 🔄 Alternatives
Assignment: You are required to research and write a comparative analysis between Zookeeper, Kerberos & LDAP and an industry alternative.
- Deliverable: A written summary (minimum 1 or 2 sentences).
- Focus: Compare performance, architecture, and specific "pain points" this tool solves compared to legacy systems or competitors.
- Goal: You must be able to justify why the department uses this tool for our specific environment.

### 🎯 User Story & Scenario
Assignment: Based on your research and understanding of the department's pipeline, define a concrete Use Case for this technology.
- Deliverable: A written summary example/story (two paragraphs approx.).
- Requirement: Describe a real-world scenario (e.g., a specific client requirement) where this technology is the optimal solution.
- Data Flow: Map out the data flow and explain how this tool integrates with other components in the Data Pipeline.

## Wrapping Up :trophy:
Review your answers with your mentor and discuss any unclear points.  Relate each concept back to actual deployments you might encounter.

## Action Items
- Note topics you want to investigate further.
- Prepare questions for the mentor Q&A session.
- Document any commands or configuration steps you used during research.

## Recommended Resources
- [Apache Zookeeper Documentation](https://zookeeper.apache.org/)
- [Kerberos: The Network Authentication Protocol](https://web.mit.edu/kerberos/)
- [LDAP: RFC 4511 Overview](https://datatracker.ietf.org/doc/html/rfc4511)
- *Hadoop Security* chapter in any modern Hadoop book for integration examples.
