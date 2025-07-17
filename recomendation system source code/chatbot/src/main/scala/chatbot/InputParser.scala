package chatbot

import Constants._

object InputParser {
  def parseInput(input: String): String = {
    val normalizedInput = input.trim.toLowerCase
    if (normalizedInput.isEmpty) return "unknown_empty"
    
    val words = normalizedInput.split("\\s+").toList
    
    // Check for greetings first
    if (matchesGreetings(words)) {
      return "greetings"
    }
    
    // Check for help request
    if (matchesHelp(words)) {
      return "help"
    }
    
    // Check for exit command
    if (matchesExit(words)) {
      return "exit"
    }
    
    // Check for property listing
    if (matchesListProperties(words)) {
      return "list_properties"
    }
    
    // Check for property comparison
    if (matchesCompare(normalizedInput)) {
      extractCompareProperties(normalizedInput) match {
        case Some((prop1, prop2)) => return s"compare_${prop1}_${prop2}"
        case None => return "unknown_compare"
      }
    }
    
    // Check for property details
    if (matchesDetails(words)) {
      extractPropertyId(normalizedInput) match {
        case Some(id) => return s"details_$id"
        case None => return "unknown_details"
      }
    }
    
    // Check for favorites
    if (matchesFavorites(words)) {
      extractPropertyId(normalizedInput) match {
        case Some(id) => return s"favorites_$id"
        case None => return "unknown_favorites"
      }
    }
    
    // Check for filtering
    if (matchesFilter(words)) {
      return "filter"
    }
    
    // If no specific command is matched, return unknown with the input
    s"unknown_$normalizedInput"
  }

  private def matchesGreetings(words: List[String]): Boolean =
    words.exists(word => greetingWords.contains(word))

  private def matchesHelp(words: List[String]): Boolean =
    words.exists(word => helpWords.contains(word)) ||
    (words.contains("what") && words.contains("can") && words.contains("you") && words.contains("do"))

  private def matchesExit(words: List[String]): Boolean =
    words.exists(word => exitWords.contains(word))

  private def matchesListProperties(words: List[String]): Boolean =
    words.exists(word => listWords.contains(word)) && 
    (words.contains("properties") || words.contains("listings"))

  private def matchesCompare(input: String): Boolean =
    compareWords.exists(word => input.contains(word))

  private def matchesDetails(words: List[String]): Boolean =
    words.exists(word => detailsWords.contains(word))

  private def matchesFavorites(words: List[String]): Boolean =
    words.exists(word => favoritesWords.contains(word))

  private def matchesFilter(words: List[String]): Boolean =
    words.exists(word => filterWords.contains(word))

  private def extractCompareProperties(input: String): Option[(String, String)] = {
    val patterns = List("compare", "vs", "versus", "and", "between")
    
    // Try to find two properties to compare
    val properties = patterns.foldLeft(input) { (acc, pattern) =>
      acc.replace(pattern, "|")
    }.split("\\|").map(_.trim).filter(_.nonEmpty)
    
    if (properties.length >= 2) {
      Some((properties(0), properties(1)))
    } else None
  }

  private def extractPropertyId(input: String): Option[String] = {
    val idPattern = """\b(\d+)\b""".r
    idPattern.findFirstMatchIn(input).map(_.group(1))
  }

  def extractBudget(input: String): Option[Double] = {
    val patterns = List(
      """under\s+(\d+(?:\.\d+)?)\s*(?:million|M|m)""".r,
      """less\s+than\s+(\d+(?:\.\d+)?)\s*(?:million|M|m)""".r,
      """budget\s+(\d+(?:\.\d+)?)\s*(?:million|M|m)""".r
    )
    
    patterns.flatMap { pattern =>
      pattern.findFirstMatchIn(input.toLowerCase).map { m =>
        val amount = m.group(1).toDouble
        amount * 1_000_000 // Convert to actual amount
      }
    }.headOption
  }

  def extractArea(input: String): Option[Double] = {
    val patterns = List(
      """(\d+(?:\.\d+)?)\s*m²""".r,
      """(\d+(?:\.\d+)?)\s*square\s+meters""".r,
      """at\s+least\s+(\d+(?:\.\d+)?)\s*m""".r
    )
    
    patterns.flatMap { pattern =>
      pattern.findFirstMatchIn(input.toLowerCase).map(_.group(1).toDouble)
    }.headOption
  }

  def extractPricePerM2(input: String): Option[Double] = {
    val patterns = List(
      """price\s+per\s+m²\s+under\s+(\d+(?:\.\d+)?)""".r,
      """price\s+per\s+square\s+meter\s+less\s+than\s+(\d+(?:\.\d+)?)""".r
    )
    
    patterns.flatMap { pattern =>
      pattern.findFirstMatchIn(input.toLowerCase).map(_.group(1).toDouble)
    }.headOption
  }

  def extractLocation(input: String): Option[String] = {
    val locations = DataLoader.getUniqueLocations
    locations.find(loc => input.toLowerCase.contains(loc.toLowerCase))
  }

  def extractPropertyType(input: String): Option[String] = {
    propertyTypes.find(pt => input.toLowerCase.contains(pt.toLowerCase))
  }
} 