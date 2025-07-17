from sklearn.metrics.pairwise import cosine_similarity

def recommend_top_n_courses(user_skills, df_courses, vectorizer, top_n=5):
    """
    Recommend top_n courses based on user skills list.
    Returns top_n courses with similarity scores.
    """
    if not user_skills:
        raise ValueError("User skill list cannot be empty")

    # Preprocess user input similarly as training (lowercase, etc.) if needed
    query = ' '.join(user_skills).lower()

    # Vectorize query and course skills
    query_vec = vectorizer.transform([query])
    course_vecs = vectorizer.transform(df_courses["skills_text"])

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(query_vec, course_vecs).flatten()

    # Get top N indices
    top_indices = similarity_scores.argsort()[::-1][:top_n]

    # Prepare and return recommendations with scores
    recommendations = df_courses.iloc[top_indices][["Title", "Skills", "Level", "URL"]].copy()
    recommendations["Similarity Score"] = similarity_scores[top_indices]

    return recommendations.reset_index(drop=True)
