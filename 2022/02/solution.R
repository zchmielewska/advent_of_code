lines <- readLines("./2022/02/data.txt", warn = FALSE)

get_shape <- function(letter) {
  if (letter == "A" | letter == "X") {
    return("Rock")
  } else if (letter == "B" | letter == "Y") {
    return("Paper")
  } else if (letter == "C" | letter == "Z") {
    return("Scissors")
  }
}

get_result <- function(op_shape, me_shape) {
  # Draw cases
  if (op_shape == me_shape) {
    return("Draw")
  }
  # Lost cases
  if (op_shape == "Rock" & me_shape == "Scissors") {
    return("Lost")
  }
  if (op_shape == "Paper" & me_shape == "Rock") {
    return("Lost")
  }
  if (op_shape == "Scissors" & me_shape == "Paper") {
    return("Lost")
  }
  return("Win")
}

get_score <- function(op_shape, me_shape) {
  score = 0

  # shape score
  if (me_shape == "Rock") {
    score = score + 1
  } else if (me_shape == "Paper") {
    score = score + 2
  } else if (me_shape == "Scissors") {
    score = score + 3
  }
  
  # result score
  result <- get_result(op_shape, me_shape)
  if (result == "Draw") {
    score = score + 3
  } else if (result == "Win") {
    score = score + 6
  }
  return(score)
}

get_me_shape <- function(op_shape, result) {
  # X = lose, Y = draw, Z = win
  
  # Draw
  if (result == "Y") {
    return(op_shape)
    
  # Lose
  } else if (result == "X") {
    if (op_shape == "Paper") {
      return("Rock")
    } else if (op_shape == "Rock") {
      return("Scissors")
    } else if (op_shape == "Scissors") {
      return("Paper")
    }
  
  # Win
  } else if (result == "Z") {
    if (op_shape == "Paper") {
      return("Scissors")
    } else if (op_shape == "Rock") {
      return("Paper")
    } else if (op_shape == "Scissors") {
      return("Rock")
    }
  }
}

solve1 <- function(lines) {
  total_score <- 0
  for (round in lines) {
    op_letter <- substr(round, 1, 1)
    me_letter <- substr(round, 3, 3)
    op_shape <- get_shape(op_letter)
    me_shape <- get_shape(me_letter)
    score <- get_score(op_shape, me_shape)
    total_score <- total_score + score
  }
  return(total_score)
}

solve2 <- function(lines) {
  total_score <- 0
  for (round in lines) {
    op_letter <- substr(round, 1, 1)
    result <- substr(round, 3, 3)
    op_shape <- get_shape(op_letter)
    
    me_shape <- get_me_shape(op_shape, result)
    
    
    score <- get_score(op_shape, me_shape)
    total_score <- total_score + score
  }
  return(total_score)
}

print(solve1(lines))  # 11767
print(solve2(lines))  # 13886