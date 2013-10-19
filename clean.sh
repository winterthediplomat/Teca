function cleanFolder {
  for dir in $(find . -mindepth 1 -type d | grep -v .git); do
    echo "going into $dir"
    #cd $dir;
    rm $dir/index.html;
    #cleanFolder;
  done
}

cleanFolder
