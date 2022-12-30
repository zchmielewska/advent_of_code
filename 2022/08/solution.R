lines <- readLines("./2022/08/data.txt", warn = FALSE)

get_forest <- function(lines) {
  df <- data.frame(matrix(nrow=length(lines), ncol=nchar(lines[1])))
  for (i in 1:length(lines)) {
    row <- as.numeric(strsplit(lines[i], "")[[1]])
    df[i,] <- row
  }
  
  forest <- as.matrix(df)
  return(forest)
}

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

solve1 <- function(lines) {
  forest <- get_forest(lines)
  total <- 0
  for (i in 1:nrow(forest)) {
    for (j in 1:nrow(forest)) {
      total <- total + is_visible(forest, i, j)
    }
  }
  return(total)
}

solve2 <- function(lines) {
  forest <- get_forest(lines)
  max_score <- 0
  for (i in 1:nrow(forest)) {
    for (j in 1:ncol(forest)) {
      score <- scenic_score(forest, i, j)
      if (score > max_score) {
        max_score <- score
      }
    }
  }
  return(max_score)
}

print(solve1(lines))  # 1789
print(solve2(lines))  # 314820