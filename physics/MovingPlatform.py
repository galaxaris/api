def update_moving_platform(moving_platforms):
    for mp in moving_platforms:
        s = mp["solid"]
        mp["_current"] += mp["speed"] * mp["direction"]

        ### Plateformes horizontales
        if mp["axis"] == "x":
            x_new = int(mp["_current"])
            s.rect.x = x_new
            try:
                s.pos[0] = float(mp["_current"])
            except (TypeError, AttributeError):
                pass
            if mp["_current"] >= mp["max_x"] or mp["_current"] <= mp["min_x"]:
                mp["direction"] *= -1

        ### Plateformes verticales
        elif mp["axis"] == "y":
            y_new = int(mp["_current"])
            s.rect.y = y_new
            try:
                s.pos[1] = float(mp["_current"])
            except (TypeError, AttributeError):
                pass
            if mp["_current"] >= mp["max_y"] or mp["_current"] <= mp["min_y"]:
                mp["direction"] *= -1