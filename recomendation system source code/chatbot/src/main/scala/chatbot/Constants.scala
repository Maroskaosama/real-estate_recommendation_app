package chatbot

object Constants {
  val CMD_UNKNOWN = "UNKNOWN"
  val CMD_HELP = "HELP"
  val CMD_LIST_PROPERTIES = "LIST_PROPERTIES"
  val CMD_FILTER = "FILTER"
  val CMD_COMPARE = "COMPARE"
  val CMD_DETAILS = "DETAILS"
  val CMD_FAVORITES = "FAVORITES"
  val CMD_EXIT = "EXIT"
  val CMD_GREETINGS = "GREETINGS"

  // Word lists
  val helpWords = List("help", "commands", "guide", "instructions")
  val listWords = List("list", "show", "display", "what")
  val filterWords = List(
    "filter", "find", "search", "looking for", "want", "need",
    "under", "less than", "more than", "at least", "maximum",
    "budget", "price", "area", "size", "location"
  )
  val compareWords = List(
    "compare", "difference", "versus", "vs", "between", "against", "and",
    "or", "difference between", "how does", "how do", "what is the difference"
  )
  val detailsWords = List(
    "details", "info", "information", "tell me about", "show me",
    "describe", "what is", "what are"
  )
  val favoritesWords = List(
    "favorite", "favourites", "save", "bookmark", "remember",
    "add to favorites", "remove from favorites"
  )
  val exitWords = List("exit", "quit", "stop", "end", "bye", "goodbye")
  val greetingWords = List("hello", "hi", "hey", "greetings", "yo")

  // Property types
  val propertyTypes = List(
    "apartment", "house", "villa", "townhouse", "studio",
    "penthouse", "duplex", "condo", "loft"
  )

  // Property features
  val propertyFeatures = List(
    "furnished", "unfurnished", "semi-furnished",
    "parking", "garden", "pool", "gym", "security",
    "elevator", "balcony", "terrace"
  )

  // Location types
  val locationTypes = List(
    "city", "district", "neighborhood", "area", "compound",
    "zone", "region", "street"
  )
} 