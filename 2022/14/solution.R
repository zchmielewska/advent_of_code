lines <- readLines("./2022/14/data.txt", warn = FALSE)

get_rocks_num <- function(values) {
  rocks_num <- list()
  for (value in values) {
    rock <- as.numeric(unlist(strsplit(value, ",")))
    rocks_num[[length(rocks_num)+1]] <- c(rock[2], rock[1])
  }
  return(rocks_num)
}

get_between_rocks <- function(rock1, rock2) {
  rocks <- list()
  
  x1 <- rock1[[1]]
  y1 <- rock1[[2]]
  x2 <- rock2[[1]]
  y2 <- rock2[[2]]
  
  for (x in x1:x2) {
    for (y in y1:y2) {
      rocks[[length(rocks)+1]] <- c(x, y)
    }
  }
  
  return(unique(rocks))
}

process_line_rocks <- function(rocks_num) {
  line_rocks <- list()
  for (i in 1:(length(rocks_num)-1)) {
    rock1 <- rocks_num[[i]]
    rock2 <- rocks_num[[i+1]]
    between_rocks <- get_between_rocks(rock1, rock2)
    line_rocks <- append(line_rocks, between_rocks)
  }
  return(unique(line_rocks))
}

get_min_y <- function(all_rocks) {
  min <- all_rocks[[1]][2]
  for (rock in all_rocks) {
    if (rock[2] < min) {
      min <- rock[2]
    }
  }
  return(min)
}

get_max_y <- function(all_rocks) {
  max <- all_rocks[[1]][2]
  for (rock in all_rocks) {
    if (rock[2] > max) {
      max <- rock[2]
    }
  }
  return(max)
}

get_max_x <- function(all_rocks) {
  max <- all_rocks[[1]][1]
  for (rock in all_rocks) {
    if (rock[1] > max) {
      max <- rock[1]
    }
  }
  return(max)
}

rebase1 <- function(all_rocks, min_y) {
  for (i in 1:length(all_rocks)) {
    all_rocks[[i]][2] <- all_rocks[[i]][2] - min_y+1
  }
  return(all_rocks)
}

rebase2 <- function(all_rocks, diff_x, diff_y) {
  for (i in 1:length(all_rocks)) {
    all_rocks[[i]][1] <- all_rocks[[i]][1] + diff_x
    all_rocks[[i]][2] <- all_rocks[[i]][2] + diff_y
  }
  return(all_rocks)
}

get_all_rocks <- function(lines) {
  all_rocks <- list()
  for (line in lines) {
    rocks_str <- unlist(strsplit(line, split = " -> "))
    rocks_num <- get_rocks_num(rocks_str)
    rocks_line <- process_line_rocks(rocks_num)
    all_rocks <- append(all_rocks, rocks_line)
  }
  all_rocks <- unique(all_rocks)
  return(all_rocks)
}

move_one_step <- function(position, cave) {
  new_position <- position
  
  # down
  if (cave[position[1]+1, position[2]] == ".") {
    new_position <- c(position[1]+1, position[2])
    
    # left abyss
  } else if (position[2]-1 == 0) {
    return(c("abyss","abyss"))
    
    # left-down  
  } else if (cave[position[1]+1, position[2]-1] == ".") {
    new_position <- c(position[1]+1, position[2]-1)
    
    # right abyss
  } else if (position[2]+1 == ncol(cave)+1) {
    return(c("abyss","abyss"))
    
    # right-down
  } else if (cave[position[1]+1, position[2]+1] == ".")  {
    new_position <- c(position[1]+1, position[2]+1)
  }
  
  return(new_position) 
}

get_cave <- function(max_x, max_y, min_y, all_rocks_rebased) {
  cave <- matrix(".", nrow=max_x, ncol=max_y - min_y+1)
  for (rock in all_rocks_rebased) {
    cave[rock[1], rock[2]] <- "#"
  }
  return(cave)
}

fall_sand1 <- function(cave, start_position) {
  i = 1
  while (i < 626) {
    position <- start_position
    new_position <- move_one_step(position, cave)
    while (!all(position == new_position)) {
      position <- new_position
      new_position <- move_one_step(position, cave)
      if (all(new_position == c("abyss","abyss"))) {
        return(i)
      }
    }
    cave[new_position[1],  new_position[2]] <- "o"
    i = i+1
  }
  return(i)
}

fall_sand2 <- function(cave, start_position) {
  i = 1
  while (TRUE) {
    position <- start_position
    new_position <- move_one_step(position, cave)
    
    if (all(new_position == start_position)) {
      return(i)
    }
    
    while (!all(position == new_position)) {
      position <- new_position
      new_position <- move_one_step(position, cave)
    }
    cave[new_position[1],  new_position[2]] <- "o"
    i = i+1
  }
}

solve1 <- function(lines) {
  all_rocks <- get_all_rocks(lines)
  min_y <- get_min_y(all_rocks)
  max_y <- get_max_y(all_rocks)
  max_x <- get_max_x(all_rocks)
  start_position <- c(1, 500-min_y+1)
  all_rocks_rebased <- rebase1(all_rocks, min_y)
  cave <- get_cave(max_x, max_y, min_y, all_rocks_rebased)
  result <- fall_sand1(cave, start_position)-1
  return(result)  
}

solve2 <- function(lines) {
  all_rocks <- get_all_rocks(lines)
  min_y <- get_min_y(all_rocks)
  max_y <- get_max_y(all_rocks)
  max_x <- get_max_x(all_rocks)
  new_max_x <- max_x + 3
  
  start_position <- c(1, new_max_x+1)
  all_rocks_rebased <- rebase2(all_rocks, diff_x = 1, diff_y = -(500-new_max_x-1))
  
  cave <- matrix(".", nrow=new_max_x, ncol=2*new_max_x+1)
  for (rock in all_rocks_rebased) {
    cave[rock[1], rock[2]] <- "#"
  }
  cave[new_max_x, ] <- "#" 
  result <- fall_sand2(cave, start_position)
  return(result)
}

print(solve1(lines))  # 625
print(solve2(lines))  # 25193
