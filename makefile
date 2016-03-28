all: help

help:
	@echo "Usage:"
	@echo "\tmake <cmd> <options>"
	@echo ""
	@echo "Command list:"
	@echo "\tmakemsg lang=__LANG__\t\tCreate or update the PO file using the given language"
	@echo "\tcompilemsg lang=__LANG__\tCompile the PO file to MO file using the given language"
	@echo "\tscss\t\t\t\tCompile and minify the SASS "
	@echo "\twatch-scss\t\t\tWatch the +NEW+ SASS project"
	@echo ""

makemsg:
	@echo "Generating the PO file..."
	python manage.py makemessages -l $(lang) --no-wrap --no-location --no-obsolete
	@echo "Done!"
	@echo ""

compilemsg:
	@echo "Compiling the PO file..."
	python manage.py compilemessages -l $(lang)
	@echo "Done!"
	@echo ""

scss:
	@echo "Compiling and minifying the NEW SASS project..."
	sass --update core/static/sass/main.scss:core/static/css/main.css \
		--unix-newline --style compressed --sourcemap=none --force --no-cache
	@echo "Done!"
	@echo ""


watch-scss:
	@echo "Watching SCSS..."
	sass --watch core/static/sass/main.scss:core/static/css/main.css \
		--unix-newline --style compressed --sourcemap=none --no-cache

compass:
	@echo "Compiling scss into css and creating sprite sheets..."
	compass compile --sass-dir core/static/sass/ --css-dir core/static/css/ --force --images-dir core/static/sass/
	@echo "Done!"
	@echo ""

coverage:
	coverage run manage.py test && coverage html