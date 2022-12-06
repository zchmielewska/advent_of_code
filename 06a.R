lines <- readLines("./input/06/example.txt")
lines <- readLines("./input/06/data.txt")

line <- lines[1]

find_marker <- function(line) {
  for (i in 1:(nchar(line)-3)) {
    code <- (substr(line, i, i+3))
    code_split <- strsplit(code, "")[[1]]
    
    if (length(unique(code_split)) == length(code_split)) {
      return(i+3)
    }
  }
}

find_marker(line)


for (line in lines) {
  marker <- find_marker(line)
  print(marker)
}


