"""
Database operations for LinkedIn Post Generator
Uses SQLite for simplicity
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
import json


class Database:
    """Handle all database operations"""
    
    def __init__(self, db_path="data/posts.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._create_tables()
    
    def _get_connection(self):
        """Create and return database connection"""
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        """Create necessary database tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Posts table - stores all generated posts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                tone TEXT NOT NULL,
                length TEXT NOT NULL,
                post_type TEXT DEFAULT 'general',
                content TEXT NOT NULL,
                hashtags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_favorite INTEGER DEFAULT 0
            )
        """)
        
        # Drafts table - stores saved drafts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                hashtags TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Settings table - stores user preferences
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ==================== POSTS OPERATIONS ====================
    
    def save_post(self, topic: str, tone: str, length: str, content: str, 
                  hashtags: str = "", post_type: str = "general") -> int:
        """
        Save a generated post to history
        
        Args:
            topic: Post topic
            tone: Post tone
            length: Post length
            content: Post content
            hashtags: Hashtags string
            post_type: Type of post
            
        Returns:
            Post ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO posts (topic, tone, length, post_type, content, hashtags)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (topic, tone, length, post_type, content, hashtags))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def get_all_posts(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Get all posts from history
        
        Args:
            limit: Maximum number of posts to return
            offset: Number of posts to skip
            
        Returns:
            List of post dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, tone, length, post_type, content, hashtags, 
                   created_at, is_favorite
            FROM posts
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                "id": row[0],
                "topic": row[1],
                "tone": row[2],
                "length": row[3],
                "post_type": row[4],
                "content": row[5],
                "hashtags": row[6],
                "created_at": row[7],
                "is_favorite": bool(row[8])
            })
        
        conn.close()
        return posts
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Get a specific post by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, tone, length, post_type, content, hashtags, 
                   created_at, is_favorite
            FROM posts
            WHERE id = ?
        """, (post_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "topic": row[1],
                "tone": row[2],
                "length": row[3],
                "post_type": row[4],
                "content": row[5],
                "hashtags": row[6],
                "created_at": row[7],
                "is_favorite": bool(row[8])
            }
        return None
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a post from history"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def toggle_favorite(self, post_id: int) -> bool:
        """Toggle favorite status of a post"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE posts 
            SET is_favorite = CASE WHEN is_favorite = 1 THEN 0 ELSE 1 END
            WHERE id = ?
        """, (post_id,))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_favorites(self) -> List[Dict]:
        """Get all favorite posts"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, tone, length, post_type, content, hashtags, 
                   created_at, is_favorite
            FROM posts
            WHERE is_favorite = 1
            ORDER BY created_at DESC
        """)
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                "id": row[0],
                "topic": row[1],
                "tone": row[2],
                "length": row[3],
                "post_type": row[4],
                "content": row[5],
                "hashtags": row[6],
                "created_at": row[7],
                "is_favorite": bool(row[8])
            })
        
        conn.close()
        return posts
    
    # ==================== DRAFTS OPERATIONS ====================
    
    def save_draft(self, title: str, content: str, hashtags: str = "", notes: str = "") -> int:
        """
        Save a draft
        
        Args:
            title: Draft title
            content: Draft content
            hashtags: Hashtags
            notes: Additional notes
            
        Returns:
            Draft ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO drafts (title, content, hashtags, notes)
            VALUES (?, ?, ?, ?)
        """, (title, content, hashtags, notes))
        
        draft_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return draft_id
    
    def get_all_drafts(self) -> List[Dict]:
        """Get all drafts"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content, hashtags, notes, created_at, updated_at
            FROM drafts
            ORDER BY updated_at DESC
        """)
        
        drafts = []
        for row in cursor.fetchall():
            drafts.append({
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "hashtags": row[3],
                "notes": row[4],
                "created_at": row[5],
                "updated_at": row[6]
            })
        
        conn.close()
        return drafts
    
    def get_draft_by_id(self, draft_id: int) -> Optional[Dict]:
        """Get a specific draft by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content, hashtags, notes, created_at, updated_at
            FROM drafts
            WHERE id = ?
        """, (draft_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "hashtags": row[3],
                "notes": row[4],
                "created_at": row[5],
                "updated_at": row[6]
            }
        return None
    
    def update_draft(self, draft_id: int, title: str = None, content: str = None, 
                    hashtags: str = None, notes: str = None) -> bool:
        """Update an existing draft"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        if hashtags is not None:
            updates.append("hashtags = ?")
            params.append(hashtags)
        if notes is not None:
            updates.append("notes = ?")
            params.append(notes)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(draft_id)
        
        query = f"UPDATE drafts SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def delete_draft(self, draft_id: int) -> bool:
        """Delete a draft"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    # ==================== ANALYTICS ====================
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Total posts
        cursor.execute("SELECT COUNT(*) FROM posts")
        total_posts = cursor.fetchone()[0]
        
        # Total drafts
        cursor.execute("SELECT COUNT(*) FROM drafts")
        total_drafts = cursor.fetchone()[0]
        
        # Most used tone
        cursor.execute("""
            SELECT tone, COUNT(*) as count 
            FROM posts 
            GROUP BY tone 
            ORDER BY count DESC 
            LIMIT 1
        """)
        most_used_tone_row = cursor.fetchone()
        most_used_tone = most_used_tone_row[0] if most_used_tone_row else "N/A"
        
        # Most used length
        cursor.execute("""
            SELECT length, COUNT(*) as count 
            FROM posts 
            GROUP BY length 
            ORDER BY count DESC 
            LIMIT 1
        """)
        most_used_length_row = cursor.fetchone()
        most_used_length = most_used_length_row[0] if most_used_length_row else "N/A"
        
        # Posts by tone
        cursor.execute("""
            SELECT tone, COUNT(*) as count 
            FROM posts 
            GROUP BY tone 
            ORDER BY count DESC
        """)
        posts_by_tone = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Recent activity (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM posts 
            WHERE created_at >= date('now', '-7 days')
        """)
        recent_posts = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_posts": total_posts,
            "total_drafts": total_drafts,
            "most_used_tone": most_used_tone,
            "most_used_length": most_used_length,
            "posts_by_tone": posts_by_tone,
            "recent_posts": recent_posts
        }
    
    # ==================== SETTINGS ====================
    
    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        """Get a setting value"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else default
    
    def set_setting(self, key: str, value: str):
        """Set a setting value"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        """, (key, value))
        
        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Test database operations
    db = Database()
    print("✓ Database initialized successfully")
    
    # Test saving a post
    post_id = db.save_post(
        topic="AI in 2024",
        tone="professional",
        length="medium",
        content="Test post content",
        hashtags="#AI #Tech"
    )
    print(f"✓ Test post saved with ID: {post_id}")
    
    # Test getting stats
    stats = db.get_statistics()
    print(f"✓ Statistics: {stats}")
