.PHONY: test install run clean

test:
	python3 -m unittest discover tests

install:
	pip install -r requirements.txt

run:
	python3 task.py

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
