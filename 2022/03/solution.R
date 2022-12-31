data <- readLines("./2022/03/data.txt", warn = FALSE)

common_letter <- function(word1, word2) {
  for (i in 1:nchar(word1)) {
    letter <- substr(word1, i, i)
    if (grepl(letter, word2)) {
      return(letter)
    }
  }
  return(FALSE)
}

common_letters <- function(word1, word2) {
  result <- c()
  for (i in 1:nchar(word1)) {
    letter <- substr(word1, i, i)
    if (grepl(letter, word2)) {
      result <- append(result, letter)
    }
  }
  return(paste(result, collapse=""))
}

solve1 <- function(data){
  alphabet <- c(letters, toupper(letters))
  total_priority <- 0
  for (rucksack in data) {
    n <- nchar(rucksack)
    compartment1 <- substr(rucksack, 1, n/2)
    compartment2 <- substr(rucksack, n/2+1, n)
    letter <- common_letter(compartment1, compartment2)
    priority <- which(letter == alphabet)
    total_priority <- total_priority + priority
  }
  
  return(total_priority)  
}

solve2 <- function(data) {
  alphabet <- c(letters, toupper(letters))
  total_priority <- 0
  for (i in seq(1, length(data), by=3)) {
    rucksack1 <- data[i]
    rucksack2 <- data[i+1]
    rucksack3 <- data[i+2]
    letter <- common_letter(common_letters(rucksack1, rucksack2), rucksack3)
    priority <- which(letter == alphabet)
    total_priority <- total_priority + priority
  }
  
  return(total_priority)
}

print(solve1(data))  # 8018
print(solve2(data))  # 2518