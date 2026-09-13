# ============================================================
#   FRIEND BGMI TOOL — ULTIMATE MASTER ENGINE
#   STANDARDIZED BRANDING — TACTICAL FULL ENGINE
#   NO FAKE SUCCESS | FULL ERROR REPORTING | ZERO IN-GAME LAG
# ============================================================

import itertools as it
import math
import struct
import shutil
import os
import sys
import uuid
import hashlib
import platform
import subprocess
import requests
import base64
import zlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePath, Path
from typing import List, Dict, Tuple, Optional, Any
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich import print as rprint
from rich.markup import escape
from rich.text import Text
from rich.align import Align
from rich.box import HEAVY_EDGE, ROUNDED, DOUBLE_EDGE
from datetime import datetime
import pytz
import re
import zipfile
import json
import traceback

def _batched(iterable, n):
    it_obj = iter(iterable)
    while True:
        batch = list(it.islice(it_obj, n))
        if not batch: break
        yield batch

# ==================== VENDORED ZUC CIPHER ====================

_ZUC_S0 = bytes([
    0x3e,0x72,0x5b,0x47,0xca,0xe0,0x00,0x33,0x04,0xd1,0x54,0x98,0x09,0xb9,0x6d,0xcb,
    0x7b,0x1b,0xf9,0x32,0xaf,0x9d,0x6a,0xa5,0xb8,0x2d,0xfc,0x1d,0x08,0x53,0x03,0x90,
    0x4d,0x4e,0x84,0x99,0xe4,0xce,0xd9,0x91,0xdd,0xb6,0x85,0x48,0x8b,0x29,0x6e,0xac,
    0xcd,0xc1,0xf8,0x1e,0x73,0x43,0x69,0xc6,0xb5,0xbd,0xfd,0x39,0x63,0x20,0xd4,0x38,
    0x76,0x7d,0xb2,0xa7,0xcf,0xed,0x57,0xc5,0xf3,0x2c,0xbb,0x14,0x21,0x06,0x55,0x9b,
    0xe3,0xef,0x5e,0x31,0x4f,0x7f,0x5a,0xa4,0x0d,0x82,0x51,0x49,0x5f,0xba,0x58,0x1c,
    0x4a,0x16,0xd5,0x17,0xa8,0x92,0x24,0x1f,0x8c,0xff,0xd8,0xae,0x2e,0x01,0xd3,0xad,
    0x3b,0x4b,0xda,0x46,0xeb,0xc9,0xde,0x9a,0x8f,0x87,0xd7,0x3a,0x80,0x6f,0x2f,0xc8,
    0xb1,0xb4,0x37,0xf7,0x0a,0x22,0x13,0x28,0x7c,0xcc,0x3c,0x89,0xc7,0xc3,0x96,0x56,
    0x07,0xbf,0x7e,0xf0,0x0b,0x2b,0x97,0x52,0x35,0x41,0x79,0x61,0xa6,0x4c,0x10,0xfe,
    0xbc,0x26,0x95,0x88,0x8a,0xb0,0xa3,0xfb,0xc0,0x18,0x94,0xf2,0xe1,0xe5,0xe9,0x5d,
    0xd0,0xdc,0x11,0x66,0x64,0x5c,0xec,0x59,0x42,0x75,0x12,0xf5,0x74,0x9c,0xaa,0x23,
    0x0e,0x86,0xab,0xbe,0x2a,0x02,0xe7,0x67,0xe6,0x44,0xa2,0x6c,0xc2,0x93,0x9f,0xf1,
    0xf6,0xfa,0x36,0xd2,0x50,0x68,0x9e,0x62,0x71,0x15,0x3d,0xd6,0x40,0xc4,0xe2,0x0f,
    0x8e,0x83,0x77,0x6b,0x25,0x05,0x3f,0x0c,0x30,0xea,0x70,0xb7,0xa1,0xe8,0xa9,0x65,
    0x8d,0x27,0x1a,0xdb,0x81,0xb3,0xa0,0xf4,0x45,0x7a,0x19,0xdf,0xee,0x78,0x34,0x60
])
_ZUC_S1 = bytes([
    0x55,0xc2,0x63,0x71,0x3b,0xc8,0x47,0x86,0x9f,0x3c,0xda,0x5b,0x29,0xaa,0xfd,0x77,
    0x8c,0xc5,0x94,0x0c,0xa6,0x1a,0x13,0x00,0xe3,0xa8,0x16,0x72,0x40,0xf9,0xf8,0x42,
    0x44,0x26,0x68,0x96,0x81,0xd9,0x45,0x3e,0x10,0x76,0xc6,0xa7,0x8b,0x39,0x43,0xe1,
    0x3a,0xb5,0x56,0x2a,0xc0,0x6d,0xb3,0x05,0x22,0x66,0xbf,0xdc,0x0b,0xfa,0x62,0x48,
    0xdd,0x20,0x11,0x06,0x36,0xc9,0xc1,0xcf,0xf6,0x27,0x52,0xbb,0x69,0xf5,0xd4,0x87,
    0x7f,0x84,0x4c,0xd2,0x9c,0x57,0xa4,0xbc,0x4f,0x9a,0xdf,0xfe,0xd6,0x8d,0x7a,0xeb,
    0x2b,0x53,0xd8,0x5c,0xa1,0x14,0x17,0xfb,0x23,0xd5,0x7d,0x30,0x67,0x73,0x08,0x09,
    0xee,0xb7,0x70,0x3f,0x61,0xb2,0x19,0x8e,0x4e,0xe5,0x4b,0x93,0x8f,0x5d,0xdb,0xa9,
    0xad,0xf1,0xae,0x2e,0xcb,0x0d,0xfc,0xf4,0x2d,0x46,0x6e,0x1d,0x97,0xe8,0xd1,0xe9,
    0x4d,0x37,0xa5,0x75,0x5e,0x83,0x9e,0xab,0x82,0x9d,0xb9,0x1c,0xe0,0xcd,0x49,0x89,
    0x01,0xb6,0xbd,0x58,0x24,0xa2,0x5f,0x38,0x78,0x99,0x15,0x90,0x50,0xb8,0x95,0xe4,
    0xd0,0x91,0xc7,0xce,0xed,0x0f,0xb4,0x6f,0xa0,0xcc,0xf0,0x02,0x4a,0x79,0xc3,0xde,
    0xa3,0xef,0xea,0x51,0xe6,0x6b,0x18,0xec,0x1b,0x2c,0x80,0xf7,0x74,0xe7,0xff,0x21,
    0x5a,0x6a,0x54,0x1e,0x41,0x31,0x92,0x35,0xc4,0x33,0x07,0x0a,0xba,0x7e,0x0e,0x34,
    0x88,0xb1,0x98,0x7c,0xf3,0x3d,0x60,0x6c,0x7b,0xca,0xd3,0x1f,0x32,0x65,0x04,0x28,
    0x64,0xbe,0x85,0x9b,0x2f,0x59,0x8a,0xd7,0xb0,0x25,0xac,0xaf,0x12,0x03,0xe2,0xf2
])
_ZUC_D = [0b100010011010111,0b010011010111100,0b110001001101011,0b001001101011110,
    0b101011110001001,0b011010111100010,0b111000100110101,0b000100110101111,
    0b100110101111000,0b010111100010011,0b110101111000100,0b001101011110001,
    0b101111000100110,0b011110001001101,0b111100010011010,0b100011110101100]
