import streamlit as st
from core import SuperAgent 

# Configuration de la page
st.set_page_config(page_title="DataMirror", page_icon="🔍")  

# Initialisation du SuperAgent
super_agent = SuperAgent()

# Barre latérale
with st.sidebar:
    reset_button_key = "reset_button"
    reset_button = st.button("Reset Session", key=reset_button_key)
    if reset_button:
        st.session_state.conversation = None
        st.session_state.chat_history = None

    st.image('assets/img/logo.jpg', width=200)
    st.caption("🔍 Bienvenue sur DataMirror, votre miroir numérique !")

# Initialiser l'état de la session pour conserver l'historique des messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "En quoi pouvons-nous vous aider à explorer vos données sur Internet ?"}]

# Affichage des messages précédents
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Gestion de l'input utilisateur
if prompt := st.chat_input("Entrez votre requête ici :"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Afficher un spinner pendant que le SuperAgent traite la requête
    with st.spinner('Recherche en cours...'):
        response = super_agent.handle_query(prompt)

    # Récupération et affichage de la réponse
    msg = response.get('final_result', "Désolé, je n'ai pas pu trouver d'informations pertinentes.")
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    with st.spinner('Affichage des résultats...'):
        st.chat_message("assistant").write(msg)