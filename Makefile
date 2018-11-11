install:
	@echo "Attempting to create GAE local datastore directory"
	[ -d ./data ] && echo "FYI: Dir Exists" || mkdir ./data

	pip install -Ur requirements_dev.txt
	pip install -Ur requirements.txt -t ./external
	@echo "Requirements installed."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

run:
	dev_appserver.py .  --enable_console --storage_path=./data/.search --datastore_path=./data/.datastore --enable_sendmail --port=8080

#deploy:
#	appcfg.py update -A blaine-garrett -V $(filter-out $@,$(MAKECMDGOALS)) ./app.yaml

deploy:
	gcloud --verbosity=debug --project blaine-garrett app deploy ./app.yaml --no-promote --version $(filter-out $@,$(MAKECMDGOALS))