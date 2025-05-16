import streamlit as st
import requests
import os

# API_URL = "http://rag-api:8000/ask"  # Modifie si tu déploies ailleurs
API_URL = os.getenv("API_URL", "http://rag-api:8000/ask")  # fallback pour local

st.title("💬 Chatbot RAG spécialisé")
st.write("Pose une question sur ton domaine...")

question = st.text_input("Ta question :", placeholder="Ex: Quels sont les effets du changement climatique ?")

if st.button("Envoyer") and question:
    with st.spinner("Recherche de réponse..."):
        response = requests.post(API_URL, json={"question": question})
        if response.status_code == 200:
            st.success(response.json().get("answer"))
        else:
            st.error(f"Erreur lors de la récupération de la réponse:{response.status_code}")

# # Zone de texte pour l'utilisateur
# user_input = st.text_input("Posez votre question:")
# # Affichage des réponses
# if user_input:
#     with st.spinner("Réflexion en cours..."):
#         response = requests.post(
#             "http://localhost:8000/ask",  # Ton endpoint FastAPI
#             json={"question": user_input}
#         )
#         if response.status_code == 200:
#             st.markdown("**Réponse :** " + response.json()["answer"])
#         else:
#             st.error("Erreur de l'API : " + response.text)