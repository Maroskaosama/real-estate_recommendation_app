package chatbot

import Colors._
import scala.util.Random

object ResponseGenerator {
  def getRandomGreeting(): String = {
    val greetings = List(
      "Hello! How can I help you find your dream property?",
      "Hi! What kind of property are you looking for?",
      "Welcome! Let me help you explore available properties.",
      "Hey there! Ready to find your perfect home?"
    )
    greetings(Random.nextInt(greetings.length))
  }

  def getHelpMessage(): String = {
    """I can help you with:
      |- Filter properties by budget, area, or price per square meter
      |- Compare properties by their IDs
      |- View detailed information about specific properties
      |- Save properties to favorites
      |- List all available properties
      |
      |Try these commands:
      |- "Show me properties under 2 million"
      |- "Find apartments with at least 150m²"
      |- "Compare properties 1 and 2"
      |- "Show details for property 3"
      |- "Save property 1 to favorites"
      |- "List all properties"
      |- "Help" for more information""".stripMargin
  }

  def formatPropertyDetails(property: DataLoader.PropertyData): String = {
    s"""${Yellow}Property Details:${Reset}
       |ID: ${property.getOrElse("id", "N/A")}
       |Type: ${property.getOrElse("type", "N/A")}
       |Location: ${property.getOrElse("city", "N/A")}, ${property.getOrElse("compound", "N/A")}
       |Price: ${formatPrice(property.getOrElse("price", "0"))}
       |Area: ${formatArea(property.getOrElse("area", "0"))}
       |Price/m²: ${formatPrice(property.getOrElse("price_per_m2", "0"))}
       |Bedrooms: ${property.getOrElse("bedrooms", "N/A")}
       |Bathrooms: ${property.getOrElse("bathrooms", "N/A")}
       |Furnished: ${property.getOrElse("furnished", "N/A")}""".stripMargin
  }

  def formatPropertyList(properties: List[DataLoader.PropertyData]): String = {
    if (properties.isEmpty) {
      s"${Red}No properties found matching your criteria.${Reset}"
    } else {
      val header = s"${Yellow}Found ${properties.length} properties:${Reset}\n"
      val propertyList = properties.take(5).map { property =>
        s"""${Cyan}ID: ${property.getOrElse("id", "N/A")}${Reset}
           |Type: ${property.getOrElse("type", "N/A")}
           |Location: ${property.getOrElse("city", "N/A")}, ${property.getOrElse("compound", "N/A")}
           |Price: ${formatPrice(property.getOrElse("price", "0"))}
           |Area: ${formatArea(property.getOrElse("area", "0"))}
           |Price/m²: ${formatPrice(property.getOrElse("price_per_m2", "0"))}
           |---""".stripMargin
      }.mkString("\n")

      val footer = if (properties.length > 5) {
        s"\n${Yellow}... and ${properties.length - 5} more properties.${Reset}"
      } else ""

      header + propertyList + footer
    }
  }

