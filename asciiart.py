from PIL import Image
import sys
from datetime import datetime, timezone
from github_functions import get_total_contributions
import html

# ASCII characters from darkest to lightest
ASCII_CHARS = "@%#*+=-:. "
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
    timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p %Z')[:-1]
    output = f"• Last Updated: "
    while (len(output) + len(timestamp)) < 60:
        output += "."
    return f"{output}{timestamp}"

def get_git_contributions():
    contributions = f"{get_total_contributions():,}"
    output = "• Github Contributions: "
    while (len(output) + len(contributions)) < 60:
        output += "."
    return f"{output}{contributions}"

INFO = f"""
Angad@Bhalla
————————————————————————————————————————————————————————————
• OS: .............................Debian 12, Android, Linux
{get_age_line(1117650600)}
• Host: ....................................Bangalore, India
• IDE: ...................................Visual Studio Code
• Portfolio: .............................https://anga.codes

• Languages.Programming: ......Python, C, JavaScript, GoLang
• Languages.Real: ............................English, Hindi
• Languages.Markup: ...................Markdown, HTML, LaTeX

• Web.Frameworks: ...........ReactJS, SolidJS, Svelte, VueJS
• Web.Tools: .....................Vite, Next.js, TailwindCSS
• Backend.Frameworks: .......Gin, FastAPI, Django, ExpressJS

———————————————————————— Contact ———————————————————————————
• Email: ..............................sayhi@angadbhalla.com
• Linkedin: ....................https://linkedin.com/in/anga
• Instagram: ......................................@_anga205
• Discord: .........................................@anga205

—————————————————————————— Stats ———————————————————————————
{get_git_contributions()}
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

    # Start SVG
    svg_lines = []
    svg_lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width + sidebar_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width + sidebar_width} {svg_height}" '
        f'style="background:#171717">'
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
                xpos = x * FONT_SIZE
                ypos = y * FONT_SIZE
                svg_lines.append(
                    f'<text x="{xpos}" y="{ypos}" fill="{fill}" font-size="{FONT_SIZE}px" text-anchor="middle">{char}</text>'
                )

    # Render INFO block
    info_x = svg_width + FONT_SIZE * 2  # padding from ASCII art

    for i, line in enumerate(info_lines):
        y_pos = int((i + 0.5) * line_height)

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
            svg_line = (
                f'<text x="{info_x}" y="{y_pos}" font-size="{info_font_size}px" text-anchor="start" style="white-space: pre;">'
                f'<tspan fill="white">{html.escape(bullet_part)}</tspan>'
                f'<tspan fill="orange">{html.escape(key_part)}</tspan>'
                f'<tspan fill="white">{html.escape(dots_part)}</tspan>'
                f'<tspan fill="lime">{html.escape(value_part)}</tspan>'
                f'</text>'
            )
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
