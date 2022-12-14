lines <- readLines("./2022/07/data.txt", warn = FALSE)

go_up <- function(path) {
  v <- strsplit(path, "/")[[1]]
  result <- paste(v[1:length(v)-1], collapse="/")
  return(result)
}

get_tree <- function(lines) {
  df <- as.data.frame(matrix(data=NA, nrow=0, ncol=5))
  for (line in lines) {
    
    # Command
    if (startsWith(line, "$")) {
      if (startsWith(line, "$ cd")) {
        target <- strsplit(line, " ")[[1]][3]
        if (target == "/") {
          path <- "home"
        } else if (target == "..") {
          path <- go_up(path)
        } else {
          path <- paste0(path, "/", target)
        }
      } else {
        next
      }
      
    } else {
      if (startsWith(line, "dir")) {
        type <- "dir"
        size <- NA
        name <- strsplit(line, " ")[[1]][2]
      } else {
        type <- "file"
        size <- strsplit(line, " ")[[1]][1]
        name <- strsplit(line, " ")[[1]][2]
      }
      
      full_path <- paste0(path, "/", name)
      row <- c(full_path, path, name, type, size)
      df <- rbind(df, row, stringsAsFactors = FALSE)
    }
  }
  colnames(df) <- c("full_path", "path", "name", "type", "size")
  
  while(any(is.na(df$size))) {
    dirs <- df[is.na(df$size), "full_path"]
    for (dir in dirs) {
      sizes <- df[df$path == dir, "size"]
      if (all(!is.na(sizes))) {
        df[df$full_path == dir, "size"] <- sum(as.numeric(sizes))
      }
    }
  }
  return(df)
}

get_summary <- function(df) {
  summary <- data.frame(matrix(data = NA, nrow = 0, ncol = 2))
  folders <- df[df$type == "dir", "full_path"]
  
  for (folder in folders) {
    size <- sum(as.numeric(df[df$path == folder, "size"]))
    row <- c(folder, size)
    summary <- rbind(summary, row, stringsAsFactors = FALSE)
  }
  colnames(summary) <- c("folder", "size")
  summary$size <- as.numeric(summary$size)
  
  total_size <- sum(summary[summary$size <= 100000, "size"])
  return(summary)
}

solve1 <- function(lines) {
  df <- get_tree(lines)
  summary <- get_summary(df)  
  result <- sum(summary[summary$size <= 100000, "size"])
  return(result)
}

solve2 <- function(lines) {
  df <- get_tree(lines)
  summary <- get_summary(df)  
  
  used_space <- sum(as.numeric(df[df$path == "home", "size"]))
  unused_space <- 70000000 - used_space
  required <- 30000000
  needed <- required - unused_space
  
  summary <- summary[order(summary$size), ]
  row_index <- which(summary$size >= needed)[1]
  result <- summary[row_index, "size"]
  return(result)
}

print(solve1(lines))  # 2104783
print(solve2(lines))  # 5883165
