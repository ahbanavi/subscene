source_dir="./Subscene V2/Subscene Files DB"
destination_dir="./fa-subs"
keyword="farsi_persian"

find "$source_dir" -type f -name "*$keyword*" -exec cp --parents {} "$destination_dir" \;