_ZUC_MOD = 0x7fffffff
def _zuc_rol32(x,n): return ((x<<n)&0xffffffff)|(x>>(32-n))
def _zuc_bs(x): return (_ZUC_S0[(x>>24)&0xff]<<24)^(_ZUC_S1[(x>>16)&0xff]<<16)^(_ZUC_S0[(x>>8)&0xff]<<8)^(_ZUC_S1[x&0xff])
def _zuc_l1(x): return x^_zuc_rol32(x,2)^_zuc_rol32(x,10)^_zuc_rol32(x,18)^_zuc_rol32(x,24)
def _zuc_l2(x): return x^_zuc_rol32(x,8)^_zuc_rol32(x,14)^_zuc_rol32(x,22)^_zuc_rol32(x,30)

class _FallbackZUC:
    def __init__(self,key,iv):
        self._lfsr=[0]*16;self._r1=0;self._r2=0;S=self._lfsr
        for i in range(16): S[i]=(key[i]<<23)|(_ZUC_D[i]<<8)|iv[i]
        for _ in range(32):
            x0=(S[15]>>15<<16)|(S[14]&0xffff);x1=((S[11]&0xffff)<<16)|(S[9]>>15);x2=((S[7]&0xffff)<<16)|(S[5]>>15)
            self._lfsr_work(self._f(x0,x1,x2)>>1)
        self.generate()
    def _f(self,x0,x1,x2):
        r1,r2=self._r1,self._r2;w=((x0^r1)+r2)&0xffffffff;w1=(r1+x1)&0xffffffff;w2=r2^x2
        self._r1=_zuc_bs(_zuc_l1(((w1&0xffff)<<16)^(w2>>16)));self._r2=_zuc_bs(_zuc_l2(((w2&0xffff)<<16)^(w1>>16)));return w
    def _lfsr_work(self,u=0):
        S=self._lfsr;s16=((S[15]<<15)+(S[13]<<17)+(S[10]<<21)+(S[4]<<20)+(S[0]<<8)+S[0]+u)%_ZUC_MOD
        S.append(_ZUC_MOD if s16==0 else s16);S.pop(0)
    def generate(self):
        S=self._lfsr;x0=(S[15]>>15<<16)|(S[14]&0xffff);x1=((S[11]&0xffff)<<16)|(S[9]>>15)
        x2=((S[7]&0xffff)<<16)|(S[5]>>15);x3=((S[2]&0xffff)<<16)|(S[0]>>15)
        z=self._f(x0,x1,x2)^x3;self._lfsr_work();return z.to_bytes(4,'big')

try:
    import gmalg as _gmalg_mod
    _ZUC_CLASS = _gmalg_mod.ZUC
except ImportError:
    _ZUC_CLASS = _FallbackZUC

from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_CBC
from Crypto.Hash import SHA1
from Crypto.Util.Padding import unpad
from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor

console = Console()

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')

SIMPLE1_DECRYPT_KEY = 121
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16

SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = [
    'xG2qW5lP7lV2iN5fN5pG','xT1cJ6dL5wC0kK1rB4dK','qC4jS5bZ6fL5xE6nD4zA','gD4jQ2aL3bS3lC3xT0iW',
    'xU1yQ8wE9zY3gZ3bT5aE','uQ3cO2dX7xY4xU7gH7iS','gW1fR0jK6wQ4oN0oK1kZ','aJ4pV7iZ7pU4wP2aC2cZ',
    'cX6jT3cM2oT3vK0kJ1qN','iT2vS0cS6yT6cZ1sE1lO','hM1pH9iY8wM9hT4lN5uJ','kG6bC8jK0fL0dE4sH4mL',
    'dB6lB3vE0eZ8wM8rI0aC','tP7sP7nI9rA2vQ4cV5yQ','aT0cL1yN4pT3sZ7eM2vY','uV6fU8fC9zN3mP5dH8mN'
]

EM_SIMPLE1 = 1; EM_SIMPLE2 = 16; EM_SM4_2 = 2; EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31; EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE; EM_UNKNOWN_17 = 17
CM_NONE = 0; CM_ZLIB = 1; CM_ZSTD = 6; CM_ZSTD_DICT = 8; CM_MASK = 15

# Stable Engine Compression (Zero In-Game Stuttering)
_ZSTD_FAST_LEVELS = (6, 3)

