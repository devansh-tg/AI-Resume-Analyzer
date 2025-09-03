"""
Enhanced Visualization Components for AI Resume Analyzer
Provides advanced charts and interactive dashboards
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import streamlit as st

class AdvancedVisualizations:
    """Advanced visualization components for resume analytics"""
    
    def __init__(self):
        self.color_schemes = {
            "primary": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"],
            "professional": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#592E83"],
            "modern": ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"]
        }
    
    def create_skill_radar_chart(self, skills_data: Dict[str, List[str]], 
                               skill_levels: Dict[str, float] = None) -> go.Figure:
        """Create an interactive radar chart for skills analysis"""
        categories = list(skills_data.keys())
        skill_counts = [len(skills) for skills in skills_data.values()]
        
        # Normalize skill counts to 0-10 scale
        max_count = max(skill_counts) if skill_counts else 1
        normalized_counts = [count / max_count * 10 for count in skill_counts]
        
        # If skill levels provided, use those instead
        if skill_levels:
            values = [skill_levels.get(cat, 0) * 10 for cat in categories]
        else:
            values = normalized_counts
        
        # Close the radar chart
        categories_closed = categories + [categories[0]]
        values_closed = values + [values[0]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill='toself',
            name='Your Skills',
            line_color='#2E86AB',
            fillcolor='rgba(46, 134, 171, 0.3)'
        ))
        
        # Add benchmark line (example: industry average)
        benchmark_values = [7] * len(categories) + [7]  # Example benchmark
        fig.add_trace(go.Scatterpolar(
            r=benchmark_values,
            theta=categories_closed,
            fill=None,
            name='Industry Average',
            line_color='#A23B72',
            line_dash='dash'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickmode='linear',
                    tick0=0,
                    dtick=2
                )
            ),
            showlegend=True,
            title="Skills Analysis Radar Chart",
            title_x=0.5,
            font=dict(size=12),
            height=500
        )
        
        return fig
    
    def create_career_trajectory_chart(self, career_data: Dict) -> go.Figure:
        """Create career trajectory visualization with predictions"""
        # Sample career progression data
        stages = ["Entry Level", "Junior", "Mid Level", "Senior", "Expert"]
        current_position = career_data.get("current_level", "Junior")
        
        # Timeline data
        years = list(range(2020, 2031))
        
        # Create salary progression
        base_salaries = {"Entry Level": 50000, "Junior": 70000, "Mid Level": 95000, 
                        "Senior": 130000, "Expert": 180000}
        
        # Current trajectory
        current_idx = stages.index(current_position) if current_position in stages else 1
        current_salaries = []
        predicted_salaries = []
        
        for i, year in enumerate(years):
            if i <= 3:  # Historical/current data
                salary = base_salaries[stages[min(current_idx + i//2, len(stages)-1)]]
                current_salaries.append(salary * (1 + 0.03)**i)  # 3% annual growth
                predicted_salaries.append(None)
            else:  # Predictions
                predicted_idx = min(current_idx + (i-3)//2, len(stages)-1)
                salary = base_salaries[stages[predicted_idx]]
                current_salaries.append(None)
                predicted_salaries.append(salary * (1 + 0.05)**(i-3))  # 5% growth in predictions
        
        fig = go.Figure()
        
        # Current/historical trajectory
        fig.add_trace(go.Scatter(
            x=years,
            y=current_salaries,
            mode='lines+markers',
            name='Historical Progress',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8)
        ))
        
        # Predicted trajectory
        fig.add_trace(go.Scatter(
            x=years,
            y=predicted_salaries,
            mode='lines+markers',
            name='Predicted Progress',
            line=dict(color='#F18F01', width=3, dash='dash'),
            marker=dict(size=8, symbol='diamond')
        ))
        
        # Add milestone markers
        milestones = {2024: "Target Promotion", 2026: "Senior Role", 2029: "Leadership Position"}
        for year, milestone in milestones.items():
            if year in years:
                idx = years.index(year)
                salary = predicted_salaries[idx] or current_salaries[idx]
                if salary:
                    fig.add_annotation(
                        x=year,
                        y=salary,
                        text=milestone,
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor='#C73E1D',
                        bgcolor='rgba(199, 62, 29, 0.8)',
                        bordercolor='#C73E1D',
                        font=dict(color='white', size=10)
                    )
        
        fig.update_layout(
            title="Career Trajectory & Salary Projection",
            xaxis_title="Year",
            yaxis_title="Salary ($)",
            hovermode='x unified',
            showlegend=True,
            height=500,
            yaxis=dict(tickformat='$,.0f')
        )
        
        return fig
    
    def create_competency_gap_analysis(self, current_skills: Dict, 
                                     target_skills: Dict, field: str) -> go.Figure:
        """Create competency gap analysis visualization"""
        # Combine all skills
        all_categories = set(current_skills.keys()) | set(target_skills.keys())
        
        categories = list(all_categories)
        current_values = [len(current_skills.get(cat, [])) for cat in categories]
        target_values = [len(target_skills.get(cat, [])) for cat in categories]
        
        # Calculate gaps
        gaps = [max(0, target - current) for target, current in zip(target_values, current_values)]
        
        fig = go.Figure()
        
        # Current skills
        fig.add_trace(go.Bar(
            x=categories,
            y=current_values,
            name='Current Skills',
            marker_color='#2E86AB',
            opacity=0.8
        ))
        
        # Target skills
        fig.add_trace(go.Bar(
            x=categories,
            y=target_values,
            name='Target Skills',
            marker_color='#F18F01',
            opacity=0.6
        ))
        
        # Gap indicators
        fig.add_trace(go.Scatter(
            x=categories,
            y=[max(current_values[i], target_values[i]) + 1 for i in range(len(categories))],
            mode='markers+text',
            marker=dict(
                size=[gap * 10 + 5 for gap in gaps],
                color='#C73E1D',
                opacity=0.7,
                symbol='triangle-up'
            ),
            text=[f'Gap: {gap}' if gap > 0 else '' for gap in gaps],
            textposition='top center',
            name='Skill Gaps',
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"Competency Gap Analysis - {field.title()}",
            xaxis_title="Skill Categories",
            yaxis_title="Number of Skills",
            barmode='group',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_resume_quality_dashboard(self, quality_metrics: Dict[str, float]) -> go.Figure:
        """Create comprehensive resume quality dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quality Scores', 'Score Distribution', 'Improvement Priority', 'Progress Tracking'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "indicator"}]]
        )
        
        # 1. Quality scores bar chart
        metrics = list(quality_metrics.keys())
        scores = [quality_metrics[metric] * 100 for metric in metrics]
        colors = ['#2E86AB' if score >= 70 else '#F18F01' if score >= 50 else '#C73E1D' for score in scores]
        
        fig.add_trace(
            go.Bar(x=metrics, y=scores, marker_color=colors, name="Quality Scores"),
            row=1, col=1
        )
        
        # 2. Score distribution pie chart
        score_ranges = {'Excellent (80-100%)': 0, 'Good (60-79%)': 0, 'Fair (40-59%)': 0, 'Poor (0-39%)': 0}
        for score in scores:
            if score >= 80:
                score_ranges['Excellent (80-100%)'] += 1
            elif score >= 60:
                score_ranges['Good (60-79%)'] += 1
            elif score >= 40:
                score_ranges['Fair (40-59%)'] += 1
            else:
                score_ranges['Poor (0-39%)'] += 1
        
        fig.add_trace(
            go.Pie(labels=list(score_ranges.keys()), values=list(score_ranges.values()),
                   marker_colors=['#2E86AB', '#2a9d8f', '#F18F01', '#C73E1D']),
            row=1, col=2
        )
        
        # 3. Improvement priority scatter plot
        importance = [0.9, 0.8, 0.7, 0.85, 0.75]  # Example importance weights
        improvement_potential = [max(0, 100 - score) for score in scores]
        
        fig.add_trace(
            go.Scatter(
                x=importance[:len(metrics)],
                y=improvement_potential,
                mode='markers+text',
                marker=dict(size=[pot/5 + 10 for pot in improvement_potential], 
                           color=scores, colorscale='RdYlBu', showscale=False),
                text=metrics,
                textposition='top center',
                name="Improvement Priority"
            ),
            row=2, col=1
        )
        
        # 4. Overall score indicator
        overall_score = np.mean(scores)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=overall_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Score"},
                delta={'reference': 80, 'position': "top"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#2E86AB"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "gray"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="Resume Quality Analysis Dashboard",
            title_x=0.5
        )
        
        return fig
    
    def create_market_insights_chart(self, field: str) -> go.Figure:
        """Create market insights and trends visualization"""
        # Sample market data (in real implementation, this would come from APIs)
        months = pd.date_range(start='2023-01', end='2024-12', freq='M')
        
        # Job demand trends
        np.random.seed(42)
        base_demand = {"data_science": 1000, "web_development": 1500, "mobile_development": 800}
        demand_base = base_demand.get(field, 1000)
        
        demand_trend = [demand_base + np.random.normal(0, 100) + i*20 for i in range(len(months))]
        salary_trend = [85000 + np.random.normal(0, 5000) + i*1000 for i in range(len(months))]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Job Demand Trend', 'Salary Trend', 'Top Skills in Demand', 'Regional Insights'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"type": "bar"}, {"type": "choropleth"}]]
        )
        
        # Job demand trend
        fig.add_trace(
            go.Scatter(
                x=months,
                y=demand_trend,
                mode='lines+markers',
                name='Job Postings',
                line=dict(color='#2E86AB', width=3)
            ),
            row=1, col=1
        )
        
        # Salary trend
        fig.add_trace(
            go.Scatter(
                x=months,
                y=salary_trend,
                mode='lines+markers',
                name='Average Salary',
                line=dict(color='#F18F01', width=3)
            ),
            row=1, col=2
        )
        
        # Top skills demand
        skills_demand = {
            "Python": 85, "JavaScript": 75, "React": 65, 
            "AWS": 70, "Docker": 60, "Machine Learning": 80
        }
        
        fig.add_trace(
            go.Bar(
                x=list(skills_demand.values()),
                y=list(skills_demand.keys()),
                orientation='h',
                marker_color='#2a9d8f',
                name='Skill Demand %'
            ),
            row=2, col=1
        )
        
        # Regional insights (simplified)
        states = ['CA', 'NY', 'TX', 'WA', 'MA']
        job_counts = [2500, 1800, 1200, 1500, 900]
        
        fig.add_trace(
            go.Bar(
                x=states,
                y=job_counts,
                marker_color='#e9c46a',
                name='Jobs by State'
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=700,
            title_text=f"Market Insights - {field.replace('_', ' ').title()}",
            title_x=0.5,
            showlegend=False
        )
        
        return fig
    
    def create_interview_performance_chart(self, interview_data: List[Dict]) -> go.Figure:
        """Create interview performance visualization"""
        if not interview_data:
            # Create empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No interview data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        # Extract performance data
        criteria = ["technical_accuracy", "communication", "problem_solving", "confidence", "examples"]
        sessions = [f"Session {i+1}" for i in range(len(interview_data))]
        
        fig = go.Figure()
        
        # Add traces for each criterion
        colors = self.color_schemes["professional"]
        for i, criterion in enumerate(criteria):
            scores = [data.get("scores", {}).get(criterion, 0) * 100 for data in interview_data]
            
            fig.add_trace(go.Scatter(
                x=sessions,
                y=scores,
                mode='lines+markers',
                name=criterion.replace('_', ' ').title(),
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ))
        
        # Add overall score
        overall_scores = [data.get("overall_score", 0) * 100 for data in interview_data]
        fig.add_trace(go.Scatter(
            x=sessions,
            y=overall_scores,
            mode='lines+markers',
            name='Overall Score',
            line=dict(color='black', width=4, dash='dash'),
            marker=dict(size=10, symbol='diamond')
        ))
        
        fig.update_layout(
            title="Interview Performance Progress",
            xaxis_title="Interview Sessions",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100]),
            hovermode='x unified',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_networking_opportunities_map(self, location_data: Dict) -> go.Figure:
        """Create networking opportunities visualization"""
        # Sample networking data
        opportunities = [
            {"type": "Meetup", "name": "Data Science Meetup", "location": "San Francisco", 
             "attendees": 250, "lat": 37.7749, "lon": -122.4194},
            {"type": "Conference", "name": "Tech Conference 2024", "location": "Seattle", 
             "attendees": 500, "lat": 47.6062, "lon": -122.3321},
            {"type": "Workshop", "name": "ML Workshop", "location": "Austin", 
             "attendees": 100, "lat": 30.2672, "lon": -97.7431},
            {"type": "Networking", "name": "Professional Mixer", "location": "New York", 
             "attendees": 150, "lat": 40.7128, "lon": -74.0060}
        ]
        
        fig = go.Figure()
        
        # Group by type for different colors
        type_colors = {"Meetup": "#2E86AB", "Conference": "#F18F01", 
                      "Workshop": "#2a9d8f", "Networking": "#C73E1D"}
        
        for opp_type in type_colors:
            filtered_opps = [opp for opp in opportunities if opp["type"] == opp_type]
            if filtered_opps:
                fig.add_trace(go.Scattermapbox(
                    lat=[opp["lat"] for opp in filtered_opps],
                    lon=[opp["lon"] for opp in filtered_opps],
                    mode='markers',
                    marker=dict(
                        size=[opp["attendees"]/10 for opp in filtered_opps],
                        color=type_colors[opp_type],
                        opacity=0.7
                    ),
                    text=[f"{opp['name']}<br>{opp['location']}<br>{opp['attendees']} attendees" 
                          for opp in filtered_opps],
                    name=opp_type,
                    hovertemplate='<b>%{text}</b><extra></extra>'
                ))
        
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=39.8283, lon=-98.5795),  # Center of US
                zoom=3
            ),
            title="Networking Opportunities Near You",
            height=500,
            showlegend=True
        )
        
        return fig

