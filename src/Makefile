gitbook:
	cp ../docs/CNAME . || echo "" 
	Rscript _render.R "bookdown::gitbook"
	rm -rf ../docs 
	mv _book ../docs 
	mv CNAME ../docs || echo ""
all:
	Rscript --quiet _render.R
