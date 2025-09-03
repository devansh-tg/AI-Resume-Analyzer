"""
Gamification System for AI Resume Analyzer
Implements badges, milestones, and progress tracking
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import sqlite3
import os

@dataclass
class Achievement:
    """Achievement/Badge data structure"""
    id: str
    name: str
    description: str
    icon: str
    category: str
    points: int
    requirements: Dict
    unlocked: bool = False
    unlocked_date: Optional[str] = None

@dataclass
class UserProgress:
    """User progress data structure"""
    user_id: str
    level: int
    experience_points: int
    total_resumes_analyzed: int
    total_interviews_completed: int
    skills_added: int
    connections_made: int
    days_active: int
    achievements_earned: List[str]
    current_streak: int
    longest_streak: int
    last_activity: str

class GamificationEngine:
    """Core gamification engine"""
    
    def __init__(self, db_path: str = "/tmp/gamification.db"):
        self.db_path = db_path
        self._init_database()
        self._init_achievements()
        
        # Level thresholds (experience points needed for each level)
        self.level_thresholds = [
            0, 100, 250, 500, 1000, 1750, 2750, 4000, 5500, 7500, 10000,
            13000, 16500, 20500, 25000, 30000, 35500, 41500, 48000, 55000, 62500
        ]
        
        # Activity point values
        self.activity_points = {
            "resume_analyzed": 25,
            "interview_completed": 50,
            "skill_added": 10,
            "daily_login": 5,
            "streak_bonus": 10,
            "achievement_earned": 100,
            "feedback_given": 15,
            "profile_updated": 20
        }
    
    def _init_database(self):
        """Initialize SQLite database for gamification data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # User progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    user_id TEXT PRIMARY KEY,
                    level INTEGER DEFAULT 1,
                    experience_points INTEGER DEFAULT 0,
                    total_resumes_analyzed INTEGER DEFAULT 0,
                    total_interviews_completed INTEGER DEFAULT 0,
                    skills_added INTEGER DEFAULT 0,
                    connections_made INTEGER DEFAULT 0,
                    days_active INTEGER DEFAULT 0,
                    achievements_earned TEXT DEFAULT "[]",
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_activity TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Activity log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    activity_type TEXT,
                    points_earned INTEGER,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Achievement unlocks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS achievement_unlocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    achievement_id TEXT,
                    unlocked_date TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def _init_achievements(self):
        """Initialize achievement definitions"""
        self.achievements = {
            # Resume Analysis Achievements
            "first_analysis": Achievement(
                id="first_analysis",
                name="Resume Rookie",
                description="Analyze your first resume",
                icon="🎯",
                category="analysis",
                points=50,
                requirements={"resumes_analyzed": 1}
            ),
            "analysis_streak": Achievement(
                id="analysis_streak",
                name="Analysis Expert",
                description="Analyze 10 resumes",
                icon="📊",
                category="analysis",
                points=200,
                requirements={"resumes_analyzed": 10}
            ),
            "power_user": Achievement(
                id="power_user",
                name="Power User",
                description="Analyze 50 resumes",
                icon="⚡",
                category="analysis",
                points=500,
                requirements={"resumes_analyzed": 50}
            ),
            
            # Interview Achievements
            "interview_starter": Achievement(
                id="interview_starter",
                name="Interview Ready",
                description="Complete your first mock interview",
                icon="🎤",
                category="interview",
                points=100,
                requirements={"interviews_completed": 1}
            ),
            "interview_master": Achievement(
                id="interview_master",
                name="Interview Master",
                description="Complete 10 mock interviews",
                icon="👑",
                category="interview",
                points=300,
                requirements={"interviews_completed": 10}
            ),
            "confident_speaker": Achievement(
                id="confident_speaker",
                name="Confident Speaker",
                description="Score 90% or higher in interview confidence",
                icon="🗣️",
                category="interview",
                points=250,
                requirements={"interview_confidence_score": 0.9}
            ),
            
            # Skill Development Achievements
            "skill_builder": Achievement(
                id="skill_builder",
                name="Skill Builder",
                description="Add 20 skills to your profile",
                icon="🛠️",
                category="skills",
                points=150,
                requirements={"skills_added": 20}
            ),
            "polyglot": Achievement(
                id="polyglot",
                name="Tech Polyglot",
                description="Have skills in 5 different categories",
                icon="🌍",
                category="skills",
                points=200,
                requirements={"skill_categories": 5}
            ),
            
            # Engagement Achievements
            "daily_user": Achievement(
                id="daily_user",
                name="Daily User",
                description="Use the platform for 7 consecutive days",
                icon="📅",
                category="engagement",
                points=100,
                requirements={"current_streak": 7}
            ),
            "dedicated_user": Achievement(
                id="dedicated_user",
                name="Dedicated User",
                description="Use the platform for 30 consecutive days",
                icon="🔥",
                category="engagement",
                points=400,
                requirements={"current_streak": 30}
            ),
            "active_member": Achievement(
                id="active_member",
                name="Active Member",
                description="Be active for 100 days total",
                icon="⭐",
                category="engagement",
                points=300,
                requirements={"days_active": 100}
            ),
            
            # Special Achievements
            "perfectionist": Achievement(
                id="perfectionist",
                name="Perfectionist",
                description="Get a perfect resume score (100%)",
                icon="💎",
                category="special",
                points=500,
                requirements={"perfect_resume_score": True}
            ),
            "mentor": Achievement(
                id="mentor",
                name="Mentor",
                description="Help 5 other users improve their resumes",
                icon="🤝",
                category="social",
                points=250,
                requirements={"users_helped": 5}
            ),
            "trendsetter": Achievement(
                id="trendsetter",
                name="Trendsetter",
                description="Be among the first 100 users",
                icon="🚀",
                category="special",
                points=200,
                requirements={"early_adopter": True}
            )
        }
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get user progress data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM user_progress WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if not row:
                # Create new user
                return self._create_new_user(user_id)
            
            # Convert row to UserProgress object
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, row))
            
            return UserProgress(
                user_id=data['user_id'],
                level=data['level'],
                experience_points=data['experience_points'],
                total_resumes_analyzed=data['total_resumes_analyzed'],
                total_interviews_completed=data['total_interviews_completed'],
                skills_added=data['skills_added'],
                connections_made=data['connections_made'],
                days_active=data['days_active'],
                achievements_earned=json.loads(data['achievements_earned']),
                current_streak=data['current_streak'],
                longest_streak=data['longest_streak'],
                last_activity=data['last_activity']
            )
    
    def _create_new_user(self, user_id: str) -> UserProgress:
        """Create new user progress record"""
        progress = UserProgress(
            user_id=user_id,
            level=1,
            experience_points=0,
            total_resumes_analyzed=0,
            total_interviews_completed=0,
            skills_added=0,
            connections_made=0,
            days_active=1,
            achievements_earned=[],
            current_streak=1,
            longest_streak=1,
            last_activity=datetime.now().isoformat()
        )
        
        self._save_user_progress(progress)
        return progress
    
    def _save_user_progress(self, progress: UserProgress):
        """Save user progress to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_progress 
                (user_id, level, experience_points, total_resumes_analyzed, 
                 total_interviews_completed, skills_added, connections_made, 
                 days_active, achievements_earned, current_streak, longest_streak, 
                 last_activity, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                progress.user_id, progress.level, progress.experience_points,
                progress.total_resumes_analyzed, progress.total_interviews_completed,
                progress.skills_added, progress.connections_made, progress.days_active,
                json.dumps(progress.achievements_earned), progress.current_streak,
                progress.longest_streak, progress.last_activity, datetime.now().isoformat()
            ))
            conn.commit()
    
    def record_activity(self, user_id: str, activity_type: str, details: Dict = None) -> Dict:
        """Record user activity and update progress"""
        if details is None:
            details = {}
        
        # Get current progress
        progress = self.get_user_progress(user_id)
        
        # Calculate points for this activity
        points_earned = self.activity_points.get(activity_type, 0)
        
        # Update streak
        self._update_streak(progress)
        
        # Update activity-specific counters
        if activity_type == "resume_analyzed":
            progress.total_resumes_analyzed += 1
        elif activity_type == "interview_completed":
            progress.total_interviews_completed += 1
        elif activity_type == "skill_added":
            progress.skills_added += details.get('count', 1)
        
        # Add experience points
        progress.experience_points += points_earned
        
        # Check for level up
        new_level = self._calculate_level(progress.experience_points)
        level_up = new_level > progress.level
        if level_up:
            progress.level = new_level
            points_earned += 50  # Level up bonus
        
        # Update last activity
        progress.last_activity = datetime.now().isoformat()
        
        # Check for new achievements
        new_achievements = self._check_achievements(progress, details)
        
        # Add achievement points
        for achievement_id in new_achievements:
            achievement = self.achievements[achievement_id]
            points_earned += achievement.points
            progress.achievements_earned.append(achievement_id)
        
        # Save progress
        self._save_user_progress(progress)
        
        # Log activity
        self._log_activity(user_id, activity_type, points_earned, details)
        
        return {
            "points_earned": points_earned,
            "level_up": level_up,
            "new_level": progress.level if level_up else None,
            "new_achievements": new_achievements,
            "total_experience": progress.experience_points,
            "current_level": progress.level
        }
    
    def _update_streak(self, progress: UserProgress):
        """Update user's activity streak"""
        if not progress.last_activity:
            progress.current_streak = 1
            progress.longest_streak = 1
            return
        
        last_activity = datetime.fromisoformat(progress.last_activity.replace('Z', '+00:00'))
        now = datetime.now()
        days_since_last = (now - last_activity).days
        
        if days_since_last == 1:
            # Consecutive day
            progress.current_streak += 1
            progress.longest_streak = max(progress.longest_streak, progress.current_streak)
        elif days_since_last > 1:
            # Streak broken
            progress.current_streak = 1
        # If days_since_last == 0, it's the same day, don't change streak
    
    def _calculate_level(self, experience_points: int) -> int:
        """Calculate level based on experience points"""
        for level, threshold in enumerate(self.level_thresholds[1:], 1):
            if experience_points < threshold:
                return level
        return len(self.level_thresholds)  # Max level
    
    def _check_achievements(self, progress: UserProgress, activity_details: Dict) -> List[str]:
        """Check for newly earned achievements"""
        new_achievements = []
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in progress.achievements_earned:
                continue  # Already earned
            
            if self._check_achievement_requirements(achievement, progress, activity_details):
                new_achievements.append(achievement_id)
                self._unlock_achievement(progress.user_id, achievement_id)
        
        return new_achievements
    
    def _check_achievement_requirements(self, achievement: Achievement, 
                                      progress: UserProgress, details: Dict) -> bool:
        """Check if achievement requirements are met"""
        requirements = achievement.requirements
        
        for req_type, req_value in requirements.items():
            if req_type == "resumes_analyzed":
                if progress.total_resumes_analyzed < req_value:
                    return False
            elif req_type == "interviews_completed":
                if progress.total_interviews_completed < req_value:
                    return False
            elif req_type == "skills_added":
                if progress.skills_added < req_value:
                    return False
            elif req_type == "current_streak":
                if progress.current_streak < req_value:
                    return False
            elif req_type == "days_active":
                if progress.days_active < req_value:
                    return False
            elif req_type == "interview_confidence_score":
                if details.get('confidence_score', 0) < req_value:
                    return False
            elif req_type == "perfect_resume_score":
                if not details.get('perfect_score', False):
                    return False
            elif req_type == "skill_categories":
                if details.get('skill_categories_count', 0) < req_value:
                    return False
            elif req_type == "users_helped":
                if details.get('users_helped', 0) < req_value:
                    return False
            elif req_type == "early_adopter":
                # Check if user is among first 100 users (simplified)
                if int(progress.user_id.split('_')[-1] if '_' in progress.user_id else '999') > 100:
                    return False
        
        return True
    
    def _unlock_achievement(self, user_id: str, achievement_id: str):
        """Record achievement unlock"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO achievement_unlocks (user_id, achievement_id)
                VALUES (?, ?)
            ''', (user_id, achievement_id))
            conn.commit()
    
    def _log_activity(self, user_id: str, activity_type: str, points_earned: int, details: Dict):
        """Log activity to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_log (user_id, activity_type, points_earned, details)
                VALUES (?, ?, ?, ?)
            ''', (user_id, activity_type, points_earned, json.dumps(details)))
            conn.commit()
    
    def get_user_achievements(self, user_id: str) -> List[Achievement]:
        """Get user's earned achievements with details"""
        progress = self.get_user_progress(user_id)
        achievements = []
        
        for achievement_id in progress.achievements_earned:
            if achievement_id in self.achievements:
                achievement = self.achievements[achievement_id]
                achievement.unlocked = True
                
                # Get unlock date
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT unlocked_date FROM achievement_unlocks 
                        WHERE user_id = ? AND achievement_id = ?
                    ''', (user_id, achievement_id))
                    
                    row = cursor.fetchone()
                    if row:
                        achievement.unlocked_date = row[0]
                
                achievements.append(achievement)
        
        return achievements
    
    def get_leaderboard(self, category: str = "experience", limit: int = 10) -> List[Dict]:
        """Get leaderboard data"""
        order_by = {
            "experience": "experience_points DESC",
            "level": "level DESC, experience_points DESC",
            "resumes": "total_resumes_analyzed DESC",
            "interviews": "total_interviews_completed DESC",
            "streak": "current_streak DESC, longest_streak DESC"
        }.get(category, "experience_points DESC")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT user_id, level, experience_points, total_resumes_analyzed,
                       total_interviews_completed, current_streak, longest_streak
                FROM user_progress 
                ORDER BY {order_by}
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "user_id": row[0],
                    "level": row[1],
                    "experience_points": row[2],
                    "total_resumes_analyzed": row[3],
                    "total_interviews_completed": row[4],
                    "current_streak": row[5],
                    "longest_streak": row[6]
                })
            
            return results
    
    def get_achievement_progress(self, user_id: str) -> Dict:
        """Get progress towards unearned achievements"""
        progress = self.get_user_progress(user_id)
        achievement_progress = {}
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in progress.achievements_earned:
                continue
            
            # Calculate progress percentage for each requirement
            req_progress = {}
            for req_type, req_value in achievement.requirements.items():
                current_value = 0
                
                if req_type == "resumes_analyzed":
                    current_value = progress.total_resumes_analyzed
                elif req_type == "interviews_completed":
                    current_value = progress.total_interviews_completed
                elif req_type == "skills_added":
                    current_value = progress.skills_added
                elif req_type == "current_streak":
                    current_value = progress.current_streak
                elif req_type == "days_active":
                    current_value = progress.days_active
                
                if isinstance(req_value, (int, float)) and req_value > 0:
                    req_progress[req_type] = min(current_value / req_value, 1.0)
                else:
                    req_progress[req_type] = 0.0
            
            # Overall progress is the minimum of all requirements
            overall_progress = min(req_progress.values()) if req_progress else 0.0
            
            achievement_progress[achievement_id] = {
                "achievement": asdict(achievement),
                "overall_progress": overall_progress,
                "requirement_progress": req_progress
            }
        
        return achievement_progress

