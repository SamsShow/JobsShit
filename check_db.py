import sqlite3

DB_NAME = 'jobs_tracker.db'

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Check if jobs exist
cursor.execute('SELECT COUNT(*) FROM jobs')
total = cursor.fetchone()[0]

print(f"\n📊 Database Stats:")
print(f"Total jobs tracked: {total}")

if total > 0:
    print("\n📝 Recent jobs:")
    cursor.execute('SELECT id, matched_keywords, posted_date FROM jobs ORDER BY posted_date DESC LIMIT 5')
    for job in cursor.fetchall():
        print(f"  • ID: {job[0]}, Keywords: {job[1]}, Date: {job[2]}")
else:
    print("\n❌ No jobs in database yet!")
    print("This means:")
    print("  1. No messages matched your keywords in the last 48 hours")
    print("  2. OR the keywords are too specific")
    print("  3. OR there were no job postings in the channel")

conn.close()

