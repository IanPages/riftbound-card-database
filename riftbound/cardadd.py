import csv
import re
from pathlib import Path

CSV_PATH = Path(__file__).parent / "cards.csv"
DB_PATH = Path(__file__).parent / "all_cards_database.csv"
HEADER = ["name", "set", "quantity", "type", "color", "altArt", "overnumbered", "image"]


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def prompt_bool(prompt: str, allow_exit: bool = False) -> bool | None:
    while True:
        suffix = " [y/n/exit]: " if allow_exit else " [y/n]: "
        response = input(f"{prompt}{suffix}").strip().lower()
        if allow_exit and response == "exit":
            return None
        if response in {"y", "yes"}:
            return True
        if response in {"n", "no"}:
            return False
        print("Please enter y or n." if not allow_exit else "Please enter y, n, or exit.")


ALLOWED_COLORS = {"CALM", "FURY", "MIND", "BODY", "CHAOS", "ORDER", "NONE"}


def normalize_color_input(color_input: str) -> str:
    parts = re.split(r"[&,;\s]+", color_input)
    normalized = []
    for part in parts:
        value = part.strip().upper()
        if value and value not in normalized:
            normalized.append(value)
    return "&".join(normalized)


def load_cards() -> list[dict[str, str]]:
    if not CSV_PATH.exists():
        return []

    with CSV_PATH.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def save_cards(cards: list[dict[str, str]]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(cards)


def normalize_card_key(card: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    return (
        card["name"].strip().lower(),
        card["set"].strip().lower(),
        card["type"].strip().lower(),
        normalize_color_input(card.get("color", "")) or "",
        str(card["altArt"]).strip().lower(),
        str(card["overnumbered"]).strip().lower(),
    )


def find_existing_card(cards: list[dict[str, str]], new_card: dict[str, str]) -> int | None:
    new_key = normalize_card_key(new_card)
    for index, card in enumerate(cards):
        if normalize_card_key(card) == new_key:
            return index
    return None


def build_image_filename(name: str, set_code: str, alt_art: bool, overnumbered: bool) -> str:
    image = f"{slugify(name)}-{slugify(set_code)}"
    if alt_art:
        image += "-a"
    if overnumbered:
        image += "-o"
    return f"{image}.avif"


def load_all_cards_db() -> list[dict[str, str]]:
    if not DB_PATH.exists():
        return []
    with DB_PATH.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def find_image_url_in_db(db_cards: list[dict[str, str]], name: str, set_code: str) -> str | None:
    for card in db_cards:
        if card["name"].strip().lower() == name.strip().lower() and card["set"].strip().lower() == set_code.strip().lower():
            return card["image"]
    return None


def prompt_color() -> str:
    while True:
        color_input = input("Color(s) for this session (calm, fury, mind, body, chaos, order; separate with &, comma, semicolon, or space; or 'exit'): ").strip()
        if color_input.lower() == "exit":
            return "exit"
        
        if not color_input:
            print("Color cannot be empty.")
            continue
        normalized_color = normalize_color_input(color_input)
        if not normalized_color:
            print("Color cannot be empty.")
            continue
        invalid = [c for c in normalized_color.split("&") if c not in ALLOWED_COLORS]
        if invalid:
            print(f"Invalid color(s): {', '.join(invalid)}. Must be one of: calm, fury, mind, body, chaos, order.")
            continue
        return normalized_color


def main() -> None:
    print("Add or update Riftbound card entries")
    print("Type 'exit' for card name to quit.\n")
    
    db_cards = load_all_cards_db()
    iterations = 0
    card_color = ""

    while True:
        if iterations == 0:
            card_color = prompt_color()
            if card_color == "exit":
                print("Done!")
                break
        else:
            change_color = prompt_bool("Would you like to change the color?", allow_exit=True)
            if change_color is None:
                print("Done!")
                break

            if change_color:
                card_color = prompt_color()
                if card_color == "exit":
                    print("Done!")
                    break

        while True:
            name = input("Card name (or 'exit'): ").strip()
            if not name:
                print("Card name cannot be empty.")
                continue
            break

        if name.lower() == "exit":
            print("Done!")
            break

        while True:
            set_code = input("Set (3 letters): ").strip().upper()
            if not set_code:
                print("Set cannot be empty.")
                continue
            if len(set_code) != 3:
                print("Set must be exactly 3 letters.")
                continue
            break

        while True:
            card_quantity_str = input("How many copies do you own? ").strip()
            if not card_quantity_str.isdigit() or int(card_quantity_str) < 1:
                print("Quantity must be a number and greater than 0.")
                continue
            card_quantity = int(card_quantity_str)
            break

        while True:
            card_type = input("Type (Legend/Unit/Rune/Spell/Gear/Battlefield/Token): ").strip().upper()
            if card_type not in {"LEGEND", "UNIT", "RUNE", "SPELL", "GEAR", "BATTLEFIELD", "TOKEN"}:
                print("Invalid card type. Make sure to select one of the allowed ones (Legend/Unit/Rune/Spell/Gear/Battlefield/Token)")
                continue

            if not card_type:
                print("Type cannot be empty.")
                continue

            break

        alt_art = prompt_bool("Alt art?")
        overnumbered = prompt_bool("Overnumbered?")

        db_image_url = find_image_url_in_db(db_cards, name, set_code)
        if db_image_url:
            image = db_image_url
            print(f"Found image URL in database: {image}")
        else:
            image = build_image_filename(name, set_code, alt_art, overnumbered)
            print(f"Image not found in database, falling back to local filename: {image}")

        cards = load_cards()
        new_card = {
            "name": name,
            "set": set_code,
            "quantity": str(card_quantity),
            "type": card_type,
            "color": card_color,
            "altArt": str(alt_art).lower(),
            "overnumbered": str(overnumbered).lower(),
            "image": image,
        }

        existing_index = find_existing_card(cards, new_card)

        if existing_index is not None:
            existing_card = cards[existing_index]
            quantity = int(existing_card.get("quantity", "0") or "0") + card_quantity
            existing_card["quantity"] = str(quantity)
            print(f"Updated existing card: {existing_card['name']} ({existing_card['set']}) now quantity {existing_card['quantity']}")
        else:
            cards.append(new_card)
            print(f"Added new card: {name} ({set_code}) with image '{image}'")

        save_cards(cards)
        iterations += 1


if __name__ == "__main__":
    main()