class BadgeSystem:
    """Visual badge system for achievements"""
    
    def __init__(self):
        self.badge_colors = {
            "analysis": "#2E86AB",
            "interview": "#F18F01", 
            "skills": "#2a9d8f",
            "engagement": "#C73E1D",
            "social": "#592E83",
            "special": "#FFD700"
        }
    
    def generate_badge_svg(self, achievement: Achievement, size: int = 64) -> str:
        """Generate SVG badge for achievement"""
        color = self.badge_colors.get(achievement.category, "#666666")
        
        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <circle cx="32" cy="32" r="30" fill="{color}" stroke="#ffffff" stroke-width="2"/>
            <text x="32" y="40" text-anchor="middle" font-size="24" fill="white">{achievement.icon}</text>
            {f'<circle cx="50" cy="14" r="8" fill="gold" stroke="white" stroke-width="1"/>' if achievement.unlocked else ''}
        </svg>
        '''
        return svg.strip()
    
    def create_achievement_card(self, achievement: Achievement, progress: float = 0.0) -> str:
        """Create HTML card for achievement display"""
        status_class = "unlocked" if achievement.unlocked else "locked"
        progress_bar = f'<div class="progress-bar" style="width: {progress*100}%"></div>' if not achievement.unlocked else ''
        
        return f'''
        <div class="achievement-card {status_class}">
            <div class="achievement-icon">{achievement.icon}</div>
            <div class="achievement-info">
                <h3>{achievement.name}</h3>
                <p>{achievement.description}</p>
                <div class="achievement-points">{achievement.points} points</div>
                {progress_bar}
                {f'<div class="unlock-date">Unlocked: {achievement.unlocked_date}</div>' if achievement.unlocked else ''}
            </div>
        </div>
        '''

# CSS styles for gamification UI
GAMIFICATION_CSS = '''
<style>
.achievement-card {
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
}

