OUTPUT := results.json
PYTHON_FILE := main.py

all: clean $(OUTPUT)

clean: 
	@echo "Cleaning files..."
	rm -rf $(OUTPUT)

$(OUTPUT): $(PYTHON_FILE)
	@echo "Getting data from nvidia..."
	uv run scrapy runspider $(PYTHON_FILE) -o $(OUTPUT)
