# Build the ISL docs:  make html   (needs: pip install -r requirements-docs.txt)
SPHINXBUILD ?= sphinx-build
PYTHON      ?= python3
BUILDDIR    = _build

.PHONY: html clean generate linkcheck

generate:
	$(PYTHON) build_rst.py

html: generate
	$(SPHINXBUILD) -W --keep-going -b html . $(BUILDDIR)/html

linkcheck: generate
	$(SPHINXBUILD) -b linkcheck . $(BUILDDIR)/linkcheck

clean:
	rm -rf $(BUILDDIR) _generated
