package chatbot

case class Config(
  dataFile: String = "egypt_House_prices.csv",
  maxResults: Int = 5,
  priceTolerance: Double = 0.1,
  areaTolerance: Double = 0.1
)

object Config {
  def load: Config = Config()
} 