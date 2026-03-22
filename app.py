import streamlit as st
import pandas as pd
import plotly.express as px

# ================== LOAD DATA ==================
df = pd.read_csv("data/placement_data.csv")

# ================== READINESS SCORE ==================
df["Score"] = (df["CGPA"] * 10) + (df["Aptitude"] * 2) + (df["Internship"] * 15)

def categorize(score):
    if score >= 80:
        return "Ready"
    elif score >= 50:
        return "Moderate"
    else:
        return "Needs Improvement"

df["Category"] = df["Score"].apply(categorize)

# ================== TITLE ==================
st.title("🎓 Smart Placement Analytics System")

# ================== TABS ==================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 Prediction", "📈 Insights"])

# =========================================================
# ================== 📊 DASHBOARD TAB ==================
# =========================================================
with tab1:

    st.subheader("🎯 Select Branch")

    selected_branch = st.selectbox("Choose Branch", df["Branch"].unique())

    filtered_df = df[df["Branch"] == selected_branch]

    st.subheader("🧠 Filter by Skill")

    selected_skill = st.selectbox("Choose Skill", ["All"] + list(filtered_df["Skills"].unique()))

    if selected_skill != "All":
        filtered_df = filtered_df[filtered_df["Skills"] == selected_skill]

    # Metrics
    total_students = len(filtered_df)
    placed_students = filtered_df['Placed'].sum()
    placement_rate = (placed_students / total_students) * 100 if total_students > 0 else 0
    avg_salary = filtered_df[filtered_df['Placed'] == 1]['Salary'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("👨‍🎓 Students", total_students)
    col2.metric("📊 Placement %", f"{placement_rate:.2f}%")
    col3.metric("💰 Avg Salary", f"₹{avg_salary:,.0f}" if pd.notnull(avg_salary) else "₹0")

    # Readiness
    st.subheader("🎯 Readiness Distribution")
    fig0 = px.pie(filtered_df, names="Category")
    st.plotly_chart(fig0)

    # Placement Distribution
    placement_counts = filtered_df['Placed'].value_counts().reset_index()
    placement_counts.columns = ["Status", "Count"]
    placement_counts["Status"] = placement_counts["Status"].map({1: "Placed", 0: "Not Placed"})

    fig_pie = px.pie(placement_counts, names="Status", values="Count",
                     title=f"Placement Distribution - {selected_branch}")
    st.plotly_chart(fig_pie)

    # Skills Analysis
    st.subheader("💡 Skills vs Placement")
    skill_group = filtered_df.groupby("Skills")["Placed"].mean().reset_index()
    skill_group["Placed"] *= 100

    fig3 = px.bar(skill_group, x="Skills", y="Placed")
    st.plotly_chart(fig3)

    # Salary Insights
    st.subheader("💰 Salary Insights")
    fig4 = px.histogram(filtered_df[filtered_df['Placed']==1], x="Salary")
    st.plotly_chart(fig4)

    st.write("### 🏢 Top Hiring Companies")
    st.write(filtered_df[filtered_df['Placed']==1]["Company"].value_counts().head(5))


# =========================================================
# ================== 🤖 PREDICTION TAB ==================
# =========================================================
with tab2:

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score

    st.subheader("🤖 Placement Prediction Model")

    X = df[["CGPA", "Aptitude", "Internship"]]
    y = df["Placed"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)

    st.write(f"Model Accuracy: {acc:.2f}")

    # User Input
    st.subheader("🎯 Check Your Placement Chances")

    cgpa = st.number_input("Enter CGPA", 0.0, 10.0)
    aptitude = st.number_input("Enter Aptitude Score", 0, 100)
    intern = st.selectbox("Internship", [0, 1])

    if st.button("Predict"):
        result = model.predict([[cgpa, aptitude, intern]])

        if result[0] == 1:
            st.success("You can get placed ✅")
        else:
            st.error("You need improvement ❌")

            suggestions = []

            if aptitude < 60:
                st.warning("⚠️ Low aptitude score.")
                suggestions.append("Improve aptitude (>60)")

            if cgpa < 7:
                st.warning("⚠️ Low CGPA.")
                suggestions.append("Increase CGPA (>7)")

            if intern == 0:
                st.warning("⚠️ No internship experience.")
                suggestions.append("Do at least 1 internship")

            if suggestions:
                st.info("💡 Suggestions: " + ", ".join(suggestions))


# =========================================================
# ================== 📈 INSIGHTS TAB ==================
# =========================================================
with tab3:

    st.subheader("📈 Smart Insights")

    highest_branch = df.groupby("Branch")["Placed"].mean().idxmax()
    st.success(f"🏆 Highest placement branch: {highest_branch}")

    best_skill = df.groupby("Skills")["Placed"].mean().idxmax()
    st.success(f"🔥 Most valuable skill: {best_skill}")

    avg_cgpa = df[df["Placed"] == 1]["CGPA"].mean()
    st.info(f"📊 Avg CGPA of placed students: {avg_cgpa:.2f}")

    avg_aptitude = df[df["Placed"] == 1]["Aptitude"].mean()
    st.info(f"🧠 Avg Aptitude of placed students: {avg_aptitude:.2f}")