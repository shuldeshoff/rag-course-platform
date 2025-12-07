#!/usr/bin/env python3
"""
CLI tool for indexing documents
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.indexer import indexer_service

async def index_file(file_path: str, course_id: int, title: str):
    """Index a single file"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📄 Indexing: {file_path}")
    print(f"   Course ID: {course_id}")
    print(f"   Title: {title}")
    
    try:
        result = await indexer_service.index_document(
            file_path=file_path,
            course_id=course_id,
            metadata={"title": title}
        )
        
        print(f"✅ Success!")
        print(f"   Chunks created: {result['chunks_created']}")
        print(f"   Characters: {result['total_characters']}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

async def index_directory(dir_path: str, course_id: int):
    """Index all documents in a directory"""
    if not os.path.isdir(dir_path):
        print(f"❌ Directory not found: {dir_path}")
        return
    
    files = [f for f in os.listdir(dir_path) 
             if f.endswith(('.pdf', '.docx', '.txt'))]
    
    if not files:
        print(f"❌ No documents found in {dir_path}")
        return
    
    print(f"📁 Found {len(files)} documents")
    
    for filename in files:
        file_path = os.path.join(dir_path, filename)
        title = os.path.splitext(filename)[0]
        await index_file(file_path, course_id, title)
        print()

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Index file:      python cli_indexer.py file <path> <course_id> <title>")
        print("  Index directory: python cli_indexer.py dir <path> <course_id>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "file":
        if len(sys.argv) < 5:
            print("Usage: python cli_indexer.py file <path> <course_id> <title>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        course_id = int(sys.argv[3])
        title = sys.argv[4]
        
        asyncio.run(index_file(file_path, course_id, title))
    
    elif command == "dir":
        if len(sys.argv) < 4:
            print("Usage: python cli_indexer.py dir <path> <course_id>")
            sys.exit(1)
        
        dir_path = sys.argv[2]
        course_id = int(sys.argv[3])
        
        asyncio.run(index_directory(dir_path, course_id))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

