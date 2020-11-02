NOTEBOOKS_FOLDER=$1
NOTEBOOKS_OUTPUT=$2

for f in $NOTEBOOKS_FOLDER/*
do
	echo "pweave -f notebook ${f}"
	pweave -f notebook ${f}
done
