# SEQuence: EXtended

## What `seqex` features

* A data structure for bytes data stream
    * insert out-of-order fragments and get in-order ones
    * window control
    * rich errors
* A `BytesView` type which similar to `&[u8]` in Rust

## What `seqex` lacks to work as TCP reorder sequence

Operator must convert TCP sequence numbers to 0-based before insert fragments. `seqex` does not provide this conversion along with `u32` rounding handling and staff.

The 1-byte virtual data in handshaking and hand-waving stages are not accepted by `seqex`. Any inserted data must be real.

## What's on `seqex`'s willing list

* Extend typing hints from bytes sequence to generic one 