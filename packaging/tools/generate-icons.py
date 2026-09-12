#!/usr/bin/env python3
"""用 Python 标准库生成固定尺寸 PNG；图形源为下面的圆角底板与五根声波柱。"""
import argparse
from pathlib import Path
import struct
import zlib


def rounded(x, y, x0, y0, x1, y1, radius):
    cx = min(max(x, x0 + radius), x1 - radius)
    cy = min(max(y, y0 + radius), y1 - radius)
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius**2


def render(size):
    """4 倍超采样；坐标统一使用 64px 画布，无字体、网络或图形库依赖。"""
    pixels = bytearray()
    for y in range(size):
        pixels.append(0)
        for x in range(size):
            samples = []
            for sy in range(4):
                for sx in range(4):
                    px = (x + (sx + 0.5) / 4) * 64 / size
                    py = (y + (sy + 0.5) / 4) * 64 / size
                    color = (245, 247, 244, 0)
                    if rounded(px, py, 3, 3, 61, 61, 14):
                        color = (28, 83, 68, 255)
                    for center, height in [(18, 12), (25, 23), (32, 34), (39, 23), (46, 12)]:
                        if rounded(px, py, center - 2, 32 - height / 2, center + 2, 32 + height / 2, 2):
                            color = (241, 248, 231, 255)
                    samples.append(color)
            pixels.extend(round(sum(c[i] for c in samples) / len(samples)) for i in range(4))

    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))

    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', size, size, 8, 6, 0, 0, 0))
            + chunk(b'sRGB', b'\0') + chunk(b'IDAT', zlib.compress(bytes(pixels), 9)) + chunk(b'IEND', b''))


def generate(root):
    for size, name in [(64, 'ICON.PNG'), (256, 'ICON_256.PNG')]:
        data = render(size)
        (root / name).write_bytes(data)
        images = root / 'app/ui/images'
        images.mkdir(parents=True, exist_ok=True)
        (images / f'icon_{size}.png').write_bytes(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1] / 'fpk')
    generate(parser.parse_args().root)
