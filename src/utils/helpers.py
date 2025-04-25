def escape_markdown(text):
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return (
        "".join(f"\\{char}" if char in escape_chars else char for char in text)
        if text
        else ""
    )


def should_remove_notes(notes: str) -> bool:
    return notes.strip().lower() in {
        "...",
        ".",
        "..",
        "none",
        "null",
        "empty",
        "n/a",
    }


def format_service_list(services: list, start: int = 0) -> str:
    if not services:
        return "📭 Empty. Use /add to start"

    chunk = services[start: start + 10]
    total_pages = (len(services) + 9) // 10
    current_page = (start // 10) + 1

    list_text = "🔢 *Your Vault*\n\n" + "\n".join(
        f"▫️ **{rowid}** `{escape_markdown(service)}`"
        for rowid, service in sorted(chunk, key=lambda x: x[0])
    )
    return f"{list_text}\n\n📄 Page *{current_page}* of *{total_pages}*"
