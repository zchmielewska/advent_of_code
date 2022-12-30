line <- readLines("./2022/06/data.txt", n = 1, warn = FALSE)

find_marker <- function(line, n) {
  for (i in 1:(nchar(line)-3)) {
    code <- (substr(line, i, i+n-1))
    code_split <- strsplit(code, "")[[1]]
    
    if (length(unique(code_split)) == length(code_split)) {
      return(i+n-1)
    }
  }
}

print(find_marker(line, n=4))   # 1198
print(find_marker(line, n=14))  # 3120