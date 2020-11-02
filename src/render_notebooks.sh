NOTEBOOKS_FOLDER=$1
NOTEBOOKS_OUTPUT=$2

for f in $NOTEBOOKS_FOLDER/*
do
	filename=$(basename -- $f)
	filename="${filename%.*}"
	echo "jupytext --to $f --output $NOTEBOOKS_OUTPUT/$filename.ipynb"
	jupytext --to notebook $f --output $NOTEBOOKS_OUTPUT/$filename.ipynb
done
