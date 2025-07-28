import pandas as pd
import plotly.graph_objects as go

# === 1. Wczytaj dane ===
df = pd.read_csv("DemoProject_state0_28.07.2025_10-37.csv")

# === 2. Przygotuj serie czasu i wypisz dostępne kolumny ===
time = df.iloc[:, 0]
data_columns = df.columns[1:]
print("Dostępne kolumny:")
for i, col in enumerate(data_columns):
    print(f"{i}: {col}")

# === 3. Wybór kolumn przez użytkownika ===
user_input = input("Podaj numery kolumn (np. 0,2:5): ")
def parse_indices(s):
    idx = set()
    for part in s.split(','):
        part = part.strip()
        if ':' in part:
            a, b = map(int, part.split(':'))
            idx.update(range(a, b+1))
        else:
            idx.add(int(part))
    return sorted(idx)

selected_idxs = parse_indices(user_input)
selected_columns = [data_columns[i] for i in selected_idxs]

# === 4. Grupuj po jednostkach (tekst w nawiasach kwadratowych) ===
unit_groups = {}
for col in selected_columns:
    if "[" in col and "]" in col:
        unit = col.split("[")[-1].split("]")[0].strip()
    else:
        unit = "unknown"
    unit_groups.setdefault(unit, []).append(col)

# === 5. Twórz trace’y ===
fig = go.Figure()
color_pool = [
    "#1f77b4", "#ff7f0e", "#217021", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#e7e724", "#17becf",
    "#00090a", "#5fee33", "#fcba03", "#a14ba0"
]
ci = 0
ycount = 1
yaxis_map = {}  # {unit: (axis_id, layout_key)}

for unit, cols in unit_groups.items():
    axis_id  = "y" if ycount == 1 else f"y{ycount}"
    layout_key = "yaxis" if axis_id == "y" else f"yaxis{axis_id[1:]}"
    yaxis_map[unit] = (axis_id, layout_key)
    for col in cols:
        fig.add_trace(go.Scatter(
            x=time,
            y=df[col],
            mode='lines+markers',
            name=col,
            marker=dict(color=color_pool[ci % len(color_pool)]),
            yaxis=axis_id
        ))
        ci += 1
    ycount += 1

# === 6. Bazowy layout ===
layout = dict(
    title="D20TIC0188: 10% Downstep",
    xaxis=dict(title=df.columns[0]),
    hovermode='x unified',
    width=1400,
    height=700
)

# === 7. Konfiguracja każdej osi Y z overlaying + position ===
left_count = 0
right_count = 0

for i, (unit, (axis_id, layout_key)) in enumerate(yaxis_map.items()):
    # która strona: parzyste → left, nieparzyste → right
    side = 'left' if i % 2 == 0 else 'right'
    axis_cfg = dict(
        title=dict(text=unit, font=dict(color=color_pool[i % len(color_pool)])),
        side=side,
        showgrid=False,
        tickfont=dict(color=color_pool[i % len(color_pool)]),
        autorange=True
    )

    if axis_id != "y":
        # nakładamy na główną oś
        axis_cfg['overlaying'] = 'y'
        # żeby position zadziałało, używamy anchor='free'
        axis_cfg['anchor'] = 'free'
        # ustawiamy przesunięcie w skali 0–1
        if side == 'left':
            axis_cfg['position'] = left_count * 0.05
            left_count += 1
        else:
            axis_cfg['position'] = 1 - right_count * 0.05
            right_count += 1
    else:
        # główna oś Y
        axis_cfg['anchor'] = 'x'

    layout[layout_key] = axis_cfg

# === 8. Zaktualizuj layout i zapisz ===
fig.update_layout(layout)
fig.write_html("interaktywny_wykres.html")
print("✅ Gotowe! Wykres zapisany jako 'interaktywny_wykres.html'")
