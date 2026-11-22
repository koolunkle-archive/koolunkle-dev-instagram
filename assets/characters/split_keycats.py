# keycats.png(흰 배경 3컷) -> keycat-angry/anxious/healing.png, keycat.png -> keycat-smile.png
# 배경 = 테두리에서 이어진 거의 흰 픽셀만 투명 처리 (몸통도 흰색이라 임계값만으론 안 됨, 검은 외곽선이 경계)
import sys, numpy as np, cv2
from PIL import Image
D = sys.argv[1] if len(sys.argv) > 1 else '.'

def cutout(rgba, pad=40):
    a = rgba.copy(); rgb = a[..., :3].astype(int)
    if (a[..., 3] == 0).mean() < .05:  # 불투명 흰 배경일 때만
        near = ((rgb.min(-1) > 232) & (rgb.max(-1) - rgb.min(-1) < 14)).astype(np.uint8)
        h, w = near.shape; m = np.zeros((h + 2, w + 2), np.uint8)
        for x, y in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
            if near[y, x] and not m[y + 1, x + 1]:
                cv2.floodFill(near, m, (x, y), 2, flags=4 | (2 << 8))
        a[near == 2, 3] = 0
    a[a[..., 3] < 24, 3] = 0  # 반투명 잡티 제거
    ys, xs = np.nonzero(a[..., 3] > 0)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    s = max(a.shape[:2]) + pad; out = np.zeros((s, s, 4), np.uint8)
    y0, x0 = s - 20 - a.shape[0] if pad == 40 else s - a.shape[0] - pad // 6, (s - a.shape[1]) // 2  # 바닥 정렬
    out[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
    return Image.fromarray(out)

sheet = np.array(Image.open(f'{D}/keycats.png').convert('RGBA'))
for name, (x0, x1) in zip(['angry', 'anxious', 'healing'], [(0, 585), (585, 1170), (1170, 1792)]):
    cutout(sheet[:, x0:x1]).save(f'{D}/keycat-{name}.png')
cutout(np.array(Image.open(f'{D}/keycat.png').convert('RGBA')), pad=220).save(f'{D}/keycat-smile.png')  # 효과 없는 컷이라 여백을 더 줘 몸통 크기를 맞춤
