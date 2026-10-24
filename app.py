import streamlit as st
import ai_engine

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="StudyBuddy AI - Learning & Research Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .status-live {
        background-color: #DEF7EC;
        color: #03543F;
        border: 1px solid #BCF0DA;
    }
    .status-demo {
        background-color: #FEF08A;
        color: #854D0E;
        border: 1px solid #FDE047;
    }
    .quiz-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# SIDEBAR CONFIGURATION
# ==============================================================================
with st.sidebar:
    st.title("⚙️ AI Control Center")
    st.caption("Configure your model settings and API keys here.")

    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        help="Get a free key at https://aistudio.google.com/app/apikey. If blank, app runs in Demo Mode.",
        placeholder="Paste AI Studio key here..."
    )

    # Status Pill
    if api_key:
        st.markdown('<div class="status-badge status-live">🟢 Live API Mode</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-demo">🟡 Educational Demo Mode</div>', unsafe_allow_html=True)
        st.info("💡 **Demo Mode Active:** The app uses built-in smart mock data so you can test all features immediately without needing an API key.")

    with st.expander("🔑 How to get a free API Key"):
        st.markdown("""
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
        2. Sign in with your Google account.
        3. Click **'Create API Key'**.
        4. Paste it in the field above! (It's 100% free with generous rate limits).
        """)

    st.divider()

    st.subheader("Model Parameters")
    model_name = st.selectbox(
        "Select Model",
        options=["gemini-3.8-flash", "gemini-3.8-pro", "gemini-3.8-flash-lite"],
        index=0,
        help="Gemini 3.8 Flash is fast and responsive; Pro is best for complex multi-step reasoning."
    )

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="0.0 = Deterministic & exact; 1.0 = Highly imaginative & varied."
    )

    st.divider()
    st.caption("Built for AI Beginners • Clean Python Architecture")


# ==============================================================================
# MAIN PAGE HEADER
# ==============================================================================
st.markdown('<div class="main-header">🧠 StudyBuddy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your intelligent assistant for conversational learning, document research, and automated quizzing.</div>', unsafe_allow_html=True)

# Tabs
tab_chat, tab_docs, tab_quiz = st.tabs([
    "💬 AI Tutor Chat",
    "📄 Document Q&A & Research",
    "🎯 Interactive Quiz Generator"
])


# ==============================================================================
# TAB 1: CONVERSATIONAL TUTOR
# ==============================================================================
with tab_chat:
    st.subheader("Interactive Learning Companion")

    # Persona Selection
    persona_choice = st.selectbox(
        "Choose AI Persona / Teaching Style:",
        options=[
            "Patient Tutor (Friendly, step-by-step guidance)",
            "Python Coding Mentor (Clean code snippets & best practices)",
            "ELI5 Explainer (Explains complex AI ideas with simple real-world analogies)",
            "Socratic Coach (Guides with questions to sharpen your reasoning)"
        ]
    )

    # Map persona to system prompt
    persona_prompts = {
        "Patient Tutor (Friendly, step-by-step guidance)":
            "You are a warm, encouraging, and patient tutor. Explain things clearly step by step, using bullet points and examples.",
        "Python Coding Mentor (Clean code snippets & best practices)":
            "You are an expert Python and AI software engineer. Provide clean, readable, well-commented code snippets and explain how they work.",
        "ELI5 Explainer (Explains complex AI ideas with simple real-world analogies)":
            "You explain complex computer science and AI concepts as if speaking to a 10-year-old. Use vivid everyday analogies (like cooking, Lego, or bicycles).",
        "Socratic Coach (Guides with questions to sharpen your reasoning)":
            "You are a Socratic tutor. Instead of just giving the answer directly, ask thoughtful questions that guide the user to discover the solution."
    }
    active_system_prompt = persona_prompts[persona_choice]

    # Initialize chat history in Streamlit session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hello! I'm your AI study partner. What topic or concept would you like to explore today?"}
        ]

    # Quick action to clear history
    col_clear, _ = st.columns([1, 5])
    with col_clear:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Chat reset! What would you like to explore?"}
            ]
            st.rerun()

    # Render previous messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat user input
    user_input = st.chat_input("Ask a question (e.g. 'How does backpropagation work?' or 'Explain lists vs dicts in Python')...")
    if user_input:
        # Display user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response from AI engine
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_text = ai_engine.chat_with_ai(
                    history=st.session_state.chat_messages,
                    system_instruction=active_system_prompt,
                    api_key=api_key,
                    model_name=model_name,
                    temperature=temperature
                )
                st.markdown(response_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})


