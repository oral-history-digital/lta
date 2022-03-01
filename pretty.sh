for i in *.xml
do
  xmllint --format "$i" > pretty/"$i"
done

