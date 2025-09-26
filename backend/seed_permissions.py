import sqlite3

def seed_permissions():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Clear old permissions
    c.execute("DELETE FROM documents")

    # Manager → all 5 PDFs
    pdfs = ["Meta.pdf", "2024_Annual_Report.pdf", "Netflix-10-K-01272025.pdf", "NVIDIA-2025-Annual-Report.pdf", "RIL-Integrated-Annual-Report-2024-25.pdf"]
    for pdf in pdfs:
        c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("manager", pdf))

    # Analyst_1 → only file1
    c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("analyst_1", "Meta.pdf"))

    # Analyst_2 → file2 + file3
    c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("analyst_2", "2024_Annual_Report.pdf"))
    c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("analyst_2", "Netflix-10-K-01272025.pdf"))

    # Analyst_3 → file1, file4, file5
    c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("analyst_3", "Meta.pdf"))
    c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("analyst_3", "NVIDIA-2025-Annual-Reporte4.pdf"))
    c.execute("INSERT INTO documents (role, document_name) VALUES (?, ?)", ("analyst_3", "RIL-Integrated-Annual-Report-2024-25.pdf"))

    conn.commit()
    conn.close()
    print("✅ Permissions seeded successfully")

if __name__ == "__main__":
    seed_permissions()
