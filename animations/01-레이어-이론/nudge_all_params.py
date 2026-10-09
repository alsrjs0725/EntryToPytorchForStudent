"""분류 모델의 파라미터 65개 모두에 '조금 늘려 보고 줄여 보기'를 해서 방향(↑/↓)을 찾고, lr만큼 옮기기를 되풀이합니다."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from manim import (
    DOWN,
    RESAMPLING_ALGORITHMS,
    UP,
    WHITE,
    Arrow,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    LaggedStart,
    ManimColor,
    Line,
    Rectangle,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    smooth,
)

from common.style import COLOR_BIAS, COLOR_GRAD, COLOR_LOSS, COLOR_OUTPUT, COLOR_TEXT, COLOR_WEIGHT, ko
from common.tensor import code

# 노트북 01-04와 같은 값입니다. torch.manual_seed(0) 뒤 init_params()의 W1, W2 (소수 넷째 자리까지)
W1_INIT = [
    [-0.5629, -0.5762], [-0.1253, -0.2169], [0.4244, 0.346], [-0.158, -1.0576],
    [0.1611, -0.6317], [0.175, 0.1541], [0.0599, 0.6188], [0.5584, -0.1236],
    [-0.6763, -0.848], [0.2833, 0.3968], [0.2994, -0.7775], [-0.1707, 0.9265],
    [0.3751, -0.2927], [-0.0867, 0.0917], [0.6947, 0.7932], [0.4731, -0.4218],
]
W2_INIT = [
    -0.3068, 0.0158, -0.2463, 0.1242, 0.2198, 0.0562, 0.3204, 0.2206,
    -0.0512, 0.3962, -0.1448, 0.0263, 0.2614, 1.1511, -0.7344, -0.7933,
]
NUDGE = 0.1
LR = 0.5
SHOW_STEPS = [1, 3, 10, 30, 100, 300, 1000]

CLASS0 = ManimColor("#5B8DEF")  # 원 바깥 (0)
CLASS1 = ManimColor("#E8604C")  # 원 안쪽 (1)
NAMES = ["W1", "b1", "W2", "b2"]


def load_data():
    # torch.manual_seed(0) 뒤 torch.rand(400, 2) * 4 - 2 를 소수 셋째 자리까지 적은 값
    x = np.array(X_DATA.split(), dtype=float).reshape(400, 2) / 1000
    y = ((x ** 2).sum(axis=1) < 1.5).astype(float)
    return x, y


X, Y = None, None


def init_params():
    return {"W1": np.array(W1_INIT), "b1": np.zeros(16), "W2": np.array(W2_INIT), "b2": np.zeros(1)}


def logits(p, x):
    h = np.maximum(x @ p["W1"].T + p["b1"], 0)  # (N, 16)
    return h @ p["W2"] + p["b2"][0]  # (N,)


def loss(p):
    z = logits(p, X)
    return float(np.mean(np.maximum(z, 0) - z * Y + np.log1p(np.exp(-np.abs(z)))))


def grads(p):
    """loss.backward()가 구하는 기울기와 같은 값."""
    pre = X @ p["W1"].T + p["b1"]
    h = np.maximum(pre, 0)
    dz = (1 / (1 + np.exp(-(h @ p["W2"] + p["b2"][0]))) - Y) / len(Y)
    dh = np.outer(dz, p["W2"]) * (pre > 0)
    return {"W1": dh.T @ X, "b1": dh.sum(axis=0), "W2": h.T @ dz, "b2": np.array([dz.sum()])}


def nudged(p, name, index, delta):
    q = {k: v.copy() for k, v in p.items()}
    q[name][index] += delta
    return q


def train():
    """SHOW_STEPS에 해당하는 단계의 파라미터를 모아 둡니다."""
    p = init_params()
    snapshots = {}
    for step in range(1, SHOW_STEPS[-1] + 1):
        g = grads(p)
        p = {k: p[k] - LR * g[k] for k in p}
        if step in SHOW_STEPS:
            snapshots[step] = {k: v.copy() for k, v in p.items()}
    return snapshots


def f2(v):
    return f"{v:.2f}".replace("-0.00", "0.00")


class NudgeAllParams(Scene):
    def construct(self):
        global X, Y
        X, Y = load_data()
        params = init_params()

        # 왼쪽: 데이터와 모델의 예측. 배경색은 확률, 흰 선은 확률 0.5인 결정 경계예요.
        size, center = 6.0, np.array([-3.95, -0.15, 0])

        def to_screen(x0, x1):
            return center + np.array([x0, x1, 0]) * size / 4

        n_bg = 100
        coords = (np.arange(n_bg) + 0.5) / n_bg * 4 - 2
        bg_points = np.array([(a, b) for b in coords[::-1] for a in coords])  # 그림의 위쪽 줄부터
        c0, c1 = np.array(CLASS0.to_rgb()), np.array(CLASS1.to_rgb())
        n_line = 41
        line_coords = np.linspace(-2, 2, n_line)
        line_points = np.array([(a, b) for b in line_coords for a in line_coords])

        def field(p):
            prob = 1 / (1 + np.exp(-logits(p, bg_points)))
            rgb = (c0 + (c1 - c0) * prob[:, None]) * 0.45  # 검은 배경 위에 반투명하게 깐 색
            image = ImageMobject((rgb.reshape(n_bg, n_bg, 3) * 255).astype(np.uint8))
            image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
            image.set_height(size).move_to(center)
            z = logits(p, line_points).reshape(n_line, n_line)
            segments = VGroup()
            for i in range(n_line - 1):
                for j in range(n_line - 1):
                    corners = [(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)]
                    cross = []
                    for (a, b), (c, d) in zip(corners, corners[1:] + corners[:1]):
                        za, zc = z[a, b], z[c, d]
                        if (za > 0) != (zc > 0):
                            t = za / (za - zc)
                            ya = line_coords[a] + t * (line_coords[c] - line_coords[a])
                            xa = line_coords[b] + t * (line_coords[d] - line_coords[b])
                            cross.append(to_screen(xa, ya))
                    for k in range(0, len(cross) - 1, 2):
                        segments.add(Line(cross[k], cross[k + 1], color=WHITE, stroke_width=3))
            return Group(image, segments)

        frame = Square(size, stroke_color=COLOR_TEXT, stroke_width=1.5).move_to(center)
        dots = VGroup(*[
            Square(0.07, stroke_width=0, fill_opacity=1, fill_color=CLASS1 if yy else CLASS0).rotate(np.pi / 4).move_to(to_screen(*xx))
            for xx, yy in zip(X, Y)
        ]).set_z_index(1)
        plot = field(params)

        def status(step, value):
            return VGroup(
                ko(f"step {step}", size=26),
                ko(f"손실 {value:.4f}", size=26, color=COLOR_LOSS),
            ).arrange(buff=0.5).next_to(frame, UP, buff=0.15)

        header = status(0, loss(params))

        # 오른쪽: 파라미터 표. 한 줄이 은닉 뉴런 하나의 값이에요 (W1 두 칸, b1, W2ᵀ).
        cw, ch = 0.95, 0.335
        col_x = {("W1", 0): -0.25, ("W1", 1): 0.7, ("b1", 0): 1.8, ("W2", 0): 2.9, ("b2", 0): 4.05}
        top = 2.75

        def cell_pos(name, index):
            if name == "W1":
                return np.array([col_x[("W1", index[1])], top - index[0] * ch, 0])
            if name == "b2":
                return np.array([col_x[("b2", 0)], top, 0])
            return np.array([col_x[(name, 0)], top - index[0] * ch, 0])

        def color_of(name):
            return COLOR_WEIGHT if name.startswith("W") else COLOR_BIAS

        def all_indices():
            for name in NAMES:
                for index in np.ndindex(params[name].shape):
                    yield name, index

        order = list(all_indices())
        boxes = VGroup(*[
            Rectangle(width=cw, height=ch, stroke_color=color_of(n), stroke_width=1.5, fill_color=color_of(n), fill_opacity=0.12).move_to(cell_pos(n, i))
            for n, i in order
        ])

        def number(p, name, index, color=COLOR_TEXT):
            return Text(f2(p[name][index]), font="Noto Sans Mono CJK KR", font_size=16, color=color).move_to(
                cell_pos(name, index) + np.array([-0.13, 0, 0])
            ).set_z_index(1)

        def numbers_of(p):
            return VGroup(*[number(p, n, i) for n, i in order])

        def arrow_at(name, index, up):
            c = cell_pos(name, index) + np.array([0.32, 0, 0])
            half = 0.13 * (1 if up else -1)
            return Arrow(c - [0, half, 0], c + [0, half, 0], buff=0, color=COLOR_GRAD, stroke_width=5,
                         max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=30).set_z_index(1)

        def arrows_of(p):
            g = grads(p)
            return VGroup(*[arrow_at(n, i, g[n][i] < 0) for n, i in order])

        numbers = numbers_of(params)
        labels = VGroup(
            ko("W1", size=24, color=COLOR_WEIGHT).move_to([(col_x[("W1", 0)] + col_x[("W1", 1)]) / 2, top + 0.45, 0]),
            ko("b1", size=24, color=COLOR_BIAS).move_to([col_x[("b1", 0)], top + 0.45, 0]),
            ko("W2ᵀ", size=24, color=COLOR_WEIGHT).move_to([col_x[("W2", 0)], top + 0.45, 0]),
            ko("b2", size=24, color=COLOR_BIAS).move_to([col_x[("b2", 0)], top + 0.45, 0]),
        )
        table = VGroup(boxes, labels)

        caption = ko("학습 전 모델이에요. 흰 선이 결정 경계예요", size=24).to_edge(DOWN, buff=0.25)

        def say(text, color=COLOR_TEXT):
            return Transform(caption, ko(text, size=24, color=color).move_to(caption))

        def held(ratio):
            """앞쪽 ratio만큼의 시간에 움직이고 나머지는 멈춰 있는 rate_func. wait()를 따로 부르지 않아 영상이 가벼워져요."""
            return lambda t: smooth(min(1.0, t / ratio))

        self.play(FadeIn(frame), FadeIn(plot), FadeIn(dots), FadeIn(header), FadeIn(caption), run_time=2.5, rate_func=held(0.4))
        self.play(
            FadeIn(table), FadeIn(numbers), say("파라미터는 65개예요. W1 32개, b1 16개, W2 16개, b2 1개"),
            run_time=3, rate_func=held(0.35),
        )

        # 1. 처음 두 칸은 천천히: 0.1 늘려 보고, 줄여 보고, 손실이 줄어든 쪽을 화살표로 남겨요.
        note_x = 5.75
        found = VGroup()
        for k, (name, index) in enumerate(order[:2]):
            slow = k == 0
            label = f"{name}[{', '.join(map(str, index))}]"
            focus = SurroundingRectangle(boxes[k], color=COLOR_TEXT, buff=0.03, stroke_width=3).set_z_index(2)
            notes = VGroup(ko(label, size=22, color=color_of(name)).move_to([note_x, 2.2, 0]))
            self.play(FadeIn(focus), FadeIn(notes[0]), run_time=0.4)
            results = []
            for sign in (1, -1):
                q = nudged(params, name, index, sign * NUDGE)
                results.append(loss(q))
                note = ko(f"{'+' if sign > 0 else '−'}{NUDGE} → {results[-1]:.4f}", size=20)
                note.move_to([note_x, 1.7 - 0.45 * (len(notes) - 1), 0])
                notes.add(note)
                extra = [say(f"{label}을 {NUDGE}만큼 {'늘려' if sign > 0 else '줄여'} 봐요")] if slow else []
                self.play(
                    Transform(numbers[k], number(q, name, index, COLOR_OUTPUT)),
                    Transform(plot, field(q)),
                    Transform(header, status(0, results[-1])),
                    FadeIn(note),
                    *extra,
                    run_time=1.8 if slow else 0.8,
                    rate_func=held(0.5),
                )
            up = results[0] < results[1]
            arrow = arrow_at(name, index, up)
            extra = [say(f"{'늘렸을' if up else '줄였을'} 때 손실이 작아요. {'↑' if up else '↓'}로 표시해요", color=COLOR_GRAD)] if slow else []
            self.play(
                Transform(numbers[k], number(params, name, index)),
                Transform(plot, field(params)),
                Transform(header, status(0, loss(params))),
                notes[1 if up else 2].animate.set_color(COLOR_GRAD),
                FadeIn(arrow),
                *extra,
                run_time=1.8 if slow else 0.9,
                rate_func=held(0.4),
            )
            found.add(arrow)
            self.play(FadeOut(notes), FadeOut(focus), run_time=0.3)

        # 2. 나머지 63칸도 같은 방법으로 채워요.
        first = arrows_of(params)
        rest = VGroup(*first[2:])
        self.play(
            say("나머지 63개도 하나씩 같은 방법으로 해 봐요"),
            LaggedStart(*[FadeIn(a, scale=1.5) for a in rest], lag_ratio=0.08),
            run_time=4.5,
        )
        arrows = VGroup(*found, *rest)

        # 3. 실제로는 미분으로 한 번에 구해요.
        backward = code("loss.backward()", size=24).move_to([note_x, 2.0, 0])
        self.play(say("실제로는 하나씩 해 보지 않고, 미분으로 65개 방향을 한 번에 구해요"), FadeIn(backward), run_time=3, rate_func=held(0.2))

        # 4. 화살표 방향으로 lr × 기울기만큼 옮기기를 되풀이해요.
        snapshots = train()
        p = snapshots[1]
        g00 = grads(params)["W1"][0, 0]
        example = VGroup(  # 예: W1[0, 0]은 -0.56 − 0.5 × 0.03 = -0.58
            ko("W1[0, 0]", size=20, color=COLOR_WEIGHT),
            ko(f"{f2(params['W1'][0, 0])} − {LR} × {g00:.2f}", size=20),
            ko(f"= {f2(p['W1'][0, 0])}", size=20, color=COLOR_OUTPUT),
        ).arrange(DOWN, buff=0.15).move_to([note_x, 1.8, 0])
        focus = SurroundingRectangle(boxes[0], color=COLOR_TEXT, buff=0.03, stroke_width=3).set_z_index(2)
        self.play(
            say(f"화살표 방향으로 lr × 기울기만큼 옮겨요 (lr = {LR})"),
            FadeOut(backward), FadeIn(example), FadeIn(focus),
            run_time=2, rate_func=held(0.25),
        )
        self.play(
            Transform(numbers, numbers_of(p)), Transform(plot, field(p)), Transform(header, status(1, loss(p))),
            run_time=2.5, rate_func=held(0.6),
        )
        self.play(
            FadeOut(example), FadeOut(focus), say("옮긴 자리에서 방향을 다시 구해요"), Transform(arrows, arrows_of(p)),
            run_time=2, rate_func=held(0.4),
        )
        self.play(say("이 과정을 되풀이하면 경계가 원을 찾아가요"), run_time=0.4)
        for step in SHOW_STEPS[1:]:
            p = snapshots[step]
            self.play(
                Transform(numbers, numbers_of(p)),
                Transform(plot, field(p)),
                Transform(header, status(step, loss(p))),
                Transform(arrows, arrows_of(p)),
                run_time=1.3,
                rate_func=held(0.6),
            )
        self.play(say(f"{SHOW_STEPS[-1]}단계 뒤 손실 {loss(p):.4f}. 원 안쪽을 골라내요", color=COLOR_OUTPUT), run_time=3, rate_func=held(0.15))

X_DATA = """
-15 1073 -1646 -1472 -770 536 -40 1586 -177 529 -604 -393 -1911 -1325 -824 74 791 1200 -1356
-871 726 1661 -412 1497 -322 212 1811 -1855 -1259 -506 -780 1728 -1296 -921 -1397 -1873 -1167
1719 892 969 105 -1025 338 -1867 -1445 -1031 1262 1173 -887 -72 1279 1988 794 270 1341 -1178 373
-1551 -1386 -1033 905 804 -1185 604 1098 -252 76 463 1241 1920 -1541 -733 786 1657 1740 1765 398
-1739 184 -1251 -1864 1777 1521 -1995 374 -337 -329 -916 769 -1185 733 1011 1432 748 -1979 -1297
999 419 -1560 -1152 1881 1348 -872 -503 -1905 -36 -1506 -1543 -110 300 -819 1187 -1217 1815 1371
-1687 -498 90 292 474 785 120 -976 946 -1918 -1185 -501 -974 -700 -1639 -425 428 -1303 -103 1432
-206 56 -173 405 1272 1894 1270 1899 -145 -1797 -948 1362 -13 -994 -1533 -1872 -1688 -406 1097
1081 -1929 1248 -1565 -423 -811 -385 -393 -1795 -1727 -313 26 -909 753 -1800 -135 1759 -816 1806
724 -1805 1265 -231 -893 1599 -1616 215 -419 1428 558 961 706 -481 -421 -1648 1084 1588 1368
-1411 89 -1410 -1101 -1165 683 -1192 -44 84 1289 -1512 -1373 -1161 1400 -719 1687 723 253 -15
-395 251 -457 -14 255 -1564 -1048 1615 -1623 -144 1978 722 57 -1733 991 -1425 -568 -671 -296 22
1650 250 1791 1223 -1264 897 -1414 -848 588 660 1500 -644 3 1030 -1934 1446 -1654 28 -340 -1053
264 1654 -585 -1187 -740 -1982 903 -961 -1335 -1152 1150 1059 1535 725 -668 -559 591 1644 544
-946 -940 -1891 432 -1122 -1783 1754 -1299 -228 573 64 -1346 -1617 1594 326 1659 -670 589 -457
-89 -1218 676 632 -41 -450 -1233 1383 -1489 819 -673 -965 359 -1039 461 393 -1485 333 852 792
-252 -1640 -308 695 -730 759 1332 -1044 20 827 157 167 250 -1572 157 1385 1802 1176 268 934 -973
-1657 -1720 1995 1270 -1382 782 1510 1999 1749 1550 -459 -702 1642 1121 -1204 1798 966 1090
-1254 574 -701 1563 -360 779 355 851 -680 975 -1397 452 -1353 -1973 -1606 1579 1082 1876 1602
-1786 -1365 -323 -1299 1389 -1512 -976 -1932 -1135 1645 1638 1432 1544 1778 -512 880 1782 662
1999 1037 1243 -700 960 230 -478 -1127 -1122 -1539 1343 1422 -228 -1157 1546 1279 149 -944 1838
818 -1518 1914 1519 -729 1124 -1136 -313 1698 83 -1414 -668 -543 -386 191 1850 107 -1235 103 959
992 -1828 -358 -1486 -853 721 -1420 743 1698 131 -1333 -717 437 -1525 994 -1816 -1923 -1943 -406
1345 -1893 1662 -800 586 91 -1803 1659 1077 1988 1010 -1320 1669 107 948 -1604 -575 -1964 -779
431 -1570 638 1074 279 -1338 -1551 -617 878 1973 1150 -225 701 -1962 -1708 933 -1133 962 -1412
-991 -1647 1044 -204 1539 1238 1107 64 -618 -435 266 991 -1401 1679 -217 -1676 -1082 1770 1829
-1853 1411 1002 1184 1693 -1078 632 818 -591 669 -575 1237 -555 -746 503 709 -977 177 1159 -199
609 -482 701 -1449 -1176 -1015 1838 -538 -5 -969 1997 1953 -1508 -1621 -1516 -10 -510 -1309 -717
378 -1045 443 -459 -969 275 1645 -1352 93 -738 1963 -1898 -1917 1971 -1265 383 -173 -421 -447
1271 96 -1947 -1181 -682 1006 -1294 1886 -445 -359 1567 1005 1696 1157 -607 -1327 -149 1655 -671
-1855 820 1947 -569 -1656 -1814 501 -151 -1010 404 760 1591 1553 -299 -1764 -1807 1867 884 872
-1730 1852 1895 1806 -1687 -755 -1376 1894 -859 -913 1048 -925 -985 -175 -192 -1558 1667 -882
709 1740 1009 283 1702 269 -925 1892 473 -1951 -569 -1362 1754 -330 -1823 -126 1256 520 632 186
746 -487 -796 -1869 -1507 867 -1184 287 638 142 -1297 1913 -1163 1645 -1591 -481 1088 -817 1680
-1376 -1680 -902 323 1842 -955 715 -501 -434 1471 -1550 212 1881 -275 1553 -616 1610 -1935 -288
-351 648 785 1536 -298 -79 1370 -541 1753 -1332 -216 -107 892 1367 -317 -1657 991 598 803 -1234
1287 1894 174 -1868 1404 -1483 460 291 -936 696 -1789 456 -1268 -216 257 1704 -954 1281 -254
-950 -1742 -1835 1953 -499 100 542 1359 1707 1622 -1482 -320 -1183 -1143 474 1877 -1602 1210
-1037 -390 1588 -452 182 -1398 1702 -259 -1463 586 -1422 -1587 122 1586 -566 941 1719 1327 -1049
-219 -629 -1608 1 1505 1685 187 454 -866 1510 -832 -1389 308 1199 -1803 1808 719 -1401 -431 1735
-1534 -585 656 -1752 1096 1041 1240 -1275 1992 -1186 1997 -1919 -1782 1228 209 115 -1108 -839
-585 -1948 104 354 -2 646 1898 532 -732 -823 -1280 -1386 -322 -354
"""
