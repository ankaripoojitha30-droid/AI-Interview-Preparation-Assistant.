
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🎯",
    layout="centered"
)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

st.title("🎯 AI Interview Preparation Assistant")
st.write(
    "Practice interview questions and receive AI-powered "
    "feedback to improve your interview skills."
)

if not api_key:
    st.error(
        "OpenAI API key not found. Add OPENAI_API_KEY "
        "to your .env file."
    )
    st.stop()

client = OpenAI(api_key=api_key)


def generate_question(role, experience, category):
    """Generate an interview question."""

    prompt = f"""
    Generate one interview question for a candidate.

    Job role: {role}
    Experience level: {experience}
    Interview category: {category}

    Return only the interview question.
    """

    response = client.responses.create(
        model="gpt-5.4",
        input=prompt
    )

    return response.output_text.strip()


def evaluate_answer(role, experience, category, question, answer):
    """Evaluate the candidate's answer."""

    prompt = f"""
    You are a professional interview coach.

    Candidate job role: {role}
    Experience level: {experience}
    Interview category: {category}

    Interview question:
    {question}

    Candidate answer:
    {answer}

    Evaluate the answer fairly, considering the candidate's
    experience level and the question being asked.

    Provide the response in this format:

    SCORE: [number out of 10]

    STRENGTHS:
    - List the strong points.

    AREAS FOR IMPROVEMENT:
    - Explain what could be improved.

    IMPROVED SAMPLE ANSWER:
    Provide a clear and effective sample answer.

    FOLLOW-UP QUESTION:
    Ask one relevant follow-up question.

    Do not invent candidate experience or qualifications.
    """

    response = client.responses.create(
        model="gpt-5.4",
        input=prompt
    )

    return response.output_text.strip()


# Sidebar settings
st.sidebar.header("Interview Settings")

role = st.sidebar.selectbox(
    "Select your job role",
    [
        "Python Developer",
        "Java Developer",
        "Web Developer",
        "Data Analyst",
        "Data Scientist",
        "Software Engineer",
        "AI/ML Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Other"
    ]
)

if role == "Other":
    role = st.sidebar.text_input("Enter your job role")

experience = st.sidebar.selectbox(
    "Experience level",
    [
        "Fresher",
        "0-2 years",
        "2-5 years",
        "5+ years"
    ]
)

category = st.sidebar.selectbox(
    "Interview category",
    [
        "Technical",
        "HR",
        "Behavioral",
        "Communication",
        "General"
    ]
)

st.sidebar.info(
    "Choose your job role and interview category "
    "before starting your practice."
)

# Store interview state
if "question" not in st.session_state:
    st.session_state.question = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "history" not in st.session_state:
    st.session_state.history = []

# Generate a question
st.subheader("Step 1: Get an Interview Question")

if st.button("Generate Interview Question", type="primary"):
    if not role.strip():
        st.warning("Please enter a job role.")
    else:
        try:
            with st.spinner("Generating your question..."):
                st.session_state.question = generate_question(
                    role, experience, category
                )
                st.session_state.feedback = ""
        except Exception as error:
            st.error(f"Could not generate question: {error}")

if st.session_state.question:
    st.info(st.session_state.question)

    # Answer input
    st.subheader("Step 2: Submit Your Answer")

    answer = st.text_area(
        "Type your interview answer below:",
        height=180,
        placeholder="Write your answer here..."
    )

    if st.button("Evaluate My Answer"):
        if not answer.strip():
            st.warning("Please enter an answer first.")
        else:
            try:
                with st.spinner("Evaluating your answer..."):
                    feedback = evaluate_answer(
                        role,
                        experience,
                        category,
                        st.session_state.question,
                        answer
                    )

                    st.session_state.feedback = feedback

                    st.session_state.history.append({
                        "question": st.session_state.question,
                        "answer": answer,
                        "feedback": feedback
                    })

            except Exception as error:
                st.error(f"Could not evaluate answer: {error}")

# Display feedback
if st.session_state.feedback:
    st.subheader("Step 3: Your Interview Feedback")
    st.markdown(st.session_state.feedback)

# Interview history
if st.session_state.history:
    st.divider()
    st.subheader("Interview Practice History")

    st.write(
        f"Questions answered: {len(st.session_state.history)}"
    )

    for index, item in enumerate(
        reversed(st.session_state.history), start=1
    ):
        with st.expander(f"Practice Session {index}"):
            st.markdown("**Question:**")
            st.write(item["question"])

            st.markdown("**Your Answer:**")
            st.write(item["answer"])

            st.markdown("**Feedback:**")
            st.markdown(item["feedback"])

    history_text = "\n\n".join(
        [
            f"Question: {item['question']}\n"
            f"Answer: {item['answer']}\n"
            f"Feedback: {item['feedback']}"
            for item in st.session_state.history
        ]
    )

    st.download_button(
        "Download Interview History",
        data=history_text,
        file_name="interview_history.txt",
        mime="text/plain"
    )

st.divider()

st.caption(
    "AI Interview Preparation Assistant | Practice, "
    "learn, and improve your interview skills."
)
