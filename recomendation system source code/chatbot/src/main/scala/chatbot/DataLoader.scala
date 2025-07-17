package chatbot

import scala.io.Source
import scala.util.{Try, Success, Failure}
import scala.collection.mutable.{Map => MutableMap}

object DataLoader {
  type PropertyData = Map[String, String]
  type PropertiesData = Map[String, PropertyData]

  def loadPropertiesData(filename: String): PropertiesData = {
    try {
      val source = Source.fromFile(filename)
      val lines = source.getLines().toList
      source.close()

      if (lines.isEmpty) return Map.empty

      val headers = lines.head.split(",").map(_.trim)
      val data = lines.tail.flatMap { line =>
        try {
          // Split by comma but respect quoted values
          val values = line.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)").map { value =>
            value.trim.stripPrefix("\"").stripSuffix("\"").trim
          }
          
          if (values.length >= headers.length) {
            val propertyData = headers.zip(values).toMap
            val id = propertyData.getOrElse("id", "unknown")
            if (id != "unknown") Some(id -> propertyData)
            else None
          } else None
        } catch {
          case e: Exception =>
            println(s"Warning: Skipping malformed line in CSV: $line")
            None
        }
      }.toMap

      data
    } catch {
      case e: Exception =>
        println(s"Error loading properties data: ${e.getMessage}")
        Map.empty[String, PropertyData]
    }
  }

  def preprocessData(data: PropertiesData): PropertiesData = {
    data.map { case (id, property) =>
      val processedProperty = property.map {
        case ("price", value) =>
          "price" -> value.replaceAll("[^0-9.]", "")
        case ("area", value) =>
          "area" -> value.replaceAll("[^0-9.]", "")
        case (key, value) =>
          key -> value
      }
      
      // Calculate price per square meter
      val price = Try(processedProperty("price").toDouble).getOrElse(0.0)
      val area = Try(processedProperty("area").toDouble).getOrElse(0.0)
      val pricePerM2 = if (area > 0) price / area else 0.0
      
      id -> (processedProperty + ("price_per_m2" -> pricePerM2.toString))
    }
  }

  // This will be initialized when needed
  lazy val propertiesData: PropertiesData = {
    val rawData = loadPropertiesData("egypt_House_prices.csv")
    preprocessData(rawData)
  }

  def getPropertyById(id: String): Option[PropertyData] = propertiesData.get(id)

  def getAllProperties: List[PropertyData] = propertiesData.values.toList

  def getPropertiesByType(propertyType: String): List[PropertyData] = {
    propertiesData.values.filter(_.getOrElse("type", "").toLowerCase == propertyType.toLowerCase).toList
  }

  def getPropertiesByLocation(location: String): List[PropertyData] = {
    propertiesData.values.filter { property =>
      val city = property.getOrElse("city", "").toLowerCase
      val compound = property.getOrElse("compound", "").toLowerCase
      city.contains(location.toLowerCase) || compound.contains(location.toLowerCase)
    }.toList
  }

  def getUniqueLocations: List[String] = {
    val cities = propertiesData.values.map(_.getOrElse("city", "")).filter(_.nonEmpty).toSet
    val compounds = propertiesData.values.map(_.getOrElse("compound", "")).filter(_.nonEmpty).toSet
    (cities ++ compounds).toList
  }

  def getUniquePropertyTypes: List[String] = {
    propertiesData.values.map(_.getOrElse("type", "")).filter(_.nonEmpty).toSet.toList
  }
} 