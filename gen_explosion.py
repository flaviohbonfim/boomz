
import sys

palette = {
    'W': '#ffffff', # White (Core)
    'Y': '#ffd700', # Yellow (Hot)
    'O': '#ff8c00', # Orange (Fire)
    'R': '#ff4500', # Red (Edges)
    'D': '#b22222', # Dark Red (Shadow)
    'S': '#2a0c0c', # Deep Shadow
}

# Connection Profiles (indices that MUST have pixels at the boundary)
PROFILES = [
    range(3, 13), # Frame 0: 10px wide (3 to 12)
    range(5, 11), # Frame 1: 6px wide (5 to 10)
    range(7, 9)   # Frame 2: 2px wide (7 to 8)
]

def get_base_color(dist, max_dist, frame_idx):
    """Simple color ramp based on distance from center/axis."""
    if dist < 2 - frame_idx: return 'W'
    if dist < 4 - frame_idx: return 'Y'
    if dist < 6 - frame_idx: return 'O'
    if dist < 8 - frame_idx: return 'R'
    if dist < 9: return 'D'
    return 'S'

def render_svg_rects(pixels, x_off, y_off):
    svg_parts = []
    for (x, y), char in pixels.items():
        if char in palette:
            svg_parts.append(f'<rect x="{x_off+x}" y="{y_off+y}" width="1" height="1" fill="{palette[char]}"/>')
    return '\n'.join(svg_parts)

def create_frame(type, frame_idx):
    pixels = {}
    prof = PROFILES[frame_idx]
    
    if type == "center":
        # Must connect on all 4 sides using 'prof'
        for y in range(16):
            for x in range(16):
                dx = abs(x - 7.5)
                dy = abs(y - 7.5)
                dist = max(dx, dy)
                
                # Check if we are at an edge and if we should be "on"
                is_edge_x = (x == 0 or x == 15)
                is_edge_y = (y == 0 or y == 15)
                
                if is_edge_x:
                    if y not in prof: continue
                if is_edge_y:
                    if x not in prof: continue
                
                # Core logic for center
                d_center = (dx**2 + dy**2)**0.5
                if d_center < 7 - (frame_idx * 1.5):
                    char = get_base_color(d_center, 8, frame_idx)
                    pixels[(x, y)] = char
        
        # Ensure ports are filled
        for i in prof:
            pixels[(0, i)] = pixels.get((1, i), 'D')
            pixels[(15, i)] = pixels.get((14, i), 'D')
            pixels[(i, 0)] = pixels.get((i, 1), 'D')
            pixels[(i, 15)] = pixels.get((i, 14), 'D')

    elif type == "h-mid":
        # Must connect on left (0) and right (15)
        for y in range(16):
            for x in range(16):
                dy = abs(y - 7.5)
                if y in prof:
                    char = get_base_color(dy, 8, frame_idx)
                    # Add some internal variation
                    idx_var = (x + frame_idx) % 4
                    if idx_var == 0 and char == 'Y': char = 'W'
                    pixels[(x, y)] = char
        # Ensure edges match profile exactly
        for y in range(16):
            if y not in prof:
                pixels.pop((0, y), None)
                pixels.pop((15, y), None)

    elif type == "v-mid":
        # Must connect on top (0) and bottom (15)
        for y in range(16):
            for x in range(16):
                dx = abs(x - 7.5)
                if x in prof:
                    char = get_base_color(dx, 8, frame_idx)
                    idx_var = (y + frame_idx) % 4
                    if idx_var == 0 and char == 'Y': char = 'W'
                    pixels[(x, y)] = char
        for x in range(16):
            if x not in prof:
                pixels.pop((x, 0), None)
                pixels.pop((x, 15), None)

    elif type == "h-end":
        # Connect on left (0), taper on right (15)
        for y in range(16):
            for x in range(16):
                dy = abs(y - 7.5)
                # Tapering logic: profile shrinks as x increases
                # Taper starts at x=2, ends at x=14
                taper_factor = max(0, 1.0 - (x / 14.0))
                effective_dy = dy / (taper_factor + 0.001)
                
                if y in prof and effective_dy < 8:
                    char = get_base_color(effective_dy, 8, frame_idx)
                    pixels[(x, y)] = char
        # Clean edges
        for y in range(16):
            if y not in prof: pixels.pop((0, y), None)

    elif type == "v-end":
        # Connect on top (0), taper on bottom (15)
        for y in range(16):
            for x in range(16):
                dx = abs(x - 7.5)
                taper_factor = max(0, 1.0 - (y / 14.0))
                effective_dx = dx / (taper_factor + 0.001)
                
                if x in prof and effective_dx < 8:
                    char = get_base_color(effective_dx, 8, frame_idx)
                    pixels[(x, y)] = char
        for x in range(16):
            if x not in prof: pixels.pop((x, 0), None)

    return pixels

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="80" viewBox="0 0 48 80" shape-rendering="crispEdges">\n'
svg += '  <rect width="48" height="80" fill="none"/>\n'

types = ["center", "h-mid", "v-mid", "h-end", "v-end"]
for row_idx, t in enumerate(types):
    for col_idx in range(3):
        pixels = create_frame(t, col_idx)
        svg += render_svg_rects(pixels, col_idx * 16, row_idx * 16) + '\n'

svg += '</svg>'
print(svg)
