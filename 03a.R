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

print(total_priority)