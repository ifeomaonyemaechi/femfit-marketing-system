# brand-voice-check.py
# FemFit.fit Marketing Operations System
#
# This is a Claude Code hook — it runs automatically before
# any file is saved to the outputs/ folder. If banned words
# are found, it blocks the save and returns an error message
# so the content can be fixed before it reaches the client.
#
# How it works:
# 1. Claude Code calls this script before writing output files
# 2. The script reads the content being saved
# 3. It checks for banned words from the FemFit brand rules
# 4. If banned words are found — it blocks the save and lists them
# 5. If content is clean — it allows the save to proceed

import sys
import json

# These are the exact banned words from the FemFit brand voice
# document. Any of these appearing in output will block the save.
BANNED_WORDS = [
    "amazing",
    "incredible",
    "game-changing",
    "game changing",
    "transform your body",
    "slay",
    "queen",
    "goddess",
    "boss babe",
    "exclusive collection",
    "luxurious",
    "best-selling",
    "best selling",
    "perfect for any occasion",
    "unleash",
    "empower your journey",
    "elevate",
    "curated",
    "effortless",
    "seamless",
    "revolutionise",
    "revolutionize",
    "supercharge",
]

def check_brand_voice(content):
    """
    Scans content for banned words.
    Returns a list of any banned words found.
    Comparison is case-insensitive so AMAZING and amazing
    both get caught.
    """
    content_lower = content.lower()
    found = []
    for word in BANNED_WORDS:
        if word.lower() in content_lower:
            found.append(word)
    return found

def main():
    """
    Main function called by Claude Code before saving output.
    Reads the content from stdin, checks it, and returns
    either an approval or a blocked save with details.
    """
    try:
        # Read the hook input from Claude Code
        # Claude Code passes file content as JSON via stdin
        input_data = json.load(sys.stdin)
        
        # Extract the content being saved
        content = input_data.get("content", "")
        file_path = input_data.get("file_path", "unknown file")
        
        # Only check files being saved to the outputs/ folder
        # We don't want to block agent or skill files
        if "outputs/" not in file_path and "outputs\\" not in file_path:
            # Not an output file — allow it through
            print(json.dumps({"approved": True}))
            return
        
        # Run the brand voice check
        violations = check_brand_voice(content)
        
        if violations:
            # Banned words found — block the save
            error_message = (
                f"BRAND VOICE CHECK FAILED\n"
                f"File: {file_path}\n"
                f"Banned words found: {', '.join(violations)}\n"
                f"Fix these before saving. "
                f"Check .claude/agents/brand-voice-guardian.md "
                f"for approved alternatives."
            )
            print(json.dumps({
                "approved": False,
                "error": error_message,
                "violations": violations
            }))
        else:
            # Content is clean — allow the save
            print(json.dumps({
                "approved": True,
                "message": "Brand voice check passed. No banned words found."
            }))
            
    except json.JSONDecodeError:
        # If we can not read the input, allow it through
        # Better to let content through than to block everything
        print(json.dumps({"approved": True}))
    except Exception as e:
        # On any unexpected error, log it but allow through
        print(json.dumps({
            "approved": True,
            "warning": f"Brand voice check error: {str(e)}"
        }))

if __name__ == "__main__":
    main()