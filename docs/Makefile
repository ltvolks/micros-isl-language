# Build the ISL docs:  make html   (needs: pip install -r requirements-docs.txt)
SPHINXBUILD ?= sphinx-build
PYTHON      ?= python3
BUILDDIR    = _build

.PHONY: html clean linkcheck

html:
	$(SPHINXBUILD) -W --keep-going -b html . $(BUILDDIR)/html
	open $(BUILDDIR)/html/index.html

linkcheck:
	$(SPHINXBUILD) -b linkcheck . $(BUILDDIR)/linkcheck

clean:
	rm -rf $(BUILDDIR)
