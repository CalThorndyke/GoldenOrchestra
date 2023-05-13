venv:
	python3 -m venv .venv

requirements:
	.venv/bin/pip install -r requirements.txt

freeze:
	.venv/bin/pip freeze > requirements.txt

install: venv requirements
	envsubst < golden-orchestra.service > /etc/systemd/system/golden-orchestra.service
	systemctl start golden-orchestra
	systemctl enable golden-orchestra

