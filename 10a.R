lines <- readLines("./input/10/example.txt", warn = FALSE)
lines <- readLines("./input/10/data.txt", warn = FALSE)

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

print(total)

