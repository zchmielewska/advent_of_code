lines <- readLines("./input/09/example2.txt")
lines <- readLines("./input/09/data.txt")


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

move_child <- function(tail_pos, head_pos) {
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
pos_h <- start_pos
pos_1 <- start_pos
pos_2 <- start_pos
pos_3 <- start_pos
pos_4 <- start_pos
pos_5 <- start_pos
pos_6 <- start_pos
pos_7 <- start_pos
pos_8 <- start_pos
pos_9 <- start_pos

all_pos <- list()
for (line in lines) {
  direction <- strsplit(line, " ")[[1]][1]
  times <-  strsplit(line, " ")[[1]][2]

  for (i in 1:times) {
    pos_h <- move_head(direction, pos_h)
    pos_1 <- move_child(pos_1, pos_h)
    pos_2 <- move_child(pos_2, pos_1)
    pos_3 <- move_child(pos_3, pos_2)
    pos_4 <- move_child(pos_4, pos_3)
    pos_5 <- move_child(pos_5, pos_4)
    pos_6 <- move_child(pos_6, pos_5)
    pos_7 <- move_child(pos_7, pos_6)
    pos_8 <- move_child(pos_8, pos_7)
    pos_9 <- move_child(pos_9, pos_8)
    all_pos[[length(all_pos)+1]] <- pos_9
  }
}

unique_pos <- unique(all_pos)
print(length(unique_pos))

