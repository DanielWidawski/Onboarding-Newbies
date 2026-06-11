# Docker Foundations

Docker is a platform for running applications in isolated environments called containers.

It introduces a standardized way to package and execute software across different environments, without depending on the underlying system configuration.

Instead of installing dependencies directly on a machine, applications are bundled into portable units that can run consistently wherever Docker is available.

---

### ⏳ Timeline
Estimated Duration: 1 Day

Day 1 – Docker Core Concepts  
- Containers vs Virtual Machines  
- Images, Containers, Dockerfile  
- Networking & Storage  
- Security & Isolation  
- Build strategies (Docker, Kaniko, DinD)

---

### 📚 Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kaniko Documentation](https://github.com/GoogleContainerTools/kaniko)
- [OCI Specification](https://opencontainers.org/)

---

# Docker Core Concepts

### ❓ Guide Questions

1. **What is Docker and what problems does it solve?**  
   Explain what a container is, how it differs from a virtual machine, and why containers are useful in modern systems (portability, consistency, isolation).

2. **What are the core Docker components and how do they interact?**  


3. **How do networking and storage work in Docker?**  
   Explain:
   - Container networking (bridge, host, ports)  
   - Communication between containers  
   - Volumes vs bind mounts  
   - When to use persistent storage

4. **What are the security and isolation risks in Docker?**  
   Discuss:
   - Namespaces and cgroups (high-level)  
   - Running containers as root vs non-root  
   - Image vulnerabilities and best practices

5. **How are Docker images built in different environments?**  
   Compare:
   - Standard Docker build  
   - Docker-in-Docker (DinD)  
   - Kaniko  
   Explain when each approach is used (e.g., CI/CD pipelines, Kubernetes).

---


## Q&A

1. האם משאבים מוקצים לnamespace או container ?

משאבים מוקצים לcontainer.

2. מה הIP של השרת DNS שקונטיינרים מתקשרים דרכו ?


3. מה זה docker internal ?

זה שם DNS שהופך לIP של הhost

4. מה יש בImage בפועל ?

בפועל זה רשימה של פקודות מול הdocker daemon

5. מה עדיף הרבה layers קטנים או קצת גדולים ?

בעקרון עדיף קצת layers גדולים כי בכל הוספה של layer יש גם extra metadata של ה layer וגם כי יצירת container דורש לכאורה הרצה של כל layer.

6. Entry, CMD, RUN

Run - מריץ פקודות שהכרחיות לבניית הimage למשל הורדת סיפריות ותלויות.
ולכן יוצר layer חדש בתמונה 

CMD - מציין ארגומנטים שיוכנסו לentry point למשל פרמטרים דיפולטים שניתן לעקוף

Entry point - קובץ הרצה שתמיד ירוץ כשהקונטיינר למעלה.

7. איך מוגדר layer בimage ?

פקודה בdockerfile יוצרת Image. 
(כאילו פקודה שהיא לא בזמן ריצה)

8. מה זה dangling image ?

תמונה שבנינו מחדש אבל לא נתנו להם שם חדש ואז הקודמים נהיים dangling image.
בפועל אלה תמונות שאין להם tag

9. מה זה Expose ולמה צריך אותו ?

זה יותר לצורך תיעוד או אם נריץ עם -P 
(הדעה שלי, לא כזה רלוונטי, תיעוד אפשר לעשות במקומות אחרים...)

10. מה ההבגל בין depends on לhealth check ?

ההבדל הוא שdepends on עובד ישר כשהקונטיינר למעלה.
healthcheck נותן אופציה לוודא שיש גם פונקציונליות עם בדיקות custom שרושמים למשל curl לאיזשהו sontainer .
כך ניתן להגדיר ממש מה זה אומר "container למעלה"

11. docker namespace vs linux/kernek namespace ?

לא ממש הבנתי את השאלה, docker משתמש בnamespaces לינוקסים למשל PID namespace.

12. איך יודעים שקרס בגלל OOM 

אפשר לראות בdocker inspect על הקונטיינר לאחר שנפל

13. מה זה image from scratch ?

אלו images שבנויים על הsctatch image שהיא ריקה בפועל.
למשל הimage של debian ועוד מלא.

14. מה זה kaniko ומה מחליף אותו ?



15. מה זה multi stage build ?

זה בגדול docker file עם כמה FROM 

16. למה משמש docker in docker ?

למשל לcicd, כשרוצים לפרוס אפליקציה.

17. מה זה busy box ?

תכנה שמאחדת אופרציות לינוקסיות.
כלומר זה executable אחד שמאחד את רוב הפקודות השימושיות בלינוקס וכך שומרים על קונטיינר קל ופונקציונלי.

18. מה זה veth pair ?

צמד תהליכים שנותן לתקשר בין שני network namespaces.
כל אחד מהממשקים האלה יושב ברשת אחרת זה סוג של "כבל אינטרנט" ווירטואלי.

19.  מה זה && ?

משרשר שתי פעולות באותו שורת RUN כך שהשנייה תעבוד אם הראשונה הצליחה.

20. מה זה -t בdocker run ?

ממש מדמה terminal על host ולא רק פקודה כמו רק עם דגל -i.

21. איך לגרום לקונטיינר למחוק את עצמו כשהוא סיים ?

הרצה עם --rm.

22. איך מריצים container כroot ?

מוסיפים --user root

23. env vs args
24. docker start vs docker run ?

run = create + start
כלומר אם כבר עצרנו את הcontainer אז ניתן להריץ אותו מחדש עם start
ואם לא אז חייב run.

25. docker swarm



26. docker ignore

כשיוצרים image, דוקר ממש יוצר context עם כל הקבצים בworking directory.
בשביל לחסוך את השליחה של כל המידע הזה לdaemon, משתמשים ב.dockerignore כדי לציין קבצים או תיקיות שלא יעלו.

27. docker0

זה הbridge הדיפולטי שקונטיינרים משתמשים בו כדי לתקשר עם הhost ובפרט החוצה.

### 🔄 Alternatives
Assignment: Compare two virtualization approaches:

- Virtual Machines (VMs) vs Containers

Deliverable:
- 1–2 sentences comparison  
- Include a real-world use case for each

Goal:
Understand the trade-offs between full virtualization and container-based isolation.

---

### 🎯 User Story & Scenario

Assignment: Describe a real-world usage of Docker.

Deliverable (2 paragraphs):

- Describe a service (e.g., API) that is packaged using Docker  
- Explain how it is built (Dockerfile), stored (registry), and deployed  
- Describe briefly how containers help ensure consistency across environments
