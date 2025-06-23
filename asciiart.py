from PIL import Image
import sys
from datetime import datetime, timezone, timedelta
from github_functions import get_total_contributions, get_total_repos
import html
from leetcode_functions import get_leetcode_solves, get_leetcode_ranking

# ASCII characters from darkest to lightest
ASCII_CHARS = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|)(1}{][?-_+~><i!lI;:,",^`'. """
FONT_SIZE = 10  # For ASCII characters only

# INFO block: 20 lines, separated by \n
def get_age_line(timestamp):
    now = datetime.now(timezone.utc)
    then = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    delta = now - then
    days = delta.days
    years, rem_days = divmod(days, 365)
    months, days = divmod(rem_days, 30)
    age = f"{years} years, {months} months, {days} days"
    output = "• Uptime:"
    while (len(output)+ len(age)) < 60:
        output += "."
    return f"{output}{age}"

def get_last_updated_line():
    ist_timezone = timezone(timedelta(hours=5, minutes=30))
    timestamp = datetime.now(ist_timezone).strftime('%d-%m-%Y %I:%M:%S %p')
    output = f"• Last Updated: "
    while (len(output) + len(timestamp)) < 60:
        output += "."
    return f"{output}{timestamp}"

def get_github_stats():
    contributions = f"{get_total_contributions():,}"
    output = "• Github Contributions: "
    while (len(output) + len(contributions)) < 60:
        output += "."
    output += f"{contributions}\n"
    repositories = f"{get_total_repos():,}"
    output += "• Github Repositories: "
    while (len(output) + len(repositories)) <= 120:
        output += "."
    output += f"{repositories}"
    return output

def get_leetcode_stats():
    solves = get_leetcode_solves()
    solves_str = f"{solves:,}"

    ranking = get_leetcode_ranking()
    ranking_str = f"{ranking:,}"

    output = "• LeetCode Solves: "
    while (len(output) + len(solves_str)) < 60:
        output += "."
    output += f"{solves_str}\n"

    output += "• LeetCode Ranking: "
    while (len(output) + len(ranking_str)) <= 120:
        output += "."
    output += f"{ranking_str}"

    return output

INFO = f"""
Angad@Bhalla
————————————————————————————————————————————————————————————
• OS: .............................Debian 12, Android, Linux
{get_age_line(1117650600)}
• IDE: ...................................Visual Studio Code
• Portfolio: .............................https://anga.codes

• Languages.Programming: ......Python, C, JavaScript, GoLang
• Languages.Real: ............................English, Hindi
• Languages.Markup: ...................Markdown, HTML, LaTeX

• Web.Frameworks: ...........ReactJS, SolidJS, Svelte, VueJS
• Web.Tools: .....................Vite, Next.js, TailwindCSS
• Backend.Frameworks: .......Gin, FastAPI, Django, ExpressJS

————————————————————————— Contacts —————————————————————————
• Email: ..............................sayhi@angadbhalla.com
• Linkedin: .................https://linkedin.com/in/anga205
• Instagram: ......................................@_anga205
• Discord: .........................................@anga205
• Reddit: .........................................u/anga205

—————————————————————————— Stats ———————————————————————————
{get_github_stats()}
{get_leetcode_stats()}
{get_last_updated_line()}
""".strip()


def resize_image(image, new_width=100):
    """Resize image while preserving aspect ratio."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))


def pixel_to_ascii(r, g, b, a):
    """Convert RGBA pixel to ASCII character based on brightness."""
    if a == 0:
        return " "  # Fully transparent → empty space
    grayscale = int(0.299 * r + 0.587 * g + 0.114 * b)
    index = grayscale * (len(ASCII_CHARS) - 1) // 255
    return ASCII_CHARS[index]


def image_to_ascii_svg(image_path, output_path="output.svg", new_width=100):
    try:
        image = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open image: {e}")
        return

    image = resize_image(image, new_width)
    width, height = image.size
    pixels = image.load()

    FONT_SIZE = 10
    PADDING = 5
    BORDER_WIDTH = 1
    CORNER_RADIUS = 5

    svg_width = width * FONT_SIZE
    svg_height = height * FONT_SIZE
    sidebar_width = FONT_SIZE * 40  # Space for INFO block
    
    info_lines = INFO.strip().split("\n")
    info_lines_count = len(info_lines)
    
    # Add line spacing by defining a line_height larger than the font_size
    line_height = svg_height / info_lines_count 
    info_font_size = line_height * 0.75 # Use 75% of line height for font, 25% for spacing

    # Calculate the maximum width of the info block
    max_info_width = max(len(line) for line in info_lines) * (info_font_size * 0.6)  # Estimate width per character
    sidebar_width = max(sidebar_width, max_info_width + FONT_SIZE * 4)  # Ensure enough space

    total_width = svg_width + sidebar_width + 2 * PADDING
    total_height = svg_height + 2 * PADDING

    # Find indices for linkable sections
    portfolio_index = next((i for i, text in enumerate(info_lines) if 'Portfolio' in text), -1)
    contact_header_index = next((i for i, text in enumerate(info_lines) if 'Contact' in text), -1)
    stats_header_index = next((i for i, text in enumerate(info_lines) if 'Stats' in text), -1)

    # Start SVG
    svg_lines = []
    svg_lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{total_width}" height="{total_height}" '
        f'viewBox="0 0 {total_width} {total_height}" '
        f'style="background:#171717">'
    )

    # Add border and background
    svg_lines.append(
        f'<rect x="{PADDING/2}" y="{PADDING/2}" width="{total_width - PADDING}" height="{total_height - PADDING}" '
        f'rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" '
        f'fill="#171717" stroke="white" stroke-width="{BORDER_WIDTH}"/>'
    )

    # Style for both blocks
    svg_lines.append(
        f'<style>'
        f'text {{ font-family: monospace; dominant-baseline: middle; }}'
        f'</style>'
    )

    # Render ASCII Art
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            char = pixel_to_ascii(r, g, b, a)
            if char != " ":
                fill = f"rgb({r},{g},{b})" if a != 0 else "rgb(0,0,0)"
                xpos = x * FONT_SIZE + PADDING
                ypos = y * FONT_SIZE + PADDING
                svg_lines.append(
                    f'<text x="{xpos}" y="{ypos}" fill="{fill}" font-size="{FONT_SIZE}px" text-anchor="middle" font-weight="bold">{html.escape(char)}</text>'
                )

    # Render INFO block
    info_x = svg_width + FONT_SIZE * 2 + PADDING  # padding from ASCII art

    for i, line in enumerate(info_lines):
        y_pos = int((i + 0.5) * line_height) + PADDING

        if i == 0 and '@' in line:
            at_index = line.find('@')
            part1 = line[:at_index]
            part2 = line[at_index]
            part3 = line[at_index+1:]
            svg_line = (
            f'<text x="{info_x}" y="{y_pos}" font-size="{info_font_size}px" text-anchor="start">'
            f'<tspan fill="#800080">{html.escape(part1)}</tspan>'  # Light Purple
            f'<tspan fill="white">{html.escape(part2)}</tspan>'
            f'<tspan fill="maroon">{html.escape(part3)}</tspan>'
            f'</text>'
            )
            svg_lines.append(svg_line)
        elif '•' in line and ':' in line:
            # Colored line using tspans
            colon_index = line.find(':')
            
            bullet_part = line[:1]
            key_part = line[1:colon_index + 1]
            rest = line[colon_index + 1:]

            value_start_index = -1
            # Find the start of the value (first non-dot/space character)
            for j, char in enumerate(rest):
                if char not in ['.', ' ']:
                    value_start_index = j
                    break
            
            if value_start_index != -1:
                dots_part = rest[:value_start_index]
                value_part = rest[value_start_index:]
            else:
                dots_part = rest
                value_part = ""

            # Using tspans for different colors. `white-space: pre` preserves dot spacing.
            svg_text_line = (
                f'<text x="{info_x}" y="{y_pos}" font-size="{info_font_size}px" text-anchor="start" style="white-space: pre;">'
                f'<tspan fill="white">{html.escape(bullet_part)}</tspan>'
                f'<tspan fill="orange">{html.escape(key_part)}</tspan>'
                f'<tspan fill="white">{html.escape(dots_part)}</tspan>'
                f'<tspan fill="lime">{html.escape(value_part)}</tspan>'
                f'</text>'
            )

            url = None
            key_text = key_part.strip().rstrip(':')
            value_text = value_part.strip()

            if i == portfolio_index:
                url = value_text
            elif contact_header_index != -1 and stats_header_index != -1 and contact_header_index < i < stats_header_index:
                if key_text == "Email":
                    url = f"mailto:{value_text}"
                elif key_text == "Linkedin":
                    url = f"https://www.linkedin.com/{value_text}"
                elif key_text == "Instagram":
                    url = f"https://www.instagram.com/{value_text.lstrip('@')}"
                elif key_text == "Discord":
                    url = "https://discord.com/users/anga205"
                elif key_text == "Reddit":
                    url = f"https://www.reddit.com/{value_text}"

            if url:
                svg_line = f'<a href="{url}" target="_blank">{svg_text_line}</a>'
            else:
                svg_line = svg_text_line
            
            svg_lines.append(svg_line)
        else:
            # Default white line for separators and headers
            svg_lines.append(
                f'<text x="{info_x}" y="{y_pos}" fill="white" font-size="{info_font_size}px" text-anchor="start">{html.escape(line)}</text>'
            )

    svg_lines.append('</svg>')

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(svg_lines))

    print(f"✅ SVG saved to: {output_path}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python ascii_svg_generator.py <image_path> [width] [output.svg]")
    else:
        image_path = sys.argv[1]
        width = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        output_file = sys.argv[3] if len(sys.argv) > 3 else "output.svg"
        image_to_ascii_svg(image_path, output_file, width)
