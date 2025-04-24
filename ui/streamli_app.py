import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"  # Modifie si tu déploies ailleurs

st.title("💬 Chatbot RAG spécialisé")
st.write("Pose une question sur ton domaine...")

question = st.text_input("Ta question :", placeholder="Ex: Quels sont les effets du changement climatique ?")

if st.button("Envoyer") and question:
    with st.spinner("Recherche de réponse..."):
        response = requests.post(API_URL, json={"question": question})
        if response.status_code == 200:
            st.success(response.json().get("answer"))
        else:
            st.error("Erreur lors de la récupération de la réponse.")
