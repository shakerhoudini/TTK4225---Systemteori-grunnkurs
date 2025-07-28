# === 7. Rozkład osi bez overlay, z pozycjami ===
for i, (unit, (axis_id, axis_key)) in enumerate(yaxis_map.items()):
    side = 'left' if i % 2 == 0 else 'right'
    position = 0.05 + i * 0.07  # odsuwamy o 7% na każdą oś

    # podstawowa konfiguracja osi
    axis_config = dict(
        title=dict(text=unit, font=dict(color=color_pool[i % len(color_pool)])),
        anchor='x',
        side=side,
        position=position,
        showgrid=False,
        tickfont=dict(color=color_pool[i % len(color_pool)]),
        autorange=True
    )
    # <<< tu jest kluczowa zmiana: nakładamy każdą dodatkową oś na główną Y
    if axis_id != 'y':
        axis_config['overlaying'] = 'y'

    layout[axis_key] = axis_config
