 	rag_lawyer/
	├── app/
	│   ├── main.py              # API FastAPI
	│   ├── rag_chain.py         # Logique RAG
	│   └── config.py            # Variables d'env
	├── requirements.txt
	├── Dockerfile
	└── .env


     		[ MongoDB ]
	              |
	              |     (1. Extraction)
	              v
	    [ Documents bruts (texte) ]
	              |
	              |     (2. Split + Embedding)
	              v
	      [ Vectorstore FAISS (vecteurs + chunks) ]
	              ^
	              |
	              |     (3. Similarité sémantique)
	    [ Question utilisateur ]
	              |
	              v
	       [ Récupération des top-k chunks ]
	              |
	              |     (4. Construction du prompt)
	              v
	        [ LLM (ex: GPT, Mistral) ]
	              |
	              v
         [ Réponse générée ]![image](https://github.com/user-attachments/assets/3b5248e9-5e42-4d73-8e9b-0862e0325cf1)
