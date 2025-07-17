import csv
from typing import Dict

class Property:
    def __init__(
        self,
        type: str,
        price: float,
        bedrooms: int,
        bathrooms: int,
        area: float,
        furnished: str,
        level: str,
        compound: str,
        payment_option: str,
        delivery_date: str,
        delivery_term: str,
        city: str,
    ):
        self.type = type
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.area = area
        self.furnished = furnished
        self.level = level
        self.compound = compound
        self.payment_option = payment_option
        self.delivery_date = delivery_date
        self.delivery_term = delivery_term
        self.city = city

    def to_dict(self):
        return {
            "type": self.type,
            "price": self.price,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "area": self.area,
            "furnished": self.furnished,
            "level": self.level,
            "compound": self.compound,
            "payment_option": self.payment_option,
            "delivery_date": self.delivery_date,
            "delivery_term": self.delivery_term,
            "city": self.city,
        }

class DataLoader:
    @staticmethod
    def load_properties_csv(filename="properties.csv") -> Dict[str, Property]:
        properties = {}
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                reader.fieldnames = [h.strip().lower() for h in reader.fieldnames]
                for idx, row in enumerate(reader):
                    row = {k.strip().lower(): v for k, v in row.items()}
                    prop = Property(
                        type=row.get("type", ""),
                        price=float(row.get("price", 0)),
                        bedrooms=int(float(row.get("bedrooms", 0))),
                        bathrooms=int(float(row.get("bathrooms", 0))),
                        area=float(row.get("area", 0)),
                        furnished=row.get("furnished", ""),
                        level=row.get("level", ""),
                        compound=row.get("compound", ""),
                        payment_option=row.get("payment_option", ""),
                        delivery_date=row.get("delivery_date", ""),
                        delivery_term=row.get("delivery_term", ""),
                        city=row.get("city", ""),
                    )
                    properties[f"{prop.compound.lower().replace(' ', '_')}_{idx}"] = prop
        except Exception as e:
            print(f"Error loading properties: {e}")
        return properties