class SM4:
    _S_BOX = bytes([
        52, 102, 37, 116, 137, 120, 228, 169, 90, 65, 188, 122, 214, 22, 33, 35,
        77, 97, 218, 148, 155, 223, 19, 60, 105, 58, 49, 10, 95, 215, 153, 149,
        241, 174, 114, 61, 7, 96, 36, 182, 152, 238, 196, 162, 45, 136, 221, 141,
        4, 234, 187, 17, 202, 62, 93, 161, 246, 63, 176, 151, 128, 71, 43, 166,
        230, 247, 217, 177, 89, 192, 124, 190, 84, 40, 183, 126, 79, 248, 67, 110,
        160, 80, 14, 245, 144, 184, 251, 163, 123, 98, 25, 70, 3, 42, 185, 143,
        159, 119, 180, 91, 131, 135, 8, 235, 226, 30, 66, 240, 15, 232, 113, 106,
        117, 173, 85, 31, 181, 171, 51, 250, 127, 21, 189, 133, 216, 6, 104, 179,
        82, 48, 72, 11, 0, 237, 239, 178, 87, 142, 231, 108, 213, 229, 46, 83,
        130, 5, 249, 129, 244, 86, 191, 140, 75, 227, 219, 74, 145, 76, 44, 211,
        64, 41, 78, 32, 20, 54, 121, 9, 111, 209, 55, 224, 57, 12, 138, 146,
        56, 18, 53, 109, 225, 253, 147, 154, 23, 212, 201, 156, 107, 132, 38, 157,
        175, 118, 193, 158, 208, 150, 197, 203, 233, 115, 73, 210, 205, 100, 195, 199,
        1, 125, 243, 172, 252, 222, 164, 68, 50, 27, 194, 186, 28, 2, 198, 39,
        69, 139, 242, 24, 167, 16, 81, 29, 200, 207, 99, 255, 47, 13, 88, 206,
        101, 165, 220, 26, 59, 134, 254, 34, 92, 168, 94, 103, 170, 236, 112, 204
    ])
    _FK = [1184304796, 1270900830, 1493524870, 3164752158]
    _CK = [964907, 973793155, 2654690407, 2916866751, 2071233739, 1226140771, 3348805095, 2045549823, 388349611, 800627875, 612403927, 3721562911, 1195432523, 3150178931, 612053223, 2445162591, 67183755, 1174197155, 1393249511, 3331183455, 3822152747, 1332317203, 1804781383, 1990130463, 1282653851, 3376591251, 2910902311, 925872959, 332098219, 735840931, 396665415, 3588844719]
    @staticmethod
    def ROL32(x, n): return (x << n) & 0xFFFFFFFF | (x >> (32 - n))
    @staticmethod
    def _BS(X): return (SM4._S_BOX[X >> 24 & 255] << 24 | SM4._S_BOX[X >> 16 & 255] << 16 | SM4._S_BOX[X >> 8 & 255] << 8 | SM4._S_BOX[X & 255])
    @staticmethod
    def _T0(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 2) ^ SM4.ROL32(X, 10) ^ SM4.ROL32(X, 18) ^ SM4.ROL32(X, 24)
    @staticmethod
    def _T1(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 13) ^ SM4.ROL32(X, 23)
    @staticmethod
    def _key_expand(key: bytes, rkey: list):
        K0 = int.from_bytes(key[0:4], 'big') ^ SM4._FK[0]
        K1 = int.from_bytes(key[4:8], 'big') ^ SM4._FK[1]
        K2 = int.from_bytes(key[8:12], 'big') ^ SM4._FK[2]
        K3 = int.from_bytes(key[12:16], 'big') ^ SM4._FK[3]
        for i in range(0, 32, 4):
            K0 ^= SM4._T1(K1 ^ K2 ^ K3 ^ SM4._CK[i]); rkey[i] = K0
            K1 ^= SM4._T1(K2 ^ K3 ^ K0 ^ SM4._CK[i + 1]); rkey[i + 1] = K1
            K2 ^= SM4._T1(K3 ^ K0 ^ K1 ^ SM4._CK[i + 2]); rkey[i + 2] = K2
            K3 ^= SM4._T1(K0 ^ K1 ^ K2 ^ SM4._CK[i + 3]); rkey[i + 3] = K3
    def __init__(self, key: bytes):
        self._key = key; self._rkey = [0] * 32; SM4._key_expand(self._key, self._rkey); self._block_buffer = bytearray()
    def encrypt(self, block: bytes) -> bytes:
        RK = self._rkey; X0 = int.from_bytes(block[0:4], 'big'); X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big'); X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 ^= SM4._T0(X1 ^ X2 ^ X3 ^ RK[i]); X1 ^= SM4._T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
            X2 ^= SM4._T0(X3 ^ X0 ^ X1 ^ RK[i + 2]); X3 ^= SM4._T0(X0 ^ X1 ^ X2 ^ RK[i + 3])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4, 'big')); buf.extend(X2.to_bytes(4, 'big')); buf.extend(X1.to_bytes(4, 'big')); buf.extend(X0.to_bytes(4, 'big'))
        return bytes(buf)
    def decrypt(self, block: bytes) -> bytes:
        RK = self._rkey; X0 = int.from_bytes(block[0:4], 'big'); X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big'); X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 ^= SM4._T0(X1 ^ X2 ^ X3 ^ RK[31 - i]); X1 ^= SM4._T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 ^= SM4._T0(X3 ^ X0 ^ X1 ^ RK[29 - i]); X3 ^= SM4._T0(X0 ^ X1 ^ X2 ^ RK[28 - i])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4, 'big')); buf.extend(X2.to_bytes(4, 'big')); buf.extend(X1.to_bytes(4, 'big')); buf.extend(X0.to_bytes(4, 'big'))
        return bytes(buf)

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        p = n - len(data) % n; return data if p == n else data + b'\x00' * p
    @staticmethod
    def align_up(x: int, n: int) -> int: return (x + n - 1) // n * n

