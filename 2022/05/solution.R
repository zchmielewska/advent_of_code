lines <- readLines("./2022/05/data.txt", warn = FALSE)

move1 <- function(stacks, from, to, times=1) {
  for (i in 1:times) {
    value <- tail(stacks[[from]], n=1)
    l <- length(stacks[[from]])-1
    stacks[[from]] <- stacks[[from]][1:l]
    stacks[[to]] <- c(stacks[[to]], value)
  }
  return(stacks)
}

move2 <- function(stacks, from, to, times=1) {
  values <- tail(stacks[[from]], n=times)
  l <- length(stacks[[from]])-length(values)
  stacks[[from]] <- stacks[[from]][1:l]
  stacks[[to]] <- c(stacks[[to]], values)
  return(stacks)
}

get_stacks <- function(lines) {
  drawing <- lines[1:(which(lines == "")-2)]
  n <- as.integer(tail(strsplit(lines[which(lines == "")-1], " ")[[1]], n=1))
  stacks <- vector("list", length=n)
  
  # Populate initial stacks
  for (line in drawing) {
    for (i in 1:n) {
      letter <- substr(line, 4*(i-1)+2, 4*(i-1)+2)
      if (letter != " ") {
        stacks[[i]] <- c(letter, stacks[[i]])
      }
    }
  }
  return(stacks)
}


solve <- function(lines, part) {
  stacks <- get_stacks(lines)
  
  for (line in lines) {
    if ((substr(line, 1, 4)) == "move") {
      line_split <- strsplit(line, " ")
      times <- as.integer(line_split[[1]][2])
      from  <- as.integer(line_split[[1]][4])
      to    <- as.integer(line_split[[1]][6])
      if (part == 1) {
        stacks <- move1(stacks, from, to, times)  
      } else {
        stacks <- move2(stacks, from, to, times)  
      }
    }
  }
  
  result <- ""
  for (i in 1:length(stacks)) {
    result <- paste0(result, tail(stacks[[i]], n=1))
  }
  
  return(result)
}

print(solve(lines, 1))  # LJSVLTWQM
print(solve(lines, 2))  # BRQWDBBJM