import json
import re

# Function to infer task_type based on query content
def infer_task_type(query):
    query_lower = query.lower()
    if "cube" in query_lower or "plane" in query_lower or "area" in query_lower or "volume" in query_lower:
        return "Geometry"
    elif "speed" in query_lower or "rate" in query_lower or "mph" in query_lower or "kmph" in query_lower:
        return "Algebra"
    elif "average" in query_lower or "percent" in query_lower or "wage" in query_lower:
        return "Arithmetic"
    elif "log" in query_lower or "exponent" in query_lower:
        return "Logarithms"
    elif "divisible" in query_lower or "remainder" in query_lower:
        return "Number Theory"
    else:
        return "Algebra"  # Default for math problems

# Function to infer difficulty based on gt explanation
def infer_difficulty(gt):
    lines = gt.split("\n")
    # Simple heuristic: more lines in explanation = higher difficulty
    if len(lines) <= 2:
        return "easy"
    elif len(lines) <= 4:
        return "medium"
    else:
        return "hard"

# Function to extract expected answer from gt
def extract_answer(gt, query):
    # Get the last line of gt, which typically contains "Answer: X"
    last_line = gt.split("\n")[-1].strip()
    # Extract the option letter or value (e.g., "A", "E")
    match = re.search(r"Answer\s*[:=]\s*([A-E]|\d+)", last_line)
    if match:
        answer = match.group(1)
        # If answer is a letter, try to map it to the numerical value from options
        if answer in ["A", "B", "C", "D", "E"]:
            # Extract options from query
            options_start = query.find("Choose the correct answer from the following options:")
            if options_start != -1:
                options_text = query[options_start:].split("\n")[1:]  # Get lines after options prompt
                for option in options_text:
                    if option.startswith(f"{answer})"):
                        # Extract the value (e.g., "6 kmph" → "6")
                        value = option.split(")")[1].strip()
                        # Remove units like "kmph", "miles", etc.
                        value = re.sub(r"\s*(kmph|mph|miles|km|%|seconds|hours|m)$", "", value)
                        return value
        return answer  # Return letter if no numerical value found
    return last_line  # Fallback to last line if no match

# Load input JSON file
input_file = "AQUA-RAT.json"  # Replace with your input file path
with open(input_file, "r") as f:
    data = json.load(f)

# Process each item and convert to new format
output_data = []
for i, item in enumerate(data, start=1):
    task_id = f"MATH_{i:03d}"  # e.g., MATH_001, MATH_002, ...
    output_item = {
        "task_id": task_id,
        "domain": "Mathematics",
        "task_type": infer_task_type(item["query"]),
        "prompt": item["query"],
        "expected_answer": extract_answer(item["gt"], item["query"]),
        "difficulty": infer_difficulty(item["gt"]),
        "evaluation_metric": "exact_match"
    }
    output_data.append(output_item)

# Save to output JSON file
output_file = "converted_data.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"Conversion complete. Output saved to {output_file}")


# import json

