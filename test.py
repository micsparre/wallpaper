from screeninfo import get_monitors, Enumerator

monitors = get_monitors(Enumerator.OSX)

for monitor in monitors:
    print(f"Monitor: {monitor.name}")
    print(f"Width: {monitor.width} pixels")
    print(f"Height: {monitor.height} pixels")
    print(f"Position: ({monitor.x}, {monitor.y})\n")