class RealEstateChatbot:
    def __init__(self, data_file="properties.csv"):
        self.data_loader = DataLoader()
        self.properties = self.data_loader.load_properties_csv(data_file)
        self.favorites = []
        self.last_results = None
        self.page = 0
        self.page_size = 10
        self.user = "default"

    def process_input(self, message: str) -> str:
        msg = message.lower()
        if "list" in msg:
            self.page = 0
            return self.list_properties()
        elif "find" in msg or "filter" in msg or "search" in msg:
            self.page = 0
            return self.filter_properties(msg)
        elif "sort" in msg:
            return self.sort_results(msg)
        elif "next" in msg:
            return self.next_page()
        elif "previous" in msg:
            return self.previous_page()
        elif "compare" in msg:
            return self.compare_properties(msg)
        elif "details" in msg:
            return self.show_details(msg)
        elif "show favorites" in msg:
            return self.show_favorites()
        # Accept both "remove favorite" and "remove ... favorites"
        elif "remove favorite" in msg or ("remove" in msg and ("favorite" in msg or "favorites" in msg)):
            return self.remove_favorite(msg)
        elif "favorite" in msg or "save" in msg:
            return self.handle_favorites(msg)
        elif "export favorites" in msg:
            return self.export_favorites()
        elif "export" in msg:
            return self.export_results()
        elif "save favorites" in msg:
            return self.save_favorites()
        elif "load favorites" in msg:
            return self.load_favorites()
        elif "user" in msg:
            return self.switch_user(msg)
        elif "help" in msg:
            return self.help_message()
        else:
            return "I'm not sure what you mean. Type 'help' to see what I can do!"

    def list_properties(self) -> str:
        if not self.properties:
            return "No properties found."
        props = list(self.properties.values())
        self.last_results = [(k, v) for k, v in zip(self.properties.keys(), props)]
        return self.show_page()

    def filter_properties(self, msg: str) -> str:
        import re
        results = []
        area_min = area_max = price_min = price_max = bedrooms_min = bedrooms_max = bathrooms_min = bathrooms_max = None

        # Area filters
        area_between = re.search(r"area (?:between|from) (\d+)[^\d]+(\d+)", msg)
        if area_between:
            area_min = float(area_between.group(1))
            area_max = float(area_between.group(2))
        else:
            area_over = re.search(r"area (?:over|greater than|above) (\d+)", msg)
            area_under = re.search(r"area (?:under|less than|below) (\d+)", msg)
            if area_over:
                area_min = float(area_over.group(1))
            if area_under:
                area_max = float(area_under.group(1))

        # Price filters
        price_between = re.search(r"price (?:between|from) (\d+)[^\d]+(\d+)", msg)
        if price_between:
            price_min = int(price_between.group(1))
            price_max = int(price_between.group(2))
        else:
            price_over = re.search(r"price (?:over|greater than|above) (\d+)", msg)
            price_under = re.search(r"price (?:under|less than|below) (\d+)", msg)
            if price_over:
                price_min = int(price_over.group(1))
            if price_under:
                price_max = int(price_under.group(1))

        # Bedrooms min
        bedrooms_match = re.search(r"bedrooms? (?:at least|>=|more than|over) (\d+)", msg)
        if bedrooms_match:
            bedrooms_min = int(bedrooms_match.group(1))
        # Bedrooms max
        bedrooms_under = re.search(r"bedrooms? (?:under|less than|below) (\d+)", msg)
        if bedrooms_under:
            bedrooms_max = int(bedrooms_under.group(1)) - 1

        # Bathrooms min
        bathrooms_match = re.search(r"bathrooms? (?:at least|>=|more than|over) (\d+)", msg)
        if bathrooms_match:
            bathrooms_min = int(bathrooms_match.group(1))
        # Bathrooms max
        bathrooms_under = re.search(r"bathrooms? (?:under|less than|below) (\d+)", msg)
        if bathrooms_under:
            bathrooms_max = int(bathrooms_under.group(1)) - 1

        for key, prop in self.properties.items():
            # Location filter
            if "new cairo" in msg and "new cairo" not in prop.city.lower():
                continue
            if "zayed" in msg and "zayed" not in prop.city.lower():
                continue
            if "madinaty" in msg and "madinaty" not in prop.city.lower():
                continue
            if "cairo" in msg and "new cairo" not in msg and "cairo" not in prop.city.lower():
                continue
            # Type filter
            if "apartment" in msg and "apartment" not in prop.type.lower():
                continue
            if "villa" in msg and "villa" not in prop.type.lower():
                continue
            # Price filter
            if price_min is not None and prop.price < price_min:
                continue
            if price_max is not None and prop.price > price_max:
                continue
            # Area filter
            if area_min is not None and prop.area < area_min:
                continue
            if area_max is not None and prop.area > area_max:
                continue
            # Bedrooms filter
            if bedrooms_min is not None and prop.bedrooms < bedrooms_min:
                continue
            if bedrooms_max is not None and prop.bedrooms > bedrooms_max:
                continue
            # Bathrooms filter
            if bathrooms_min is not None and prop.bathrooms < bathrooms_min:
                continue
            if bathrooms_max is not None and prop.bathrooms > bathrooms_max:
                continue
            results.append((key, prop))
        if not results:
            self.last_results = []
            return "No properties match your filter."
        self.last_results = results
        return self.show_page()

    def sort_results(self, msg: str) -> str:
        if not self.last_results:
            return "No results to sort."
        field = "price"
        reverse = False
        if "area" in msg:
            field = "area"
        elif "bedrooms" in msg:
            field = "bedrooms"
        elif "bathrooms" in msg:
            field = "bathrooms"
        if "desc" in msg or "descending" in msg:
            reverse = True
        self.last_results.sort(key=lambda x: getattr(x[1], field), reverse=reverse)
        self.page = 0
        return self.show_page()

    def show_page(self):
        if not self.last_results:
            return "No results to show."
        start = self.page * self.page_size
        end = start + self.page_size
        results = self.last_results[start:end]
        return "\n".join(
            f"{i+1+start}. {p.compound} | {p.type} | {p.city} | {p.price:,.0f} EGP | {p.bedrooms}BR/{p.bathrooms}BA | {p.area:.0f}m²"
            for i, (k, p) in enumerate(results)
        )

    def next_page(self):
        if not self.last_results:
            return "No results to show."
        if (self.page + 1) * self.page_size >= len(self.last_results):
            return "No more pages."
        self.page += 1
        return self.show_page()

    def previous_page(self):
        if not self.last_results:
            return "No results to show."
        if self.page == 0:
            return "Already at the first page."
        self.page -= 1
        return self.show_page()

    def remove_favorite(self, msg: str) -> str:
        import re
        idxs = re.findall(r"\d+", msg)
        if not idxs:
            return "Please specify a favorite number to remove."
        idx = int(idxs[0]) - 1
        if idx < 0 or idx >= len(self.favorites):
            return "Invalid favorite number."
        removed_key = self.favorites.pop(idx)
        return f"Removed property #{idx+1} from your favorites."

    def show_favorites(self) -> str:
        if not self.favorites:
            return "You have no favorites yet."
        lines = []
        for idx, key in enumerate(self.favorites, 1):
            prop = self.properties[key]
            lines.append(
                f"{idx}. {prop.compound} | {prop.type} | {prop.city} | {prop.price:,.0f} EGP | {prop.bedrooms}BR/{prop.bathrooms}BA | {prop.area}m²"
            )
        return "\n".join(lines)

    def show_details(self, msg: str) -> str:
        import re
        idxs = re.findall(r"\d+", msg)
        if not idxs:
            return "Please specify a property number for details."
        idx = int(idxs[0]) - 1
        if self.last_results and 0 <= idx < len(self.last_results):
            prop = self.last_results[idx][1] if isinstance(self.last_results[idx], tuple) else self.last_results[idx]
        else:
            props = list(self.properties.values())
            if idx < 0 or idx >= len(props):
                return "Property not found."
            prop = props[idx]
        p = prop
        return (
            f"Details for {p.compound}:\n"
            f"Type: {p.type}\n"
            f"Price: {p.price:,.0f} EGP\n"
            f"Bedrooms: {p.bedrooms}\n"
            f"Bathrooms: {p.bathrooms}\n"
            f"Area: {p.area} m²\n"
            f"Furnished: {p.furnished}\n"
            f"Level: {p.level}\n"
            f"Compound: {p.compound}\n"
            f"Payment Option: {p.payment_option}\n"
            f"Delivery Date: {p.delivery_date}\n"
            f"Delivery Term: {p.delivery_term}\n"
            f"City: {p.city}"
        )

    def save_favorites(self):
        filename = f"favorites_{self.user}.txt"
        with open(filename, "w") as f:
            for key in self.favorites:
                f.write(key + "\n")
        return "Favorites saved."

    def load_favorites(self):
        filename = f"favorites_{self.user}.txt"
        try:
            with open(filename, "r") as f:
                self.favorites = [line.strip() for line in f if line.strip() in self.properties]
            return "Favorites loaded."
        except FileNotFoundError:
            self.favorites = []
            return "No favorites file found."

    def export_favorites(self) -> str:
        import pandas as pd
        if not self.favorites:
            return "No favorites to export."
        data = [self.properties[key].to_dict() for key in self.favorites]
        df = pd.DataFrame(data)
        df.to_csv("exported_favorites.csv", index=False)
        return "Exported favorites to exported_favorites.csv."

    def switch_user(self, msg: str) -> str:
        import re
        user_match = re.search(r"user (\w+)", msg)
        if not user_match:
            return "Please specify a username."
        self.user = user_match.group(1)
        self.favorites = []
        self.load_favorites()
        return f"Switched to user {self.user}."

    def handle_favorites(self, msg: str) -> str:
        import re
        if not self.last_results:
            return "Please list or filter properties first, then favorite by their number."
        idxs = re.findall(r"\d+", msg)
        if not idxs:
            return "Please specify a property number to favorite."
        idx = int(idxs[0]) - 1
        try:
            key, prop = self.last_results[idx]
        except IndexError:
            return "Invalid property number."
        if key in self.favorites:
            return f"Property #{idx+1} is already in your favorites."
        self.favorites.append(key)
        return f"Added property #{idx+1} to your favorites."

    def compare_properties(self, msg: str) -> str:
        import re
        if not self.last_results or len(self.last_results) < 2:
            return "Please list or filter properties first, then compare by their numbers."
        ids = re.findall(r"\d+", msg)
        if len(ids) < 2:
            return "Please specify two property numbers to compare (e.g., 'compare 1 and 2')."
        try:
            idx1 = int(ids[0]) - 1
            idx2 = int(ids[1]) - 1
            item1 = self.last_results[idx1]
            item2 = self.last_results[idx2]
            p1 = item1[1] if isinstance(item1, tuple) else item1
            p2 = item2[1] if isinstance(item2, tuple) else item2
        except (IndexError, ValueError):
            return "Invalid property numbers for comparison."
        return (
            f"Comparison:\n"
            f"{p1.compound} | {p1.type} | {p1.city}\n"
            f"  Price: {p1.price:,.0f} EGP\n"
            f"  Bedrooms: {p1.bedrooms}, Bathrooms: {p1.bathrooms}, Area: {p1.area} m²\n"
            f"  Furnished: {p1.furnished}, Level: {p1.level}, Delivery: {p1.delivery_date} ({p1.delivery_term})\n"
            f"  Payment: {p1.payment_option}\n"
            f"---\n"
            f"{p2.compound} | {p2.type} | {p2.city}\n"
            f"  Price: {p2.price:,.0f} EGP\n"
            f"  Bedrooms: {p2.bedrooms}, Bathrooms: {p2.bathrooms}, Area: {p2.area} m²\n"
            f"  Furnished: {p2.furnished}, Level: {p2.level}, Delivery: {p2.delivery_date} ({p2.delivery_term})\n"
            f"  Payment: {p2.payment_option}"
        )

    def export_results(self) -> str:
        import pandas as pd
        if not self.last_results:
            return "No results to export."
        data = [p.to_dict() if hasattr(p, "to_dict") else p[1].to_dict() for p in self.last_results]
        df = pd.DataFrame(data)
        df.to_csv("exported_properties.csv", index=False)
        return "Exported current results to exported_properties.csv."

    def help_message(self) -> str:
        return (
            "I can help you with:\n"
            "- Listing all properties\n"
            "- Filtering by price, area, bedrooms, bathrooms, or location\n"
            "- Combined filters (e.g. 'filter zayed apartment area under 150 price under 2000000')\n"
            "- Range filters (e.g. 'area between 100 and 200')\n"
            "- Sorting results (e.g. 'sort by price ascending')\n"
            "- Pagination (type 'next' or 'previous')\n"
            "- Comparing properties (e.g. 'compare 1 and 2')\n"
            "- Showing property details (e.g. 'details 3')\n"
            "- Managing your favorites (add, remove, show, save, load, export)\n"
            "- User profiles (e.g. 'user alice')\n"
            "- Exporting results\n"
            "Type 'exit' to quit."
        )

if __name__ == "__main__":
    bot = RealEstateChatbot()
    print("Welcome to the Real Estate Chatbot!")
    print("Type 'help' for available commands. Type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(bot.process_input(user_input))