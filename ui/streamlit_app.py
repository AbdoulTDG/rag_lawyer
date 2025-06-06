import streamlit as st
import requests
import os

#Favicon
st.set_page_config(page_title="Assistant Juridique", page_icon="⚖️")

API_URL = os.getenv("API_URL", "http://rag-api:8000/ask")  # fallback pour local

st.title("💬 Chatbot RAG spécialisé en RGPD")


# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# affichage historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Pose une question sur le RGPD"):
    if prompt.strip() == "":
        st.warning("Merci de poser une vraie question.")
        st.stop()  # Empêche appel API vide (corrige 422)
        
    # Ajout message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG API
    with st.chat_message("ai"):
        with st.spinner("Recherche de réponse..."):
            try : 
                
                # Activation du stream de la réponse
                response = requests.post(API_URL, json={"question": prompt}, stream=True, timeout=180)

                if response.status_code == 200:
                    response_box = st.empty() # conteneur temporaire pour éviter les réponses multiples
                    result = ""
                    # Lecture ligne par ligne du flux streamé
                    for line in response.iter_lines():
                        if line:
                            chunk = line.decode("utf-8")
                            result += chunk
                            #mise à jour dynamique du conteneur
                            response_box.markdown(result + "▌")
                    response_box.markdown(result)  # Affichage final sans le curseur
                else:
                    result = f"Erreur API : {response.status_code}"
                    st.markdown(result)
            except requests.RequestException as e:
                result = f"Erreur API : {e}"
                #Affichage reponse
                st.error(result)
        # MAJ historique
        st.session_state.messages.append({"role": "ai", "content": result})



#Renitialisation conversation
if st.button("Effacer la conversation"):
    st.session_state.messages = []
    st.rerun()