# # Input JSON data
# input_data = [
#     {"question": "Find the sum of all integer bases $b>9$ for which $17_{b}$ is a divisor of $97_{b}$.", "answer": "70"},
#     {"question": "On $\\triangle ABC$ points $A,D,E$, and $B$ lie that order on side $\\overline{AB}$ with $AD=4, DE=16$, and $EB=8$. Points $A,F,G$, and $C$ lie in that order on side $\\overline{AC}$ with $AF=13, FG=52$, and $GC=26$. Let $M$ be the reflection of $D$ through $F$, and let $N$ be the reflection of $G$ through $E$. Quadrilateral $DEGF$ has area 288. Find the area of heptagon $AFNBCEM$.", "answer": "588"},
#     {"question": "The 9 members of a baseball team went to an ice cream parlor after their game. Each player had a singlescoop cone of chocolate, vanilla, or strawberry ice cream. At least one player chose each flavor, and the number of players who chose chocolate was greater than the number of players who chose vanilla, which was greater than the number of players who chose strawberry. Let $N$ be the number of different assignments of flavors to players that meet these conditions. Find the remainder when $N$ is divided by 1000.", "answer": "16"},
#     {"question": "Find the number of ordered pairs $(x,y)$, where both $x$ and $y$ are integers between $-100$ and $100$, inclusive, such that $12x^{2}-xy-6y^{2}=0$.", "answer": "117"},
#     {"question": "There are $8!=40320$ eight-digit positive integers that use each of the digits $1,2,3,4,5,6,7,8$ exactly once. Let $N$ be the number of these integers that are divisible by 22. Find the difference between $N$ and 2025.", "answer": "279"},
#     {"question": "An isosceles trapezoid has an inscribed circle tangent to each of its four sides. The radius of the circle is 3, and the area of the trapezoid is 72. Let the parallel sides of the trapezoid have lengths $r$ and $s$, with $r \\neq s$. Find $r^{2}+s^{2}$.", "answer": "504"},
#     {"question": "The twelve letters $A,B,C,D,E,F,G,H,I,J,K$, and $L$ are randomly grouped into six pairs of letters. The two letters in each pair are placed next to each other in alphabetical order to form six two-letter words, and those six words are listed alphabetically. For example, a possible result is $AB,CJ,DG,EK,FL,HI$. The probability that the last word listed contains $G$ is $\\frac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m+n$.", "answer": "821"},
#     {"question": "Let $k$ be real numbers such that the system $|25+20i-z|=5$ and $|z-4-k|=|z-3i-k|$ has exactly one complex solution $z$. The sum of all possible values of $k$ can be written as $\\frac{m}{n}$, where $m$ and $n$ are relatively prime positive integers. Find $m+n$. Here $i=\\sqrt{-1}$.", "answer": "77"},
#     {"question": "The parabola with equation $y=x^{2}-4$ is rotated $60^{\\circ}$ counterclockwise around the origin. The unique point in the fourth quadrant where the original parabola and its image intersect has $y$-coordinate $\\frac{a-\\sqrt{b}}{c}$, where $a$, $b$, and $c$ are positive integers, and $a$ and $c$ are relatively prime. Find $a+b+c$.", "answer": "62"},
#     {"question": "The 27 cells of a $3\\times9$ grid are filled in using the numbers 1 through 9 so that each row contains 9 different numbers, and each of the three $3\\times3$ blocks heavily outlined in the example below contains 9 different numbers, as in the first three rows of a Sudoku puzzle. \n | 4 | 2 | 8 | 9 | 6 | 3 | 1 | 7 | 5 | \n | 3 | 7 | 9 | 5 | 2 | 1 | 6 | 8 | 4 | \n | 5 | 6 | 1 | 8 | 4 | 7 | 9 | 2 | 3 | \n The number of different ways to fill such a grid can be written as $p^a\\cdot q^b\\cdot r^c\\cdot s^d$, where $p,q,r,$ and $s$ are distinct prime numbers and $a,b,c,$ and $d$ are positive integers. Find $p\\cdot a+q\\cdot b+r\\cdot c+s\\cdot d$.", "answer": "81"},
#     {"question": "A piecewise linear periodic function is defined by $f(x)=\\begin{cases}x&\\text{if }x\\in[-1,1)\\\\2-x&\\text{if }x\\in[1,3)\\end{cases}$ and $f(x+4)=f(x)$ for all real numbers $x$. The graph of $f(x)$ has the sawtooth pattern. The parabola $x=34y^2$ intersects the graph of $f(x)$ at finitely many points. The sum of the $y$-coordinates of these intersection points can be expressed in the form $\\frac{a+b\\sqrt{c}}{d}$, where $a,b,c,$ and $d$ are positive integers, $a,b,$ and $d$ have greatest common divisor equal to 1, and $c$ is not divisible by the square of any prime. Find $a+b+c+d$.", "answer": "259"},
#     {"question": "The set of points in 3-dimensional coordinate space that lie in the plane $x+y+z=75$ whose coordinates satisfy the inequalities $x-yz<y-zx<z-xy$ forms three disjoint convex regions. Exactly one of those regions has finite area. The area of this finite region can be expressed in the form $a\\sqrt{b}$, where $a$ and $b$ are positive integers and $b$ is not divisible by the square of any prime. Find $a+b$.", "answer": "510"},
#     {"question": "Alex divides a disk into four quadrants with two perpendicular diameters intersecting at the center of the disk. He draws 25 more line segments through the disk, drawing each segment by selecting two points at random on the perimeter of the disk in different quadrants and connecting those two points. Find the expected number of regions into which these 27 line segments divide the disk.", "answer": "204"},
#     {"question": "Let $ABCDE$ be a convex pentagon with $AB=14, BC=7, CD=24, DE=13, EA=26,$ and $\\angle B=\\angle E=60^\\circ$. For each point $X$ in the plane, define $f(X)=AX+BX+CX+DX+EX$. The least possible value of $f(X)$ can be expressed as $m+n\\sqrt{p}$, where $m$ and $n$ are positive integers and $p$ is not divisible by the square of any prime. Find $m+n+p$.", "answer": "60"},
#     {"question": "Let $N$ denote the number of ordered triples of positive integers $(a,b,c)$ such that $a,b,c\\leq3^6$ and $a^3+b^3+c^3$ is a multiple of $3^7$. Find the remainder when $N$ is divided by $1000$.", "answer": "735"}
# ]

# # Define task types based on question content
# task_types = {
#     0: "Number Theory",
#     1: "Geometry",
#     2: "Combinatorics",
#     3: "Algebra",
#     4: "Number Theory",
#     5: "Geometry",
#     6: "Combinatorics",
#     7: "Complex Numbers",
#     8: "Geometry",
#     9: "Combinatorics",
#     10: "Geometry",
#     11: "Geometry",
#     12: "Combinatorics",
#     13: "Geometry",
#     14: "Number Theory"
# }

# # Convert to the desired format
# converted_data = [
#     {
#         "task_id": f"MATH_{str(i+1).zfill(3)}",
#         "domain": "Mathematics",
#         "task_type": task_types[i],
#         "prompt": item["question"],
#         "expected_answer": item["answer"],
#         "difficulty": "hard",
#         "evaluation_metric": "exact_match"
#     }
#     for i, item in enumerate(input_data)
# ]

# # Write to output JSON file
# with open('output.json', 'w') as file:
#     json.dump(converted_data, file, indent=2)