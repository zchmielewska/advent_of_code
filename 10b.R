lines <- readLines("./input/10/example.txt", warn = FALSE)
lines <- readLines("./input/10/data.txt", warn = FALSE)

X <- 2
cycle <- 0

monitor <- matrix(data=NA, nrow=6, ncol=40)

for (line in lines) {
  if(startsWith(line, "noop")) {
    cycle <- cycle + 1
  
    row <- cycle %/% 40 + 1
    row <- ifelse(cycle %% 40 == 0, row-1, row)
    col <- cycle %% 40
    col <- ifelse(col == 0, 40, col)
    
    sprite <- cycle %% 40
    sprite <- ifelse(sprite == 0, 40, sprite)
    if (sprite >= X-1 & sprite <= X+1) {
      monitor[row, col] <- "#" 
    } else {
      monitor[row, col] <- "."
    }
    
  } else if (startsWith(line, "addx")) {
    value <- as.integer(strsplit(line, " ")[[1]][2])
    
    for (i in 1:2) {
      cycle <- cycle + 1
     
      row <- cycle %/% 40 + 1
      row <- ifelse(cycle %% 40 == 0, row-1, row)
      col <- cycle %% 40
      col <- ifelse(col == 0, 40, col)
      
      sprite <- cycle %% 40
      sprite <- ifelse(sprite == 0, 40, sprite)
      if (sprite >= X-1 & sprite <= X+1) {
        monitor[row, col] <- "#" 
      } else {
        monitor[row, col] <- "."
      }
      
      if (i == 2) {
        X <- X + value
      }
      
    }
  }
}
