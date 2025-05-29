# Computer-Security-Project


הפרויקט הוא מערכת לניהול משתמשים ולקוחות, הכוללת ממשקי Frontend ו-Backend. המערכת תומכת ברישום משתמשים, התחברות, איפוס סיסמה וצפייה או הוספה של לקוחות.


### טכנולוגיות

* **Frontend**: React, JavaScript, CSS
* **Backend**: FastAPI, Python, SQLAlchemy
* **Database**: MySQL
* **Containerization**: Docker & Docker Compose
* **סיסמה למסד הנתונים:** password

### מבנה הפרויקט

בתיקיית הפרויקט קיימות שתי גרסאות – **Secured** ו-**Not-Secured**, המבדילות לפי רמת אבטחה.
כל גרסה כוללת:

* **Backend**: קבצי שרת, ניהול נתיבים, מודלים, לוגיקה עסקית, תצורות סיסמה ומסד נתונים.
* **Frontend**: עמודי משתמש (Login, Register, Forgot Password), רכיבי UI, קבצי עיצוב, והגדרות כלליות.
* **Docker**: קבצי Docker ו-Docker Compose.

### הרצה

* יש לוודא ש-Docker מותקן ופועל.
* בתוך תיקיית `backend`, יש להריץ:

  ```bash
  docker-compose up --build  
  ```
* לאחר מכן:

  * ה-Backend יהיה זמין בכתובת [http://localhost:5000/docs](http://localhost:5000/docs)
  * ה-Frontend יהיה זמין בכתובת [http://localhost:3000](http://localhost:3000)


### API עיקריים

* **POST /register** – רישום משתמש
* **POST /login** – התחברות
* **POST /forgot-password** – איפוס סיסמה
* **GET /system** – קבלת נתוני מערכת (דורש התחברות)


שמות המגישים: מרדכי ישראל אהרונסון, ינון קרני, ספיר טויג, ג׳ון עשור, אושר קיקירוב
