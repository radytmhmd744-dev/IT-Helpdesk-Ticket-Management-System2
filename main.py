import sqlite3

# الاتصال بقاعدة البيانات
def connect_database():
    conn = sqlite3.connect('helpdesk.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    print("تم الاتصال بقاعدة البيانات بنجاح!")

    return conn, cursor


conn, cursor = connect_database()

# إنشاء جداول قاعدة البيانات

def create_tables(conn, cursor):

   
    # إنشاء جدول الأقسام
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_name TEXT NOT NULL UNIQUE
        )
    """)


    # إنشاء جدول التذاكر
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            status TEXT,
            priority TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id)
            REFERENCES departments(department_id)
        )
    """)

    conn.commit()

    print("Departments table created successfully!")
    print("Tickets table created successfully!")


# استدعاء دالة إنشاء الجداول
create_tables(conn, cursor)


cursor.execute("""
    DELETE FROM departments
    WHERE department_id NOT IN (
        SELECT MIN(department_id)
        FROM departments
        GROUP BY department_name
    )
""")

# حذف التذكرة المكررة
cursor.execute("""
    DELETE FROM tickets
    WHERE ticket_id NOT IN (
        SELECT MIN(ticket_id)
        FROM tickets
        GROUP BY employee_name,
                 issue_description,
                 status,
                 priority,
                 department_id
    )
""")

conn.commit()

print("Duplicate tickets removed!")

# Prevent future duplicate departments
cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_unique_department_name
    ON departments(department_name)
""")

conn.commit()

print("Duplicate departments removed!")



# إضافة الأقسام

def insert_departments(conn, cursor):
    department_names = ['IT', 'HR', 'Finance']

    for department in department_names:
        cursor.execute("""
            INSERT INTO departments (department_name)
            SELECT ?
            WHERE NOT EXISTS (
                SELECT 1 FROM departments
                WHERE department_name = ?
            )
        """, (department, department))

    conn.commit()

    print("Departments checked successfully!")


# استدعاء دالة إضافة الأقسام
insert_departments(conn, cursor)


# إضافة تذكرة جديدة

def create_ticket(conn, cursor, employee_name, issue_description, status, priority, department_id):

    cursor.execute("""
        INSERT INTO tickets (
            employee_name,
            issue_description,
            status,
            priority,
            department_id
        )
        VALUES (?, ?, ?, ?, ?)
    """, (employee_name, issue_description, status, priority, department_id))

    conn.commit()

    print("New ticket added successfully!")



cursor.execute("""
    UPDATE tickets
    SET priority = 'Medium'
    WHERE priority = 'medium'
""")

conn.commit()

#  Update Ticket
def update_ticket(conn, cursor, new_status, new_priority, ticket_id):

    cursor.execute("""
        UPDATE tickets
        SET status = ?, priority = ?
        WHERE ticket_id = ?
    """, (new_status, new_priority, ticket_id))

    conn.commit()

    print("Ticket updated successfully!")


update_ticket(conn, cursor, 'In Progress', 'High', 4)
 
# اضافة عشرين تذكرة 

test_tickets = [
    ('Omar', 'Email not working', 'Open', 'High', 1),
    ('Nora', 'Keyboard not working', 'In Progress', 'Medium', 1),
    ('Khalid', 'Cannot access website', 'Closed', 'Low', 1),
    ('Maha', 'Printer paper jam', 'Open', 'Medium', 1),
    ('Fahad', 'Computer is slow', 'In Progress', 'High', 1),
    ('Lama', 'Password reset request', 'Closed', 'Low', 1),
    ('Sara A', 'Software installation', 'Open', 'High', 1),
    ('Yousef', 'Network connection issue', 'In Progress', 'Medium', 1),
    ('Huda', 'Monitor not working', 'Closed', 'Low', 1),
    ('Rayan', 'System login error', 'Open', 'High', 1),
    ('Amal', 'HR system access', 'Open', 'Medium', 2),
    ('Salman', 'Attendance system issue', 'In Progress', 'High', 2),
    ('Reem', 'Employee record update', 'Closed', 'Low', 2),
    ('Majed', 'Leave request problem', 'Open', 'Medium', 2),
    ('Dana', 'HR portal not opening', 'In Progress', 'Low', 2),
    ('Faisal', 'Invoice system error', 'Open', 'High', 3),
    ('Nouf', 'Payment report issue', 'In Progress', 'Medium', 3),
    ('Turki', 'Financial report access', 'Closed', 'Low', 3),
    ('Abeer', 'Budget system problem', 'Open', 'High', 3),
    ('Bader', 'Account statement error', 'In Progress', 'Medium', 3)
]

for ticket in test_tickets:

    cursor.execute("""
        SELECT 1 FROM tickets
        WHERE employee_name = ?
        AND issue_description = ?
        AND status = ?
        AND priority = ?
        AND department_id = ?
    """, ticket)


    if cursor.fetchone() is None:
        create_ticket(conn, cursor, *ticket)

conn.commit()

print("20 test tickets checked and added successfully!")


# تحديث حالة التذكرة

cursor.execute("""
    UPDATE tickets
    SET status = ?, priority = ?
    WHERE ticket_id = ?
