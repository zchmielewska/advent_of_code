data <- readLines("./2022/01/data.txt")

solve1 <- function(data) {
  current_cals = 0
  max_cals = 0
  for (i in 1:length(data)) {
    value <- data[i]
    
    if (value == "") {
      if (current_cals > max_cals) {
        max_cals <- current_cals
      }
      current_cals <- 0
    } else {
      current_cals <- current_cals + as.integer(value)
    }
  }

  return(max_cals)  
}


solve2 <- function(data) {
  x <- data.frame(matrix(data = NA, ncol = 2, nrow = 0))
  
  current_cals = 0
  max_cals = c(0, 0, 0) 
  
  for (i in 1:length(data)) {
    value <- data[i]
    if (value == "") {
      if (current_cals > min(max_cals)) {
        if (current_cals > max_cals[3]) {
          max_cals[3] <- current_cals
        } else if (current_cals > max_cals[2]) {
          max_cals[2] <- current_cals
        } else {
          max_cals[1] <- current_cals
        }
      }
      x <- rbind(x, c(nrow(x) + 1, current_cals))
      current_cals <- 0
      
    } else if (i == length(data)) {
      current_cals <- current_cals + as.integer(value)
      x <- rbind(x, c(nrow(x) + 1, current_cals))
    } else {
      current_cals <- current_cals + as.integer(value)
    }
  }
  
  colnames(x) <- c("no", "value")
  result <- sort(x$value, decreasing = TRUE)
  return(sum(result[1:3]))
}


print(solve1(data))  # 64929
print(solve2(data))  # 193697
