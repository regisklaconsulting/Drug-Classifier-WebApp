format:	
	black -v app 
		
hf-login: 
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF_TOKEN) --add-to-git-credential

hf-push-model: 
	huggingface-cli upload $(HF_REPO_ID) $(MODEL_LOCAL_PATH) $(MODEL_REMOTE_PATH) --repo-type=space --commit-message="Sync model prediction pipeline"
	
deploy: hf-login hf-push-model

all: format deploy
