data <- readLines("./input/03/example.txt")
data <- readLines("./input/03/data.txt")

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

print(total_priority)