""", ('In Progress', 'Medium', 5))

conn.commit()

print("Ticket updated successfully!")


# حذف التذكرة

def delete_ticket(conn, cursor, ticket_id):

    cursor.execute("""
        DELETE FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    conn.commit()

    print("Test ticket deleted successfully!")



# استدعاء دالة حذف التذكرة
delete_ticket(conn, cursor, 5)


# البحث عن تذكرة

def search_ticket(cursor, ticket_id):

    cursor.execute("""
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()

    print("Search Result:")
    print(ticket)


# استدعاء دالة البحث عن التذكرة
search_ticket(cursor, 4)


# عرض الاقساام 
cursor.execute("SELECT * FROM departments")

print("Departments:")
print(cursor.fetchall())


# عرض جميع التذاكر

def read_tickets(cursor):

    cursor.execute("""
        SELECT
            tickets.ticket_id,
            tickets.employee_name,
            tickets.issue_description,
            tickets.status,
            tickets.priority,
            departments.department_name
        FROM tickets
        JOIN departments
        ON tickets.department_id = departments.department_id
    """)

    tickets = cursor.fetchall()

    print("All Tickets:")

    for ticket in tickets:
        print(ticket)

 
# استدعاء دالة عرض التذاكر
read_tickets(cursor)


#اجمالي التذاكر 

cursor.execute("""
    SELECT COUNT(*)
    FROM tickets
""")

total_tickets = cursor.fetchone()

print("Total Tickets:", total_tickets[0])


# حساب عدد التذاكر حسب الحالةاكر حسب الحالة 

cursor.execute("""
    SELECT status, COUNT(*)
    FROM tickets
    GROUP BY status
""")

status_counts = cursor.fetchall()

print("Tickets By Status:")

for row in status_counts:
    print(row)


# حساب التذاكر حسب الاولوية

cursor.execute("""
    SELECT priority, COUNT(*)
    FROM tickets
    GROUP BY priority
""") 

priority_counts = cursor.fetchall()

print("Tickets By Priority:")

for row in priority_counts:
    print(row)


# حساب التذاكر حسب الاقسام

cursor.execute("""
    SELECT departments.department_name, COUNT(*)
    FROM tickets
    JOIN departments
    ON tickets.department_id = departments.department_id
    GROUP BY departments.department_name
""")

department_counts = cursor.fetchall()

print("Tickets By Department:")

for row in department_counts:
    print(row)



# عرض التذاكر ذات الاولوية العالية

cursor.execute("""
    SELECT *
    FROM tickets
    WHERE priority = 'High'
""")

high_priority_tickets = cursor.fetchall()

print("High Priority Tickets:")

for ticket in high_priority_tickets:
    print(ticket)

    # Display Tickets Ordered By Priority

cursor.execute("""
    SELECT *
    FROM tickets
    ORDER BY priority ASC
""")

ordered_tickets = cursor.fetchall()

print("Tickets Ordered By Priority:")

for ticket in ordered_tickets:
    print(ticket)

# اختبار البيانات الغير صحيحة

try:
    cursor.execute("""
        INSERT INTO tickets (
            employee_name,
            issue_description,
            status,
            priority,
            department_id
        )
        VALUES (?, ?, ?, ?, ?)
    """, (None, 'Test issue', 'Open', 'High', 1))

    conn.commit()

except sqlite3.IntegrityError as e:
    print("Invalid data rejected:", e)
conn.close()

print("Database connection closed successfully!") 