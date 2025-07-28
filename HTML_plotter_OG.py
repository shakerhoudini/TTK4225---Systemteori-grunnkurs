import pandas as pd
import plotly.graph_objects as go

# === 1. Wczytaj dane ===
df = pd.read_csv("DemoProject_state0_28.07.2025_10-37.csv")

time = df[df.columns[0]]
data_columns = df.columns[1:]

print("Available columns for plotting:")
for i, col in enumerate(data_columns):
    print(f"{i}: {col}")

# === 2. Wybierz kolumny do rysowania ===
user_input = input("Enter the column numbers to plot (e.g., 0,1,2,3:10,14:24,29): ")

def parse_indices(input_str):
    indices = set()
    parts = input_str.split(',')
    for part in parts:
        if ':' in part:
            start, end = map(int, part.split(':'))
            indices.update(range(start, end + 1))
        else:
            indices.add(int(part))
    return sorted(indices)

selected_indices = parse_indices(user_input)
selected_columns = [data_columns[i] for i in selected_indices]

# === 3. Grupuj kolumny według jednostek ===
unit_groups = {}
for col in selected_columns:
    if "[" in col and "]" in col:
        unit = col.split("[")[-1].split("]")[0].strip()
    else:
        unit = "unknown"
    unit_groups.setdefault(unit, []).append(col)

# === 4. Twórz wykres ===
fig = go.Figure()
color_pool = [
    "#1f77b4", "#ff7f0e", "#217021", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#e7e724", "#17becf",
    "#00090a", "#5fee33", "#fcba03", "#a14ba0"
]

color_index = 0
yaxis_count = 1
yaxis_map = {}

# === 5. Dodaj linie ===
for unit, cols in unit_groups.items():
    axis_id = f'y{yaxis_count}' if yaxis_count > 1 else 'y'
    yaxis_map[unit] = axis_id

    for col in cols:
        fig.add_trace(go.Scatter(
            x=time,
            y=df[col],
            mode='lines+markers',
            name=col,
            marker=dict(color=color_pool[color_index % len(color_pool)]),
            yaxis=axis_id
        ))
        color_index += 1
    yaxis_count += 1

# === 6. Layout bazowy ===
layout = dict(
    title="D20TIC0188: 10% Downstep",
    xaxis=dict(title=df.columns[0]),
    hovermode='x unified',
    width=1400,
    height=700
)

# === 7. Dynamiczne, estetyczne Y-axes ===
for i, (unit, axis_id) in enumerate(yaxis_map.items()):
    axis_key = f'yaxis{"" if axis_id == "y" else axis_id[1:]}'
    side = 'left' if i % 2 == 0 else 'right'
    position = 0.05 + i * 0.07  # rozsuń osie

    layout[axis_key] = dict(
        title=dict(text=unit, font=dict(color=color_pool[i % len(color_pool)])),
        anchor='x',
        side=side,
        position=position,
        showgrid=False,
        tickfont=dict(color=color_pool[i % len(color_pool)])
    )

fig.update_layout(layout)

# === 8. Zapisz HTML ===
fig.write_html("interaktywny_wykres.html")
print("✅ Zapisano: interaktywny_wykres.html – otwórz w przeglądarce.")
