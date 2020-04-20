from seqex import BytesView

import pytest


def test_get_item():
    cowsay = BytesView('Hello, cowsay!'.encode(), 7, 6)
    assert cowsay[0] == ord('c')
    assert cowsay[1] == ord('o')
    assert cowsay[2] == ord('w')
    assert cowsay[3] == ord('s')
    assert cowsay[4] == ord('a')
    assert cowsay[5] == ord('y')
    assert cowsay[-1] == ord('y')
    assert cowsay[-2] == ord('a')
    assert cowsay[-3] == ord('s')
    assert cowsay[-4] == ord('w')
    assert cowsay[-5] == ord('o')
    assert cowsay[-6] == ord('c')
    with pytest.raises(IndexError):
        _ = cowsay[6]
    with pytest.raises(IndexError):
        _ = cowsay[-7]
