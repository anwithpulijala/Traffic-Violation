import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")

# Clean URL
if "[" in db_url and "]" in db_url:
    db_url = db_url.replace("[", "").replace("]", "")

try:
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("Connected to DB.")
    
    # 1. Create Bucket
    print("Creating 'traffic-uploads' bucket...")
    cur.execute("""
        INSERT INTO storage.buckets (id, name, public)
        VALUES ('traffic-uploads', 'traffic-uploads', true)
        ON CONFLICT (id) DO NOTHING;
    """)
    print("Bucket created (or already exists).")
    
    # 2. Add Policy for Public Uploads/Selects
    # Note: For simplicity, we allow all operations for anon (if valid key) for this bucket
    print("Creating policies...")
    
    # Policy for INSERT
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_policies 
                WHERE tablename = 'objects' 
                AND policyname = 'Allow Public Insert traffic-uploads'
            ) THEN
                CREATE POLICY "Allow Public Insert traffic-uploads"
                ON storage.objects FOR INSERT 
                WITH CHECK ( bucket_id = 'traffic-uploads' );
            END IF;
        END
        $$;
    """)
    
    # Policy for SELECT
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_policies 
                WHERE tablename = 'objects' 
                AND policyname = 'Allow Public Select traffic-uploads'
            ) THEN
                CREATE POLICY "Allow Public Select traffic-uploads"
                ON storage.objects FOR SELECT
                USING ( bucket_id = 'traffic-uploads' );
            END IF;
        END
        $$;
    """)

    print("Policies applied successfully.")
    
    conn.close()
    print("Setup Complete.")

except Exception as e:
    print(f"Setup Error: {e}")
