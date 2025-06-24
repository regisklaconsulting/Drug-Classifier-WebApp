install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black -v app 
		
update-branch:
	git config --global user.name $(USER_NAME)
	git config --global user.email $(USER_EMAIL)
	git commit -am "Update with new results" || true
	git push --force origin $(SOURCE_BRANCH):$(TARGET_BRANCH)
	
hf-pull-login: 
	pip install -U "huggingface_hub[cli]"
	git pull origin $(TARGET_BRANCH)
	git switch $(TARGET_BRANCH)
	huggingface-cli login --token $(HF_TOKEN) --add-to-git-credential

hf-push: 
	huggingface-cli upload $(HF_REPO_ID) $(LOCAL_PATH) --repo-type=space --commit-message="Sync web app files"

deploy: hf-pull-login hf-push

all: install format update-branch deploy
