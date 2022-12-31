data <- readLines("./2022/04/data.txt", warn = FALSE)

to_ranges <- function(line) {
  part1 <- strsplit(line, ",")[[1]][1]
  part2 <- strsplit(line, ",")[[1]][2]
  
  part1_min <- strsplit(part1, "-")[[1]][1]
  part1_max <- strsplit(part1, "-")[[1]][2]
  
  part2_min <- strsplit(part2, "-")[[1]][1]
  part2_max <- strsplit(part2, "-")[[1]][2]
  
  range1 <- seq(part1_min, part1_max)
  range2 <- seq(part2_min, part2_max)
  
  ranges <- list()
  ranges$range1 <- range1
  ranges$range2 <- range2
  
  return(ranges)
}

contains <- function(range1, range2) {
  result <- all(range2 %in% range1)
  return(result)
}

overlaps <- function(range1, range2) {
  result <- any(range1 %in% range2)
  return(result)
}

solve1 <- function(data) {
  total <- 0
  for (line in data) {
    ranges <- to_ranges(line)
    range1 <- ranges$range1
    range2 <- ranges$range2
    
    if (contains(range1, range2) | contains(range2, range1)) {
      total <- total + 1
    }
  }
  
  return(total)
}

solve2 <- function(data) {
  total <- 0
  for (line in data) {
    ranges <- to_ranges(line)
    range1 <- ranges$range1
    range2 <- ranges$range2
    
    if (overlaps(range1, range2)) {
      total <- total + 1
    }
  }
  
  return(total)
}

print(solve1(data))  # 485
print(solve2(data))  # 857
