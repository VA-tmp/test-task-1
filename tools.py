import numexpr as ne


notes = []


def add_note(note: str) -> str:
    """Add a note to the list of notes."""
    notes.append(note)
    return f'Note added: "{note}"'

def list_notes() -> str:
    """List all notes."""
    if not notes:
        return 'No notes yet.'
    return '\n'.join([f'- {n}' for n in notes])

def calculate(expression: str) -> str:
    """Evaluates a basic arithmetic expression. Example: '2 + 3 * 4'"""
    return str(ne.evaluate(expression))
