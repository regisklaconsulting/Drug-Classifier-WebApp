install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black -v app 
		
update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results"
	git push --force origin $(SOURCE_BRANCH):$(TARGET_BRANCH)
	
hf-login: 
	pip install -U "huggingface_hub[cli]"
	git pull origin $(TARGET_BRANCH)
	git switch $(TARGET_BRANCH)
	huggingface-cli login --token $(HF) --add-to-git-credential

push-hub: 
	huggingface-cli upload kingabzpro/Drug-Classification ./App --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload kingabzpro/Drug-Classification ./Model /Model --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload kingabzpro/Drug-Classification ./Results /Metrics --repo-type=space --commit-message="Sync Model"

deploy: hf-login push-hub

all: install format train eval update-branch deploy