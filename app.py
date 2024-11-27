import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# App Title
st.title("📊 Religiousness Assessment Tool with Advanced Insights")
st.write("""
Welcome to the Religiousness Assessment Tool! This app evaluates your religiousness across four dimensions:
- **Physicality:** Your connection to rituals, symbols, and spaces.
- **Scientific:** How science aligns with your beliefs.
- **Psychological:** The role of introspection and emotions.
- **Spiritual:** Your connection to the unknown and greater forces.

Answer the questions, and we’ll provide insights and advanced feedback based on your responses.
""")

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Choose a section", ["Introduction", "Take the Assessment", "Your Results", "Advanced Insights"])

# Introduction Section
if section == "Introduction":
    st.header("📝 About This Assessment")
    st.write("""
    This tool combines introspection and technology to provide insights into your religiousness profile. 
    Answer all the questions to receive personalized and data-driven feedback.
    """)

# Questionnaire
if section == "Take the Assessment":
    st.header("📝 Take the Assessment")

    # All 33 Questions grouped by dimensions
    questions = {
        "Physicality": [
            "I find that physical rituals (e.g., prayer, fasting) make me feel connected to my beliefs.",
            "Attending religious or spiritual gatherings in person is essential to my practice.",
            "Physical symbols (e.g., icons, sacred objects) hold deep significance for me.",
            "I feel most connected to my beliefs when I engage in physical expressions like dancing or singing.",
            "My spiritual experiences are most meaningful when they are physically grounded."
        ],
        "Psychological": [
            "I rely on self-reflection or introspection to navigate emotions and actions.",
            "My beliefs are closely tied to understanding my mind and emotions.",
            "I align my beliefs with my emotional and mental well-being.",
            "I often look for meaning within my thoughts and experiences.",
            "My beliefs help me process my psychological states."
        ],
        "Scientific": [
            "I seek scientific explanations for phenomena in my spiritual beliefs.",
            "I value scientific advancements that challenge or align with my faith.",
            "Empirical evidence is important in shaping my worldview.",
            "I think science and religion should coexist harmoniously.",
            "I question religious teachings that conflict with scientific understanding."
        ],
        "Spiritual": [
            "I often feel connected to something greater than myself.",
            "I value mystical experiences and a deep spiritual connection.",
            "Spirituality for me is about surrendering to the unknown.",
            "I feel drawn inward, exploring depths beyond conscious understanding.",
            "I embrace spiritual experiences that challenge my understanding."
        ]
    }

    # Initialize scores
    scores = {dimension: 0 for dimension in questions.keys()}
    max_score = len(questions["Physicality"]) * 5  # 5-point scale per question

    # Display questions by dimension
    for dimension, q_list in questions.items():
        st.subheader(dimension)
        for q in q_list:
            scores[dimension] += st.slider(q, 1, 5, 3)

    # Save scores for the Results section
    st.session_state.scores = scores

# Results Section
if section == "Your Results":
    if "scores" in st.session_state:
        st.header("📊 Your Results")
        scores = st.session_state.scores
        total_scores = sum(scores.values())
        
        # Calculate percentages
        results = {k: (v / total_scores) * 100 for k, v in scores.items()}
        
        # Display results
        for dimension, percentage in results.items():
            st.write(f"**{dimension}:** {percentage:.2f}%")
        
        # Feedback
        st.subheader("Feedback")
        for dimension, percentage in results.items():
            if percentage > 50:
                st.write(f"🌟 **{dimension}**: You are highly attuned to this dimension.")
            elif 30 <= percentage <= 50:
                st.write(f"⚖️ **{dimension}**: You show a balanced approach to this dimension.")
            else:
                st.write(f"🌀 **{dimension}**: This dimension may not play a central role in your beliefs.")

        # Visualization
        st.subheader("Visual Representation")
        st.bar_chart(pd.DataFrame(results, index=["Score Percentage"]))
    else:
        st.write("Please complete the assessment first.")

# Advanced Insights Section
if section == "Advanced Insights":
    st.header("📈 Advanced Insights")
    st.write("Using machine learning, we analyze patterns to give you deeper insights into your religiousness profile.")

    # Simulated dataset (replace with actual data in production)
    data = pd.DataFrame({
        "Physicality": np.random.randint(10, 26, 100),
        "Psychological": np.random.randint(10, 26, 100),
        "Scientific": np.random.randint(10, 26, 100),
        "Spiritual": np.random.randint(10, 26, 100),
        "Category": np.random.choice(["Balanced", "Spiritual Focused", "Scientific Skeptic"], 100)
    })

    # Train a model
    X = data[["Physicality", "Psychological", "Scientific", "Spiritual"]]
    y = data["Category"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Predict user's category
    if "scores" in st.session_state:
        user_data = pd.DataFrame([st.session_state.scores])
        category = model.predict(user_data)[0]
        st.write(f"**Predicted Category:** {category}")
    else:
        st.write("Complete the assessment first to get advanced insights.")


