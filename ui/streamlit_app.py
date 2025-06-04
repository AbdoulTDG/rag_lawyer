import streamlit as st
import requests
import os

#Favicon
st.set_page_config(page_title="Assistant Juridique", page_icon="⚖️")
# API_URL = "http://rag-api:8000/ask"  # Modifie si tu déploies ailleurs
API_URL = os.getenv("API_URL", "http://rag-api:8000/ask")  # fallback pour local

st.title("💬 Chatbot RAG spécialisé")
#===============Version chat gpt BEGIN=======================================
# # 🟦 Initialisation de l'historique si absent
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # 🟦 Affichage de l'historique
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # 🟦 Saisie utilisateur
# if prompt := st.chat_input("Pose une question sur le domaine juridique..."):
#     if prompt.strip() == "":
#         st.warning("Merci de poser une vraie question.")
#         st.stop()  # ✅ Empêche appel API vide (corrige 422)
        
#     # Ajout message utilisateur
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # 🟦 Appel API
#     with st.chat_message("ai"):
#         with st.spinner("Recherche de réponse..."):
#             try:
#                 response = requests.post(API_URL, json={"question": prompt}, timeout=60)

#                 if response.status_code == 200:
#                     # ✅ Utilisation de st.empty() pour éviter les doublons
#                     result = response.json()["answer"]
#                     container = st.empty()
#                     container.markdown(result)
#                 else:
#                     result = f"❌ Erreur API : {response.status_code}"
#                     st.error(result)
#             except requests.RequestException as e:
#                 result = f"❌ Erreur API : {e}"
#                 st.error(result)

#         # ✅ Mise à jour historique après récupération
#         st.session_state.messages.append({"role": "assistant", "content": result})

# # 🟦 Réinitialisation conversation
# if st.button("🗑️ Effacer la conversation"):
#     st.session_state.messages = []
#     st.rerun()

#===============Version chat gpt END=======================================

#===============Version Axel BEGIN=======================================
# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# affichage historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input
if prompt := st.chat_input("Pose une question sur le domaine juridique..."):
    if prompt.strip() == "":
        st.warning("Merci de poser une vraie question.")
        st.stop()  # ✅ Empêche appel API vide (corrige 422)
        
    # Ajout message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
# if prompt := st.chat_input("Pose une question sur le RGPD..."):
#     with st.chat_message("user"):
#         # Gestion de l'erreur 442
#         if prompt.strip() == "":
#             st.warning("Merci de poser une vraie question.")
#             st.stop()
#         st.markdown(prompt)
#     # MAJ de l'historique
#     st.session_state.messages.append({"role": "user", "content": prompt})

    # RAG API
    with st.chat_message("ai"):
        # question = prompt
        with st.spinner("Recherche de réponse..."):
            try : 
                #=============old version BEGIN=========================================================
                # response = requests.post(API_URL, json={"question": prompt}, timeout=180)
                # if response.status_code == 200:
                #     #res = response.json().get("answer")["result"] 
                #     #result = f"Echo: {res}"
                #     #result = response.json().get("answer" , {}).get("result", "❓ Aucune réponse trouvée.")
                #     result = response.json()["answer"]
                #     #st.markdown(result)
                # else:
                #     result = f"❌ Erreur API : {response.status_code}"
                #=============old version END=========================================================
                # ✅ Correction : on active le stream de la réponse
                response = requests.post(API_URL, json={"question": prompt}, stream=True, timeout=180)

                if response.status_code == 200:
                    response_box = st.empty() # conteneur temporaire pour éviter les réponses multiples
                    result = ""
                    # ✅ Correction : lecture ligne par ligne du flux streamé
                    for line in response.iter_lines():
                        if line:
                            chunk = line.decode("utf-8")
                            result += chunk
                            #break
                            #mise à jour dynamique du conteneur
                            response_box.markdown(result + "▌")
                    response_box.markdown(result)  # Affichage final sans le curseur
                else:
                    result = f"❌ Erreur API : {response.status_code}"
                    st.markdown(result)
            except requests.RequestException as e:
                # st.error(f"Erreur lors de la récupération de la réponse:{response.status_code}")
                # st.markdown(response)
                result = f"❌ Erreur API : {e}"
                #Affichage reponse
                st.error(result)
        # MAJ historique
        st.session_state.messages.append({"role": "ai", "content": result})



#Renitialisation conversation
if st.button("🗑️ Effacer la conversation"):
    st.session_state.messages = []
    st.rerun()
#===============Version Axel END=======================================

# import streamlit as st
# import requests
# import os

# # API_URL = "http://rag-api:8000/ask"  # Modifie si tu déploies ailleurs
# API_URL = os.getenv("API_URL", "http://rag-api:8000/ask")  # fallback pour local

# # interface.py

# st.title("Assistant RGPD 🤖")

# question = st.text_input("Posez votre question sur le RGPD :")

# if st.button("Envoyer") and question:
#     with st.spinner("Réflexion en cours..."):
#         response = requests.post(
#             "http://rag-api:8000/ask",  # L'API FastAPI locale
#             json={"question": question}
#         )
#         if response.status_code == 200:
#             st.markdown("### 💬 Réponse")
#             st.write(response.json()["answer"])
#         else:
#             st.error("Erreur côté serveur.")



# # st.title("💬 Chatbot RAG spécialisé")
# # st.write("Pose une question sur ton domaine...")

# # question = st.text_input("Ta question :", placeholder="Ex: Quels sont les effets du changement climatique ?")

# # if st.button("Envoyer") and question:
# #     with st.spinner("Recherche de réponse..."):
# #         response = requests.post(API_URL, json={"question": question})
# #         if response.status_code == 200:
# #             st.success(response.json().get("answer"))
# #         else:
# #             st.error(f"Erreur lors de la récupération de la réponse:{response.status_code}")

# # # Zone de texte pour l'utilisateur
# # user_input = st.text_input("Posez votre question:")
# # # Affichage des réponses
# # if user_input:
# #     with st.spinner("Réflexion en cours..."):
# #         response = requests.post(
# #             "http://localhost:8000/ask",  # Ton endpoint FastAPI
# #             json={"question": user_input}
# #         )
# #         if response.status_code == 200:
# #             st.markdown("**Réponse :** " + response.json()["answer"])
# #         else:
# #             st.error("Erreur de l'API : " + response.text)