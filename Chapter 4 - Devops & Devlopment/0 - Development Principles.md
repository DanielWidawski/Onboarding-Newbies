# Software Development Foundations & Python Basics

Before building data pipelines or services, it is important to understand the
core principles of modern software development.

This module introduces the development practices, conventions, and tools that
are commonly used in professional engineering environments.

The goal is not only to learn *what the tools are*, but also *why they exist*
and how they help create maintainable, scalable, and collaborative systems.

---

### ⏳ Timeline
Estimated Duration: 2 Days

Day 1 – Software Development Foundations  
- Development principles and clean architecture
- Development workflows and collaboration
- Testing approaches and design paradigms

Day 2 – Python and API Foundations  
- Python ecosystem and development patterns
- REST APIs and Python frameworks
- Testing, mocking, and service design

---

### 📚 Resources
Use the resources below and practice researching additional information online.

- [Clean Python - Sunil Kapil](https://edu.anarcho-copy.org/Programming%20Languages/Python/Clean%20Python.pdf)
- [SOLID Principles Overview](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Python Official Documentation](https://docs.python.org/3/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

---

# Software Development Principles

### ❓ Guide Questions

1. What are **Clean Code principles**, and why are they important in software development?  
   Explain ideas such as readability, maintainability, and the principle of  
   **“Leave the codebase cleaner than you found it.”**

כל הרעיון של "clean code" הוא כדי לגרום לקוד להיות כמה שיותר מובן קריא ונוח לתחזוקה.
זה נובע מכמה עקרונות.
למשל עקרונות SOLID שנדבר עליהם בהמשך.
ואפילו ברמת הקוד עצמו, כמו להימנע מhard coding מספרים ומחרוזות, שימוש בשמות אינדיקטיביים, פונקציות בסיסיות שעושות דבר יחיד ולשאוף לכמה שפחות side effects, העקרון של dry כלומר dont repeat yourself לא לרשום את אותה לוגיקה פעמים אלא להשתמש באבסטרקציות.

boy scout rule - תמיד להשאיר את הקוד יותר "clean" מאיך שנכנסת אליו.
למשל שינוי שם של משתנה או כל דבר קטן שמנקה את הקוד.
או פיצול של פונקציה ארוכה.
כלומר שיפור של הקוד על ידי כל מפתח לאורך זמן.

readability - למשל בא לידי ביטוי בבחירת שמות אינדיקטיביים למשל לא לקרוא לפונקציה סתם make() אלא השם של הפונקציה צריך להסביר למה הפונקציה קיימת, מה היא עושה ואיך משתמשים בה.
אם צריך הערה אז השם לא מספיק טוב.

maintainability - היכולת לשנות ולהרחיב את הקוד לאורך זמן זה משפיע על הפיתוח של הcode base לאורך זמן ועל הקלות בה ניתן לדבג ולמצוע באגים.


2. What are the **SOLID principles**?  
   Describe each principle and explain how they help create maintainable
   object-oriented systems.

אלה בעצם ראשי תיבות (לראשי תיבות) לחמישה עקרונות פיתוח לעיצוב קוד שהם בעצם "חמשת הדיברות" לאיך לשמות על clean code וקוד שבנוי בצורה נכונה.

S - S.R.P - Single Responsibility Principle - כלומר כל דבר או יחידה בקוד למשל class או פונקציה צריכות להשתנות מסיבה אחת יחידה.
בגדול מה שהעקרון אומר זה "לאחד את כל הדברים שיש להם אותה סיבה להשתנות ולהפריד דברים שיש להם סיבות שונות".
"תופעת לוואי" של SRP היא קוד פשוט יותר.

O - O.C.P - Open-Closed Principle - המודל צריך להיות פתוח להרחבות וסגור לשינויים.
למשל לא נרצה שכתיבות יתנהגו שונה למדפסת מלדיסק, כלומר המודל של כתיבה לדיסק לא צריך להשתנות אבל נרצה להרחיב ולאפשר כתיבה למדפסת או למסך.
בפועל למשל עם יש שגיאת במודל שרושם למדפסת לא נרצה לשנות בטעות גם את המודל שרושם למסך.

L - L.S.P - Liskov's Substitution Principle - כל קוד שמשתמש בממשק (בעברית זה קשה לתרגם מונחים...) לא יכול "להתבלבל" מהמימוש של הממשק עצמו.
בפועל זה אומר שנוכל להחליף בין מופע של מחלקה יורשת למופע של מחלקת האב ועדיין הלוגיקה של הקוד תעמוד.
אם זה לא ככה זה יכול לגרום לשגיאות לא צפויות והמון if else.

I - I.S.P - Interface Sergregation Principle - לשמור על interfaces קטנים וקצרים, כך שמשתמשים לא סתם יהיו תלויים בדברים שהם לא צריכים.
במידה ולא שומרים על העקרון הזה, מודל A מסויים שתלוי במודל B ומממש רק חלק מהפונקציונליות שלו יצטרך להתקמפל מחדש גם אם לא שינינו משהו שהוא תלוי בו.
מה גם שתלות מאוד ארוכה יכולה להקשות על מציאת באגים, למשל באג בB יכול לקרות בA למרות שלא צריך את התלות הזאת.

D - Dependency Inversion Principle - התלות צריכה להיות בכיוון של האבסטרקציה, מודלים ברמה גבוהה יותר לא צריכים להיות תלויים במודלים ברמה נמוכה יותר.
למשל לא נרצה שפונקציה שעושה חישוב מסובך תהיה תלויה בפונקציה שקוראת מקובץ או למשל שהמודל של הלוגיקה של העסק תהיה תלויה בDB מעליו אנחנו שולפים.

3. Explain the **KISS principle** and its importance in software design.
Why does simple and intuitive software scale well?  
   Why do overly complex systems tend to fail over time?

הרעיון של העיקרון הזה הוא לשמור על קוד כמה שיותר פשוט.
קוד פשוט הוא יותר קל לתחזוקה וההבנה של הלוגיקה שלו יותר פשוטה.
סיבוכיות מובילה לבלבול ושגיאות, מפתחים מתחלפים והרבה יותר קשה להיכנס לקוד שלא רשום בצורה פשוטה ויש בו לוגיקה מורכבת.
הרבה יותר קשה לבנות מערכות מורכבות על קוד מורכב, כלומר כל רכיב שמוסיפים עלול לפגוע במשהו כאשר הקוד לא מספיק ברור.
עקרון KISS מקל על סקיילביליות בכך שהבסיס של המערכת מאוד פשוט ולכן יותר קשה "לשבור אותו".

4. What are the most common **paradigms / programming** (ex. Object Orianted) styles, what are the differences and when should each be used

Imperative programming - תכנות על ידי סדר מוגדר היטב של פעולות למכונה.
שימושי כאשר המתכנת צריך שליטה מוחלטת על התכנית.

OOP - תכנות מונחה עצמים, תכנות על ידי הגדרה של אובייקטים עם states והתנהגות שמשוייכת להם.
כלומר לכל אובייקט מוגדר מידע שהוא ה"עיקר" והפעולות הן משניות.

Procedural programming - נובע מתכנות אימפרטיבי ובמקום רצף לינארי של פעולות, אוסף ביחד כמה פעולות לתת רוטינות או פרוצדורות.
זאת השיטה המודרנית יותר של תכנות אימפרטיבי עם הגדרה של פרוצדורות אינדיקטיביות במקום GOTO לא מובנים, וניתן להגדיר סדר יותר קריא לתכנית באמצעות הפרוצדורות.

Declarative programming - הגדרה של משימות ללא האופן בו הם יתבצעו. בניגוד לתכנות אימפרטיבי בו אנחנו אומרים בפירוש איזו פעולה לבצע, פה אנחנו רק מציינים את התוצאה.
שימוש מאוד נפוץ הוא SQL בה אנחנו מציינים תוצאה באמצעות השאילתה, והDBMS מבצע אותה מאחורי הקלעים.
שימושי כאשר צריך את האבסטרקציה הזאת למשל שימוש בשפה SQL וכל DBMS מממש שאילתות בפועל בצורה קצת שונה.

Functional programming - מתייחסים לפונקציות כמו משתנים והם אבן הבניין הבסיסית ביותר של הקוד.
זה סוג של בנוי על תכנות דקלרטיבי כיוון שניתן באמצעות פונקציות קטנות להגדיר לוגיקה מבלי לציין את הcontrol flow בפועל על ידי השמה של פונקציות והרכבה שלהן במשתנים, או הפעלת פונקציות על פונקציות אחרות, למשל נגזרת.
הפרדיגמה היא stateless כלומר אי אפשר לשנות אובייקטים אלא רק ליצור חדשים.


5. What is **Test Driven Development (TDD)**?  
   Explain the development cycle and how it improves code reliability.

כותבים קודם tests שמן הסתם יכשל, ואז רושמים קוד ואז רושמים את הקוד הכי פשוט שאפשר שיעבור את כל הבדיקות.
וחוזרים חלילה.
בגישה הזאת מבטיחים קוד תקין ופשוט.

---

# Development Workflows & Architecture Concepts

### ❓ Guide Questions

1. Explain the difference between a **Pull Request (PR)**, **Code Review (CR)**,
   and **Design Review (DR)**.  
   Why are these processes important in team development?

2. Define the role of a **Pull Request (PR) / Merge Request**.
What is **squshing**? Why is it common practice to squash commits before the final merge?
Find how can you **apply specific fixes** from one branch to another without merging the entire history?
What is the process for **safely undoing** a merged PR using git revert?

3. Explain the difference between **CLI (Command Line Interface)** and
   **UI (User Interface)** applications.  
   What are the benefits of each?

4. What is the difference between a **compiler** and an **interpreter**?  
   Provide examples of languages that use each approach.

5. What is **event-driven programming**?  
   Explain how it differs from procedural execution and where it is commonly used.

---

# Python & API Foundations

### ❓ Guide Questions

1. What is **Python**, and what are its main characteristics compared to other
   programming languages (for example c#)?  
   Discuss readability, ecosystem, and runtime behavior.

2. What is a **REST API**?  
   Explain the core concepts such as resources, HTTP methods, and stateless communication.

3. **What is the Global Interpreter Lock (GIL) in Python?**  
   Explain:
   - What the GIL is and why it exists  
   - How it affects multi-threading and CPU-bound vs I/O-bound tasks  
   - Differences (if any) in how the GIL behaves across Python versions  
   - What Python 3.14 introduces regarding optionally disabling the GIL and why this is significant  
   - Common strategies to work around its limitations (e.g., multiprocessing)

   **Bonus:** Compare **FastAPI** and **Flask**.
   What are the architectural differences and when would you use each framework?

4. What are e2e testings? What are **tests** in software development, and why are they important?  
   Explain unit tests, integration tests, and the role of automated testing.

5. What are **mocks**, and why are they used in testing?  
   Compare **pytest** with other Python testing frameworks and explain its advantages.

---

### 🔄 Alternatives
Assignment: Research and briefly compare **two development approaches or tools** mentioned above.

Examples:
- FastAPI vs Flask
- Interpreted languages vs compiled languages

Deliverable:
- A short written comparison (1–2 sentences).
- Include a **real-life use case** for each alternative.

Goal:
Be able to explain **why a specific tool or development approach would be chosen in a real system.**

---

### 🎯 User Story & Scenario
Assignment: Based on your research, describe a small example of a **Python service or tool**.

Deliverable:
Two short paragraphs describing:

- A realistic scenario where a Python service is required.
- How testing (pytest), mocking, and clean code practices would be applied.