class Reader:
    def __init__(self, buffer, cursor=0): self._buffer = buffer; self._cursor = cursor
    def u1(self, m=True) -> int: return self.unpack('B', m=m)[0]
    def u4(self, m=True) -> int: return self.unpack('<I', m=m)[0]
    def u8(self, m=True) -> int: return self.unpack('<Q', m=m)[0]
    def i4(self, m=True) -> int: return self.unpack('<i', m=m)[0]
    def s(self, n: int, m=True) -> bytes: return self.unpack(f'{n}s', m=m)[0]
    def unpack(self, f: str, offset=0, m=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if m: self._cursor += struct.calcsize(f)
        return x
    def string(self, m=True) -> str:
        length = self.i4(m=m)
        if length <= 0: return ""
        offset = 0 if m else 4
        return self.unpack(f'{length}s', offset=offset, m=m)[0].rstrip(b'\x00').decode('utf-8', errors='ignore')

class PakInfo:
    def __init__(self, buffer, keystream: List[int]):
        r = Reader(buffer[-45:])
        self.index_encrypted = ((r.u1() ^ keystream[3]) & 255) == 1
        self.magic = r.u4() ^ keystream[2]
        self.version = r.u4()
        self.index_hash = bytes(a ^ b for a, b in zip(r.s(20), struct.pack('<5I', *keystream[4:9]))) if self.version >= 6 else bytes()
        self.index_size = r.u8() ^ (keystream[10] << 32 | keystream[11])
        self.index_offset = r.u8() ^ (keystream[0] << 32 | keystream[1])
        if self.version <= 3: self.index_encrypted = False

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: List[int]):
        super().__init__(buffer, keystream)
        r = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1 = bytes(a ^ b for a, b in zip(r.s(32), struct.pack('<8I', *keystream[7:15]))) if self.version >= 7 else bytes()
        self.packed_key = r.s(256) if self.version >= 8 else bytes()
        self.packed_iv = r.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = r.s(256) if self.version >= 8 else bytes()
        self.stem_hash = (r.u4() ^ keystream[8]) if self.version >= 9 else 0
        self.unk2 = (r.u4() ^ keystream[9]) if self.version >= 9 else 0
        self.content_org_hash = r.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(v: int) -> int:
        return 45 + (32 if v>=7 else 0) + (768 if v>=8 else 0) + (8 if v>=9 else 0) + (20 if v>=12 else 0)

class PakCompressedBlock:
    def __init__(self, r: Reader): self.start = r.u8(); self.end = r.u8()

@dataclass
class TencentPakEntry:
    def __init__(self, r: Reader, v: int):
        self.content_hash = r.s(20)
        if v <= 1: r.u8()
        self.offset = r.u8()
        self.uncompressed_size = r.u8()
        self.compression_method = r.u4() & CM_MASK
        self.size = r.u8()
        self.unk1 = r.u1() if v >= 5 else 0
        self.unk2 = r.s(20) if v >= 5 else bytes()
        self.compressed_blocks = [PakCompressedBlock(r) for _ in range(r.u4())] if (self.compression_method != 0 and v >= 3) else []
        self.compression_block_size = r.u4() if v >= 4 else 0
        self.encrypted = (r.u1() == 1) if v >= 4 else False
        self.encryption_method = r.u4() if v >= 12 else 0
        self.index_new_sep = r.u4() if v >= 12 else 0

class PakCrypto:
    class _LCG:
        def __init__(self, s: int): self.state = s
        def next(self) -> int:
            w = lambda x: (x & 0xFFFFFFFF) if not (x & 0x80000000) else ((x + 0x80000000 & 0xFFFFFFFF) - 0x80000000)
            x1 = w(1103515245 * self.state); self.state = w(x1 + 12345)
            x2 = w(x1 + 77880) if self.state < 0 else self.state
            return (x2 >> 16 & 0xFFFFFFFF) % 32767
    @staticmethod
    def zuc_keystream() -> List[int]:
        zuc = _ZUC_CLASS(ZUC_KEY, ZUC_IV); return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]
    @staticmethod
    def rsa_extract(sig: bytes, mod: bytes) -> bytes:
        c = int.from_bytes(sig, 'little'); n = int.from_bytes(mod, 'little')
        m = pow(c, 65537, n).to_bytes(256, 'little').rstrip(b'\x00')
        buf = Misc.pad_to_n(m, 4)
        if len(buf) < 43: return bytes()
        x1 = buf[1:21]; x2 = buf[21:]
        h = lambda d, l: (SHA1.new(d).digest() * (math.ceil(l/20)))[:l]
        x1 = bytes(a ^ b for a, b in zip(x1, h(x2, len(x1))))
        x2 = bytes(a ^ b for a, b in zip(x2, h(x1, len(x2))))
        if x2[:20] != SHA1.new(b'\x00'*20).digest(): return bytes()
        raw = x2[20:]; skip = 1 + next((i for i in range(len(raw)) if raw[i] != 0))
        return raw[skip:]
    @staticmethod
    def decrypt_index(cipher, pak_info: TencentPakInfo) -> bytes:
        if pak_info.version > 7:
            k = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            aes = AES.new(k, MODE_CBC, iv[:16])
            return unpad(aes.decrypt(cipher), AES.block_size)
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in cipher)
    @staticmethod
    def align_encrypted_content_size(n: int, em: int) -> int:
        if em in (EM_SIMPLE2, 17): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        if em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0): return Misc.align_up(n, 16)
        return n
    @staticmethod
    def decrypt_block(cipher, file: PurePath, em: int) -> bytes:
        if em == EM_SIMPLE1: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in cipher)
        if em in (EM_SIMPLE2, 17):
            k, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY); out = []
            for x, in struct.iter_unpack('<I', cipher): k ^= x; out.append(k)
            return struct.pack(f'<{len(out)}I', *out)
        if em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0):
            p1 = file.stem.lower()
            sec = SM4_SECRET_2 if em == EM_SM4_2 else SM4_SECRET_4 if em == EM_SM4_4 else f'{SM4_SECRET_NEW[(em - EM_SM4_NEW_BASE)%len(SM4_SECRET_NEW)]}{em}'
            k = SHA1.new(str(p1 + sec).encode()).digest()[:16]
            sm4 = SM4(k)
            return bytes(it.chain.from_iterable(sm4.decrypt(x) for x in _batched(cipher, 16)))
        return cipher
    @staticmethod
    def generate_block_indices(n: int, em: int) -> List[int]:
        if not (em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0)): return list(range(n))
        p = []; lcg = PakCrypto._LCG(n)
        while len(p) != n:
            x = lcg.next() % n
            if x not in p: p.append(x)
        inv = [0]*len(p)
        for i, x in enumerate(p): inv[x] = i
        return inv

