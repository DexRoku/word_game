import streamlit as st
import random
from collections import Counter
import time

# Custom CSS for fancy styling with interactive letters
def load_custom_css():
    st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom containers */
    .game-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    .letter-grid {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    .letter-item {
        display: inline-block;
        background: white;
        color: #333;
        padding: 15px 20px;
        margin: 5px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 24px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        user-select: none;
        min-width: 50px;
        position: relative;
    }
    
    .letter-item:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: white;
    }
    
    .letter-item.selected {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 30px rgba(255, 107, 107, 0.4);
        animation: bounce 0.3s ease;
    }
    
    .letter-item.used {
        background: #ccc;
        color: #666;
        opacity: 0.5;
        cursor: not-allowed;
        transform: scale(0.9);
    }
    
    .letter-count {
        position: absolute;
        top: -8px;
        right: -8px;
        background: #FF6B6B;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 12px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .current-word-display {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        letter-spacing: 3px;
    }
    
    .current-word-display.empty {
        color: rgba(255,255,255,0.6);
        font-style: italic;
        font-size: 1.2rem;
        letter-spacing: normal;
    }
    
    .found-word {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 10px 20px;
        margin: 5px;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        animation: slideInRight 0.5s ease;
    }
    
    .score-display {
        background: linear-gradient(45deg, #ffd89b, #19547b);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .hint-box {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .game-title {
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-size: 3rem;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .subtitle {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    
    .action-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
        to { text-shadow: 0 0 30px rgba(255,255,255,0.8), 0 0 40px rgba(255,255,255,0.8); }
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: translateY(-8px) scale(1.05); }
        40%, 43% { transform: translateY(-15px) scale(1.1); }
        70% { transform: translateY(-10px) scale(1.08); }
        90% { transform: translateY(-9px) scale(1.06); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .shake-animation {
        animation: shake 0.5s ease-in-out;
    }
    
    .celebration {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #333;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        animation: bounce 2s infinite;
        margin: 2rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 15px;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    
    <script>
    function selectLetter(letterId, letter) {
        // Send the selected letter back to Streamlit
        const event = new CustomEvent('letterSelected', {
            detail: { letterId: letterId, letter: letter }
        });
        window.dispatchEvent(event);
        
        // Add visual feedback
        const element = document.getElementById(letterId);
        if (element && !element.classList.contains('used')) {
            element.classList.add('selected');
            setTimeout(() => {
                element.classList.remove('selected');
            }, 300);
        }
    }
    </script>
    """, unsafe_allow_html=True)

# Enhanced word lists
EASY_WORDS = [
    'cat', 'dog', 'bat', 'rat', 'hat', 'mat', 'sat', 'pat', 'fat', 'at',
    'an', 'am', 'as', 'it', 'in', 'is', 'to', 'go', 'no', 'so', 'do',
    'eat', 'tea', 'sea', 'see', 'bee', 'red', 'bed', 'led', 'fed',
    'car', 'bar', 'far', 'jar', 'tar', 'war', 'are', 'ear', 'net', 'ten',
    'pen', 'den', 'men', 'hen', 'get', 'set', 'wet', 'let', 'met', 'pet'
]

MEDIUM_WORDS = [
    'game', 'name', 'same', 'came', 'fame', 'time', 'lime', 'dime',
    'home', 'dome', 'some', 'come', 'bone', 'tone', 'cone', 'zone',
    'make', 'take', 'lake', 'cake', 'wake', 'sake', 'rake', 'bake',
    'team', 'beam', 'seam', 'dream', 'cream', 'steam', 'stream',
    'fire', 'tire', 'wire', 'hire', 'dire', 'mire', 'sire', 'spire',
    'love', 'move', 'dove', 'cove', 'wove', 'rove', 'grove', 'stove'
]

HARD_WORDS = [
    'stream', 'master', 'faster', 'castle', 'battle', 'rattle',
    'create', 'relate', 'debate', 'update', 'locate', 'rotate',
    'winter', 'center', 'hunter', 'wonder', 'tender', 'render',
    'simple', 'temple', 'sample', 'example', 'purple', 'circle',
    'nature', 'future', 'picture', 'culture', 'capture', 'feature',
    'strong', 'string', 'spring', 'brings', 'things', 'change'
]

def get_letters_for_words(words, num_extra=2):
    """Generate a set of letters that can form the given words plus some extras"""
    all_letters = []
    for word in words:
        all_letters.extend(list(word.upper()))
    
    letter_counts = Counter(all_letters)
    extra_letters = random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=num_extra)
    
    result = []
    for letter, count in letter_counts.items():
        result.extend([letter] * count)
    result.extend(extra_letters)
    
    return result

def can_form_word(word, available_letters):
    """Check if a word can be formed from available letters"""
    word_upper = word.upper()
    available_counter = Counter(available_letters)
    word_counter = Counter(word_upper)
    
    for letter, needed_count in word_counter.items():
        if available_counter[letter] < needed_count:
            return False
    return True

def display_interactive_letters(letters):
    """Display letters as clickable buttons"""
    letter_counts = Counter(letters)
    unique_letters = sorted(set(letters))
    
    st.markdown("""
    <div class="letter-grid">
        <h3 style="color: white; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🎲 Click Letters to Form Words 🎲
        </h3>
    """, unsafe_allow_html=True)
    
    # Create columns for letter layout
    cols_per_row = 6
    letter_rows = [unique_letters[i:i+cols_per_row] for i in range(0, len(unique_letters), cols_per_row)]
    
    for row_idx, row in enumerate(letter_rows):
        cols = st.columns(len(row))
        for col_idx, letter in enumerate(row):
            with cols[col_idx]:
                count = letter_counts[letter]
                used_count = st.session_state.current_word.count(letter.upper())
                remaining = count - used_count
                
                # Button styling based on availability
                if remaining > 0:
                    if st.button(
                        f"{letter}",
                        key=f"letter_{letter}_{row_idx}_{col_idx}",
                        use_container_width=True
                    ):
                        # Add letter to current word
                        st.session_state.current_word += letter.upper()
                        st.rerun()
                else:
                    # Disabled button for used letters
                    st.button(
                        f"{letter}",
                        key=f"letter_disabled_{letter}_{row_idx}_{col_idx}",
                        disabled=True,
                        use_container_width=True
                    )
                
                # Show count if more than 1
                if count > 1:
                    st.caption(f"{remaining}/{count}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def display_current_word():
    """Display the currently formed word"""
    current_word = st.session_state.get('current_word', '')
    
    if current_word:
        display_word = ' '.join(current_word)
        st.markdown(f"""
        <div class="current-word-display">
            {display_word}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="current-word-display empty">
            Click letters above to form a word...
        </div>
        """, unsafe_allow_html=True)

def display_word_actions():
    """Display action buttons for the current word"""
    col1, col2 = st.columns(2)
    
    with col1:
        submit_word = st.button("✅ Submit Word", type="primary", use_container_width=True)
    
    with col2:
        clear_word = st.button("🗑️ Clear Word", use_container_width=True)
    
    return submit_word, clear_word

def display_found_words(found_words):
    """Display found words with fancy styling"""
    if found_words:
        words_html = ""
        for word in sorted(found_words):
            points = len(word) * 10
            words_html += f'<div class="found-word">✨ {word.upper()} ({points} pts)</div>'
        
        st.markdown(f"""
        <div class="game-container">
            <h3 style="text-align: center; color: #333; margin-bottom: 1rem;">🏆 Found Words 🏆</h3>
            <div style="text-align: center;">
                {words_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="game-container">
            <h3 style="text-align: center; color: #333;">🔍 No Words Found Yet</h3>
            <p style="text-align: center; color: #666;">Click letters to form words!</p>
        </div>
        """, unsafe_allow_html=True)

def display_game_stats(score, found_count, total_count, attempts):
    """Display game statistics with fancy styling"""
    progress_percent = (found_count / total_count) * 100
    
    st.markdown(f"""
    <div class="score-display">
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; text-align: center;">
            <div>
                <div style="font-size: 2rem;">💎</div>
                <div>Score</div>
                <div style="font-size: 1.5rem;">{score}</div>
            </div>
            <div>
                <div style="font-size: 2rem;">🎯</div>
                <div>Words</div>
                <div style="font-size: 1.5rem;">{found_count}/{total_count}</div>
            </div>
            <div>
                <div style="font-size: 2rem;">🎮</div>
                <div>Attempts</div>
                <div style="font-size: 1.5rem;">{attempts}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fancy progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div style="text-align: center; margin-bottom: 1rem; font-weight: bold; color: #333;">
            Game Progress: {progress_percent:.1f}%
        </div>
        <div style="background: #e0e0e0; border-radius: 15px; overflow: hidden;">
            <div style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                        width: {progress_percent}%; 
                        height: 20px; 
                        border-radius: 15px;
                        transition: width 0.5s ease;
                        box-shadow: 0 2px 10px rgba(78, 205, 196, 0.3);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_celebration():
    """Display celebration animation when game is completed"""
    st.markdown("""
    <div class="celebration">
        <h1>🎉 CONGRATULATIONS! 🎉</h1>
        <h2>🏆 You Found All Words! 🏆</h2>
        <p style="font-size: 1.2rem; margin: 1rem 0;">
            Amazing job! You're a true Word Master! ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

def initialize_game():
    """Initialize a new game"""
    difficulty = st.session_state.get('difficulty', 'Easy')
    
    if difficulty == 'Easy':
        target_words = random.sample(EASY_WORDS, 6)
        num_extra = 3
    elif difficulty == 'Medium':
        target_words = random.sample(MEDIUM_WORDS, 5)
        num_extra = 4
    else:  # Hard
        target_words = random.sample(HARD_WORDS, 4)
        num_extra = 5
    
    letters = get_letters_for_words(target_words, num_extra)
    random.shuffle(letters)
    
    st.session_state.target_words = set(target_words)
    st.session_state.available_letters = letters
    st.session_state.found_words = set()
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.hints_used = 0
    st.session_state.current_word = ''

def main():
    st.set_page_config(
        page_title="Word Master Game",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_custom_css()
    
    # Game title
    st.markdown("""
    <h1 class="game-title">🌟 WORD MASTER 🌟</h1>
    <p class="subtitle">✨ Click Letters • Form Words • Score Points! ✨</p>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'target_words' not in st.session_state:
        st.session_state.difficulty = 'Easy'
        st.session_state.current_word = ''
        initialize_game()
    
    # Ensure current_word exists
    if 'current_word' not in st.session_state:
        st.session_state.current_word = ''
    
    # Sidebar for game controls
    with st.sidebar:
        st.markdown("### 🎮 Game Controls")
        
        # Difficulty selector with emojis
        difficulty_options = {
            'Easy': '🌱 Easy (6 short words)',
            'Medium': '🌿 Medium (5 medium words)', 
            'Hard': '🌳 Hard (4 long words)'
        }
        
        selected_display = st.selectbox(
            "Choose Difficulty:",
            list(difficulty_options.values()),
            index=list(difficulty_options.keys()).index(st.session_state.get('difficulty', 'Easy'))
        )
        
        # Extract actual difficulty from display string
        difficulty = [k for k, v in difficulty_options.items() if v == selected_display][0]
        
        if difficulty != st.session_state.get('difficulty', 'Easy'):
            st.session_state.difficulty = difficulty
            initialize_game()
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🎲 New Game", type="primary", use_container_width=True):
            initialize_game()
            st.rerun()
        
        st.markdown("---")
        
        # Display game stats in sidebar
        display_game_stats(
            st.session_state.score,
            len(st.session_state.found_words),
            len(st.session_state.target_words),
            st.session_state.attempts
        )
        
        # Hints section
        st.markdown("### 💡 Need Help?")
        if st.button("🔍 Get Hint", use_container_width=True):
            remaining_words = st.session_state.target_words - st.session_state.found_words
            if remaining_words:
                hint_word = random.choice(list(remaining_words))
                st.session_state.hints_used += 1
                st.markdown(f"""
                <div class="hint-box">
                    💡 Hint #{st.session_state.hints_used}<br>
                    Word starts with '<strong>{hint_word[0].upper()}</strong>' 
                    and has <strong>{len(hint_word)}</strong> letters
                </div>
                """, unsafe_allow_html=True)
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display interactive letters
        display_interactive_letters(st.session_state.available_letters)
        
        # Display current word being formed
        display_current_word()
        
        # Word action buttons
        submit_clicked, clear_clicked = display_word_actions()
        
        # Handle clear word
        if clear_clicked:
            st.session_state.current_word = ''
            st.rerun()
        
        # Handle word submission
        if submit_clicked and st.session_state.current_word:
            user_word = st.session_state.current_word.lower()
            st.session_state.attempts += 1
            
            if user_word in st.session_state.target_words:
                if user_word not in st.session_state.found_words:
                    st.session_state.found_words.add(user_word)
                    points = len(user_word) * 10
                    st.session_state.score += points
                    st.session_state.current_word = ''  # Clear the word
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(45deg, #56ab2f, #a8e6cf); 
                                color: white; 
                                padding: 1rem; 
                                border-radius: 15px; 
                                text-align: center; 
                                margin: 1rem 0;
                                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                                animation: bounce 0.6s ease;">
                        ✨ <strong>EXCELLENT!</strong> ✨<br>
                        '<strong>{user_word.upper()}</strong>' is correct!<br>
                        <strong>+{points} Points!</strong> 🎉
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Check if all words found
                    if len(st.session_state.found_words) == len(st.session_state.target_words):
                        st.balloons()
                        show_celebration()
                    
                    time.sleep(1)
                    st.rerun()
                else:
                    st.info(f"🔄 You already found '{user_word.upper()}'! Try another word.")
                    st.session_state.current_word = ''
                    time.sleep(1)
                    st.rerun()
            elif can_form_word(user_word, st.session_state.available_letters):
                st.warning(f"🤔 '{user_word.upper()}' can be formed but isn't a target word. Keep trying!")
            else:
                st.error(f"❌ Cannot form '{user_word.upper()}' with the available letters.")
    
    with col2:
        # Display found words
        display_found_words(st.session_state.found_words)
        
        # Remaining words counter
        remaining = len(st.session_state.target_words) - len(st.session_state.found_words)
        if remaining > 0:
            st.markdown(f"""
            <div class="game-container">
                <div style="text-align: center;">
                    <h3 style="color: #333;">🎯 Words Remaining</h3>
                    <div style="font-size: 3rem; color: #FF6B6B; font-weight: bold;">
                        {remaining}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Game completion section
    if len(st.session_state.found_words) == len(st.session_state.target_words):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎮 Play Again", type="primary", use_container_width=True):
                initialize_game()
                st.rerun()
    
    # Instructions (collapsible)
    with st.expander("📖 How to Play", expanded=False):
        st.markdown("""
        <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px;">
            <h4>🎯 Objective</h4>
            <p>Click letters to form words and find all target words!</p>
            
            <h4>🖱️ How to Play</h4>
            <ul>
                <li>🖱️ <strong>Click letters</strong> in the grid to add them to your word</li>
                <li>👀 Watch your word form in the display box</li>
                <li>✅ Click "Submit Word" when you're ready</li>
                <li>🗑️ Use "Clear Word" to start over</li>
                <li>🔄 Letters show remaining count (e.g., 2/3 means 2 left of 3 total)</li>
                <li>💡 Use hints when you're stuck</li>
            </ul>
            
            <h4>🌟 Difficulty Levels</h4>
            <ul>
                <li>🌱 <strong>Easy:</strong> 6 short words (2-4 letters)</li>
                <li>🌿 <strong>Medium:</strong> 5 medium words (4-6 letters)</li>
                <li>🌳 <strong>Hard:</strong> 4 longer words (5-7 letters)</li>
            </ul>
            
            <h4>💡 Pro Tips</h4>
            <ul>
                <li>🎯 Look for common word patterns</li>
                <li>🔄 Remember: you can use each letter multiple times if available</li>
                <li>📝 Try shorter words first, then longer combinations</li>
                <li>🖱️ The interface is fully interactive - no typing needed!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()