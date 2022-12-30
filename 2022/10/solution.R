lines <- readLines("./2022/10/data.txt", warn = FALSE)

solve1 <- function(lines) {
  X <- 1
  cycle <- 0
  
  total <- 0
  for (line in lines) {
    if(startsWith(line, "noop")) {
      cycle <- cycle + 1
      
      if (cycle %% 40 == 20) {
        signal_strength <- cycle * X
        if (cycle <= 220) {
          total <- total + signal_strength
        }
      }
      
    } else if (startsWith(line, "addx")) {
      value <- as.integer(strsplit(line, " ")[[1]][2])
      
      for (i in 1:2) {  # addx has two cycles
        cycle <- cycle + 1
        
        if (cycle %% 40 == 20) {
          signal_strength <- cycle * X
          if (cycle <= 220) {
            total <- total + signal_strength
          }
        }
        
        if (i == 2) {
          X <- X + value
        }
      }
    }
  }
  return(total)
}

solve2 <- function(lines) {
  
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
  return(monitor)
}

print(solve1(lines))  # 12840
print(solve2(lines))  # ZKJFBJFZ