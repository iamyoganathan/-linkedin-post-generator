"""
LinkedIn Post Generator - Main Streamlit Application
Developed for M.C.A. Final Year Project
"""

import streamlit as st
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Import custom modules
from src.generator import LinkedInPostGenerator, test_api_connection
from src.database import Database
from src.utils import (
    count_words, count_characters, get_relative_time,
    format_post_preview, validate_post_content, 
    export_to_text, get_post_statistics,
    calculate_engagement_factors, format_hashtags
)

# Page configuration
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0077B5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .post-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0077B5;
        margin: 1rem 0;
    }
    .stat-box {
        background-color: #0077B5;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = ""
    if 'generated_hashtags' not in st.session_state:
        st.session_state.generated_hashtags = ""
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = ""
    if 'generator' not in st.session_state:
        try:
            st.session_state.generator = LinkedInPostGenerator()
        except ValueError as e:
            st.session_state.generator = None
            st.session_state.api_error = str(e)
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"


init_session_state()


# Sidebar Navigation
def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("### 📱 LinkedIn Post Generator")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Home", "📝 My Drafts", "📊 History", "⭐ Favorites", "⚙️ Settings", "📈 Analytics"],
            index=["🏠 Home", "📝 My Drafts", "📊 History", "⭐ Favorites", "⚙️ Settings", "📈 Analytics"].index(st.session_state.page)
        )
        st.session_state.page = page
        
        st.markdown("---")
        
        # Quick stats
        if st.session_state.db:
            stats = st.session_state.db.get_statistics()
            st.markdown("### 📊 Quick Stats")
            st.metric("Total Posts", stats['total_posts'])
            st.metric("Saved Drafts", stats['total_drafts'])
            st.metric("This Week", stats['recent_posts'])
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("• Be specific with topics")
        st.markdown("• Use storytelling")
        st.markdown("• Add personal insights")
        st.markdown("• Include a CTA")
        
        st.markdown("---")
        st.caption("Made with ❤️ for M.C.A. Project")


