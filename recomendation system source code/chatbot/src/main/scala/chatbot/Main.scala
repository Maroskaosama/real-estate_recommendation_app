package chatbot

import scala.io.StdIn
import scala.util.{Try, Success, Failure}

object Main {
  def main(args: Array[String]): Unit = {
    println(s"${Colors.Cyan}Welcome to the Real Estate Chatbot!${Colors.Reset}")
    println(s"${Colors.Yellow}Type 'help' for available commands or 'exit' to quit.${Colors.Reset}\n")

    // Initialize data
    Try(DataLoader.propertiesData) match {
      case Success(_) =>
        println(s"${Colors.Green}Data loaded successfully!${Colors.Reset}\n")
        chatLoop()
      case Failure(e) =>
        println(s"${Colors.Red}Error loading data: ${e.getMessage}${Colors.Reset}")
        println("Please make sure the data file exists and is properly formatted.")
        System.exit(1)
    }
  }

  private def chatLoop(): Unit = {
    var running = true
    while (running) {
      print(s"${Colors.Cyan}You: ${Colors.Reset}")
      val input = StdIn.readLine().trim.toLowerCase

      if (input == "exit") {
        running = false
        println(s"\n${Colors.Yellow}Thank you for using the Real Estate Chatbot. Goodbye!${Colors.Reset}")
      } else {
        val command = InputParser.parseInput(input)
        val response = ResponseGenerator.respond(command)
        println(s"\n${Colors.Green}Chatbot: ${Colors.Reset}$response\n")
      }
    }
  }
} 