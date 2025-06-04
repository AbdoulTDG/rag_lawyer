## Resumé
Ce projet porte sur l'implémentation d'un RAG (retrieval augmented generation, génération augmentée de récupération) à partir d'un modèle d'IA existant.
Le RAG porte uniquement sur les données juridique, plus précisement sur la RGPD européeenne (règlement général de protection des données).
Les technologies utilisées sont : python, docker, qdrant, streamlit, FastAPI.

## Exécution
Une fois le repo git récupérer, veuillez suivre les étapes suivantes en vous plaçant dans le répertoire rag_lawyer/

1. Vectoriser les données avec qdrant  
Objectif : récupérer les données de la base mongoDB et les vectoriser à partir du script ask_rag.py  
1.1. Lancer le service qdrant uniquement en exécutant la commande suivante : *__docker-compose up --build qdrant__*  
1.2. Installer la librairie qdrant_client : *__pip install qdrant_client__*  
1.3. Exéuter le script *__ask_rag.py__*  

2. Utiliser le modèle  
Objectif : démarrer l'ensemble des service pour utiliser le modèle  
2.2. Toujours dans le répertoire rag_lawyer/, démarrer tous les services en exécutant la commande suivante : *__docker-compose up --build__*  
2.3. Accéder à l'UI via le lien suivant : __http://0.0.0.0:8051__ ou (http://localhost:8501/)  


## Organisation du répertoire

  	rag_lawyer/
	├── app/
	│   ├── main.py              # API FastAPI
	│   ├── rag_chain.py         # Logique RAG
 	│   └── ask_rag.py           # qdrant : vectorisation des données
  	├── ui/
	│   ├── dockerfile           # Conteneurisation de l'UI streamlit
	│   ├── requirements.txt     # Liste des librairies utilisées par l'UI
	│   └── streamlit_app.py     # Chat bot : UI streamlit
 	│   └── ask_rag.py  
	├── requirements.txt         # Liste des librairies utilisées par l'API
	├── dockerfile		     # Conteneurisation des l'API
 	├── docker-compose.yml	     # Gestionnaire des services : qdrant, ollama, rag-api, rag-ui.
	└── .env		     # Variables d'env


## Architecture du modèle

     	[ MongoDB ]  --> base documentaire contenant les données brutes
	              |
	              |     (1. Extraction)
	              v
	    [ Documents bruts (texte) ]
	              |
	              |     (2. Split + Embedding)
	              v
	[ Vectorstore QDRANT (vecteurs + chunks) ]
	              ^
	              |
	              |     (3. Similarité sémantique)
	       	      |
	    [ Question utilisateur ] --> UI streamlit
	              |
	              v
	[ Récupération des top-k chunks ]
	              |
	              |     (4. Construction du prompt)
	              v
	   [ LLM (ex: Mistral) ]
	              |
	              v
        [ Réponse générée ]
