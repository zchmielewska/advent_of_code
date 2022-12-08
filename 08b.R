lines <- readLines("./input/08/example.txt")
lines <- readLines("./input/08/data.txt")


df <- data.frame(matrix(nrow=length(lines), ncol=nchar(lines[1])))
for (i in 1:length(lines)) {
  row <- as.numeric(strsplit(lines[i], "")[[1]])
  df[i,] <- row
}

forest <- as.matrix(df)


first_false <- function(vector) {
  total <- 0
  for (i in 1:length(vector)) {
    value <- vector[i]
    if (value) {
      total <- total+1
    } else {
      return(total+1)
    }
  }
  return(total)
}

scenic_score <- function(forest, i, j) {
  n <- nrow(forest)
  m <- ncol(forest)

  height <- forest[[i, j]]
  
  if (i == 1 | j == 1 | i == m | j == n) {
    return(0)
  }
  
  left   <- first_false(rev(forest[i, 1:(j-1)] < height))
  right  <- first_false(forest[i, (j+1):m] < height)
  top    <- first_false(rev(forest[1:(i-1), j] < height))
  bottom <- first_false(forest[(i+1):n, j] < height)
  return(left * right * top * bottom)
}

max_score <- 0
for (i in 1:nrow(forest)) {
  for (j in 1:ncol(forest)) {
    score <- scenic_score(forest, i, j)
    if (score > max_score) {
      max_score <- score
    }
  }
}

print(max_score)
