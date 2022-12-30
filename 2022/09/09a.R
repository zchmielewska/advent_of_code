lines <- readLines("./2022/09/example.txt")
lines <- readLines("./2022/09/data.txt")


move_head <- function(direction, head_pos) {
  if(direction == "R") {
    head_pos$col <- head_pos$col + 1
  }
  
  if (direction == "L") {
    head_pos$col <- head_pos$col - 1
  }
  
  if(direction == "U") {
    head_pos$row <- head_pos$row + 1
  }
  
  if(direction == "D") {
    head_pos$row <- head_pos$row - 1
  }
  
  return(head_pos)
}

touch <- function(pos1, pos2) {
  return(abs(pos1$row-pos2$row) <= 1 & abs(pos1$col-pos2$col) <= 1)
}

move_tail <- function(tail_pos, head_pos) {
  # don't move if you touch
  if (touch(tail_pos, head_pos)) {
    return(tail_pos)
  }

  col_diff <- head_pos$col - tail_pos$col
  row_diff <- head_pos$row - tail_pos$row
  
  # go right
  if (col_diff == 2 & row_diff == 0) {
    tail_pos$col <- tail_pos$col + 1
    return(tail_pos)
  }
  
  # go left
  if (col_diff == -2 & row_diff == 0) {
    tail_pos$col <- tail_pos$col - 1
    return(tail_pos)
  }
  
  # go up
  if (row_diff == 2 & col_diff == 0) {
    tail_pos$row <- tail_pos$row + 1
    return(tail_pos)
  }
  
  # go down
  if (row_diff == -2 & col_diff == 0) {
    tail_pos$row <- tail_pos$row - 1
    return(tail_pos)
  }
  
  # go up-right
  if (row_diff >= 1 & col_diff >= 1) {
    tail_pos$col <- tail_pos$col + 1
    tail_pos$row <- tail_pos$row + 1
    return(tail_pos)
  }
  
  # go down-right
  if (row_diff <= -1 & col_diff >= 1) {
    tail_pos$col <- tail_pos$col + 1
    tail_pos$row <- tail_pos$row - 1
    return(tail_pos)
  }
  
  # go up-left
  if (row_diff >= 1 & col_diff <= -1) {
    tail_pos$col <- tail_pos$col - 1
    tail_pos$row <- tail_pos$row + 1
    return(tail_pos)
  }
  
  # go down-left
  if (row_diff <= -1 & col_diff <= -1) {
    tail_pos$col <- tail_pos$col - 1
    tail_pos$row <- tail_pos$row - 1
    return(tail_pos)
  }
}




start_pos <- list(row=0, col=0)
head_pos <- start_pos
tail_pos <- start_pos

all_pos <- list()
for (line in lines) {
  direction <- strsplit(line, " ")[[1]][1]
  times <-  strsplit(line, " ")[[1]][2]
  #print(paste("direction: ", direction))
  #print(paste("times: ", times))
  
  for (i in 1:times) {
    head_pos <- move_head(direction, head_pos)
    #print(paste0("head_pos: [", head_pos$row, ", ", head_pos$col, "]"))
    tail_pos <- move_tail(tail_pos, head_pos)
    #print(paste0("tail_pos: [", tail_pos$row, ", ", tail_pos$col, "]"))
    #print("")
    all_pos[[length(all_pos)+1]] <- tail_pos
  }
#  print("")
}

unique_pos <- unique(all_pos)
print(length(unique_pos))