  def formatComparison(prop1: DataLoader.PropertyData, prop2: DataLoader.PropertyData): String = {
    val commonKeys = prop1.keySet.intersect(prop2.keySet)
    val comparisons = commonKeys.toList.flatMap { key =>
      val value1 = prop1(key)
      val value2 = prop2(key)
      
      key match {
        case "id" => None
        case "price" =>
          val p1 = Try(value1.toDouble).getOrElse(0.0)
          val p2 = Try(value2.toDouble).getOrElse(0.0)
          val diff = p1 - p2
          val percentDiff = if (p2 != 0) (diff / p2) * 100 else 0
          Some(s"Price: ${formatPrice(value1)} vs ${formatPrice(value2)} (${formatPriceDiff(diff, percentDiff)})")
        case "area" =>
          val a1 = Try(value1.toDouble).getOrElse(0.0)
          val a2 = Try(value2.toDouble).getOrElse(0.0)
          val diff = a1 - a2
          val percentDiff = if (a2 != 0) (diff / a2) * 100 else 0
          Some(s"Area: ${formatArea(value1)} vs ${formatArea(value2)} (${formatAreaDiff(diff, percentDiff)})")
        case "price_per_m2" =>
          val p1 = Try(value1.toDouble).getOrElse(0.0)
          val p2 = Try(value2.toDouble).getOrElse(0.0)
          val diff = p1 - p2
          val percentDiff = if (p2 != 0) (diff / p2) * 100 else 0
          Some(s"Price/m²: ${formatPrice(value1)} vs ${formatPrice(value2)} (${formatPriceDiff(diff, percentDiff)})")
        case _ =>
          Some(s"${key.replace("_", " ").capitalize}: $value1 vs $value2")
      }
    }

    s"""${Yellow}Comparison:${Reset}
       |${Cyan}Property ${prop1.getOrElse("id", "N/A")}:${Reset}
       |${formatPropertyDetails(prop1)}
       |
       |${Cyan}Property ${prop2.getOrElse("id", "N/A")}:${Reset}
       |${formatPropertyDetails(prop2)}
       |
       |${Yellow}Key Differences:${Reset}
       |${comparisons.mkString("\n")}""".stripMargin
  }

  private def formatPrice(price: String): String = {
    Try(price.toDouble).map { p =>
      if (p >= 1_000_000) {
        f"${p / 1_000_000}%.2fM"
      } else if (p >= 1_000) {
        f"${p / 1_000}%.2fK"
      } else {
        f"$p%.2f"
      }
    }.getOrElse("N/A")
  }

  private def formatArea(area: String): String = {
    Try(area.toDouble).map(a => f"$a%.1fm²").getOrElse("N/A")
  }

  private def formatPriceDiff(diff: Double, percentDiff: Double): String = {
    val sign = if (diff > 0) "+" else ""
    s"$sign${formatPrice(diff.toString)} (${sign}${f"$percentDiff%.1f"}%)"
  }

  private def formatAreaDiff(diff: Double, percentDiff: Double): String = {
    val sign = if (diff > 0) "+" else ""
    s"$sign${formatArea(diff.toString)} (${sign}${f"$percentDiff%.1f"}%)"
  }

  def getRandomUnknownResponse(): String = {
    val responses = List(
      "I'm not sure I understand. Try asking about properties, prices, or locations.",
      "Could you rephrase that? Try 'help' to see what I can do.",
      "I didn't catch that. Maybe try asking about a specific property or feature?"
    )
    responses(Random.nextInt(responses.length))
  }

  def respond(command: String): String = {
    command match {
      case "greetings" => getRandomGreeting()
      case "help" => getHelpMessage()
      case "list_properties" => formatPropertyList(DataLoader.getAllProperties)
      case "filter" => "Please specify your filter criteria (e.g., 'Show me properties under 2 million')"
      case cmd if cmd.startsWith("compare_") =>
        val ids = cmd.substring("compare_".length).split("_")
        if (ids.length == 2) {
          (DataLoader.getPropertyById(ids(0)), DataLoader.getPropertyById(ids(1))) match {
            case (Some(prop1), Some(prop2)) => formatComparison(prop1, prop2)
            case _ => s"${Red}One or both properties not found.${Reset}"
          }
        } else {
          s"${Red}Please specify two properties to compare.${Reset}"
        }
      case cmd if cmd.startsWith("details_") =>
        val id = cmd.substring("details_".length)
        DataLoader.getPropertyById(id) match {
          case Some(property) => formatPropertyDetails(property)
          case None => s"${Red}Property not found.${Reset}"
        }
      case cmd if cmd.startsWith("favorites_") =>
        val id = cmd.substring("favorites_".length)
        DataLoader.getPropertyById(id) match {
          case Some(property) => s"${Green}Property ${property.getOrElse("id", "N/A")} added to favorites.${Reset}"
          case None => s"${Red}Property not found.${Reset}"
        }
      case cmd if cmd.startsWith("unknown_") =>
        val query = cmd.substring("unknown_".length)
        getRandomUnknownResponse()
      case _ => getRandomUnknownResponse()
    }
  }
} 