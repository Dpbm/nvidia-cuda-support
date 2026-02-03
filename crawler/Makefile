OUTPUT_SCRAPY := results.json
OUTPUT_BOARDS_INFO := drivers_boards_data.json
SCRAPY_PYTHON_FILE := main.py
BOARDS_PYTHON_FILE := get-boards-info.py

all: clean $(OUTPUT_SCRAPY) $(OUTPUT_BOARDS_INFO)

clean: 
	@echo "Cleaning files..."
	rm -rf $(OUTPUT) $(OUTPUT_BOARDS_INFO)

$(OUTPUT_SCRAPY): $(SCRAPY_PYTHON_FILE)
	@echo "Getting compute capability data from nvidia..."
	uv run scrapy runspider $(SCRAPY_PYTHON_FILE) -o $(SCRAPY_OUTPUT)

$(OUTPUT_BOARDS_INFO): $(BOARDS_PYTHON_FILE)
	@echo "Getting boards data from nvidia ..."
	uv run python $(BOARD_PYTHON_FILE)
