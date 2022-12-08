lines <- readLines("./input/08/example.txt")
lines <- readLines("./input/08/data.txt")


df <- data.frame(matrix(nrow=length(lines), ncol=nchar(lines[1])))
for (i in 1:length(lines)) {
  row <- as.numeric(strsplit(lines[i], "")[[1]])
  df[i,] <- row
}

forest <- as.matrix(df)

is_visible <- function(forest, i, j) {
  n <- nrow(forest)
  m <- ncol(forest)
  
  if (i == 1 | j == 1 | i == m | j == n) {
    return(TRUE)
  }
  
  height <- forest[[i, j]]
  
  left   <- all(forest[i, 1:(j-1)] < height)
  right  <- all(forest[i, (j+1):m] < height)
  top    <- all(forest[1:(i-1), j] < height)
  bottom <- all(forest[(i+1):n, j] < height)
  result <- any(left, right, top, bottom)
  return(result)
}

total <- 0
for (i in 1:nrow(forest)) {
  for (j in 1:nrow(forest)) {
    total <- total + is_visible(forest, i, j)
  }
}

print(total)