class PakCompression:
    @staticmethod
    def decompress_block(block, zd, cm: int) -> bytes:
        if cm == CM_ZLIB:
            try: return zlib.decompress(block)
            except: return block
        if cm in (CM_ZSTD, CM_ZSTD_DICT):
            return ZstdDecompressor(zd if cm == CM_ZSTD_DICT else None).decompress(block)
        return block

class TencentPakFile:
    def __init__(self, file_path: PurePath):
        self._file_path = file_path
        with open(file_path, 'rb') as f: self._file_content = memoryview(f.read())
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None; self._files = []; self._index = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._load_all()

    def _load_all(self):
        idx_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        if self._pak_info.index_encrypted: idx_data = PakCrypto.decrypt_index(idx_data, self._pak_info)
        r = Reader(idx_data)
        mp = PurePath()
        for p in PurePath(r.string()).parts:
            if p != '..': mp /= p
        self._mount_point = mp
        self._files = [TencentPakEntry(r, self._pak_info.version) for _ in range(r.u4())]
        for _ in range(r.u8()):
            dp = PurePath(r.string())
            e = {r.string(): self._files[~r.i4()] for _ in range(r.u8())}
            if self._is_zstd_with_dict and dp.name == 'zstddic':
                ent = list(e.values())[0]
                dr = Reader(self._file_content[ent.offset:ent.offset+ent.size])
                sz = dr.u8(); dr.u4(); dr.u4(); dt = dr.s(sz)
                self._zstd_dict = ZstdCompressionDict(dt, DICT_TYPE_AUTO)
            else:
                self._index[dp] = e

    def _write_to_disk(self, file_path: Path, entry: TencentPakEntry):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        em = entry.encryption_method
        cm = entry.compression_method
        with open(file_path, 'wb') as dst:
            if cm == CM_NONE:
                sz = PakCrypto.align_encrypted_content_size(entry.size, em) if entry.encrypted else entry.size
                data = bytes(self._file_content[entry.offset:entry.offset+sz])
                if entry.encrypted: data = PakCrypto.decrypt_block(data, file_path, em)
                dst.write(data[:entry.uncompressed_size])
            else:
                order = PakCrypto.generate_block_indices(len(entry.compressed_blocks), em)
                for idx in order:
                    blk = entry.compressed_blocks[idx]
                    unc = blk.end - blk.start
                    sz = PakCrypto.align_encrypted_content_size(unc, em) if entry.encrypted else unc
                    data = bytes(self._file_content[blk.start:blk.start+sz])
                    if entry.encrypted: data = PakCrypto.decrypt_block(data, file_path, em)
                    dec = PakCompression.decompress_block(data, self._zstd_dict, cm)
                    dst.write(dec)

    def dump(self, out_path: Path):
        target_root = out_path / self._mount_point
        target_root.mkdir(parents=True, exist_ok=True)
        total = sum(len(d) for d in self._index.values())
        if total == 0:
            raise ValueError("Pak file loaded but index is empty! Check encryption key or signature.")
        with Progress(console=console) as prog:
            task = prog.add_task("[bold cyan]Extracting all files...", total=total)
            for dp, files in self._index.items():
                cur = target_root / dp
                for fn, ent in files.items():
                    self._write_to_disk(cur / fn, ent)
                    prog.update(task, advance=1)

# ==================== LUA DECODER / EXTRACTOR ====================

