# Load necessary libraries
if (!require("ARTool")) {
  install.packages("ARTool")
}
library(ARTool)

# Load your data
data <- read.csv("data.csv") # Use the file name directly

# Convert Correctness to numeric (1 for True, 0 for False)
data$Correctness <- as.numeric(data$Correctness == "True")

# Ensure ReactionTime is numeric
data$ReactionTime <- as.numeric(data$ReactionTime)

# Convert Immersion and Modality to factors
data$Immersion <- as.factor(data$Immersion)
data$Modality <- as.factor(data$Modality)

# Remove rows with missing values
data <- na.omit(data)

# Aggregate average correctness and mean reaction time per participant, immersion, and condition
aggregated_data <- aggregate(cbind(avg_correctness = Correctness, avg_reaction_time = ReactionTime) ~ ParticipantID + Immersion + Modality, data, mean)

# Calculate error rate
aggregated_data$error_rate <- 1 - aggregated_data$avg_correctness

# Function to extract ANOVA results
extract_anova_results <- function(anova_result, condition, metric) {
  result_df <- as.data.frame(anova_result)
  result_df$Condition <- condition
  result_df$Metric <- metric
  return(result_df)
}

# Function to round non-integer numerical values to two decimal places
round_non_integers <- function(df) {
  numeric_cols <- sapply(df, is.numeric)
  df[numeric_cols] <- lapply(df[numeric_cols], function(x) {
    ifelse(x == floor(x), x, round(x, 2))
  })
  return(df)
}

# Perform ART ANOVA for error rate with interaction
anova_error_rate <- art(error_rate ~ Immersion * Modality, data = aggregated_data)
anova_results_error_rate <- extract_anova_results(anova(anova_error_rate), "Combined", "Error Rate")

# Perform ART ANOVA for reaction time with interaction
anova_reaction_time <- art(avg_reaction_time ~ Immersion * Modality, data = aggregated_data)
anova_results_reaction_time <- extract_anova_results(anova(anova_reaction_time), "Combined", "Reaction Time")

# Write the main effects and interactions results to separate CSV files
write.csv(round_non_integers(anova_results_error_rate), "anova_results_error_rate.csv", row.names = FALSE)
write.csv(round_non_integers(anova_results_reaction_time), "anova_results_reaction_time.csv", row.names = FALSE)

# Separate the data by Modality pairs
h_v_data <- subset(aggregated_data, Modality %in% c("H", "V"))
h_vh_data <- subset(aggregated_data, Modality %in% c("H", "VH"))
v_vh_data <- subset(aggregated_data, Modality %in% c("V", "VH"))

# Separate the data by individual Modality
haptic_data <- subset(aggregated_data, Modality == "H")
visual_data <- subset(aggregated_data, Modality == "V")
visuohaptic_data <- subset(aggregated_data, Modality == "VH")

# Function to perform ART ANOVA with checks
perform_art_anova_with_checks <- function(data, condition, metric) {
  results <- data.frame()
  
  if (nrow(data) > 1 && length(unique(data$Immersion)) > 1 && length(unique(data$Modality)) > 1) {
    anova_result <- art(as.formula(paste(metric, "~ Immersion * Modality")), data = data)
    results <- extract_anova_results(anova(anova_result), condition, metric)
  } else if (nrow(data) > 1 && length(unique(data$Immersion)) > 1) {
    anova_result <- art(as.formula(paste(metric, "~ Immersion")), data = data)
    results <- extract_anova_results(anova(anova_result), condition, metric)
  }
  
  return(results)
}

# Perform ART ANOVA for error rate in each pairwise condition with interaction checks
anova_results_error_rate_h_v <- perform_art_anova_with_checks(h_v_data, "H vs V", "error_rate")
anova_results_error_rate_h_vh <- perform_art_anova_with_checks(h_vh_data, "H vs VH", "error_rate")
anova_results_error_rate_v_vh <- perform_art_anova_with_checks(v_vh_data, "V vs VH", "error_rate")

# Perform ART ANOVA for reaction time in each pairwise condition with interaction checks
anova_results_reaction_time_h_v <- perform_art_anova_with_checks(h_v_data, "H vs V", "avg_reaction_time")
anova_results_reaction_time_h_vh <- perform_art_anova_with_checks(h_vh_data, "H vs VH", "avg_reaction_time")
anova_results_reaction_time_v_vh <- perform_art_anova_with_checks(v_vh_data, "V vs VH", "avg_reaction_time")

# Perform ART ANOVA for error rate in each individual condition
anova_results_error_rate_haptic <- perform_art_anova_with_checks(haptic_data, "H", "error_rate")
anova_results_error_rate_visual <- perform_art_anova_with_checks(visual_data, "V", "error_rate")
anova_results_error_rate_visuohaptic <- perform_art_anova_with_checks(visuohaptic_data, "VH", "error_rate")

# Perform ART ANOVA for reaction time in each individual condition
anova_results_reaction_time_haptic <- perform_art_anova_with_checks(haptic_data, "H", "avg_reaction_time")
anova_results_reaction_time_visual <- perform_art_anova_with_checks(visual_data, "V", "avg_reaction_time")
anova_results_reaction_time_visuohaptic <- perform_art_anova_with_checks(visuohaptic_data, "VH", "avg_reaction_time")

# Combine all results into a single data frame
anova_results_combined <- rbind(
  anova_results_error_rate,
  anova_results_reaction_time,
  anova_results_error_rate_h_v,
  anova_results_error_rate_h_vh,
  anova_results_error_rate_v_vh,
  anova_results_reaction_time_h_v,
  anova_results_reaction_time_h_vh,
  anova_results_reaction_time_v_vh,
  anova_results_error_rate_haptic,
  anova_results_error_rate_visual,
  anova_results_error_rate_visuohaptic,
  anova_results_reaction_time_haptic,
  anova_results_reaction_time_visual,
  anova_results_reaction_time_visuohaptic
)

# Apply rounding to non-integer numerical values
anova_results_combined <- round_non_integers(anova_results_combined)

# Write the combined results to a CSV file
write.csv(anova_results_combined, "anova_results_combined.csv", row.names = FALSE)

# Print a message indicating the results have been saved
cat("ANOVA results have been saved to 'anova_results_combined.csv'.\n")