# Home Page - Main Post Generator
def render_home_page():
    """Render the main post generation page"""
    
    # Header
    st.markdown('<div class="main-header">📱 LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create engaging LinkedIn content in seconds with AI</div>', unsafe_allow_html=True)
    
    # Check if API is configured
    if st.session_state.generator is None:
        st.error("⚠️ Groq API Key not configured!")
        st.info("Please add your GROQ_API_KEY to the .env file")
        
        with st.expander("🔧 How to get Groq API Key"):
            st.markdown("""
            1. Visit https://console.groq.com/
            2. Sign up for a free account
            3. Navigate to API Keys section
            4. Create a new API key
            5. Copy the key and paste it in the `.env` file
            6. Restart the application
            """)
        return
    
    # Main content in columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Details")
        
        # Topic input
        topic = st.text_area(
            "What would you like to write about?",
            height=100,
            placeholder="E.g., The importance of continuous learning in tech careers...",
            help="Be as specific as possible for better results"
        )
        
        # Advanced options in expander
        with st.expander("⚙️ Advanced Options"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                tone = st.selectbox(
                    "Tone",
                    ["Professional", "Casual", "Motivational", "Educational", "Storytelling", "Thought-Leadership"],
                    help="Choose the tone that fits your message"
                )
                
                post_type = st.selectbox(
                    "Post Type",
                    ["General", "Announcement", "Tips", "Question", "Achievement", "Industry Insight"],
                    help="Select the type of post you want to create"
                )
            
            with col_b:
                length = st.select_slider(
                    "Length",
                    options=["Short", "Medium", "Long"],
                    value="Medium",
                    help="Short: 2-4 lines, Medium: 5-8 lines, Long: 10-15 lines"
                )
                
                include_hashtags = st.checkbox("Generate Hashtags", value=True)
        
        # Generate button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            generate_btn = st.button("🚀 Generate Post", use_container_width=True, type="primary")
        
        with col_btn2:
            variations_btn = st.button("🔄 Generate 3 Variations", use_container_width=True)
        
        with col_btn3:
            hooks_btn = st.button("🎣 Generate Hooks", use_container_width=True)
        
        # Generation logic
        if generate_btn and topic:
            with st.spinner("✨ Generating your post..."):
                try:
                    # Generate post
                    post = st.session_state.generator.generate_post(
                        topic=topic,
                        tone=tone.lower(),
                        length=length.lower(),
                        post_type=post_type.lower().replace(" ", "_")
                    )
                    st.session_state.generated_post = post
                    st.session_state.current_topic = topic
                    
                    # Generate hashtags if requested
                    if include_hashtags:
                        hashtags = st.session_state.generator.generate_hashtags(topic)
                        st.session_state.generated_hashtags = format_hashtags(hashtags)
                    else:
                        st.session_state.generated_hashtags = ""
                    
                    st.success("✅ Post generated successfully!")
                    
                    # Save to history
                    st.session_state.db.save_post(
                        topic=topic,
                        tone=tone.lower(),
                        length=length.lower(),
                        content=post,
                        hashtags=st.session_state.generated_hashtags,
                        post_type=post_type.lower()
                    )
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        elif generate_btn:
            st.warning("⚠️ Please enter a topic first!")
        
        # Generate variations
        if variations_btn and topic:
            with st.spinner("✨ Generating 3 variations..."):
                try:
                    variations = st.session_state.generator.generate_variations(
                        topic=topic,
                        tone=tone.lower(),
                        length=length.lower(),
                        count=3
                    )
                    
                    st.session_state.variations = variations
                    st.success("✅ Variations generated!")
                    
                    # Display variations in col2
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Generate hooks
        if hooks_btn and topic:
            with st.spinner("🎣 Generating hooks..."):
                try:
                    hooks = st.session_state.generator.generate_hooks(topic)
                    st.session_state.hooks = hooks
                    st.success("✅ Hooks generated!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### 🎯 Generated Content")
        
        # Display generated post
        if st.session_state.generated_post:
            st.markdown('<div class="post-box">', unsafe_allow_html=True)
            st.markdown(st.session_state.generated_post)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display hashtags
            if st.session_state.generated_hashtags:
                st.markdown("**Suggested Hashtags:**")
                st.code(st.session_state.generated_hashtags)
            
            # Post statistics
            with st.expander("📊 Post Statistics"):
                stats = get_post_statistics(st.session_state.generated_post)
                col_s1, col_s2, col_s3 = st.columns(3)
                
                with col_s1:
                    st.metric("Words", stats['word_count'])
                    st.metric("Characters", stats['character_count'])
                
                with col_s2:
                    st.metric("Lines", stats['line_count'])
                    st.metric("Read Time", f"{stats['read_time_seconds']}s")
                
                with col_s3:
                    st.metric("Sentences", stats['sentence_count'])
                    st.metric("Hashtags", stats['hashtag_count'])
            
            # Engagement prediction
            with st.expander("📈 Engagement Prediction"):
                with st.spinner("Analyzing..."):
                    try:
                        prediction = st.session_state.generator.predict_engagement(
                            st.session_state.generated_post
                        )
                        
                        # Display score
                        score = prediction.get('total', 0)
                        score_color = "#28a745" if score >= 70 else "#ffc107" if score >= 50 else "#dc3545"
                        
                        st.markdown(f"""
                        <div style='text-align: center; padding: 1rem; background-color: {score_color}20; border-radius: 8px;'>
                            <h1 style='color: {score_color}; margin: 0;'>{score}/100</h1>
                            <p style='margin: 0;'><strong>{prediction.get('prediction', 'Unknown')}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        
                        # Detailed scores
                        col_p1, col_p2 = st.columns(2)
                        with col_p1:
                            st.metric("Hook Quality", f"{prediction.get('hook', 0)}/25")
                            st.metric("Content Value", f"{prediction.get('content', 0)}/25")
                            st.metric("Readability", f"{prediction.get('readability', 0)}/20")
                        
                        with col_p2:
                            st.metric("Call-to-Action", f"{prediction.get('cta', 0)}/15")
                            st.metric("Authenticity", f"{prediction.get('authenticity', 0)}/15")
                        
                    except Exception as e:
                        st.error(f"Could not predict engagement: {str(e)}")
            
            # Action buttons
            st.markdown("### ⚡ Actions")
            col_a1, col_a2, col_a3, col_a4 = st.columns(4)
            
            with col_a1:
                if st.button("📋 Copy", use_container_width=True):
                    full_text = st.session_state.generated_post
                    if st.session_state.generated_hashtags:
                        full_text += "\n\n" + st.session_state.generated_hashtags
                    st.code(full_text)
                    st.success("✅ Copy the text above!")
            
            with col_a2:
                if st.button("💾 Save Draft", use_container_width=True):
                    title = st.session_state.current_topic[:50]
                    st.session_state.db.save_draft(
                        title=title,
                        content=st.session_state.generated_post,
                        hashtags=st.session_state.generated_hashtags
                    )
                    st.success("✅ Saved to drafts!")
            
            with col_a3:
                if st.button("🔄 Regenerate", use_container_width=True):
                    st.rerun()
            
            with col_a4:
                if st.button("✨ Add Emojis", use_container_width=True):
                    with st.spinner("Adding emojis..."):
                        try:
                            post_with_emojis = st.session_state.generator.add_emojis(
                                st.session_state.generated_post,
                                st.session_state.current_topic
                            )
                            st.session_state.generated_post = post_with_emojis
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            # Refinement options
            st.markdown("### 🔧 Refine Post")
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                if st.button("📉 Make Shorter", use_container_width=True):
                    with st.spinner("Refining..."):
                        try:
                            refined = st.session_state.generator.refine_post(
                                st.session_state.generated_post,
                                "make_shorter"
                            )
                            st.session_state.generated_post = refined
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            with col_r2:
                if st.button("📈 Make Longer", use_container_width=True):
                    with st.spinner("Refining..."):
                        try:
                            refined = st.session_state.generator.refine_post(
                                st.session_state.generated_post,
                                "make_longer"
                            )
                            st.session_state.generated_post = refined
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            with col_r3:
                if st.button("💼 More Professional", use_container_width=True):
                    with st.spinner("Refining..."):
                        try:
                            refined = st.session_state.generator.refine_post(
                                st.session_state.generated_post,
                                "more_professional"
                            )
                            st.session_state.generated_post = refined
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        else:
            st.info("👆 Enter a topic and click 'Generate Post' to get started!")
        
        # Display variations if generated
        if 'variations' in st.session_state and st.session_state.variations:
            st.markdown("### 🔄 Variations")
            for i, var in enumerate(st.session_state.variations, 1):
                with st.expander(f"Variation {i}"):
                    st.markdown(var)
                    if st.button(f"Use Variation {i}", key=f"use_var_{i}"):
                        st.session_state.generated_post = var
                        st.rerun()
        
        # Display hooks if generated
        if 'hooks' in st.session_state and st.session_state.hooks:
            st.markdown("### 🎣 Hook Ideas")
            for i, hook in enumerate(st.session_state.hooks, 1):
                st.markdown(f"**{i}.** {hook}")


# Drafts Page
def render_drafts_page():
    """Render drafts management page"""
    st.markdown('<div class="main-header">📝 My Drafts</div>', unsafe_allow_html=True)
    
    drafts = st.session_state.db.get_all_drafts()
    
    if not drafts:
        st.info("📭 No drafts saved yet. Generate some posts and save them as drafts!")
        return
    
    st.markdown(f"### Total Drafts: {len(drafts)}")
    
    for draft in drafts:
        with st.expander(f"📄 {draft['title']} - {get_relative_time(draft['updated_at'])}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Content:**")
                st.markdown(draft['content'])
                
                if draft['hashtags']:
                    st.markdown("**Hashtags:**")
                    st.code(draft['hashtags'])
                
                if draft['notes']:
                    st.markdown("**Notes:**")
                    st.info(draft['notes'])
            
            with col2:
                st.markdown("**Actions:**")
                
                if st.button("📋 Copy", key=f"copy_draft_{draft['id']}", use_container_width=True):
                    full_text = draft['content']
                    if draft['hashtags']:
                        full_text += "\n\n" + draft['hashtags']
                    st.code(full_text)
                
                if st.button("✏️ Edit", key=f"edit_draft_{draft['id']}", use_container_width=True):
                    st.session_state.editing_draft = draft
                
                if st.button("🗑️ Delete", key=f"del_draft_{draft['id']}", use_container_width=True):
                    st.session_state.db.delete_draft(draft['id'])
                    st.success("Deleted!")
                    st.rerun()


# History Page
def render_history_page():
    """Render post history page"""
    st.markdown('<div class="main-header">📊 Post History</div>', unsafe_allow_html=True)
    
    posts = st.session_state.db.get_all_posts(limit=100)
    
    if not posts:
        st.info("📭 No posts in history yet. Start generating posts!")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_tone = st.multiselect(
            "Filter by Tone",
            ["professional", "casual", "motivational", "educational", "storytelling"],
            default=[]
        )
    
    with col2:
        filter_length = st.multiselect(
            "Filter by Length",
            ["short", "medium", "long"],
            default=[]
        )
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First"])
    
    # Apply filters
    filtered_posts = posts
    if filter_tone:
        filtered_posts = [p for p in filtered_posts if p['tone'] in filter_tone]
    if filter_length:
        filtered_posts = [p for p in filtered_posts if p['length'] in filter_length]
    
    if sort_by == "Oldest First":
        filtered_posts = reversed(filtered_posts)
    
    st.markdown(f"### Showing {len(filtered_posts)} posts")
    
    # Export button
    if st.button("📥 Export to Text File"):
        export_content = export_to_text(filtered_posts)
        st.download_button(
            label="💾 Download",
            data=export_content,
            file_name=f"linkedin_posts_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    # Display posts
    for post in filtered_posts:
        with st.expander(f"📄 {post['topic'][:60]}... - {get_relative_time(post['created_at'])}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**Content:**")
                st.markdown(post['content'])
                
                if post['hashtags']:
                    st.markdown("**Hashtags:**")
                    st.code(post['hashtags'])
                
                st.caption(f"Tone: {post['tone'].title()} | Length: {post['length'].title()}")
            
            with col2:
                st.markdown("**Actions:**")
                
                if st.button("📋 Copy", key=f"copy_post_{post['id']}", use_container_width=True):
                    full_text = post['content']
                    if post['hashtags']:
                        full_text += "\n\n" + post['hashtags']
                    st.code(full_text)
                
                fav_label = "⭐ Unfavorite" if post['is_favorite'] else "⭐ Favorite"
                if st.button(fav_label, key=f"fav_post_{post['id']}", use_container_width=True):
                    st.session_state.db.toggle_favorite(post['id'])
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"del_post_{post['id']}", use_container_width=True):
                    st.session_state.db.delete_post(post['id'])
                    st.success("Deleted!")
                    st.rerun()


# Favorites Page
def render_favorites_page():
    """Render favorites page"""
    st.markdown('<div class="main-header">⭐ Favorite Posts</div>', unsafe_allow_html=True)
    
    favorites = st.session_state.db.get_favorites()
    
    if not favorites:
        st.info("⭐ No favorite posts yet. Mark posts as favorites from the History page!")
        return
    
    st.markdown(f"### {len(favorites)} Favorite Posts")
    
    for post in favorites:
        with st.expander(f"📄 {post['topic'][:60]}... - {get_relative_time(post['created_at'])}"):
            st.markdown(post['content'])
            
            if post['hashtags']:
                st.markdown("**Hashtags:**")
                st.code(post['hashtags'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📋 Copy", key=f"copy_fav_{post['id']}", use_container_width=True):
                    full_text = post['content']
                    if post['hashtags']:
                        full_text += "\n\n" + post['hashtags']
                    st.code(full_text)
            
            with col2:
                if st.button("⭐ Unfavorite", key=f"unfav_{post['id']}", use_container_width=True):
                    st.session_state.db.toggle_favorite(post['id'])
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"del_fav_{post['id']}", use_container_width=True):
                    st.session_state.db.delete_post(post['id'])
                    st.rerun()


# Settings Page
def render_settings_page():
    """Render settings page"""
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Settings", "🎨 Preferences", "🗑️ Data Management"])
    
    with tab1:
        st.markdown("### Groq API Configuration")
        
        # Test API connection
        if st.button("🧪 Test API Connection"):
            with st.spinner("Testing..."):
                success, message = test_api_connection()
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
        
        st.markdown("---")
        st.markdown("**API Key Location:** `.env` file in project root")
        st.code("GROQ_API_KEY=your_key_here")
        
    with tab2:
        st.markdown("### Default Preferences")
        
        default_tone = st.selectbox(
            "Default Tone",
            ["Professional", "Casual", "Motivational", "Educational", "Storytelling"],
            index=0
        )
        
        default_length = st.select_slider(
            "Default Length",
            options=["Short", "Medium", "Long"],
            value="Medium"
        )
        
        auto_hashtags = st.checkbox("Auto-generate Hashtags", value=True)
        
        if st.button("💾 Save Preferences"):
            st.session_state.db.set_setting("default_tone", default_tone.lower())
            st.session_state.db.set_setting("default_length", default_length.lower())
            st.session_state.db.set_setting("auto_hashtags", str(auto_hashtags))
            st.success("✅ Preferences saved!")
    
    with tab3:
        st.markdown("### Data Management")
        st.warning("⚠️ These actions cannot be undone!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear History", use_container_width=True):
                # This would need a confirmation dialog
                st.session_state.confirm_clear_history = True
        
        with col2:
            if st.button("🗑️ Clear Drafts", use_container_width=True):
                st.session_state.confirm_clear_drafts = True


# Analytics Page
def render_analytics_page():
    """Render analytics dashboard"""
    st.markdown('<div class="main-header">📈 Analytics Dashboard</div>', unsafe_allow_html=True)
    
    stats = st.session_state.db.get_statistics()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Total Posts", stats['total_posts'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Saved Drafts", stats['total_drafts'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Most Used Tone", stats['most_used_tone'].title())
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("This Week", stats['recent_posts'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    if stats['posts_by_tone']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Posts by Tone")
            df_tone = pd.DataFrame(
                list(stats['posts_by_tone'].items()),
                columns=['Tone', 'Count']
            )
            fig = px.bar(df_tone, x='Tone', y='Count', color='Tone')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🥧 Tone Distribution")
            fig = px.pie(df_tone, values='Count', names='Tone')
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("📊 Generate some posts to see analytics!")


# Main App Router
def main():
    """Main application router"""
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.page
    
    if page == "🏠 Home":
        render_home_page()
    elif page == "📝 My Drafts":
        render_drafts_page()
    elif page == "📊 History":
        render_history_page()
    elif page == "⭐ Favorites":
        render_favorites_page()
    elif page == "⚙️ Settings":
        render_settings_page()
    elif page == "📈 Analytics":
        render_analytics_page()


if __name__ == "__main__":
    main()