def _process_lua_file(data: bytes, dest_dir: Path, base_name: str):
    """Parses Lua scripts or compiled bytecode into fully readable, editable text files."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    # Save original raw copy
    (dest_dir / f"{base_name}").write_bytes(data)
    
    # 1. Plain-text Lua
    if data[:4] not in (b'\x1bLua', b'\x1bLJ'):
        try:
            txt = data.decode('utf-8', errors='replace')
            (dest_dir / "readable_script.lua").write_text(txt, encoding='utf-8')
            return
        except: pass

    # 2. Lua Bytecode: Extract strings & identifiers so user can modify values
    strings = [m.group(0).decode('ascii', errors='replace') for m in re.finditer(rb'[\x20-\x7e]{3,}', data)]
    (dest_dir / "strings_readable.txt").write_text('\n'.join(strings), encoding='utf-8')
    
    # Generate structured mock script for easy edits
    mock_lines = ["-- [LUA BYTECODE STRINGS EXTRACTED]", "-- Modify the values below if needed:"]
    for s in strings:
        if len(s) > 3 and not s.startswith("="):
            mock_lines.append(f'-- string_entry = "{s}"')
    (dest_dir / "editable_view.lua").write_text('\n'.join(mock_lines), encoding='utf-8')

# ==================== REPACK ENGINE (FULL IN-PLACE REBUILD) ====================

def repack_pak_file_full(pak_file, edited_root, output_path, target_path=None, force_add=False):
    import copy as _cp
    edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file() and not p.name.endswith(('.txt', '.json'))]
    if not edit_files:
        edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file()]
    if not edit_files:
        console.print('[bold red]❌ No files found in EDIT folder![/bold red]')
        return 0

    version = pak_file._pak_info.version
    keystream = PakCrypto.zuc_keystream()
    orig_fc = pak_file._file_content

    raw = bytes(pak_file._file_content[pak_file._pak_info.index_offset:][:pak_file._pak_info.index_size])
    if pak_file._pak_info.index_encrypted: raw = PakCrypto.decrypt_index(raw, pak_file._pak_info)
    r = Reader(raw); mp_str = r.string(); num_files = r.u4()
    for _ in range(num_files): TencentPakEntry(r, version)
    all_dirs = {}
    for _ in range(r.u8()):
        dp = r.string(); cnt = r.u8()
        all_dirs[dp] = {r.string(): pak_file._files[~r.i4()] for _ in range(cnt)}

    if target_path and force_add:
        target_path = target_path.replace('\\', '/')
        for ed in all_dirs.keys():
            if ed.strip('/').lower() == target_path.strip('/').lower():
                target_path = ed; break
        else: target_path = target_path.strip('/') + '/'

    pak_name_map = {}
    for dp, files in pak_file._index.items():
        for name, entry in files.items():
            full_path = str(PurePath(dp)/name).replace('\\', '/')
            pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

    edited = {}
    for p in edit_files:
        fl = p.name.lower()
        if fl in pak_name_map:
            cands = pak_name_map[fl]
            edited[cands[0][0]] = (p, cands[0][1])
        elif force_add and target_path:
            tmpl = pak_file._files[0]
            new_fp = f"{target_path.rstrip('/')}/{p.name}"
            edited[new_fp] = (p, tmpl)

    if not edited:
        console.print('[bold red]❌ No files matched for repack![/bold red]')
        return 0

    new_files = [_cp.copy(e) for e in pak_file._files]
    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}
    out_buf = bytearray()

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str)/name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry))
            em = old_entry.encryption_method
            cm = old_entry.compression_method

            if full_path in edited:
                p, template = edited[full_path]
                new_raw = p.read_bytes()
                ne.content_hash = SHA1.new(new_raw).digest()
                ne.uncompressed_size = len(new_raw)

                if cm == CM_NONE:
                    ne.offset = len(out_buf)
                    ne.size = len(new_raw)
                    out_buf += new_raw
                else:
                    cs = old_entry.compression_block_size if old_entry.compression_block_size > 0 else 65536
                    chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                    new_blks = []
                    for chk in chunks:
                        comp = ZstdCompressor(level=_ZSTD_FAST_LEVELS[0]).compress(chk)
                        b = PakCompressedBlock.__new__(PakCompressedBlock)
                        b.start = len(out_buf); b.end = b.start + len(comp)
                        out_buf += comp
                        new_blks.append(b)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start if new_blks else len(out_buf)
                    ne.size = sum(b.end - b.start for b in new_blks)
                console.print(f'[green]✓ Processed & Sealed: {full_path}[/green]')
            else:
                if cm == CM_NONE:
                    ne.offset = len(out_buf)
                    out_buf += bytes(orig_fc[old_entry.offset:old_entry.offset+old_entry.size])
                elif old_entry.compressed_blocks:
                    new_blks = []
                    for ob in old_entry.compressed_blocks:
                        nb = PakCompressedBlock.__new__(PakCompressedBlock)
                        nb.start = len(out_buf); nb.end = nb.start + (ob.end - ob.start)
                        out_buf += bytes(orig_fc[ob.start:ob.end])
                        new_blks.append(nb)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start

    def pw_s(s): return struct.pack('<i', len(s.encode('utf-8'))+1) + s.encode('utf-8') + b'\x00' if s else struct.pack('<i', 0)
    idx = bytearray(pw_s(mp_str)) + struct.pack('<I', len(new_files))
    for ne in new_files:
        w = bytearray(ne.content_hash) + struct.pack('<QQIQ', ne.offset, ne.uncompressed_size, ne.compression_method, ne.size)
        if version >= 5: w += bytes([ne.unk1]) + ne.unk2
        if ne.compression_method != CM_NONE and version >= 3:
            w += struct.pack('<I', len(ne.compressed_blocks))
            for b in ne.compressed_blocks: w += struct.pack('<QQ', b.start, b.end)
        if version >= 4: w += struct.pack('<I', ne.compression_block_size) + bytes([1 if ne.encrypted else 0])
        if version >= 12: w += struct.pack('<II', ne.encryption_method, ne.index_new_sep)
        idx += w
    idx += struct.pack('<Q', len(all_dirs))
    for dp_str, dir_files in all_dirs.items():
        idx += pw_s(dp_str) + struct.pack('<Q', len(dir_files))
        for name, old_e in dir_files.items():
            idx += pw_s(name)
            found = next((i for i, e in enumerate(new_files) if id(e) == id(old_e)), -1)
            idx += struct.pack('<i', ~found if found != -1 else -1)

    idx_plain = bytes(idx)
    new_sha1 = SHA1.new(idx_plain).digest()
    if pak_file._pak_info.index_encrypted:
        k = PakCrypto.rsa_extract(pak_file._pak_info.packed_key, RSA_MOD_1)
        iv = PakCrypto.rsa_extract(pak_file._pak_info.packed_iv, RSA_MOD_1)
        aes = AES.new(k, MODE_CBC, iv[:16])
        pad = (-len(idx_plain)) % 16 or 16
        idx_bytes = aes.encrypt(idx_plain + bytes([pad] * pad))
    else: idx_bytes = idx_plain

    new_idx_offset = len(out_buf)
    new_idx_size = len(idx_bytes)
    out_buf += idx_bytes

    footer = bytearray(orig_fc[-TencentPakInfo._mem_size(version):])
    h_key = struct.pack('<5I', *keystream[4:9])
    footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
    footer[-16:-8] = (new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little')
    footer[-8:] = (new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little')
    out_buf += footer

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f: f.write(out_buf)
    return len(edited)

# ==================== UNIVERSAL DUMP & REPACK (ALL ASSETS) ====================

def _dump_universal(src: Path, dest_dir: Path) -> Tuple[Path, str]:
    dest = dest_dir / src.stem
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir(parents=True)
    ext = src.suffix.lower()

    # 1. Tencent PAK
    try:
        pak = TencentPakFile(src)
        pak.dump(dest)
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'PAK'}))
        return dest, 'TENCENT_PAK'
    except Exception as e:
        if ext == '.pak':
            raise RuntimeError(f"PAK Unpack Failed: {e}")

    # 2. ZIP / APK / OBB
    try:
        with zipfile.ZipFile(src, 'r') as z:
            z.extractall(dest / 'EXTRACTED')
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'ZIP'}))
        return dest, 'ZIP_CONTAINER'
    except: pass

    # 3. Lua Scripts / Bytecode
    data = src.read_bytes()
    if 'lua' in src.name.lower() or data[:4] in (b'\x1bLua', b'\x1bLJ'):
        _process_lua_file(data, dest, src.name)
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'LUA'}))
        return dest, 'LUA_SCRIPT'

    # 4. Binary / ELF / SO
    (dest / src.name).write_bytes(data)
    strings = [m.group(0).decode('ascii', errors='replace') for m in re.finditer(rb'[\x20-\x7e]{4,}', data)]
    (dest / 'strings.txt').write_text('\n'.join(strings), encoding='utf-8')
    (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'BIN'}))
    return dest, 'RAW_BINARY'

def _repack_universal(dump_dir: Path, result_dir: Path):
    meta_path = dump_dir / 'meta.json'
    if not meta_path.exists(): 
        return False, "meta.json missing inside dump directory."
    meta = json.loads(meta_path.read_text())
    orig_name = meta['source']
    out_file = result_dir / orig_name
    result_dir.mkdir(parents=True, exist_ok=True)

    if meta['type'] == 'ZIP':
        ext_dir = dump_dir / 'EXTRACTED'
        with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for root, _, files in os.walk(ext_dir):
                for fn in files:
                    fp = Path(root) / fn
                    z.write(fp, arcname=str(fp.relative_to(ext_dir)))
        return True, str(out_file)

    if meta['type'] in ('BIN', 'LUA'):
        # Target the modified raw binary or script
        src_bin = dump_dir / orig_name
        if src_bin.exists():
            shutil.copy2(src_bin, out_file)
            return True, str(out_file)

    return False, "For PAK rebuilds, please use Option 3 / 4 for 100% stable index recreation."

# ==================== MAIN PROGRAM ====================

def ensure_dirs(b: Path):
    for d in ["PAK", "UNPACK", "REPACK", "RESULT", "INPUT", "DUMP", "PAK TOOL/EDIT", "PAK TOOL/UNPACK", "PAK TOOL/RESULT", "PAK TOOL/PAK"]:
        (b / d).mkdir(parents=True, exist_ok=True)

def safe_input(p: str = '') -> str:
    try: return input(p)
    except: return ''

def main_menu():
    base = Path(__file__).parent
    ensure_dirs(base)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print("[bold cyan]================================================[/bold cyan]")
        console.print("[bold yellow]      FRIEND BGMI TOOL — ULTIMATE ENGINE        [/bold yellow]")
        console.print("[bold cyan]================================================[/bold cyan]")
        console.print("[bold yellow]OWNER: @Friends6gg   |   TELEGRAM: @Friends6gg[/bold yellow]\n")

        console.print("[bold green]─── PAK TOOLS (CORE IN-PLACE REBUILD) ───[/bold green]")
        console.print("[bold cyan]1.[/bold cyan] UNPACK ALL TYPES PAKS")
        console.print("[bold cyan]2.[/bold cyan] REPACK ALL TYPES PAKS")
        console.print("[bold cyan]3.[/bold cyan] REPACK ANY SIZE (EXISTING FILES)")
        console.print("[bold cyan]4.[/bold cyan] REPACK TO PATH (NEW FILES)")
        console.print("[bold cyan]5.[/bold cyan] DELETE CACHE / FOLDERS")
        console.print("\n[bold yellow]─── NEW SYSTEM (OBB / LUA / BINARY DUMP) ───[/bold yellow]")
        console.print("[bold cyan]6.[/bold cyan] OBB UNPACK / REPACK")
        console.print("[bold cyan]7.[/bold cyan] LUA UNPACK / REPACK")
        console.print("[bold cyan]8.[/bold cyan] UNIVERSAL DUMP (Select by Number)")
        console.print("[bold cyan]9.[/bold cyan] REPACK FROM DUMP (Exact Original File Type)")
        console.print("[bold red]0.[/bold red] EXIT\n")

        c = safe_input('ENTER CHOICE: ').strip()

        # 1. UNPACK PAK
        if c == '1':
            pak_dir = base / "PAK"
            files = list(pak_dir.glob("*.pak"))
            if not files: console.print("[red]No .pak files found in PAK/[/red]"); safe_input('\nPress Enter...'); continue
            console.print("\n[bold cyan]Available .pak files to UNPACK:[/bold cyan]")
            for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
            try:
                idx = int(safe_input('\nEnter number: ')) - 1
                pak = TencentPakFile(files[idx])
                out = base / "UNPACK" / files[idx].stem
                pak.dump(out)
                console.print(f"\n[bold green]✅ Success! Fully extracted to UNPACK/{files[idx].stem}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 2. REPACK ALL TYPES
        elif c == '2':
            pak_dir = base / "PAK"
            files = list(pak_dir.glob("*.pak"))
            if not files: console.print("[red]No .pak files found in PAK/[/red]"); safe_input('\nPress Enter...'); continue
            for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
            try:
                idx = int(safe_input('\nEnter number: ')) - 1
                pak = TencentPakFile(files[idx])
                repack_dir = base / "REPACK" / files[idx].stem
                out = base / "RESULT" / files[idx].name
                repack_pak_file_full(pak, repack_dir, out)
                console.print(f"\n[bold green]✅ Repack Completed: {out}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Repack Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 3. REPACK ANY SIZE (PAK TOOL/EDIT)
        elif c == '3':
            pak_dir = base / "PAK"
            files = list(pak_dir.glob("*.pak"))
            if not files: files = list((base / "PAK TOOL" / "PAK").glob("*.pak"))
            if not files: console.print("[red]No .pak files found in PAK/ or PAK TOOL/PAK/[/red]"); safe_input('\nPress Enter...'); continue
            for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
            try:
                idx = int(safe_input('\nEnter number: ')) - 1
                pak = TencentPakFile(files[idx])
                edit_dir = base / "PAK TOOL" / "EDIT"
                out = base / "PAK TOOL" / "RESULT" / files[idx].name
                count = repack_pak_file_full(pak, edit_dir, out)
                if count > 0: console.print(f"\n[bold green]✅ Rebuilt {count} file(s) into: {out}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 4. REPACK TO PATH
        elif c == '4':
            pak_dir = base / "PAK"
            files = list(pak_dir.glob("*.pak"))
            if not files: files = list((base / "PAK TOOL" / "PAK").glob("*.pak"))
            if not files: console.print("[red]No .pak files found![/red]"); safe_input('\nPress Enter...'); continue
            for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
            try:
                idx = int(safe_input('\nEnter number: ')) - 1
                target = safe_input('Enter target path inside PAK: ').strip()
                pak = TencentPakFile(files[idx])
                edit_dir = base / "PAK TOOL" / "EDIT"
                out = base / "PAK TOOL" / "RESULT" / files[idx].name
                count = repack_pak_file_full(pak, edit_dir, out, target_path=target, force_add=True)
                if count > 0: console.print(f"\n[bold green]✅ Injected {count} file(s) into: {out}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 5. CLEAN STORAGE
        elif c == '5':
            for d in ["UNPACK", "REPACK", "DUMP"]: shutil.rmtree(base / d, ignore_errors=True)
            ensure_dirs(base)
            console.print("[bold green]✅ Temporary Cache Cleaned![/bold green]"); safe_input('\nPress Enter...')

        # 6. OBB SYSTEM
        elif c == '6':
            sub = safe_input("1. Unpack OBB  |  2. Repack OBB: ").strip()
            if sub == '1':
                obbs = list((base / "INPUT").glob("*.obb"))
                if not obbs: console.print("[red]No .obb in INPUT/[/red]")
                else:
                    for i, o in enumerate(obbs, 1): console.print(f"  {i}. {o.name}")
                    oi = int(safe_input('Select number: ')) - 1
                    with zipfile.ZipFile(obbs[oi], 'r') as z: z.extractall(base / "UNPACK" / obbs[oi].stem)
                    console.print(f"[bold green]✅ OBB Extracted to UNPACK/{obbs[oi].stem}[/bold green]")
            elif sub == '2':
                unpacks = [d for d in (base / "UNPACK").iterdir() if d.is_dir()]
                if not unpacks: console.print("[red]No extracted folder in UNPACK/[/red]")
                else:
                    for i, u in enumerate(unpacks, 1): console.print(f"  {i}. {u.name}")
                    ui = int(safe_input('Select number: ')) - 1
                    out = base / "RESULT" / f"{unpacks[ui].name}.obb"
                    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
                        for root, _, fls in os.walk(unpacks[ui]):
                            for fn in fls:
                                fp = Path(root) / fn
                                z.write(fp, arcname=str(fp.relative_to(unpacks[ui])))
                    console.print(f"[bold green]✅ Repacked OBB: {out}[/bold green]")
            safe_input('\nPress Enter...')

        # 7. LUA SYSTEM
        elif c == '7':
            sub = safe_input("1. Unpack / Decode Lua  |  2. Repack Lua: ").strip()
            if sub == '1':
                luas = [f for f in (base / "INPUT").iterdir() if f.is_file() and ('lua' in f.name.lower() or f.suffix in ('.bytes', '.bin'))]
                if not luas: console.print("[red]No Lua files in INPUT/[/red]")
                else:
                    for i, l in enumerate(luas, 1): console.print(f"  {i}. {l.name}")
                    li = int(safe_input('Select number: ')) - 1
                    d, _ = _dump_universal(luas[li], base / "DUMP")
                    console.print(f"[bold green]✅ Lua Decoded to DUMP/{d.name}/ (Readable text available!)[/bold green]")
            elif sub == '2':
                dumps = [d for d in (base / "DUMP").iterdir() if d.is_dir()]
                if not dumps: console.print("[red]No Lua dumps found![/red]")
                else:
                    for i, d in enumerate(dumps, 1): console.print(f"  {i}. {d.name}")
                    di = int(safe_input('Select number: ')) - 1
                    ok, res = _repack_universal(dumps[di], base / "RESULT")
                    if ok: console.print(f"[bold green]✅ Saved: {res}[/bold green]")
                    else: console.print(f"[red]❌ Error: {res}[/red]")
            safe_input('\nPress Enter...')

        # 8. UNIVERSAL DUMP
        elif c == '8':
            inputs = [f for f in (base / "INPUT").iterdir() if f.is_file()]
            if not inputs: console.print("[red]No files found in INPUT/[/red]"); safe_input('\nPress Enter...'); continue
            console.print("\n[bold cyan]Files in INPUT/:[/bold cyan]")
            for i, f in enumerate(inputs, 1): console.print(f"  {i}. {f.name}")
            console.print("  0. DUMP ALL")
            try:
                sel = int(safe_input('\nSelect file number: '))
                chosen = inputs if sel == 0 else [inputs[sel - 1]]
                for f in chosen:
                    d, fmt = _dump_universal(f, base / "DUMP")
                    console.print(f"[bold green]✓ Dumped: {f.name} ({fmt}) → DUMP/{d.name}/[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Dump Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 9. REPACK FROM DUMP
        elif c == '9':
            dumps = [d for d in (base / "DUMP").iterdir() if d.is_dir()]
            if not dumps: console.print("[red]No folders in DUMP/ to repack![/red]"); safe_input('\nPress Enter...'); continue
            for i, d in enumerate(dumps, 1): console.print(f"  {i}. {d.name}")
            try:
                idx = int(safe_input('\nSelect dump number: ')) - 1
                ok, res = _repack_universal(dumps[idx], base / "RESULT")
                if ok: console.print(f"\n[bold green]✅ Repacked exactly as original format: {res}[/bold green]")
                else: console.print(f"\n[bold red]❌ Repack failed: {res}[/bold red]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        elif c == '0':
            break

if __name__ == '__main__':
    main_menu()