.achievement-card.unlocked {
    border-color: #2E86AB;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.achievement-card.locked {
    opacity: 0.6;
    background: #f9f9f9;
}

.achievement-icon {
    font-size: 48px;
    margin-right: 20px;
    min-width: 60px;
    text-align: center;
}

.achievement-info h3 {
    margin: 0 0 5px 0;
    color: #333;
}

.achievement-info p {
    margin: 0 0 10px 0;
    color: #666;
    font-size: 14px;
}

.achievement-points {
    background: #2E86AB;
    color: white;
    padding: 3px 8px;
    border-radius: 15px;
    font-size: 12px;
    display: inline-block;
}

.progress-bar {
    height: 6px;
    background: #2E86AB;
    border-radius: 3px;
    margin-top: 10px;
    transition: width 0.3s ease;
}

.unlock-date {
    font-size: 12px;
    color: #888;
    margin-top: 5px;
}

.level-badge {
    background: linear-gradient(45deg, #FFD700, #FFA500);
    color: white;
    padding: 10px 20px;
    border-radius: 25px;
    font-weight: bold;
    text-align: center;
    margin: 10px 0;
}

.xp-bar {
    background: #e0e0e0;
    height: 20px;
    border-radius: 10px;
    overflow: hidden;
    margin: 10px 0;
}

.xp-fill {
    background: linear-gradient(90deg, #2E86AB, #4CAF50);
    height: 100%;
    transition: width 0.5s ease;
}

.streak-counter {
    background: #FF4500;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    display: inline-block;
    margin: 5px;
}
</style>
'''