import sqlite3
from datetime import datetime

DB_NAME = 'jobs_tracker.db'

def view_all_jobs():
    """View all tracked jobs"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM jobs ORDER BY posted_date DESC')
    jobs = cursor.fetchall()
    
    if not jobs:
        print("No jobs tracked yet.")
        return
    
    print(f"\n📊 Total Jobs Tracked: {len(jobs)}\n")
    print("=" * 80)
    
    for job in jobs:
        job_id, msg_id, channel_id, content, keywords, posted_date, notified = job
        print(f"\n🆔 Job ID: {job_id}")
        print(f"📅 Posted: {posted_date}")
        print(f"🔑 Matched Keywords: {keywords}")
        print(f"📝 Content Preview: {content[:200]}{'...' if len(content) > 200 else ''}")
        print(f"✉️  Notified: {'Yes' if notified else 'No'}")
        print("-" * 80)
    
    conn.close()

def search_jobs(keyword):
    """Search jobs by keyword"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM jobs 
        WHERE content LIKE ? OR matched_keywords LIKE ?
        ORDER BY posted_date DESC
    ''', (f'%{keyword}%', f'%{keyword}%'))
    
    jobs = cursor.fetchall()
    
    if not jobs:
        print(f"No jobs found matching '{keyword}'")
        return
    
    print(f"\n🔍 Found {len(jobs)} jobs matching '{keyword}':\n")
    print("=" * 80)
    
    for job in jobs:
        job_id, msg_id, channel_id, content, keywords, posted_date, notified = job
        print(f"\n🆔 Job ID: {job_id}")
        print(f"📅 Posted: {posted_date}")
        print(f"🔑 Matched Keywords: {keywords}")
        print(f"📝 Content Preview: {content[:200]}{'...' if len(content) > 200 else ''}")
        print("-" * 80)
    
    conn.close()

def get_stats():
    """Get statistics about tracked jobs"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Total jobs
    cursor.execute('SELECT COUNT(*) FROM jobs')
    total = cursor.fetchone()[0]
    
    # Jobs by keyword
    cursor.execute('SELECT matched_keywords, COUNT(*) FROM jobs GROUP BY matched_keywords')
    by_keyword = cursor.fetchall()
    
    # Recent jobs (last 7 days)
    cursor.execute('''
        SELECT COUNT(*) FROM jobs 
        WHERE posted_date >= datetime('now', '-7 days')
    ''')
    recent = cursor.fetchone()[0]
    
    print("\n📈 Job Tracker Statistics")
    print("=" * 50)
    print(f"Total Jobs Tracked: {total}")
    print(f"Jobs in Last 7 Days: {recent}")
    print("\nJobs by Keyword:")
    for keywords, count in by_keyword:
        print(f"  • {keywords}: {count}")
    print("=" * 50)
    
    conn.close()

def main():
    print("\n🔍 Job Tracker Database Viewer")
    print("=" * 50)
    print("1. View all jobs")
    print("2. Search jobs by keyword")
    print("3. View statistics")
    print("4. Exit")
    print("=" * 50)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        view_all_jobs()
    elif choice == '2':
        keyword = input("Enter keyword to search: ").strip()
        search_jobs(keyword)
    elif choice == '3':
        get_stats()
    elif choice == '4':
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == '__main__':
    main()