def create_gamification_dashboard(user_progress: Dict) -> go.Figure:
    """Create gamification progress dashboard"""
    # Sample achievement data
    achievements = {
        "Resume Optimizer": {"earned": True, "date": "2024-01-15"},
        "Interview Master": {"earned": True, "date": "2024-01-20"},
        "Skill Builder": {"earned": False, "date": None},
        "Network Navigator": {"earned": False, "date": None},
        "Career Strategist": {"earned": True, "date": "2024-01-25"}
    }
    
    # Progress metrics
    metrics = {
        "Resumes Analyzed": {"current": 5, "target": 10},
        "Interviews Completed": {"current": 3, "target": 5},
        "Skills Added": {"current": 8, "target": 15},
        "Connections Made": {"current": 2, "target": 10}
    }
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Achievement Progress', 'Skill Development', 'Weekly Activity', 'Level Progress'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "scatter"}, {"type": "indicator"}]]
    )
    
    # Achievement progress
    earned_count = sum(1 for ach in achievements.values() if ach["earned"])
    total_achievements = len(achievements)
    
    fig.add_trace(
        go.Bar(
            x=["Earned", "Remaining"],
            y=[earned_count, total_achievements - earned_count],
            marker_color=['#2E86AB', '#lightgray'],
            name="Achievements"
        ),
        row=1, col=1
    )
    
    # Skill development pie
    skill_categories = ["Technical", "Soft Skills", "Industry Knowledge", "Leadership"]
    skill_progress = [75, 60, 45, 30]  # Progress percentages
    
    fig.add_trace(
        go.Pie(
            labels=skill_categories,
            values=skill_progress,
            marker_colors=['#2E86AB', '#F18F01', '#2a9d8f', '#C73E1D']
        ),
        row=1, col=2
    )
    
    # Weekly activity
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    activity_points = [10, 15, 8, 20, 12, 5, 18]
    
    fig.add_trace(
        go.Scatter(
            x=days,
            y=activity_points,
            mode='lines+markers',
            line=dict(color='#2a9d8f', width=3),
            marker=dict(size=8),
            name="Activity Points"
        ),
        row=2, col=1
    )
    
    # Overall level progress
    current_level = user_progress.get("level", 2)
    current_xp = user_progress.get("experience_points", 350)
    next_level_xp = 500
    
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=current_xp,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Level {current_level} Progress"},
            gauge={
                'axis': {'range': [None, next_level_xp]},
                'bar': {'color': "#2E86AB"},
                'steps': [
                    {'range': [0, next_level_xp * 0.5], 'color': "lightgray"},
                    {'range': [next_level_xp * 0.5, next_level_xp * 0.8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': next_level_xp
                }
            }
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text="Your Progress Dashboard",
        title_x=0.5,
        showlegend=False
    )
    
    return fig