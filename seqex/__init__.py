from __future__ import annotations
from typing import *


class BytesView(Sequence[int]):
    """An immutable slice into data source.

    Python's builtin `bytes` is always cloned when sliced, a view will prevent it.
    """

    def __init__(self, buffer: Sequence[int], start: int, length: int):
        assert start >= 0
        assert length >= 0
        assert start + length <= len(buffer)
        self.start = start
        self.length = length
        self.buffer = buffer

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        if not - self.length <= item < self.length:
            raise IndexError('out of range of bytes view')
        if item >= 0:
            return self.buffer[self.start + item]
        else:
            return self.buffer[self.start + self.length + item]

    EMPTY: BytesView


BytesView.EMPTY = BytesView(bytes(), 0, 0)


class DataHandler:
    def on_data(self, offset: int, view: BytesView):
        pass

    def on_end(self, offset: int):
        pass


class ErrorHandler:
    def on_overlap(self, start: int, previous: BytesView, current: BytesView) -> bool:
        """Triggered when data fragment is partial existed in sequence.

        Return `True` to override content in buffer, `False` to discard current version.
        """
        return False

    def on_retrx(self, start: int, previous: BytesView, current: BytesView) -> bool:
        """Triggered when data fragment is totally existed in sequence.

        Return `True` to override content in buffer, `False` to discard current version.
        """
        return False

    def on_out_of_window(self, start: int, view: BytesView):
        """Triggered with bytes view whose offset is greater than window size.

        If data fragment is partially out of window, it will be split and only the latter part is passed.
        """
        pass

    def on_out_of_buffer(self, start: int, view: BytesView) -> int:
        """Triggered when there is no mistake for data fragment, but buffer size is not enough to hold it.

        Return the new size of sequence buffer, any data that still not fits in will be discard. The new size should be
        either greater than current size or `0` to keep current size.
        """
        return 0

    def on_missing_data(self, start: int, length: int):
        """Triggered when window offset is greater than the first data fragment's offset expected by sequence.

        This may happen some part of data is "forgotten" because of out-of-buffer issue. Operator could try to "rescue"
        data if she saved it from previous out-of-buffer handling.
        """
        pass

    def on_insufficient_buffer(self, required: int) -> int:
        """Triggered when buffer size is less than window range.

        Return the new size of sequence buffer. The new size should be either greater than current size or `0` to keep
        current size.
        """
        return 0


class Seqex:
    def insert(self, start: int, view: BytesView, window: int, window_size: int, on_error: ErrorHandler):
        """Insert a data fragment into sequence.

        `start` should be offset of fragment in the whole data stream. It counts from 0.
        """
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def assemble(self, on_data: DataHandler):
        raise NotImplementedError()