# ==============================================================================
# TAB 2: DOCUMENT Q&A & RESEARCH (Mini-RAG)
# ==============================================================================
with tab_docs:
    st.subheader("Document Analysis & Grounded Q&A")
    st.write("Feed documents, lecture notes, or articles to the AI and extract insights strictly grounded in the text.")

    # Option to load sample text
    sample_text = """ARTIFICIAL INTELLIGENCE & MACHINE LEARNING CHEAT SHEET
1. Tokens:
   Language models do not process text letter-by-letter or word-by-word. Instead, text is broken into sub-word chunks called 'tokens'. For example, 1,000 tokens is roughly 750 English words.

2. Temperature:
   Temperature is a hyperparameter between 0.0 and 2.0 that controls randomness. A temperature of 0.0 makes the model choose the single most likely token every time (deterministic, ideal for math and coding). A temperature around 0.7 introduces variability suitable for creative writing.

3. Embeddings:
   An embedding is a vector (a list of floating-point numbers) representing the semantic meaning of a piece of text. Texts with similar meanings have high vector similarity (e.g. measured via cosine similarity).

4. Retrieval-Augmented Generation (RAG):
   RAG prevents hallucinations by first searching an external database or document for relevant excerpts and then injecting those excerpts into the prompt as factual reference material.
"""

    col_btn1, col_btn2 = st.columns([2, 5])
    with col_btn1:
        load_sample = st.button("📋 Load Sample AI Notes")

    # Document text box
    default_content = sample_text if load_sample else ""
    doc_content = st.text_area(
        "Paste your study notes or document text below:",
        value=default_content,
        height=200,
        placeholder="Paste text here or click 'Load Sample AI Notes' above..."
    )

    st.markdown("#### Choose an Analysis Task:")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        summarize_btn = st.button("📝 3-Bullet Summary")
    with action_col2:
        takeaways_btn = st.button("💡 Key Takeaways")
    with action_col3:
        faq_btn = st.button("❓ Generate FAQ")

    custom_question = st.text_input("Or ask a specific question about the document:", placeholder="e.g. What is the difference between high and low temperature?")
    ask_btn = st.button("🔍 Answer Question")

    # Process action
    chosen_task = None
    if summarize_btn:
        chosen_task = "Summarize this document in 3 concise, high-impact bullet points."
    elif takeaways_btn:
        chosen_task = "Extract the top 5 key takeaways or definitions from this text."
    elif faq_btn:
        chosen_task = "Generate 3 frequently asked questions and their answers based strictly on this text."
    elif ask_btn and custom_question.strip():
        chosen_task = custom_question.strip()

    if chosen_task:
        if not doc_content.strip():
            st.warning("⚠️ Please paste some text into the box above or click 'Load Sample AI Notes' first!")
        else:
            with st.spinner("Analyzing document..."):
                analysis_result = ai_engine.analyze_document(
                    document_text=doc_content,
                    question_or_task=chosen_task,
                    api_key=api_key,
                    model_name=model_name
                )
                st.markdown("### 📊 Results")
                st.info(analysis_result)


# ==============================================================================
# TAB 3: INTERACTIVE QUIZ GENERATOR
# ==============================================================================
with tab_quiz:
    st.subheader("Interactive Knowledge Check")
    st.write("Generate interactive multiple-choice questions on any subject to test your understanding.")

    quiz_topic = st.text_input(
        "Enter a topic or skill you are studying:",
        value="Foundations of Machine Learning & LLMs"
    )

    num_q = st.slider("Number of questions:", min_value=1, max_value=5, value=3)

    if st.button("🚀 Generate Quiz"):
        with st.spinner("Drafting questions and answer choices..."):
            quiz_data = ai_engine.generate_quiz(
                topic_or_notes=quiz_topic,
                num_questions=num_q,
                api_key=api_key,
                model_name=model_name
            )
            st.session_state.current_quiz = quiz_data
            st.session_state.quiz_submitted = False

    # Render quiz if generated
    if "current_quiz" in st.session_state and st.session_state.current_quiz:
        st.markdown("---")
        user_answers = {}

        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.current_quiz):
                st.markdown(f"**Question {i+1}: {q['question']}**")
                user_answers[i] = st.radio(
                    f"Select your answer for Q{i+1}:",
                    options=list(range(len(q["options"]))),
                    format_func=lambda idx, opts=q["options"]: opts[idx],
                    key=f"q_{i}"
                )
                st.write("")

            submitted = st.form_submit_button("✅ Submit Answers")

        if submitted:
            score = 0
            total = len(st.session_state.current_quiz)

            st.markdown("### 📝 Score Report")
            for i, q in enumerate(st.session_state.current_quiz):
                correct = q["correct_index"]
                user_choice = user_answers[i]
                if user_choice == correct:
                    score += 1
                    st.success(f"**Q{i+1}: Correct!** 🎉\n\n*Explanation:* {q.get('explanation', '')}")
                else:
                    st.error(f"**Q{i+1}: Incorrect.** Correct answer: **{q['options'][correct]}**\n\n*Explanation:* {q.get('explanation', '')}")

            percentage = int((score / total) * 100)
            if percentage >= 70:
                st.balloons()
                st.success(f"### Final Score: {score} / {total} ({percentage}%) - Great job!")
            else:
                st.warning(f"### Final Score: {score} / {total} ({percentage}%) - Keep reviewing!")
